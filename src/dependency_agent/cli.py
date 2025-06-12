from openai import OpenAI
import requests
import json
import os
import sys
import subprocess
import argparse
from pathlib import Path
from pydantic import BaseModel
from collections import defaultdict
from googlesearch import search


class ProblematicPackage(BaseModel):
    package_plain_name: str


class ChangelogEntryAnalysis(BaseModel):
    version: str
    release_date: str
    changelog_quote: str
    explanation_relevant_to_build_failure: str
    advice_to_fix: str


class ChangelogAnalysisOutput(BaseModel):
    entries: list[ChangelogEntryAnalysis]


def collect_versions(tree: dict, package: str) -> dict:
    versions = defaultdict(list[tuple[str, int]])

    def traverse(node: dict, depth: int):
        gid = node.get("groupId", "").lower()
        aid = node.get("artifactId", "").lower()
        if package in gid or package in aid:
            versions[aid].append((node.get("version"), depth))
        for child in node.get("children", []):
            traverse(child, depth + 1)

    traverse(tree, 0)
    return versions


def main() -> None:
    parser = argparse.ArgumentParser(prog="depguy", description="")
    parser.add_argument(
        "-p",
        "--pom",
        dest="pom",
        default="pom.xml",
        help="The name of the pom file to use for the given project (if it is a maven project).",
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="dir",
        default=".",
        help="The directory of the project, defaults to .",
    )
    parser.add_argument(
        "-j",
        "--just",
        dest="just",
        default="",
        help="just command to run (if using just)",
    )

    args = parser.parse_args()

    project_dir = Path(os.path.curdir).joinpath(args.dir)
    filepath = project_dir.joinpath(args.pom)
    if not filepath.exists() and not args.just:
        print(f"No file named {filepath.absolute()} found.")
        sys.exit(1)

    run_cmd = (
        f"just {args.just}"
        if args.just
        else f"cd {project_dir} && mvn clean install -f {args.pom}"
    )

    mvn_result = subprocess.run(
        [run_cmd],
        capture_output=True,
        text=True,
        shell=True,
    )
    build_output = mvn_result.stdout + mvn_result.stderr

    build_output_errors = [
        line for line in build_output.splitlines() if "error" in line.lower()
    ]

    if mvn_result.returncode == 0:
        print("Build succeeded – no dependency issues detected.")
        sys.exit(0)

    deptree = subprocess.run(
        [
            f"cd {project_dir} && mvn dependency:tree -DoutputType=json -f {args.pom} -Dverbose"
        ],
        capture_output=True,
        text=True,
        shell=True,
    )

    deptree_output = deptree.stdout + deptree.stderr

    deptree_lines: list[str] = deptree_output.splitlines()

    deptree_start_line_idx = next(
        idx
        for idx, line in enumerate(deptree_lines)
        if "dependency" in line and ":tree" in line
    )

    deptree_end_line_idx = next(
        idx
        for idx, line in enumerate(deptree_lines)
        if idx > deptree_start_line_idx and line.split(" ")[1] == "}"
    )

    filtered_deptree = "\n".join(
        [
            x.split(" ", 1)[-1]
            for x in deptree_lines[
                deptree_start_line_idx + 1 : deptree_end_line_idx + 1
            ]
        ]
    )
    deptree_dict = json.loads(filtered_deptree)

    filtered_errors = "\n".join([x.split(" ", 1)[-1] for x in build_output_errors])

    client = OpenAI()
    response = client.responses.parse(
        model="gpt-4.1",
        input=f"""Tell me, with no extra text, the exact package that is being problematic in the following build output. The package name should not include the prefixes such as org. or com.
                  output the package name as one would refer to it when referring to it by name: {filtered_errors}""",
        text_format=ProblematicPackage,
    )
    problematic_package: ProblematicPackage = ProblematicPackage.model_validate_json(
        response.output_text
    )

    print("Inferred problematic package:", problematic_package.package_plain_name)
    versions = collect_versions(deptree_dict, problematic_package.package_plain_name)

    multi_version_packages = {k: v for k, v in versions.items() if len(v) > 1}

    if not multi_version_packages:
        print("No conflicting module versions found. Aborting search.", file=sys.stderr)

    for key, value in multi_version_packages.items():
        used_version = min(value, key=lambda x: x[1])[0]
        oldest_version = min(value, key=lambda x: x[0])[0]
        newest_version = max(value, key=lambda x: x[0])[0]
        print(
            {"oldest": oldest_version, "newest": newest_version, "used": used_version}
        )

        first_url = next(
            search(
                f"{problematic_package.package_plain_name} changelog",
                num=1,
                stop=1,
                pause=2,
            ),
            None,
        )
        print("Finding changelog entries...")
        resp = requests.get(first_url, timeout=10)
        if resp.status_code != 200:
            print("Failed to retrieve changelog page.")
            sys.exit(1)
        html = resp.text
        # quick sanity check: verify both version numbers appear in the page text
        if oldest_version not in html or used_version not in html:
            print(
                "Changelog page found, but expected versions not present - might be the wrong page."
            )
            sys.exit(1)

        idx_new = html.find(newest_version)
        idx_old = html.find(oldest_version)
        if idx_new == -1 or idx_old == -1:
            print("Could not locate version entries in changelog text.")
            sys.exit(1)
        # ensure idx_new comes before idx_old (assuming newer version listed first)
        if idx_new > idx_old:
            idx_new, idx_old = idx_old, idx_new
        relevant_section = html[idx_new:idx_old]

        # print(filtered_errors)
        # print(relevant_section)

        messages = [
            {
                "role": "system",
                "content": "You are an expert Java build-tool assistant.",
            },
            {
                "role": "user",
                "content": f"""Changelog for {problematic_package.package_plain_name}:
                {relevant_section}

                Between version {oldest_version} and {newest_version}, find **only** those entries that directly **introduce**, **remove**, or **break** the exact classes, methods, or fields cited in this build-error.  
                - **Exclude** any entry that is purely a bug-fix, documentation change, performance tweak, or otherwise unrelated to the missing/changed symbols in the error.  
                - For each relevant entry, quote the snippet and tag it with its version and ISO release date (if given).  

                Context:
                - Current version in use: {used_version}  
                - Build error output:
                {filtered_errors}

                **Rules for selection**:
                1. If the error says a class/method is **not found**, include the entry where it was **first introduced**, and omit any later refactorings.  
                2. If the error is about a class/method **changing** (signature, behavior, config), include the entry where that change was **made**.  
                3. **Do not** include entries that merely fix bugs or add features unrelated to the failing symbol.
                4. If the entry does not seem directly relevant, do not include it.
                """,
            },
        ]

        response = client.responses.parse(
            model="gpt-4o", input=messages, text_format=ChangelogAnalysisOutput
        )
        advice_json = response.output_text
        changelog_analysis = ChangelogAnalysisOutput.model_validate_json(advice_json)

        print(changelog_analysis.model_dump_json(indent=2))

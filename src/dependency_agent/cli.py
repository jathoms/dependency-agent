from openai import OpenAI
import json
import re
import os
import sys
import subprocess
import argparse
from pathlib import Path
from pydantic import BaseModel
from collections import defaultdict


class ProblematicPackage(BaseModel):
    package_plain_name: str


def collect_versions(tree: dict, package: str) -> dict:
    versions = defaultdict(list[tuple[str, int]])

    def traverse(node: dict, depth: int):
        gid = node.get("groupId", "").lower()
        aid = node.get("artifactId", "").lower()
        if package in gid or package in aid:
            versions[aid].append((node.get("version"), depth))
        for child in node.get("children", []):
            traverse(child, depth+1)

    traverse(tree, 0)
    return versions


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="uv", description="UV project script – process a project directory"
    )
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

    print(versions.items())

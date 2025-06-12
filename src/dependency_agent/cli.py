from openai import OpenAI
import os
import sys
import subprocess
import argparse
from pathlib import Path
from pydantic import BaseModel


class ProblematicPackage(BaseModel):
    package: str
    

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
    args = parser.parse_args()

    project_dir = Path(os.path.curdir).joinpath(args.dir)
    filepath = project_dir.joinpath(args.pom)
    if not filepath.exists():
        print(f"No file named {filepath.absolute()} found.")
        sys.exit(1)

    mvn_result = subprocess.run(
        [f"cd {project_dir} && mvn clean install -f {args.pom}"],
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
        [f"cd {project_dir} && mvn clean dependency:tree -f {args.pom}"],
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
        if idx > deptree_start_line_idx and len(set(list(line.split(" ")[-1]))) == 1
    )

    filtered_deptree = "\n".join(
        [
            x.split(" ", 1)[-1]
            for x in deptree_lines[deptree_start_line_idx:deptree_end_line_idx]
        ]
    )
    filtered_errors = "\n".join([x.split(" ", 1)[-1] for x in build_output_errors])

    client = OpenAI()
    response = client.responses.parse(
        model="gpt-4.1",
        input=f"Tell me, with no extra text, the exact package that is being problematic in the following build output: {filtered_errors}",
        text_format=ProblematicPackage,
    )

    print(response.output_text)

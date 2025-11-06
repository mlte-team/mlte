"""
Script that handles updating the sample catalog entries with the corresponding demo notebook.

Build mode: Take demo notebook script conversions and put them into the sample catalog
Check mode: Checks that all sample test catalog entries are updated
"""

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import nbformat
from nbformat import NotebookNode

from mlte.catalog.model import CatalogEntry, CatalogEntryHeader

SAMPLE_CATALOG_PATH = "../mlte/store/catalog/sample"


def main():
    if len(sys.argv) < 3:
        print("Required parameters: mode, notebook path.")
        sys.exit(1)

    mode = sys.argv[1]
    if mode not in ["build", "check"]:
        print('Invalid mode. Valid modes are "build" and "check"')
        sys.exit(1)

    timestamp = int(time.time())
    notebook_path = Path(sys.argv[2])
    demo_name = notebook_path.parent
    entry_qa = notebook_path.name.split("evidence_")[-1][:-6]
    entry_identifier = f"{demo_name}-{entry_qa}"
    entry_path = Path(f"{SAMPLE_CATALOG_PATH}/{entry_identifier}.json")

    notebook_data, notebook_entry_json = read_notebook(notebook_path)
    code_str = create_code_str(notebook_data)
    new_entry = create_entry(
        notebook_entry_json, entry_identifier, timestamp, code_str
    )
    current_entry: CatalogEntry | None = None
    if os.path.exists(entry_path):
        with open(entry_path, "r") as entry_file:
            current_entry = CatalogEntry.from_json(json.load(entry_file))

    if mode == "check":
        if not current_entry or not compare_entries(new_entry, current_entry):
            print(
                f"Sample Catalog Entry: {entry_qa}, in demo {demo_name} is not updated."
            )
            sys.exit(1)
        else:
            sys.exit(0)

    elif mode == "build":
        if not current_entry or not compare_entries(new_entry, current_entry):
            with open(entry_path, "w") as entry_file:
                json.dump(new_entry.to_json(), entry_file, indent=4)


def read_notebook(notebook_path: Path) -> tuple[NotebookNode, dict]:
    """
    Read a demo notebook and return the code and the entry data

    :param notebook_path: Path to notebook to be read

    :returns:
        notebook_data: Demo notebook as a NotebookNode
        notebook_entry_json: Data used to create the test catalog entry stored in the notebook
    """
    notebook_data: NotebookNode = nbformat.read(
        notebook_path, nbformat.NO_CONVERT
    )
    try:
        # JSON entry data will be in the second cell of the notebook
        notebook_entry_data = notebook_data.cells[1].source
        # Remove the trailing comma, so that it can be parsed
        notebook_entry_data = re.sub(r",\s(})", "\n}", notebook_entry_data)
        notebook_entry_json = json.loads(notebook_entry_data)
    except Exception as e:
        print(e)
        print(f"Misformatted entry data in {notebook_path}.")
        print(
            f"Ensure that the second cell in the notebook contains JSON data for the sample test catalog."
        )
        sys.exit(1)

    for key in [
        "tags",
        "quality_attribute",
        "description",
        "inputs",
        "output",
    ]:
        if key not in notebook_entry_json:
            print(
                f"Key, {key} was not provided in the entry data in {notebook_path}"
            )
            sys.exit(1)

    return notebook_data, notebook_entry_json


def create_entry(
    notebook_entry_json: dict[str, Any],
    entry_identifier: str,
    timestamp: int,
    code_str: str,
) -> CatalogEntry:
    """Create CatalogEntry from notebook entry json, timestamp, and code string."""
    header = CatalogEntryHeader(
        identifier=entry_identifier,
        creator="admin",
        created=timestamp,
        updater=None,
        updated=timestamp,
        catalog_id="sample",
    )
    entry = CatalogEntry(
        header=header,
        tags=notebook_entry_json["tags"],
        quality_attribute=notebook_entry_json["quality_attribute"],
        code=code_str,
        description=notebook_entry_json["description"],
        inputs=notebook_entry_json["inputs"],
        output=notebook_entry_json["output"],
    )
    return entry


def create_code_str(notebook_data: NotebookNode) -> str:
    """
    Write notebook to temp file, convert temp notebook to script with nbconvert,
    read the script file, cleanup code string to take out notebook leftovers and
    to make it a valid JSON string.

    :param notebook_data: Demo notebook as a NotebookNode

    :return: notebook_data code as a JSON valid string, without the entry data
    """
    # Create a copy to not mutate the original object
    local_notebook_data: NotebookNode = copy.deepcopy(notebook_data)
    # Take the JSON entry data out of the notebook data so that it doesn't end up in the code string
    local_notebook_data.cells.pop(1)

    with tempfile.NamedTemporaryFile(
        mode="r", suffix=".ipynb"
    ) as temp_notebook_file, tempfile.NamedTemporaryFile(
        mode="r", suffix=".py"
    ) as temp_script_file:
        script_path = Path(temp_script_file.name)
        notebook_path = Path(temp_notebook_file.name)
        nbformat.write(local_notebook_data, notebook_path)
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "script",
                "--output-dir",
                script_path.parent,
                "--output",
                script_path.stem,
                notebook_path,
            ],
            stdout=subprocess.DEVNULL,
        )
        script = temp_script_file.readlines()

    # Remove "#!/usr/bin/env python", # coding: utf-8\n" at the start and extra new line at the end
    script = script[3:-1]
    # Remove all the execution lines and extra new lines along with them
    index = 0
    while index < len(script):
        if script[index] == "# In[ ]:\n":
            del script[index : index + 3]
        else:
            index += 1

    # Make the list into a raw string that can be inserted into the json
    script_str: str = "".join(script)
    script_str = script_str.replace("'", '"')
    script_str = script_str.replace(r'"', r"\"")
    return script_str


def compare_entries(entry1: CatalogEntry, entry2: CatalogEntry) -> bool:
    """Compare two Catalog entries to see if they are identical, ignoring timestamps."""
    if (
        entry1.header.identifier == entry2.header.identifier
        and entry1.header.creator == entry2.header.creator
        and entry1.header.updater == entry2.header.updater
        and entry1.header.catalog_id == entry2.header.catalog_id
        and entry1.tags == entry2.tags
        and entry1.quality_attribute == entry2.quality_attribute
        and entry1.code == entry2.code
        and entry1.description == entry2.description
        and entry1.inputs == entry2.inputs
        and entry1.output == entry2.output
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    main()

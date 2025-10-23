# Build mode: Take demo notebook script conversions and put them into the sample catalog
# Check mode: Checks that all sample test catalog entries are updated

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import nbformat

from mlte.catalog.model import CatalogEntry, CatalogEntryHeader

def compare_entries(entry1: CatalogEntry, entry2: CatalogEntry) -> bool:
    if (entry1.header.creator == entry2.header.creator and
        entry1.header.updater == entry2.header.updater and
        entry1.header.catalog_id == entry2.header.catalog_id and
        entry1.tags == entry2.tags and
        entry1.quality_attribute == entry2.quality_attribute and
        entry1.code == entry2.code and
        entry1.description == entry2.description and
        entry1.inputs == entry2.inputs and
        entry1.output == entry2.output
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Required parameters: mode, notebook path.")
        sys.exit(1)

    MODE = sys.argv[1]
    NOTEBOOK_PATH = Path(sys.argv[2])
    SCRIPT_PATH = Path(f"./conversions/{Path(sys.argv[2]).parent}/{NOTEBOOK_PATH.stem}.py")

    timestamp = int(time.time())
    notebook_data = nbformat.read(NOTEBOOK_PATH, nbformat.NO_CONVERT)
    try:
        notebook_entry_json = json.loads(notebook_data.cells[1].source)
    except:
        print(f"Misformatted entry data in {NOTEBOOK_PATH}.")
        sys.exit(1)
    # Take the JSON entry data out of the notebook so that it doesn't end up in the code for the catalog entry
    notebook_data.cells.pop(1)

    for key in ["identifier", "tags", "quality_attribute", "description", "inputs", "output"]:
        if key not in notebook_entry_json:
            print(f"Key, {key} was not provided in the entry data in, {NOTEBOOK_PATH}")
            sys.exit(1)

    new_header = CatalogEntryHeader(
        identifier=notebook_entry_json["identifier"],
        creator="admin",
        created=timestamp,
        updater=None,
        updated=timestamp,
        catalog_id="sample"
    )
    new_entry = CatalogEntry(
        header=new_header,
        tags=notebook_entry_json["tags"],
        quality_attribute=notebook_entry_json["quality_attribute"],
        code="",
        description=notebook_entry_json["description"],
        inputs=notebook_entry_json["inputs"],
        output=notebook_entry_json["output"]
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb") as temp_notebook_file:
        nbformat.write(notebook_data, temp_notebook_file.name)
        subprocess.run(["jupyter", "nbconvert", "--to", "script", "--output-dir", SCRIPT_PATH.parent, "--output", SCRIPT_PATH.stem, temp_notebook_file.name])

    script = open(SCRIPT_PATH, "r").readlines()
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
    script_str = "".join(script)
    script_str = script_str.replace("'", '"')
    script_str = script_str.replace(r'"', r"\"")
    new_entry.code = script_str

    timestamp = int(time.time())
    entry_file_name = SCRIPT_PATH.name.split("evidence_")[-1][:-3]
    entry_path = Path(f"../mlte/store/catalog/sample/demo-{entry_file_name}.json")
    if os.path.exists(entry_path):
        with open(entry_path, "r") as entry_file:
            current_entry = CatalogEntry.from_json(json.load(entry_file))

    if MODE == "check":
        if not compare_entries(new_entry, current_entry):
            print(f"Sample Catalog Entry: {entry_file_name}, was not updated.")
            sys.exit(1)
        else:
            sys.exit(0)

    elif MODE == "build":
        if not compare_entries(new_entry, current_entry):
            with open(entry_path, "w") as entry_file:
                json.dump(new_entry.to_json(), entry_file, indent=4)

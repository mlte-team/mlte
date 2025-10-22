# Build mode: Take demo notebook script conversions and put them into the sample catalog
# Check mode: Checks that all sample test catalog entries are updated

import json
import os
import sys
import time

from mlte.catalog.model import CatalogEntryHeader, CatalogEntry

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Mode and file path CLI argument not provided.")
    
    mode = sys.argv[1]
    file_path = sys.argv[2]
    script = open(file_path, "r").readlines()

    # Remove "#!/usr/bin/env python", # coding: utf-8\n" at the start and extra new line at the end
    script = script[3:-1]

    # Remove all the execution lines and extra new lines along with them
    index = 0
    while index < len(script):
        if script[index] == "# In[ ]:\n":
            del script[index:index+3]
        else:
            index += 1

    # Make the list into a raw string that can be inserted into the json
    script_str = "".join(script)
    script_str = script_str.replace("'", '"')
    script_str = script_str.replace(r'"', r'\"')
    
    demo_name = file_path.split("evidence_")[-1][:-3]
    demo_json_path = f"../mlte/store/catalog/sample/demo-{demo_name}.json"
    timestamp = int(time.time())

    if os.path.exists(demo_json_path):
        with open(demo_json_path, "r") as json_file:
            json_data = json.load(json_file)

        json_data["header"]["updated"] = timestamp
    else:
        new_header = CatalogEntryHeader(
            identifier=demo_name,
            creator="admin",
            created=timestamp,
            updated=timestamp,
            catalog_id="sample",
        )
        new_entry = CatalogEntry(
            header=new_header,
            tags=[],
            quality_attribute="",
            code="",
            description="",
            inputs="",
            output="",
        )
        json_data = new_entry.to_json()

    if mode == "check":
        if json_data["code"] != script_str:
            print(f"Sample Catalog Entry: {demo_name}, was not updated.")
            sys.exit(1)
        else:
            sys.exit(0)

    elif mode == "build":
        json_data["code"] = script_str

        with open(demo_json_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        
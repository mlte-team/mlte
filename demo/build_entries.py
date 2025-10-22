# Take demo notebook script conversions and put them into the sample catalog

import json
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("File path CLI argument not provided.")

    file_path = sys.argv[1]
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

    if os.path.exists(demo_json_path):
        with open(demo_json_path, "r") as json_file:
            json_data = json.load(json_file)

        json_data["code"] = script_str

        with open(demo_json_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        
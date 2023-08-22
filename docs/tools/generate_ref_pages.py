"""
docs/tools/generate_reference_page.py

A script to generate a reference page for the MLTE documentation.
"""

from pathlib import Path

import mkdocs_gen_files

# The root path to the MLTE package
ROOT_PATH = "../src"

g_nav = mkdocs_gen_files.Nav()

for path in sorted(Path(ROOT_PATH).rglob("*.py")):
    if str(path).endswith("__init__.py"):
        continue
    if str(path).endswith("_version.py"):
        continue
    if "_private" in str(path):
        continue

    module_path = path.relative_to(ROOT_PATH).with_suffix("")
    doc_path = path.relative_to(ROOT_PATH).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    g_nav[module_path.parts] = doc_path

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(module_path.parts)
        print(f"::: {identifier}", file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(g_nav.build_literate_nav())

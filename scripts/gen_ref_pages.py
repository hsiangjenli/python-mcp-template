import mkdocs_gen_files
import subprocess
import sys

# Run the document generation script as a separate process
try:
    result = subprocess.run(
        [sys.executable, "-m", "scripts.generate_docs"],
        capture_output=True,
        text=True,
        check=True,
    )
except subprocess.CalledProcessError as e:
    print(f"Error running generate_docs.py: {e.stderr}", file=sys.stderr)
    raise

# Get the generated markdown from stdout
api_docs_md = result.stdout

# Write the generated documentation to the file that MkDocs will render
with mkdocs_gen_files.open("reference/api.md", "w") as f:
    f.write(api_docs_md)

# Create the navigation file for literate-nav plugin
with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
    nav_file.write("* [Home](index.md)\n")
    nav_file.write("* [API Reference](reference/api.md)\n")

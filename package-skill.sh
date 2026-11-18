#!/usr/bin/env bash
# Build the standalone skill archive: dist/academic-writing-committee.zip, with the folder
# academic-writing-committee/ (SKILL.md and everything it uses) at the top of the archive,
# ready to copy into a skills directory or to upload as a skill.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
name=academic-writing-committee
mkdir -p "$here/dist"
out="$here/dist/$name.zip"
rm -f "$out"
cd "$here/skills"
python3 - "$name" "$out" <<'EOF'
import os, sys, zipfile
name, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(name):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for f in sorted(files):
            if f.endswith(".pyc"):
                continue
            z.write(os.path.join(root, f))
print(out)
EOF

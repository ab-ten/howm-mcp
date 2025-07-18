import subprocess, json, pathlib, os


def search_notes(query: str, basedir: pathlib.Path):
  cmd = ["rg", "--no-heading", "--with-filename", "-ni", query, "."]
  res = subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=basedir)
  matches = []
  for line in res.stdout.splitlines():
    path, lineno, text = line.split(":", 2)
    if path.startswith("./"):
      path = path[2:]
    if not path.endswith(".howm"):
      continue
    matches.append({"file": os.path.basename(path),
                    "line": int(lineno),
                    "text": text.strip()})
  return matches

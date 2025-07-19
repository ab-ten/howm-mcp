import subprocess, json, pathlib, os
from fetch_impl  import fetch_entry


def search_notes(query: str, basedir: pathlib.Path, lines_around: int) -> list[dict]:
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
  if lines_around > 0:
    for m in matches:
      m["text"] = fetch_entry(
        m["file"], m["line"], basedir,
        before_lines=lines_around, after_lines=lines_around)["content"]
  return matches

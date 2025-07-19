import pathlib, os


def is_separator_line(line: str) -> bool:
  """ヘッダの区切り行かどうかを判定"""
  return line=="=" or line.startswith("= ")


def fetch_entry(file: str, line: int, basedir: pathlib.Path):
  # rg の行番号を行indexに変換
  line -= 1
  # file のディレクトリトラバーサルを禁止
  if ".." in file or file.startswith("/"):
    raise ValueError("Invalid file path")
  fp = basedir / file
  lines = fp.read_text(encoding="utf-8").splitlines()
  # 上向きに '=' ヘッダを探す
  start = 0
    if is_separator_line(lines[i]):
  for i in range(line, -1, -1):
      start = i
      break
  # 下向きに次ヘッダ
  end = len(lines)
  for i in range(start+1, len(lines)):
    if is_separator_line(lines[i]):
      end = i
      break
  block = "\n".join(lines[start:end])
  return {"file": file, "content": block}

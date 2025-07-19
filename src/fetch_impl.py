import pathlib, os
from typing import Annotated, Optional


def is_separator_line(line: str) -> bool:
  """ヘッダの区切り行かどうかを判定"""
  return line=="=" or line.startswith("= ")


def fetch_entry(
    file: str,
    line: int,
    basedir: pathlib.Path,
    before_lines: Annotated[Optional[int], "None means unlimited"],
    after_lines: Annotated[Optional[int], "None means unlimited"]
  ) -> dict:
  # rg の行番号を行indexに変換
  line -= 1
  # file のディレクトリトラバーサルを禁止
  if ".." in file or file.startswith("/"):
    raise ValueError("Invalid file path")
  fp = basedir / file
  lines = fp.read_text(encoding="utf-8").splitlines()
  # 上向きに '=' ヘッダを探す
  start = 0
  if before_lines is not None:
    start = max(0, line-before_lines)
  for i in range(line, start-1, -1):
     if is_separator_line(lines[i]):
      start = i
      break
  # 下向きに次ヘッダ
  end = len(lines)
  if after_lines is not None:
    end = min(len(lines), line+after_lines+1)
  for i in range(start+1, end):
    if is_separator_line(lines[i]):
      end = i
      break
  block = "\n".join(lines[start:end])
  return {"file": file, "content": block}

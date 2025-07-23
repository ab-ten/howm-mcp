#!/usr/bin/env python3.12
import pathlib, os, sys
from mcp.server.fastmcp import FastMCP
from search_impl import search_notes
from fetch_impl  import fetch_entry

HOWM_DIR_PATH = os.environ.get("HOWM_DIR", "/docs/howm")
HOWM_DIR = pathlib.Path(HOWM_DIR_PATH).resolve()

SEARCH_LINES_AROUND = 3 # default
try:
  SEARCH_LINES_AROUND = int(os.environ.get("SEARCH_LINES_AROUND", "3"))
except ValueError:
  # error message to stderr
  print(f"Invalid SEARCH_LINES_AROUND value: {os.environ.get('SEARCH_LINES_AROUND', '3')}, using default {SEARCH_LINES_AROUND}", file=sys.stderr)


mcp = FastMCP("howm-mcp")


@mcp.tool()
def search(query: str) -> list[dict]:
  """
  ユーザーの howm メモ群に対してキーワード検索を行い、マッチしたファイル名・行番号・周辺テキストを返します。

  引数:
    - query (string, 必須): 検索キーワード（大/小文字区別なし・正規表現可）

  戻り値:
    - items (array): 検索結果のリスト。各要素は { file: string, line: integer, text: string } のオブジェクト

  使用例:
    search({"query": "プロジェクト"})

  正規表現使用例:
    短いキーワード（例：RTS）をそのまま検索すると、freebsdのportsなど
    関係ないメモもヒットしてしまいます。
    単語境界を使って search({"query": "\\bRTS\\b"}) とすることで
    RTS単体の単語のみにマッチさせることができます。
  """
  return search_notes(query, basedir=HOWM_DIR, lines_around=SEARCH_LINES_AROUND)

@mcp.tool()
def fetch(file: str, line: int) -> dict:
  """
  ファイル名と行番号を指定し、その行を含むメモブロック全体を取得します。
  ファイル名と行番号は必ず `search` ツールで返された値を使用してください。

  引数:
    - file (string, 必須): 対象の howm ファイル名
    - line (integer, 必須): 抽出開始の行番号（1始まり）

  戻り値:
    - file (string): 要求されたファイル名
    - content (string): 抽出されたメモブロック全体
  """
  return fetch_entry(file, line, basedir=HOWM_DIR, before_lines=None, after_lines=None)

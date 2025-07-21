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
  """全文検索: query を case insensitive で検索し、ファイル名と行番号を返却"""
  return search_notes(query, basedir=HOWM_DIR, lines_around=SEARCH_LINES_AROUND)

@mcp.tool()
def fetch(file: str, line: int) -> dict:
  """ファイル名と行番号から、その行を含むブロック全体を抽出"""
  return fetch_entry(file, line, basedir=HOWM_DIR, before_lines=None, after_lines=None)

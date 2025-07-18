#!/usr/bin/env python3.12
import pathlib, os
from mcp.server.fastmcp import FastMCP
from search_impl import search_notes
from fetch_impl  import fetch_entry

HOWM_DIR_PATH = os.environ.get("HOWM_DIR", "/docs/howm")
HOWM_DIR = pathlib.Path(HOWM_DIR_PATH).resolve()


mcp = FastMCP("howm-mcp")


@mcp.tool()
def search(query: str) -> list[dict]:
  """全文検索: query を case insensitive で検索し、ファイル名と行番号を返却"""
  return search_notes(query, basedir=HOWM_DIR)

@mcp.tool()
def fetch(file: str, line: int) -> dict:
  """ファイル名と行番号から、その行を含むブロック全体を抽出"""
  return fetch_entry(file, line, basedir=HOWM_DIR)

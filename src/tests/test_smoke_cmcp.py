import json
import os
import subprocess
import pytest


@pytest.fixture
def mock_basedir(tmp_path):
  """テスト用のhowmディレクトリを作成"""
  test_dir = tmp_path / "test_dir"
  test_dir.mkdir()

  # テスト用の .howm ファイルを作成
  file1 = test_dir / "2003_02_21.howm"
  file1.write_text("""= テストメモ1
これはテスト用のメモです。
プロジェクトの進捗について記録
= 別のトピック
他の内容も含まれています。
テストデータとして使用
""")

  file2 = test_dir / "2025_07_24.howm"
  file2.write_text("""= 開発ログ
CMCPコマンドのテスト実装
テスト結果の確認が必要
= バグ修正
エラーハンドリングを追加
""")

  return test_dir


@pytest.fixture
def test_env(mock_basedir):
  """テスト用の環境変数を作成"""
  env = os.environ.copy()
  env["HOWM_DIR"] = str(mock_basedir)
  return env


def test_cmcp_smoke_list(test_env):
  """Smoke test: tools/list command returns a JSON list."""
  result = subprocess.run(
    "cmcp 'mcp run mcp_server.py' tools/list",
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=test_env)
  assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
  data = json.loads(result.stdout)
  assert isinstance(data, dict), "Expected dict from tools/list"
  assert "tools" in data
  tool_list = data["tools"]
  assert isinstance(tool_list, list)
  # tools should contain search and fetch
  tool_names = [tool["name"] for tool in tool_list]
  assert "search" in tool_names, "search tool not found"
  assert "fetch" in tool_names, "fetch tool not found"
  assert len(tool_names) == 2


def test_cmcp_smoke_search(test_env):
  """Smoke test: tools/call name=search returns a JSON list."""
  result = subprocess.run(
    "cmcp 'mcp run mcp_server.py' tools/call name=search arguments:='{\"query\":\"テスト\"}'",
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=test_env)
  assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
  data = json.loads(result.stdout)
  assert isinstance(data, dict), "Expected dict from search"
  assert "content" in data
  result = data["content"]
  assert isinstance(result, list)
  # Should find the test data
  assert len(result) == 5
  for item in result:
    assert isinstance(item, dict)
    assert "type" in item
    assert item["type"] == "text"
    assert "text" in item
    text = item["text"]
    assert isinstance(text, str)
    item_result = json.loads(text)
    assert isinstance(item_result, dict)
    assert "file" in item_result
    assert isinstance(item_result["file"], str)
    assert "line" in item_result
    assert isinstance(item_result["line"], int)
    assert "text" in item_result
    assert isinstance(item_result["text"], str)
    assert "テスト" in item_result["text"], "Search result should contain query string"


def test_cmcp_smoke_fetch(test_env):
  """Smoke test: tools/call name=fetch returns a JSON object."""
  result = subprocess.run(
    "cmcp 'mcp run mcp_server.py' tools/call name=fetch arguments:='{\"file\":\"2003_02_21.howm\",\"line\":1}'",
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=test_env)
  assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
  data = json.loads(result.stdout)
  assert isinstance(data, dict), "Expected dict from search"
  assert "content" in data
  result = data["content"]
  assert isinstance(result, list)
  # Should find the test data
  assert len(result) == 1
  item = result[0]
  assert isinstance(item, dict)
  assert "type" in item
  assert item["type"] == "text"
  assert "text" in item
  assert isinstance(item["text"], str)
  js = json.loads(item["text"])
  assert isinstance(js, dict)
  assert "file" in js
  assert js["file"] == "2003_02_21.howm"
  assert "content" in js
  assert isinstance(js["content"], str)
  assert "= テストメモ1" in js["content"]
  assert "プロジェクトの進捗について記録" in js["content"]
  assert "テストデータとして使用" not in js["content"]
  assert "開発ログ" not in js["content"]

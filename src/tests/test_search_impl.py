import pytest
import pathlib
from search_impl import search_notes


@pytest.fixture
def mock_basedir(tmp_path):
  # テスト用の一時ディレクトリを作成
  test_dir = tmp_path / "test_dir"
  test_dir.mkdir()

  # ダミーの .howm ファイルを作成
  file1 = test_dir / "note1.howm"
  file1.write_text("This is a test note.\nAnother line with query.")

  file2 = test_dir / "note2.howm"
  file2.write_text("Query is here too.\nYet another line.")

  file3 = test_dir / "note3.howm"
  file3.write_text("test file.")

  # ダミーの他の拡張子のファイルを作成
  file4 = test_dir / "other.txt"
  file4.write_text("This file should be ignored for query.")

  # ダミーの長い行のファイルを作成
  file_l = test_dir / "long_line.howm"
  file_l.write_text(
    "za\nb\nc\nd\ne\nf\ng\nh\ni\njj\nk\nl\nm\nn\no\np\nq\nr\ns\nt\nu\nv\nw\nx\nzy\nz")

  return test_dir


def test_search_notes(mock_basedir):
  # 検索クエリ
  query = "query"

  # search_notes を実行
  results = search_notes(query, mock_basedir, lines_around=0)

  # 結果を検証
  assert len(results) == 2  # .howm ファイルのみが対象
  # file フィールドでソート
  results.sort(key=lambda x: x["file"])
  assert results[0]["file"] == "note1.howm"
  assert results[1]["file"] == "note2.howm"
  assert "query" in results[0]["text"].lower()
  assert "query" in results[1]["text"].lower()


@pytest.mark.parametrize("query,lines_around,expected_text", [
  ("za", 2, "za\nb\nc"),
  ("za", 1, "za\nb"),
  ("za", 0, "za"),
  ("b", 1, "za\nb\nc"),
  ("c", 2, "za\nb\nc\nd\ne"),
  ("jj", 2, "h\ni\njj\nk\nl"),
  ("jj", 1, "i\njj\nk"),
  ("jj", 0, "jj"),
  ("zy", 2, "w\nx\nzy\nz"),
  ("zy", 1, "x\nzy\nz"),
  ("zy", 0, "zy"),
])
def test_search_notes_with_lines_around(mock_basedir, query, lines_around, expected_text):
  results = search_notes(query, mock_basedir, lines_around)
  assert len(results) == 1
  assert results[0]["file"] == "long_line.howm"
  assert results[0]["text"] == expected_text

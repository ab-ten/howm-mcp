import pytest
import pathlib
from fetch_impl import fetch_entry

@pytest.fixture
def mock_basedir(tmp_path):
  # テスト用の一時ディレクトリを作成
  test_dir = tmp_path / "test_dir"
  test_dir.mkdir()

  # ダミーの .howm ファイルを作成
  file1 = test_dir / "note1.howm"
  file1.write_text("""= Header 1
Content line 1
Content line 2
= Header 2
Content line 3
Content line 4
= Header 3
""")

  # ダミーの .howm ファイルを作成
  file2 = test_dir / "note2.howm"
  file2.write_text("""no Header 1
Content line 1
Content line 2
=
Content line 3
Content line 4
""")

  # ダミーの長い行のファイルを作成
  file_l = test_dir / "long_line.howm"
  file_l.write_text("za\nb\nc\nd\ne\nf\ng\nh\ni\nj\nk\nl\nm\nn\no\np\nq\nr\ns\nt\nu\nv\nw\nx\ny\nz")

  return test_dir

@pytest.mark.parametrize("line_number", [1, 2, 3])
def test_fetch_entry_first_block(mock_basedir, line_number):
  # 最初のブロックを取得
  result = fetch_entry("note1.howm", line_number, mock_basedir, before_lines=None, after_lines=None)
  assert result["file"] == "note1.howm"
  assert result["content"] == "= Header 1\nContent line 1\nContent line 2"

@pytest.mark.parametrize("line_number", [4, 5, 6])
def test_fetch_entry_next_block(mock_basedir, line_number):
  # 次のブロックを取得
  result = fetch_entry("note1.howm", line_number, mock_basedir, before_lines=None, after_lines=None)
  assert result["file"] == "note1.howm"
  assert result["content"] == "= Header 2\nContent line 3\nContent line 4"

@pytest.mark.parametrize("line_number", [7])
def test_fetch_entry_last_block(mock_basedir, line_number):
  # 最後のブロックを取得
  result = fetch_entry("note1.howm", line_number, mock_basedir, before_lines=None, after_lines=None)
  assert result["file"] == "note1.howm"
  assert result["content"] == "= Header 3"

def test_fetch_entry_invalid_path(mock_basedir):
  # 無効なファイルパス
  with pytest.raises(ValueError):
    fetch_entry("../note1.howm", 2, mock_basedir, before_lines=None, after_lines=None)

@pytest.mark.parametrize("line_number", [1, 2, 3])
def test_fetch_entry_no_header_first_block(mock_basedir, line_number):
  # 最初のブロックを取得（ヘッダなし）
  result = fetch_entry("note2.howm", line_number, mock_basedir, before_lines=None, after_lines=None)
  assert result["file"] == "note2.howm"
  assert result["content"] == "no Header 1\nContent line 1\nContent line 2"

@pytest.mark.parametrize("line_number", [4, 5, 6])
def test_fetch_entry_no_header_next_block(mock_basedir, line_number):
  # 次のブロックを取得（=のみヘッダ）
  result = fetch_entry("note2.howm", line_number, mock_basedir, before_lines=None, after_lines=None)
  assert result["file"] == "note2.howm"
  assert result["content"] == "=\nContent line 3\nContent line 4"

def test_fetch_around(mock_basedir):
  # 長い行のファイルから周囲の行を取得
  result = fetch_entry("long_line.howm", 1, mock_basedir, before_lines=2, after_lines=2)
  assert result["file"] == "long_line.howm"
  assert result["content"] == "za\nb\nc"

  result = fetch_entry("long_line.howm", 10, mock_basedir, before_lines=2, after_lines=2)
  assert result["file"] == "long_line.howm"
  assert result["content"] == "h\ni\nj\nk\nl"

  result = fetch_entry("long_line.howm", 26, mock_basedir, before_lines=2, after_lines=2)
  assert result["file"] == "long_line.howm"
  assert result["content"] == "x\ny\nz"

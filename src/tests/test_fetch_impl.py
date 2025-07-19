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

    return test_dir

@pytest.mark.parametrize("line_number", [1, 2, 3])
def test_fetch_entry_first_block(mock_basedir, line_number):
    # 最初のブロックを取得
    result = fetch_entry("note1.howm", line_number, mock_basedir)
    assert result["file"] == "note1.howm"
    assert result["content"] == "= Header 1\nContent line 1\nContent line 2"

@pytest.mark.parametrize("line_number", [4, 5, 6])
def test_fetch_entry_next_block(mock_basedir, line_number):
    # 次のブロックを取得
    result = fetch_entry("note1.howm", line_number, mock_basedir)
    assert result["file"] == "note1.howm"
    assert result["content"] == "= Header 2\nContent line 3\nContent line 4"

@pytest.mark.parametrize("line_number", [7])
def test_fetch_entry_next_block(mock_basedir, line_number):
    # 最後のブロックを取得
    result = fetch_entry("note1.howm", line_number, mock_basedir)
    assert result["file"] == "note1.howm"
    assert result["content"] == "= Header 3"

def test_fetch_entry_invalid_path(mock_basedir):
    # 無効なファイルパス
    with pytest.raises(ValueError):
        fetch_entry("../note1.howm", 2, mock_basedir)

@pytest.mark.parametrize("line_number", [1, 2, 3])
def test_fetch_entry_no_header_first_block(mock_basedir, line_number):
    # 最初のブロックを取得（ヘッダなし）
    result = fetch_entry("note2.howm", line_number, mock_basedir)
    assert result["file"] == "note2.howm"
    assert result["content"] == "no Header 1\nContent line 1\nContent line 2"

@pytest.mark.parametrize("line_number", [4, 5, 6])
def test_fetch_entry_no_header_next_block(mock_basedir, line_number):
    # 次のブロックを取得（=のみヘッダ）
    result = fetch_entry("note2.howm", line_number, mock_basedir)
    assert result["file"] == "note2.howm"
    assert result["content"] == "=\nContent line 3\nContent line 4"

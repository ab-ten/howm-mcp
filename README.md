# howm-mcp

整理されていない雑多な howm メモでも、十分に活用できる可能性がある――そんな発想を試してみたくて、まずは実験的に組んでみた MCP サーバーです。

現時点では、コンセプトの実証と検証が主な目的です。ここではシンプルな構成を重視し、ripgrep を使った検索＋メモブロック抽出のみで構成しています。

Emacs の howm（*"Write fragmentarily and read collectively"*）を日々のメモに使っていて、
メモをいくら書いても、量が増えると検索も参照も面倒になりがち……。
でも、howm‑mcp を使えば、整理せずとも必要な情報にアクセスでき、
そのまま LLM（GitHub Copilot Chat やなど）に渡して処理することが可能です。

* 🔍 **キーワード全文検索**
* 📂 **該当メモブロック単位で抽出**

howm の思想「フラグメントとして書き留めて、集合的に読む」を守りながら、
雑多なメモを「LLM対応の知識データベース」に変える橋渡しとして活躍します。

> Emacs howm 公式: [kaorahi/howm](https://github.com/kaorahi/howm)

## 🏠 対象ユーザー

* Emacs と howm に慣れている方
* VS Code や Claude Desktop など、MCP クライアント環境を使っている方（Claudeではテストしていないのでもしかすると不具合があるかもしれません）
* 自分の雑多なメモを LLM に食わせたい方

## 💪 コア機能

### `search(query: str) -> list[dict]`

キーワードを含む行を全文検索し、以下の情報を返します：

* `file`: ファイル名
* `line`: 該当行の行番号
* `text`: 行の内容（前後3行を含む）

### `fetch(file: str, line: int) -> dict`

与えられた行を含むメモブロック全体（`=`だけの行、または`= `で始まる行を区切りとした範囲）を抽出します：

* `file`: ファイル名
* `content`: ブロック全体のテキスト

## 🚀 セットアップと利用方法

### ☕ Docker を使う

```sh
cp Makefile.local.sample Makefile.local
# Makefile.local を編集して HOWM_DIR を設定
make build print # MCP サーバーコンテナイメージの作成と、MCP サーバー起動コマンドの表示
```

```sh
make build-all
make dev  # 開発用シェルを起動
```

GNU make がない環境では以下のようにしてMCPサーバーコンテナイメージをビルドします。

```sh
docker build --target runtime -t howm-mcp .
```

`make print` でコンテナの起動コマンドを確認できます。  
通常はこのように表示されます：
> docker run --rm -i --network=none -v C:/Projects/howm-mcp/src:/app -v [your howm dir, please set HOWM_DIR in Makefile.local]:/docs/howm:ro howm-mcp


### 🤖 MCP クライアントとの連携

VS Code Copilot Chat の MCP サーバー設定例：Shift-Ctrl-P のコマンドパレットから `MCP: Add Server` を選択し、stdio command 形式を選び、以下のように入力します（`make print` で表示された文字列を入力します）：

> `docker run --rm -i --network=none -v <proj>/src:/app -v <your-howm>:/docs/howm:ro howm-mcp`

`<proj>` は `git clone` したプロジェクトのパス、`<your-howm>` はホストの howm ディレクトリのパスに置き換えてください。

### 🔧 開発モード

```sh
make dev
cmcp 'mcp run mcp_server.py' tools/list
cmcp 'mcp run mcp_server.py' tools/call name=search arguments:='{"query":"テスト"}'
cmcp 'mcp run mcp_server.py' tools/call name=fetch arguments:='{"file":"2003_02_21.howm", "line": 49}'
```

`cmcp` と `mcp` コマンドはコンテナ内に同梱されています。

### テストの実行方法

開発モードでテストを実行するには、以下の手順を実行してください：

```sh
make dev  # 開発用シェルを起動
pytest tests/  # テストを実行
```

これにより、すべてのテストが実行され、結果が表示されます。

## 🔹 使用例

以下は VSCode Copilot Chat 経由での利用例：

> **質問**：「#my-howm-mcp-server 今 howm のメモを oxygen not included で検索して、検索結果からfetchして要約して」  
> （my-howm-mcp-server という名前で登録している場合）
>
> ✔ search 実行
>
> ✔ fetch 実行
>
> ✔ LLM が対象ブロックを取得・要約

実際の howm メモがそのまま LLM に活かされる例です。
（今と付けないと、そのような機能を持つプログラムコードを提案される可能性が高くなります）

## 検索結果の前後行数制御について

MCPサーバーの `search` ツールは、デフォルトで検索ヒットした行の「前後3行」を含めて返すようになりました。
この前後行数は、環境変数 `SEARCH_LINES_AROUND` で調整できます。
注意事項としては、docker コンテナで実行する場合、環境変数は `docker run` の `-e` オプションで指定する必要があります。

## 👍 ライセンス

このプロジェクトは [MIT License](./LICENSE) の下でライセンスされています。

## なんとなくの今後の予定

- **複数キーワードの検索機能**  
  キーワードごとに検索し、全キーワードが揃っているファイルを返すようにする。

- **fetch, search を pagenation 対応にする**  

- **README-EN.md**:  
  Create English version of this README.

- CI の整備

## ChangeLog

### 2025-07-24
- ツールの description の詳細化と README の利用例の更新

### 2025-07-21
- `fetch` ツールを呼び出すとエラーになっていた不具合を修正
- Docker イメージをマルチステージ化してランタイムのみのコンテナを軽量化
  - `base`, `runtime`, `dev` の3ステージ構成に変更
  - 共通セットアップは `base` ステージで実行
- Makefile を大幅にリファクタリング
  - `build`, `build-dev`, `build-all`, `dev`, `remake-requirements`, `print`, `test` ターゲットを追加
  - 開発用イメージ (`howm-mcp-dev`) と汎用的な `DOCKER_COMMAND` を導入
- Python 依存管理を pip-tools に移行
  - `src/requirements/*.in` → `*.txt` 自動生成用スクリプト `remake.sh` を追加
  - ルートの古い `requirements.txt`/`requirements-dev.txt` を削除し、`src/requirements` 配下で一元管理

### 2025-07-20
- `search` ツールの前後行数を環境変数で制御可能に
  - デフォルトは前後3行
  - `SEARCH_LINES_AROUND` 環境変数で調整可能

### 2025-07-19
- 初期プロトタイプ公開

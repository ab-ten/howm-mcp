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
* `text`: 行の内容

### `fetch(file: str, line: int) -> dict`

与えられた行を含むメモブロック全体（`=`または`= `で始まる行を区切りとした範囲）を抽出します：

* `file`: ファイル名
* `content`: ブロック全体のテキスト

## 🚀 セットアップと利用方法

### ☕ Docker を使う

```sh
make build
make dev  # 開発用シェルを起動
```

Make がない環境では：

```sh
docker build -t howm-mcp .
```

### 🤖 MCP クライアントとの連携

VS Code Copilot Chat の MCP サーバー設定例：Shift-Ctrl-P のコマンドパレットから `MCP: Add Server` を選択し、stdio command 形式を選び、以下のように入力します。

> `docker run --rm -i --network=none -v <proj>/src:/app -v <your-howm>:/docs/howm:ro howm-mcp`

`<proj>` は `git clone` したプロジェクトのパス、`<your-howm>` はホストの howm ディレクトリのパスに置き換えてください。

### 🔧 開発モード

```sh
make dev
cmcp 'mcp run mcp_server.py' tools/list
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

> **質問**：「#my-howm-mcp-server を oxygen not included で検索して、検索結果からfetchして要約して」  
> （my-howm-mcp-server という名前で登録している場合）
>
> ✔ search 実行
>
> ✔ fetch 実行
>
> ✔ LLM が対象ブロックを取得・要約

実際の howm メモがそのまま LLM に活かされる例です。

## 👍 ライセンス

このプロジェクトは [MIT License](./LICENSE) の下でライセンスされています。

## 今後の予定

- **複数キーワードの検索機能**  
  キーワードごとに検索し、全キーワードが揃っているファイルを返すようにする。

- **fetch を search に統合**  
  search で howm のメモブロック単位で返せるようにする。また、メモブロックが大きすぎる場合に適当に切り詰める。

- **README-EN.md**:  
  Create English version of this README.

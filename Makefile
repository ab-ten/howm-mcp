#

MCP_DEV_IMAGE := howm-mcp-dev
#MCP_IMAGE := ubuntu:latest
HOWM_DIR = "[your howm dir, please set HOWM_DIR in Makefile.local]"
DOCKER_ENTRYPOINT = "/bin/bash"

# include Makefile.local if it exists
-include Makefile.local

# Cygwin 環境なら Windows ネイティブパスを取得、そうでなければ CURDIR
UNAME_O := $(shell uname -o)
ifeq ($(UNAME_O),Cygwin)
  CURRENT_DIR := $(shell cygpath -ma .)
else
  CURRENT_DIR := $(CURDIR)
endif

.PHONY: build build-dev dev remake-requirements test print


# ランタイム専用イメージのビルド
build:
	docker build --target runtime -t howm-mcp .

# 開発用イメージのビルド
build-dev:
	docker build --target dev -t ${MCP_DEV_IMAGE} .

# 両方のイメージをビルド
build-all: build build-dev
	@echo "All images built successfully."

# 開発用コンテナを対話シェルで起動
dev:
	docker run --rm -it \
		-v ${CURRENT_DIR}/src:/app \
		-v ${HOWM_DIR}:/docs/howm:ro \
		--entrypoint ${DOCKER_ENTRYPOINT} ${MCP_DEV_IMAGE} ${DOCKER_COMMAND}

# requirements*.txt を最新に更新する
remake-requirements:
	cp src/requirements/requirements.in src/requirements/requirements.txt
	cp src/requirements/requirements-dev.in src/requirements/requirements-dev.txt
	$(MAKE) --no-print-directory build-dev
	$(MAKE) --no-print-directory DOCKER_COMMAND="requirements/remake.sh" dev
	$(MAKE) --no-print-directory build-all

# MCP server の起動設定用コマンドラインの表示
print:
	@echo "docker run --rm -i --network=none -v ${CURRENT_DIR}/src:/app -v ${HOWM_DIR}:/docs/howm:ro howm-mcp"

test:
	$(MAKE) --no-print-directory DOCKER_COMMAND="-c 'pytest tests/'" dev

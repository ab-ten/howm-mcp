#

MCP_IMAGE := howm-mcp
#MCP_IMAGE := ubuntu:latest
HOWM_DIR = "set in Makefile.local"

# include Makefile.local if it exists
-include Makefile.local

# Cygwin 環境なら Windows ネイティブパスを取得、そうでなければ CURDIR
UNAME_O := $(shell uname -o)
ifeq ($(UNAME_O),Cygwin)
  CURRENT_DIR := $(shell cygpath -ma .)
else
  CURRENT_DIR := $(CURDIR)
endif


build:
	docker build -t howm-mcp .

dev:
	docker run --rm -it \
		-v ${CURRENT_DIR}/src:/app \
		-v ${HOWM_DIR}:/docs/howm:ro \
		--entrypoint /bin/bash ${MCP_IMAGE}

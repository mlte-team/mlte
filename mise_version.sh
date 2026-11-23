#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$PROJECT_ROOT/mise.toml"

VERSION="$(sed -nE \
  's/^[[:space:]]*min_version[[:space:]]*=[[:space:]]*"([0-9]+\.[0-9]+\.[0-9]+)"[[:space:]]*(#.*)?$/\1/p' \
  "$CONFIG")"

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: mise.toml must contain one min_version = \"X.Y.Z\" entry" >&2
  exit 1
fi

printf '%s\n' "$VERSION"
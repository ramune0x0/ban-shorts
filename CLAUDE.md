# ban-youtube

YouTube の視聴をブロックするツール群。

## 概要

- `/etc/hosts` ベースの Mac 向けブロックスクリプト
- 自作 DNS ブロッカー（クロスデバイス対応、プロダクト化を視野）

## 技術スタック

- Python（スクリプト・DNS サーバー）
- uv（パッケージ管理）

## コマンド

```bash
# hosts ブロックの ON/OFF
sudo python scripts/hosts_blocker.py on
sudo python scripts/hosts_blocker.py off

# DNS サーバー起動（開発中）
# uv run python -m ban_youtube.server
```

## ディレクトリ構成

```
scripts/         # 単発スクリプト（hosts_blocker 等）
src/ban_youtube/ # 自作 DNS ブロッカー本体
docs/            # 設計ドキュメント
```

# ban-youtube

YouTube の視聴をコントロールするためのツール群。

- **PC ブラウザでは Shorts だけ止めたい**（勉強動画は見たい）→ Chrome 拡張
- **スマホでは YouTube 全体を止めたい**（時間の浪費・勉強目的なら PC で）→ NextDNS

## 1. Shorts ブロック Chrome 拡張（Phase 1 完了）

Arc / Chrome で動作する Shorts 専用ブロッカー。
設計の詳細は [`docs/adr/0001-browser-extension-blocker.md`](docs/adr/0001-browser-extension-blocker.md)。

### インストール（開発者モードでローカル読み込み）

1. Arc / Chrome で `chrome://extensions` を開く
2. 右上の **デベロッパーモード** を ON
3. **パッケージ化されていない拡張機能を読み込む** をクリック
4. このリポジトリの `extension/` ディレクトリを選択

読み込むと `*.youtube.com/shorts/*` と `youtu.be/shorts/*` がブロック画面にリダイレクトされ、
ホーム・サイドバー・検索結果の Shorts 関連 UI も非表示になる。

## 2. スマホで YouTube 全体ブロック（NextDNS）

iPhone / Android のすべてのアプリ・ブラウザから YouTube を遮断する個人運用向け手順。
Shorts だけを選択的にブロックすることは DNS レベルでは不可能なため、**YouTube 全体を止める**
割り切り運用。手順は [`docs/nextdns-setup.md`](docs/nextdns-setup.md) を参照。

## 3. hosts ブロッカー（Mac ローカル）

`/etc/hosts` を編集して自分の Mac だけ YouTube を遮断する軽量版。
NextDNS を使うほどでもない検証用や、短時間の集中ブロックに。

```bash
sudo python scripts/hosts_blocker.py on      # ブロック有効化
sudo python scripts/hosts_blocker.py off     # ブロック解除
sudo python scripts/hosts_blocker.py status  # 状態確認
```

## セットアップ（Python 側）

```bash
# Python 3.12+
uv sync
```

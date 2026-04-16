# ADR-0001: YouTube Shorts ブロッカーは Chrome 拡張で実装する

- ステータス: 採用
- 日付: 2026-04-16

## 背景

YouTube Shorts を見てしまうのを止めたい。**PC では Shorts だけ止めたい**
（勉強動画の視聴は継続したい）。同じ悩みを持つ人にも配布できる形にしたい。

スマホで YouTube を見てしまう問題は別レイヤーで解決する（後述）。

## 検討した選択肢

### 1. DNS / NextDNS でのブロック
- DNS クエリはホスト名しか含まず、URL パス（`/shorts/...`）は不可視
- Shorts 単体ブロックは原理的に不可能
- ただし「YouTube 全体ブロック」なら端末横断・アプリ内にも効く最強の手段

### 2. HTTPS 復号プロキシ（mitmproxy 等）
- 端末に自前 CA を仕込めばパスで判別可能
- 設定が重く、配布には向かない

### 3. Chrome 拡張（採用）
- `declarativeNetRequest` で URL パス単位のブロックが宣言的に書ける
- content script で DOM を操作して Shorts 関連 UI を消せる
- Arc / Chrome は Chromium ベースで同一拡張が動く
- Chrome ウェブストアで配布すれば非エンジニアでも 1 クリックで導入できる

### 4. Safari 拡張化（不採用）
- iPhone Safari も WebExtension 規格対応で、Xcode でラップすれば可能
- ただし App Store 公開には Apple Developer Program $99/年が必要
- 自分の主ブラウザが Chrome/Arc で Safari をほぼ使わない
- ランニングコストに見合わないため**スコープ外**とする

## 決定

**Chrome 拡張（MV3）で実装する。** 配布は Chrome ウェブストア経由。

スマホ対応は拡張としては行わず、「YouTube 全体ブロック（NextDNS）」で各自が対処する運用を推奨する
（[`docs/nextdns-setup.md`](../nextdns-setup.md) 参照）。

## フェーズ

### Phase 1（完了）: Chrome 拡張で Shorts 専用ブロック
- Arc / Chrome で動作
- `*://*.youtube.com/shorts/*` と `*://youtu.be/shorts/*` をブロック画面へリダイレクト
- SPA 内部遷移にも対応（content script で URL を監視）
- Shorts 関連 UI 要素（サイドバー・ホームの棚・検索結果・日本語「ショート」チップ）を DOM で非表示
- 開発者モードでローカル読み込みにて動作確認済み

### Phase 2（将来）: Chrome ウェブストア公開
- $5 の開発者登録（1 回のみ・生涯有効）
- アイコン・スクリーンショット・説明文・プライバシーポリシー整備
- 審査提出

## 非対象（やらないこと）

- **iPhone Safari 対応**: Apple Developer Program $99/年のランニングコストが見合わない
- **Android ブラウザ対応**: Chrome は拡張非対応、Firefox Mobile は配布先想定外
- **スマホで Shorts だけブロック**: DNS では不可能、Safari 拡張は非対象のため実現手段なし

スマホで YouTube を遮断したい人は NextDNS で**全体**ブロックを推奨する。
これは「スマホで YouTube を見るのは時間の浪費、勉強目的なら PC を使うべき」
という自戒の観点でもむしろ理に適っている。

## 設計（Phase 1）

### スコープ
- 対象 URL: `*://*.youtube.com/shorts/*`, `*://youtu.be/shorts/*`
- 対象 resource: `main_frame` のみ（他サイトへの埋め込み iframe は対象外）

### ブロック方式
- `declarativeNetRequest` の redirect で `extension/blocked.html` へ遷移
- SPA 内部遷移は `declarativeNetRequest` で捕捉できないため、content script でも
  `location.pathname` を監視してリダイレクトする二重構え

### UI 要素の非表示
URL ブロックだけでは「Shorts」タブやホームの Shorts 棚が空枠で残るため、
content script で CSS を注入して DOM から隠す。日本語環境の「ショート」チップは
CSS だけではテキスト判定できないため MutationObserver + JS で対応。

### 設定 UI
**持たない**。常時 Shorts ブロック。トグルを付けると抜け道になりセルフコントロールを弱める。
オフにしたい時は拡張自体を無効化する。

## 構成

```
extension/
├── manifest.json       # MV3
├── content.js          # URL 監視 + DOM 非表示
├── blocked.html        # リダイレクト先
└── rules/
    └── shorts.json     # /shorts/* を redirect
```

background service worker は不要（ruleset が常時有効、状態を持たない）。

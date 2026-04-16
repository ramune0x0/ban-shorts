# スマホ向け YouTube 全体ブロック（NextDNS セットアップ）

スマホ（iPhone / Android）のすべてのアプリ・ブラウザから YouTube を遮断するための手順。
DNS レベルでブロックするので、YouTube アプリを入れ直そうが Safari で開こうが無力化される。

## 前提

- DNS では URL パスが見えないため **Shorts だけのブロックは不可能**
- この手順は **YouTube 全体を遮断**する。スマホで勉強動画を見ることも出来なくなる
- スマホで見ない運用前提（勉強目的の視聴は PC 側で行う）

## 1. NextDNS アカウント作成

1. <https://my.nextdns.io/signup> にアクセス
2. Google アカウントでサインアップ（無料）
3. 初期プロファイル（例: `abc123`）が自動作成される。この **プロファイル ID** を後で使う

無料枠は月 30 万クエリ。個人利用なら十分。

## 2. denylist にドメインを登録

管理画面の **Denylist** タブで以下を追加する。

### 最低限

| ドメイン | 用途 |
| --- | --- |
| `youtube.com` | 本体（サブドメイン含む設定で `m.` `www.` もカバー） |
| `youtu.be` | 短縮 URL |

NextDNS の denylist は**ドメイン単位で登録するとサブドメインも自動でブロック対象**になるため、
`youtube.com` 1 件で `www.youtube.com` / `m.youtube.com` も落ちる。

### 念のため追加（動画再生経路まで封じる）

`youtube.com` だけだとキャッシュ等で動画再生が成功するケースがあるため、以下も追加すると確実。

| ドメイン | 用途 |
| --- | --- |
| `googlevideo.com` | 動画ストリーミング |
| `ytimg.com` | サムネ画像 |
| `youtubei.googleapis.com` | YouTube API |

## 3. iPhone に構成プロファイルを導入

1. iPhone の Safari で以下の URL を開く:

    ```
    https://apple.nextdns.io/
    ```

2. NextDNS にサインインするか、プロファイル ID（`abc123` など）を直接入力
3. `.mobileconfig` ファイルがダウンロードされる
4. iPhone の **設定** → **一般** → **VPN とデバイス管理** に移動
5. 「ダウンロード済みプロファイル」に NextDNS が出ているのでタップ → **インストール**
6. パスコードを入力

これで iPhone の DNS が NextDNS 経由になる。

## 4. Android（補足）

Android 9+ は OS 標準で Private DNS をサポート。

1. **設定** → **ネットワークとインターネット** → **プライベート DNS**
2. 「プライベート DNS プロバイダのホスト名」に以下を入力:

    ```
    <プロファイルID>.dns.nextdns.io
    ```

    例: `abc123.dns.nextdns.io`

3. 保存

## 5. 動作確認

- iPhone Safari で `https://www.youtube.com/` を開く → **接続できない** / **DNS エラー**
- YouTube アプリを起動 → 動画一覧が読み込めない
- 他のサイトは普通に開けることを確認

## 困ったとき

- **一時的に無効化したい**: 設定 → 一般 → VPN とデバイス管理 → NextDNS のプロファイルを削除。元に戻す時は再インストール
- **ブロックが効かない**: NextDNS 管理画面の「ログ」タブを見ると、どの端末からどのドメインに問い合わせがあったか確認できる。プロファイル ID が合っているか、denylist が反映されているか確認
- **一部の動画だけ再生できてしまう**: 「念のため追加」のドメインをまだ入れてない可能性。`googlevideo.com` を追加する

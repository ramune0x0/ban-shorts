"""YouTube ブロッカー: /etc/hosts を編集して YouTube ドメインをブロックする。

Usage:
    sudo python scripts/hosts_blocker.py on   # ブロック有効化
    sudo python scripts/hosts_blocker.py off   # ブロック解除
    sudo python scripts/hosts_blocker.py status # 現在の状態を表示
"""

import sys
from pathlib import Path

HOSTS_PATH = Path("/etc/hosts")
BLOCK_MARKER_BEGIN = "# >>> ban-youtube BEGIN"
BLOCK_MARKER_END = "# >>> ban-youtube END"

YOUTUBE_DOMAINS = [
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "youtube-nocookie.com",
    "www.youtube-nocookie.com",
    "youtubei.googleapis.com",
    "yt3.ggpht.com",
    "yt3.googleusercontent.com",
    "i.ytimg.com",
    "s.ytimg.com",
]


def build_block_entries() -> str:
    lines = [BLOCK_MARKER_BEGIN]
    for domain in YOUTUBE_DOMAINS:
        lines.append(f"0.0.0.0 {domain}")
    lines.append(BLOCK_MARKER_END)
    return "\n".join(lines)


def read_hosts() -> str:
    return HOSTS_PATH.read_text()


def is_blocked(content: str) -> bool:
    return BLOCK_MARKER_BEGIN in content


def remove_block(content: str) -> str:
    """既存のブロックエントリを除去する。"""
    lines = content.splitlines()
    result: list[str] = []
    inside_block = False
    for line in lines:
        if line.strip() == BLOCK_MARKER_BEGIN:
            inside_block = True
            continue
        if line.strip() == BLOCK_MARKER_END:
            inside_block = False
            continue
        if not inside_block:
            result.append(line)
    return "\n".join(result)


def enable_block() -> None:
    content = read_hosts()
    if is_blocked(content):
        print("既にブロック中です")
        return
    new_content = content.rstrip("\n") + "\n\n" + build_block_entries() + "\n"
    HOSTS_PATH.write_text(new_content)
    flush_dns_cache()
    print(f"YouTube をブロックしました（{len(YOUTUBE_DOMAINS)} ドメイン）")


def disable_block() -> None:
    content = read_hosts()
    if not is_blocked(content):
        print("ブロックされていません")
        return
    new_content = remove_block(content)
    HOSTS_PATH.write_text(new_content)
    flush_dns_cache()
    print("YouTube のブロックを解除しました")


def show_status() -> None:
    content = read_hosts()
    if is_blocked(content):
        print("状態: ブロック中")
    else:
        print("状態: ブロックなし")


def flush_dns_cache() -> None:
    import subprocess

    subprocess.run(
        ["dscacheutil", "-flushcache"],
        check=True,
    )
    subprocess.run(
        ["killall", "-HUP", "mDNSResponder"],
        check=True,
    )
    print("DNS キャッシュをクリアしました")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    match command:
        case "on":
            enable_block()
        case "off":
            disable_block()
        case "status":
            show_status()
        case _:
            print(f"不明なコマンド: {command}")
            print(__doc__)
            sys.exit(1)


if __name__ == "__main__":
    main()

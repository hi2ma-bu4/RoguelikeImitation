# coding: utf-8
"""
起動用ファイル
"""

from lib.auto_pip import ImportCheck


def main() -> None:
    print("起動しない場合はgame.pyを直接実行して下さい")
    ic = ImportCheck(debug=True)
    # pip install
    ic.loadPip("pygame")
    ic.loadPip("readchar")

    # game.py を読み込み
    ic.loadImport("game")
    # game.py を実行
    ic.importData["game"].main()


if __name__ == "__main__":
    main()
    exit(0)

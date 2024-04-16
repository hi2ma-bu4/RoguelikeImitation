# coding: utf-8
"""
pythonでローグライクを作りたい！！！
"""


import pygame
import sys
import os

from roguelike import Roguelike
from lib.windowsColor import W_Color as w
from control import main as ctrl_main
from MANUAL import main as manual_main


# todo: 必要性一覧
# ◆アイテム鑑定
# ┗◆アイテム

############################################################
# *init(ファイルパス)
############################################################
dataPath = {
    "userData": "data/userData.db",

    "imageCSV": "data/imageList.csv",
    "floorData": "data/floorData.json",
    "enemyData": "data/enemyData.json",
    "itemData": "data/itemData.json",

    "mainFont": "font/Nasu-Regular.ttf",
    "subFont": "font/SourceHanCodeJP.ttc",
}
############################################################
# *main
############################################################


def main():

    # カレントディレクトリ修正
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # pygame初期化
    pygame.init()
    pygame.key.set_repeat(50, 50)
    pygame.display.set_caption("ローグライクを作りたかった...")

    # 本体生成
    rl = Roguelike(
        pygame, (20, 30), 32,
        fontPath=[dataPath["mainFont"], dataPath["subFont"]]
    )
    # 構成ファイルpath読み込み
    rl.fileInit(
        dataPath["imageCSV"], dataPath["floorData"],
        dataPath["enemyData"], dataPath["itemData"]
    )
    rl.db_setting(dataPath["userData"])

    # 表示更新ループ
    is_running = True
    while is_running:
        if rl.isPlayGame:
            # ターン処理実行
            rl.playTurn()

        # 描画処理実行
        chDr = rl.allDrawing()
        rl.Menu.drawAll(chDr)

        # イベントを処理
        ret = rl.Menu.getEvent()
        if ret == 1:
            if not rl.isGameOver:
                rl.game_save()
        elif ret == -1:
            is_running = False
            if not rl.isGameOver:
                rl.game_save()
        elif ret == -2:
            is_running = False

        # 描画
        try:
            pygame.display.flip()
        except Exception:
            pygame.display.update()

    pygame.quit()
    sys.exit()


def cont() -> None:
    ctrl_main(dataPath["userData"], "saveData")


def manual() -> None:
    manual_main()


if __name__ == '__main__':
    # コマンド引数取得
    args = sys.argv
    if len(args) <= 1:
        print(f"""
{w.FLASH}{w.L_RED}起動はinit.pyを実行して下さい！{w.RESET}
init.pyを{w.UNDERLINE}{w.RED}無視して実行する{w.RESET}場合は{w.YELLOW}Ctrl+C{w.RESET}か{w.YELLOW}Ctrl+Z{w.L_YELLOW}->{w.YELLOW}Enter{w.RESET}を
init.pyを{w.UNDERLINE}{w.RED}実行する{w.RESET}場合は{w.YELLOW}Enter{w.RESET}を実行してgame.pyを終了して下さい
{w.L_BLACK}この警告を表示させずに実行する場合は{w.DARK}{w.YELLOW}load{w.RESET}{w.L_BLACK}オプションを使用して下さい{w.RESET}
{w.L_BLACK}セーブデータの内容を確認する場合は{w.DARK}{w.YELLOW}control{w.RESET}{w.L_BLACK}オプションを使用して下さい{w.RESET}""")
        f = 1
        try:
            s = input(">> ")
            f = 0
            if s == "control":
                cont()
                exit(0)
            elif s == "manual":
                manual()
                exit(0)
        except:
            if f:
                os.system("cls")
                print("game.py強制実行")
                main()
                exit(0)
        print("終了しています...")
        exit(1)
    else:
        if args[1] == "load":
            main()
            exit(0)
        elif args[1] == "control":
            cont()
            exit(0)
        elif args[1] == "manual":
            manual()
            exit(0)
        else:
            print(f"{w.L_RED}不明な引数{w.RESET}")
            exit(1)

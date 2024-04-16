# coding: utf-8
"""
roguelikeのシステムデータを確認するためのモジュール
"""

from typing import Any, List, Dict, Final, final
import readchar
import os
from json import dumps

from lib.files import SqlManager
import lib.terminalDraw as td
import lib.stringLib as sl
from lib.windowsColor import W_Color
from lib.compress import Comp


@final
def main(db_path: str, table_name: str) -> None:
    # カレントディレクトリ修正
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    cr = Control(db_path, table_name)
    while 1:
        cr.drawDisplay()
        if cr.getKey():
            break
    os.system("cls")
    print(W_Color.RESET)
    exit(0)


@final
class Control:
    def __init__(self, db_path: str, table_name: str) -> None:
        self.data: Final[SqlManager] = SqlManager(db_path, table_name)
        self.td_dos: Final[td.DrawObjStore] = td.DrawObjStore({
            "ENTER": readchar.key.ENTER,
            "BACKSPACE": readchar.key.BACKSPACE,
            "DELETE": readchar.key.DELETE,
            "TAB": readchar.key.TAB,
        })
        self.comp = Comp()

        self.displayType: List[int] = [0]

        self.userDataList: List[Any] = []
        self.userData: Dict[str, Any] = dict()

        # 内容配列
        self.dbKeys = [
            "seed", "posData", "status",
            "killEnemy", "floorEnemyData", "darkData"
        ]
        self._menuStrList = ["セーブデータ一覧", "特定セーブデータ表示", "終了"]

        self._drawMenu()

    def drawDisplay(self) -> None:
        self.td_dos.drawTerminal()

    def getKey(self) -> bool:
        key = readchar.readchar()
        if key in "\u0000\u00E0":
            key = "\u0000"+readchar.readchar()

        dl = len(self.displayType)
        if dl == 1:
            if key == "1" or key == "2":
                self.changeDisplayType(int(key), 0)
                self.td_dos.addLayer(True)
                self.td_dos.addObj(td.DrawSquare(
                    1, 1, lambda ts: ts.column, lambda ts: ts.line,
                    border=f"{W_Color.DARK}#{W_Color.RESET}"
                ))

                self.td_dos.addObj(td.DrawText(
                    2, 3, lambda ts: ts.column-2, text=self._menuStrList[self.displayType[0]-1]
                ))

                if key == "1":
                    self.td_dos.popupDraw(
                        f"wait...\n\nユーザー名一覧を取得しています...",
                        sec=0.2,
                        waitFunc=lambda: self.get_userDataList(),
                    )
                    self.td_dos.addObj(td.DrawText(
                        4, 5,
                        text=f"{W_Color.L_CYAN}{sl.rjust('名前', 26)}{W_Color.RESET} データサイズ"
                    ))
                    drl = [
                        [
                            W_Color.CYAN+v["userName"]+W_Color.RESET,
                            str(v["useByte"])+"byte"
                        ] for v in self.userDataList
                    ]
                    self.td_dos.addObj(td.DrawTableText(
                        4, 7, lambda ts: ts.column-8, lambda ts: ts.line-6,
                        drl, [(25, "r"), (-1, "l")],
                    ))
                elif key == "2":
                    self.td_dos.addLayer(False)
                    self.td_dos.addObj(td.DrawSquare(
                        lambda ts: int(ts.column/2)-18, 6, 38, 9,
                    ))
                    self.td_dos.addObj(td.DrawText(
                        lambda ts: int(ts.column/2)-16, 8, 32, text="ユーザー名を入力"
                    ))
                    self.td_dos.addObj(td.DrawSquare(
                        lambda ts: int(ts.column/2)-16, 10, 34, 3
                    ))
                    self.td_dos.addObj(td.DrawText(
                        lambda ts: int(ts.column/2)-14, 11, text=""
                    ))

            if key == "@":
                self.td_dos.popupDraw("wait...\n\n終了処理を実行しています...", sec=0.5)
                return True
        elif dl == 2:
            if key == readchar.key.ESC:
                if self.displayType == [2, 0]:
                    self.td_dos.removeLayer()
                self.td_dos.removeLayer()
                self.changeDisplayType(-1)
                self.changeDisplayType(0)

            ret = -1
            if self.displayType[0] == 1:
                if self.displayType[1] == 0:
                    tObj = self.td_dos.getObj()
                    if isinstance(tObj, td.DrawTableText):
                        if key == readchar.key.UP:
                            tObj.listScroll(-1)
                        elif key == readchar.key.DOWN:
                            tObj.listScroll(1)
                        self.td_dos.displayChange()
                    else:
                        raise RuntimeError("テーブルオブジェクトが取得できません")
            elif self.displayType[0] == 2:
                if self.displayType[1] == 0:
                    if key not in [readchar.key.LEFT, readchar.key.UP, readchar.key.RIGHT, readchar.key.DOWN]:
                        ret = self.td_dos.addStrObj(
                            key, "\\S", 30, True, objInd=-1
                        )
                    if isinstance(ret, str):
                        self.usName = ret
                        self.td_dos.popupDraw(
                            f"wait...\n\nユーザー名「{ret}」を検索しています...",
                            sec=0.2,
                            waitFunc=lambda: self.get_userData(self.usName),
                        )
                        if len(self.userData) > 0:
                            self.td_dos.removeLayer()
                            drl = [
                                [
                                    W_Color.CYAN+"seed:"+W_Color.RESET,
                                    self.userData["seed"]
                                ],
                                [
                                    W_Color.CYAN+"posData:"+W_Color.RESET,
                                    self.comp.decompress(
                                        self.userData["posData"])
                                ],
                                [
                                    W_Color.CYAN+"status:"+W_Color.RESET,
                                    self.comp.decompress(
                                        self.userData["status"])
                                ],
                                [
                                    W_Color.CYAN+"killEnemy:"+W_Color.RESET,
                                    self.comp.decompress(
                                        self.userData["killEnemy"])
                                ],
                                [
                                    W_Color.CYAN+"floorEnemyData:"+W_Color.RESET,
                                    self.comp.decompress(
                                        self.userData["floorEnemyData"])
                                ],
                                [
                                    W_Color.CYAN+"darkData:"+W_Color.RESET,
                                    self.comp.decompress(
                                        self.userData["darkData"])
                                ],
                            ]
                            self.td_dos.addObj(td.DrawTableText(
                                4, 5, lambda ts: ts.column-8, lambda ts: ts.line-6,
                                drl, [(15, "r"), (-1, "l")],
                                isBlankLine=True
                            ))
                            self.changeDisplayType(1)
                        else:
                            self.td_dos.popupDraw(
                                f"{W_Color.L_RED}Error{W_Color.RESET}\n\nユーザー名「{ret}」は存在しません！",
                                sec=1
                            )
                elif self.displayType[1] == 1:
                    tObj = self.td_dos.getObj()
                    if isinstance(tObj, td.DrawTableText):
                        if key == readchar.key.UP:
                            tObj.listScroll(-1)
                        elif key == readchar.key.DOWN:
                            tObj.listScroll(1)
                        self.td_dos.displayChange()
                    else:
                        raise RuntimeError("テーブルオブジェクトが取得できません")

        return False

    def changeDisplayType(self, parInd: int = -2, addInd: int = -1) -> None:
        dl = len(self.displayType)
        if parInd == -1:
            if dl <= 0:
                self.displayType.append(0)
            else:
                self.displayType.pop(-1)
        else:
            if parInd >= 0:
                if dl <= 0:
                    self.displayType.append(parInd)
                else:
                    self.displayType[-1] = parInd
            if addInd >= 0:
                self.displayType.append(addInd)

    def _drawMenu(self) -> None:
        self.td_dos.addLayer()
        self.td_dos.addObj(td.DrawSquare(
            1, 1,
            lambda ts: ts.column, lambda ts: ts.line,
            border=f"{W_Color.DARK}#{W_Color.RESET}"
        ))
        self.td_dos.addObj(td.DrawText(
            2, 3,
            lambda ts: ts.column-2, text="MENU"
        ))

        msl = len(self._menuStrList)
        for i in range(msl):
            ind = "@" if i == msl-1 else i+1
            self.td_dos.addObj(td.DrawText(
                4, 6+i*2,
                text=f"{ind} :{self._menuStrList[i]}"
            ))

    def get_userDataList(self) -> bool:
        tmp = self.data.select()
        if len(tmp) > 0:
            tDBKeys = [
                "userName",
                *self.dbKeys
            ]
            self.userDataList = []
            for v in tmp:
                self.userDataList.append({
                    tDBKeys[i]: v[i] for i in range(len(tDBKeys))
                })
                self.userDataList[-1]["useByte"] = len(
                    str(self.userDataList[-1])
                )
            return True
        else:
            self.userDataList = []
            return False

    def get_userData(self, name) -> bool:
        tmp = self.data.select(
            select=",".join(self.dbKeys),
            where=f"userName='{name}'"
        )
        if len(tmp) > 0:
            self.userData = {
                self.dbKeys[i]: tmp[0][i] for i in range(len(self.dbKeys))
            }
            return True
        else:
            self.userData = {}
            return False

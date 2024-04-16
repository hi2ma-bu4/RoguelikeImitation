# coding: utf-8
"""
tkcをjsonで操作出来るようにしたやつ
(本体)
"""

from typing import Any, Dict, Tuple, List, Optional, Union, Literal, TypeVar, cast, Final
from json import load

from tkinterControl import Tkc
from tkinterJSON.func import TkJSONFunc

# type alias

ta_dict_inout = TypeVar("ta_dict_inout")

ta_poss = Tuple[Union[int, Literal["max"]], Union[int, Literal["max"]]]

# ここまで


class TkJson:
    """
    tkinterJSON (本体)

    ---
    以下の順に実行して下さい
    * loadFunctionClass
    * runConfiguration
    * drawStart

    """

    Tkc = Tkc

    def __init__(self, jsonPath: str, tkc: Optional[Tkc] = None) -> None:
        self._windowData: Dict[str, Any] = {}

        self._jsonPath: Final[str] = jsonPath
        self.jsonData: Final[
            Dict[str, Dict[str, Any]]
        ] = self._jsonLoad(jsonPath)

        if tkc is None:
            tj = self._dictGet(self.jsonData, "TkJSON")
            if tj is not None:
                # ウィンドウ
                win: Optional[Dict[str, Any]] = self._dictGet(
                    tj, "window"
                )
                if win is not None:
                    self._windowData = win

            w_title: Optional[str] = self._dictGet(self._windowData, "title")
            if w_title is None:
                w_title = "TkJson"
            w_size: Optional[ta_poss] = self._dictGet(
                self._windowData, "size"
            )
            if w_size is None:
                w_size = (500, 300)
            w_pos: Optional[ta_poss] = self._dictGet(
                self._windowData, "pos"
            )
            w_resizable: Optional[tuple[bool, bool]] = self._dictGet(
                self._windowData, "resizable"
            )
            w_minSize: Optional[Tuple[int, int]] = self._dictGet(
                self._windowData, "minSize"
            )
            W_maxSize: Optional[Tuple[int, int]] = self._dictGet(
                self._windowData, "maxSize"
            )
            tkc = Tkc(
                title=w_title, windowSize=w_size,
                windowPos=w_pos, resizable=w_resizable,
                minSize=w_minSize, maxSize=W_maxSize
            )
        self.tkc: Final[Tkc] = tkc

        self._tkf: TkJSONFunc

    def loadFunctionClass(self, tkf: TkJSONFunc) -> None:
        """
        内部関数呼び出し用の設定クラスを設定する
        (TkJSONFuncの継承クラス)
        """
        self._tkf = tkf

    def runConfiguration(self) -> None:
        """
        jsonを元にframe,widgetを設置
        """

        fl = self._tkf._getFuncList()

        firstFrame: str = ""
        for frameName, frameData in self.jsonData.items():
            # 設定の読み込み
            if frameName == "TkJSON":
                # テーマ
                t: Optional[str] = self._dictGet(frameData, "theme")
                if t is not None:
                    if not self.tkc.useTheme(t):
                        raise ValueError(f"存在しないテーマ名「{t}」")

                # フォント
                fs = self._dictGet(frameData, "fonts")
                if fs is not None:
                    for font in fs:
                        self.tkc.createFont(**font)

                # スタイル
                ss = self._dictGet(frameData, "styles")
                if ss is not None:
                    for style in ss:
                        self.tkc.createStyle(**style)

                continue

            # フレーム設定
            ic: Optional[Dict[str, Any]] = self._dictGet(frameData, "isChild")
            pn: Optional[str] = self._dictGet(frameData, "parent")
            if ic is None:
                self.tkc.frames.add(frameName)
                if firstFrame == "":
                    firstFrame = frameName
            else:
                if pn is not None:
                    self.tkc.frames.call(pn)
                self.tkc.frames.addChild(
                    frameName, **ic
                )

            # グリッド設定
            grids: Optional[
                Dict[str, Dict[str, Any]]
            ] = self._dictGet(frameData, "grid")
            if grids is not None:
                for key, grid in grids.items():
                    k: List[str] = key.split("-")
                    if len(k) <= 1:
                        continue
                    rc = cast(Literal["row", "column"], k[0])
                    if k[1] == "all":
                        self.tkc.frames.allGridConfigure(rc, **grid)
                    else:
                        self.tkc.frames.gridConfigure(rc, int(k[1]), **grid)

            widget: Optional[
                List[Dict[str, Any]]
            ] = self._dictGet(frameData, "widgets")
            if widget is not None:
                oldWidType = ""

                for wid in widget:
                    widType: Optional[str] = self._dictGet(wid, "widType")
                    if widType is None:
                        widType = oldWidType
                    else:
                        oldWidType = widType

                    command = None

                    callName: Optional[str] = self._dictGet(wid, "call")

                    if callName is not None:
                        command = (
                            lambda e=None, c=callName: self.tkc.frames.call(c)
                        )
                    else:
                        com: Optional[str] = self._dictGet(wid, "command")
                        if com is not None and com in fl:
                            command = fl[com]

                    args: Optional[Dict[str, Any]] = self._dictGet(wid, "args")
                    if args is None:
                        args = {}

                    w = None

                    if widType == "label":
                        w = self.tkc.widgets.addLabel(**args)
                    elif widType == "button":
                        w = self.tkc.widgets.addButton(com=command, **args)
                    elif widType == "entry":
                        w = self.tkc.widgets.addEntry(**args)
                    elif widType == "placeholderEntry":
                        w = self.tkc.widgets.addPlaceholderEntry(**args)
                    elif widType == "listbox":
                        w = self.tkc.widgets.addListbox(**args)
                    elif widType == "treeview":
                        w = self.tkc.widgets.addTreeview(**args)
                    elif widType == "checkbutton":
                        w = self.tkc.widgets.addCheckbutton(
                            com=command, **args)
                    elif widType == "radiobutton":
                        w = self.tkc.widgets.addRadiobutton(
                            com=command, **args)
                    elif widType == "scale":
                        w = self.tkc.widgets.addScale(com=command, **args)
                    elif widType == "scrollbar":
                        w = self.tkc.widgets.addScrollbar(com=command, **args)
                    elif widType == "message":
                        w = self.tkc.widgets.addMessage(**args)
                    elif widType == "combobox":
                        w = self.tkc.widgets.addCombobox(**args)
                    elif widType == "progressbar":
                        w = self.tkc.widgets.addProgressbar(**args)
                    elif widType == "spinbox":
                        w = self.tkc.widgets.addSpinbox(com=command, **args)
                    elif widType == "text":
                        w = self.tkc.widgets.addText(**args)
                    else:
                        print("unknown widType: " + widType)

                    if w is not None:
                        bi = self._dictGet(wid, "bind")
                        if bi is not None:
                            for key, value in bi.items():
                                if value in fl:
                                    w.bind(key, fl[value], True)

            forget: Optional[bool] = self._dictGet(frameData, "forget")
            if forget:
                self.tkc.frames.forget(frameName)

        self.tkc.frames.call(firstFrame)

    def drawStart(self) -> None:
        self.tkc.drawStart()

    def drawEnd(self) -> None:
        self.tkc.drawEnd()

    @staticmethod
    def _jsonLoad(jsonPath: str) -> Any:
        with open(jsonPath, "r", encoding="utf-8") as f:
            return load(f)

    @staticmethod
    def _dictGet(dic: Dict[Any, ta_dict_inout], key: str) -> Optional[ta_dict_inout]:
        if key in dic:
            return dic[key]
        return None

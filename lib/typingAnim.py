# coding: utf-8
"""
タイピングアニメーション作成用
"""

from typing import List, Tuple, Final
from re import compile

from lib.romaji import Romaji


class TypingAnim:
    r"""
    ### タイピングアニメーション
    ---

    #### 制御文字
    * \n            : 改行(確定)
    * //b            : 前の文字を消す

    * //k           : 強制確定
    * //e           : 英語入力開始(初期値)
    * //j           : 日本語入力開始
    * ≪text,text,≫: 変換アニメーション

    * \u2061: 使用不可(コマンド置き換え用)
    """

    NOT_USE_CHAR: Final[str] = "\u2061"

    # *形式に変換
    # 特殊文字取得
    _RE_SPECIAL_CHAR: Final = compile(
        r"\n|//[bejk]|≪[^,≫]+?(?:,[^,≫]+?)*≫"
    )
    # 「かな文字」の前に「//j」設置
    _RE_KANA_CHAR: Final = compile(
        r"((?:[あ-んア-ン\n、。！？]|//[bjk])+)"
    )
    # 「カタカナ」の後ろに変換記号設置
    _RE_KATAKANA_CHAR: Final = compile(
        r"((?:[ア-ン])+)"
    )
    # 「英数字」の前に「//e」設置
    _RE_ENG_CHAR: Final = compile(
        r"([a-zA-Z0-9](?<!//[bejk])[a-zA-Z0-9]*)"
    )

    # 変換記号の後ろに「//k」設置
    _RE_END_PARENTHESIS_CHAR: Final = compile(
        r"(≪[^≫]+≫)"
    )
    # 連続した変換記号を結合
    _RE_JOIN_PARENTHESIS_CHAR: Final = compile(
        r"(≪[^≫]+)≫(?://k)?≪([^≫]+≫)"
    )

    # *無駄な処理を減らす
    # [jk]の後のeやeの後のkは無駄なので削除
    _RE_IDENTITY1_CHAR: Final = compile(
        r"//[jk]//e|//e//k"
    )
    # kの前後のjは無駄なので削除
    _RE_IDENTITY2_CHAR: Final = compile(
        r"(?://j)?//k(?://j)?"
    )
    # [ejk]を繰り返し設置するのは無駄なので削除
    _RE_REPETITION_CHAR: Final = compile(
        r"(//[ejk])\1*"
    )

    # 変換記号の中に特殊文字はいらないので削除
    _RE_DEL_INTERIOR_CHAR: Final = compile(
        r"//[bejk]"
    )

    def __init__(self, text: str, surroundChar: Tuple[str, str] = ("|", "|"), *, animSpeed: int = 1, autoChange: bool = True, debug: bool = False) -> None:
        self._text: str = text + "//k"
        if autoChange:
            # 自動で形式に変換
            self._text = self._RE_ENG_CHAR.sub(
                r"//e\1", self._text
            )
            self._text = self._RE_KANA_CHAR.sub(
                r"//j\1", self._text
            )
            self._text = self._RE_KATAKANA_CHAR.sub(
                r"\1≪\1≫", self._text
            )
            self._text = self._RE_END_PARENTHESIS_CHAR.sub(
                r"\1//k", self._text
            )

            # 無駄な処理を減らす
            self._text = self._RE_REPETITION_CHAR.sub(
                r"\1", self._text
            )
            self._text = self._RE_IDENTITY1_CHAR.sub(
                r"//e", self._text
            )
            self._text = self._RE_IDENTITY2_CHAR.sub(
                r"//k", self._text
            )
            self._text = self._RE_REPETITION_CHAR.sub(
                r"\1", self._text
            )

        # 変換文字結合
        self._text = self._RE_JOIN_PARENTHESIS_CHAR.sub(
            r"\1,\2", self._text
        )
        if debug:
            print(self._text)

        self._surroundChar = surroundChar
        # アニメーション
        self.animSpeed = animSpeed
        self._animCou = 0

        self.end = False

        # テキスト
        self._currentInd = 0
        self._specialCurrentInd = 0
        self._conversionInd = 0
        self._textMode = 0
        self._isConversion = False
        self._maxConversionCou = 0
        self._conversionList: List[str] = []
        self.jpRomaji = ""
        self._outText = ""
        self._tmpOutText = ""

        # 整形
        self._useSpecialChar = self._RE_SPECIAL_CHAR.findall(
            self._text
        )
        self._typingText = self._RE_SPECIAL_CHAR.sub(
            self.NOT_USE_CHAR, self._text
        )
        if autoChange:
            self._typingText = Romaji.kana2Romaji(self._typingText)
        self._maxLen = len(self._typingText)

    def __str__(self) -> str:
        ret = self._outText
        if self._tmpOutText != "":
            ret += f"{self._surroundChar[0]}{self._tmpOutText}{self._surroundChar[1]}"
        return ret

    def update(self) -> int:
        """
        更新処理
        """
        if self.end:
            return -1

        self._animCou += 1
        if self._animCou >= self.animSpeed:
            self._animCou = 0
            self.changeAnim()
            return 1
        return 0

    def changeAnim(self) -> None:
        """
        テキスト変更(更新)
        """
        if self._currentInd >= self._maxLen:
            self.end = True
            return

        noNext = False
        oneMore = False

        currentChar = self._typingText[self._currentInd]
        if self._isConversion:
            self._tmpOutText = self._conversionList[self._conversionInd]
            self._conversionInd += 1
            if self._maxConversionCou <= self._conversionInd:
                self._isConversion = False
            noNext = True
        elif currentChar == self.NOT_USE_CHAR:
            spStr = self._useSpecialChar[self._specialCurrentInd]
            if spStr == "//k":
                # 強制確定
                self._decision()
            elif spStr == "//e":
                # 英語モード
                if self._textMode == 1:
                    self._decision()
                else:
                    oneMore = True
                self._textMode = 0
            elif spStr == "//j":
                # 日本語モード
                self._textMode = 1
                oneMore = True
            elif spStr == "\n":
                # 改行(変換確定)
                if self._textMode == 1:
                    self._decision()
                self._outText += "\n"
            elif spStr == "//b":
                # 1文字削除
                if self.jpRomaji != "":
                    tmp = Romaji.Romaji2Hira(self.jpRomaji)[:-1]
                    self.jpRomaji = Romaji.kana2Romaji(tmp)
                elif self._tmpOutText != "":
                    self._tmpOutText = self._tmpOutText[:-1]
                else:
                    self._outText = self._outText[:-1]

            elif spStr.startswith("≪"):
                # 変換リスト
                self.jpRomaji = ""
                self._isConversion = True
                self._conversionList = self._RE_DEL_INTERIOR_CHAR.sub(
                    "", spStr[1:-1]).split(",")
                self._maxConversionCou = len(self._conversionList)
                self._conversionInd = 0
                oneMore = True
            else:
                raise ValueError("unknown special char: " + spStr)
            self._specialCurrentInd += 1
        else:
            if self._textMode == 0:
                # 普通の英語入力
                self._outText += currentChar
            elif self._textMode == 1:
                # 日本語入力
                self.jpRomaji += currentChar
                self._tmpOutText = Romaji.Romaji2Hira(self.jpRomaji)

        if not noNext:
            self._currentInd += 1
        if oneMore:
            self.changeAnim()

        if self._currentInd >= self._maxLen:
            self.end = True
            return

    def _decision(self):
        if self.jpRomaji == "":
            # 変換
            self._outText += self._tmpOutText
        else:
            # ローマ字
            self._outText += Romaji.Romaji2Hira(self.jpRomaji)
            self.jpRomaji = ""
        self._tmpOutText = ""


if __name__ == "__main__":
    from os import system
    t = TypingAnim(
        "きょうの≪今日の≫3ふん≪分≫//kクッキングは//kしゅん≪旬≫//kの//kやさい≪野菜≫//kが//kはいった≪入った≫//kおにぎり≪西岡≫//k//b//bおにぎり≪西岡,おにぎり≫//kです//k//j≪ - ≫//k10そう≪層≫",
        animSpeed=800000
    )
    while 1:
        ty = t.update()
        if ty == -1:
            break
        elif ty == 1:
            system("cls")
            print(t)

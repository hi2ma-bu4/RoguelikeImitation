# coding: utf-8
"""
tkJsonのjsonからの関数呼び出し用の
継承用クラス定義
"""

from typing import Dict, Callable, Final, final
from abc import ABCMeta
import inspect


class TkJSONFunc(metaclass=ABCMeta):
    """
    tkjの関数呼び出し用の設定クラス

    継承して使用して下さい

    インスタンス関数(メゾット)として
    関数は作成して下さい

    _(アンダーバー)で始まる関数は
    無視されます
    """

    @final
    def _getFuncList(self) -> Dict[str, Callable]:
        funcDict = {}

        for met in inspect.getmembers(self, inspect.ismethod):
            if met[0].startswith("_"):
                continue
            funcDict[met[0]] = met[1]
        return funcDict

    @final
    def _addFunc(self, name: str, func: Callable) -> bool:
        if name == "":
            return False
        if name in self._getFuncList():
            return False
        setattr(self, name, func)
        return True

# coding: utf-8
"""
文字列圧縮ライブラリ
"""

from typing import Any, List, final
from copy import deepcopy
from json import dumps, loads
from re import compile, Match
import bz2
import zlib
import base64


class Comp:
    """
    文字列圧縮クラス
    """

    def __init__(self, dicStr: str = "") -> None:
        # *LZW
        # 初期辞書作成
        self._baseDict: List[str]
        if dicStr == "":
            self._baseDict = list("0123456789abcdef")
        else:
            self._baseDict = list(dicStr)

    @final
    @classmethod
    def class_init(cls):
        # *RLE
        # 正規表現コンパイル
        cls._re_RLE_comp = compile(r"0+|1+")

    @staticmethod
    def compress(text: str) -> str:
        """
        zlibで文字列を圧縮する
        """
        return base64.b64encode(zlib.compress(text.encode())).decode().replace("=", "-")

    @staticmethod
    def decompress(text: str) -> str:
        """
        zlibで文字列を復元する
        """
        return zlib.decompress(base64.b64decode(text.replace("-", "="))).decode()

    def LZW_compress(self, text: str) -> str:
        """
        LZWで文字列を圧縮する
        """
        hexCode = bz2.compress(text.encode('utf-8')).hex()
        codes = self._LZW_compress(hexCode)
        return ','.join([str(c) for c in codes])

    def LZW_decompress(self, text: str) -> str:
        """
        文字列を復元する
        """
        codes = [int(c) for c in text.split(',')]
        hexCode = self._LZW_decompress(codes)
        return bz2.decompress(bytes.fromhex(hexCode)).decode('utf-8')

    def json_compress(self, json: Any) -> str:
        """
        jsonを圧縮する
        """
        return self.compress(dumps(json, separators=(',', ':')))

    def json_decompress(self, text: str) -> Any:
        """
        jsonを復元する
        """
        return loads(self.decompress(text))

    def _LZW_compress(self, text: str) -> List[int]:
        """
        LZWで文字列を圧縮する
        (辞書使用時用)
        """
        dictionary = deepcopy(self._baseDict)
        encoded = []

        current_phrase = text[0]
        for char in text[1:]:
            new_phrase = current_phrase + char
            if new_phrase in dictionary:
                current_phrase = new_phrase
            else:
                encoded.append(dictionary.index(current_phrase))
                dictionary.append(new_phrase)
                current_phrase = char

        encoded.append(dictionary.index(current_phrase))

        return encoded

    def _LZW_decompress(self, codes: List[int]) -> str:
        """
        LZWで文字列を復元する
        (辞書使用時用)
        """
        dictionary = deepcopy(self._baseDict)
        decoded = ''

        current_phrase = dictionary[codes[0]]
        decoded += current_phrase

        for code in codes[1:]:
            if code < len(dictionary):
                new_phrase = dictionary[code]
            else:
                new_phrase = current_phrase + current_phrase[0]

            decoded += new_phrase
            dictionary.append(current_phrase + new_phrase[0])
            current_phrase = new_phrase

        return decoded

    @staticmethod
    def _RLEbin_comp_rep(m: Match) -> str:
        """
        ランレングス圧縮用正規表現
        """
        l = len(m.group())
        if l <= 1:
            return ","
        else:
            return f",{l}"

    def RLEbin_compress(self, text: str) -> str:
        """
        ランレングス圧縮
        """
        return text[0] + self._re_RLE_comp.sub(self._RLEbin_comp_rep, text)[1:]

    def RLEbin_decompress(self, text: str) -> str:
        """
        ランレングス復元
        """
        start = text[0]
        sp = text[1:].split(",")
        ret = ""
        for sp in sp:
            if sp == "":
                ret += start
            else:
                ret += start * int(sp)
            start = "0" if start == "1" else "1"
        return ret


Comp.class_init()


if __name__ == "__main__":
    c = Comp()
    # print(c.compress(""))
    # print(c.json_decompress(""))
    # print(c.RLEbin_decompress(""))

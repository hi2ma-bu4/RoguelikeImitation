# coding: utf-8
"""
terminal色関連ライブラリ
"""

from typing import Final, final
from dataclasses import dataclass


@dataclass
class W_Color:
    """
    文字&背景色 装飾

    ※一部関数&定数は一部の環境で使用できない場合があります
    """
    RESET: Final[str] = "\033[0m"
    BOLD: Final[str] = "\033[1m"
    DARK: Final[str] = "\033[2m"
    ITALIC: Final[str] = "\033[3m"
    UNDERLINE: Final[str] = "\033[4m"
    FLASH: Final[str] = "\033[5m"
    BLINK: Final[str] = "\033[6m"
    INVERT: Final[str] = "\033[7m"
    NO_DISPLAY: Final[str] = "\u001b[8m"
    STRIKE: Final[str] = "\u001b[9m"

    BLACK: Final[str] = "\033[30m"
    RED: Final[str] = "\033[31m"
    GREEN: Final[str] = "\033[32m"
    YELLOW: Final[str] = "\033[33m"
    BLUE: Final[str] = "\033[34m"
    PURPLE: Final[str] = "\033[35m"
    CYAN: Final[str] = "\033[36m"
    WHITE: Final[str] = "\033[37m"
    _F_EXTENSION5: Final[str] = "\033[38;5;{}m"
    _F_EXTENSION2: Final[str] = "\033[38;2;{};{};{}m"
    F_RESET: Final[str] = "\033[39m"

    B_BLACK: Final[str] = "\033[40m"
    B_RED: Final[str] = "\033[41m"
    B_GREEN: Final[str] = "\033[42m"
    B_YELLOW: Final[str] = "\033[43m"
    B_BLUE: Final[str] = "\033[44m"
    B_PURPLE: Final[str] = "\033[45m"
    B_CYAN: Final[str] = "\033[46m"
    B_WHITE: Final[str] = "\033[47m"
    _B_EXTENSION5: Final[str] = "\033[48;5;{}m"
    _B_EXTENSION2: Final[str] = "\033[48;2;{};{};{}m"
    B_RESET: Final[str] = "\033[49m"

    L_BLACK: Final[str] = "\033[90m"
    L_RED: Final[str] = "\033[91m"
    L_GREEN: Final[str] = "\033[92m"
    L_YELLOW: Final[str] = "\033[93m"
    L_BLUE: Final[str] = "\033[94m"
    L_PURPLE: Final[str] = "\033[95m"
    L_CYAN: Final[str] = "\033[96m"
    L_WHITE: Final[str] = "\033[97m"

    BL_BLACK: Final[str] = "\033[100m"
    BL_RED: Final[str] = "\033[101m"
    BL_GREEN: Final[str] = "\033[102m"
    BL_YELLOW: Final[str] = "\033[103m"
    BL_BLUE: Final[str] = "\033[104m"
    BL_PURPLE: Final[str] = "\033[105m"
    BL_CYAN: Final[str] = "\033[106m"
    BL_WHITE: Final[str] = "\033[107m"

    @final
    @classmethod
    def __getitem__(cls, key: str) -> str:
        return vars(cls)[key]

    @final
    @classmethod
    def fColor(cls, color: int) -> str:
        return cls._F_EXTENSION5.format(color)

    @final
    @classmethod
    def bColor(cls, color: int) -> str:
        return cls._B_EXTENSION5.format(color)

    @final
    @classmethod
    def fRGB(cls, r: int, g: int, b: int):
        return cls._F_EXTENSION2.format(r, g, b)

    @final
    @classmethod
    def bRGB(cls, r: int, g: int, b: int):
        return cls._B_EXTENSION2.format(r, g, b)

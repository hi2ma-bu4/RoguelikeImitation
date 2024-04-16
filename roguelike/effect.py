# coding: utf-8
"""
ローグライク - エフェクト
"""

from typing import Tuple, Final, Union, Optional, final
from dataclasses import dataclass
from random import randint

from lib.calc2d import Vector2, ta_pos
from lib.typingAnim import TypingAnim


# type aliases
ta_tuple_color = Tuple[int, int, int]
ta_color = Union[ta_tuple_color, str]

# ここまで


class EffectBase:
    """
    エフェクト基底クラス
    """

    @classmethod
    def set_baseInit(cls, pg, screen, world, basePos: ta_pos = (0, 0), impPos: ta_pos = (0, 0), addPos: ta_pos = (0, 0)) -> None:
        """
        初期化処理
        """
        cls._pg = pg
        cls._screen = screen
        cls._world = world

        cls._basePos = Vector2.convert(basePos)
        cls._impPos = Vector2.convert(impPos)
        cls._addPos = Vector2.convert(addPos)

        cls.BLEND_RGBA_MULT = cls._pg.BLEND_RGBA_MULT
        cls.SRCALPHA = cls._pg.SRCALPHA


class TextPopup(EffectBase):
    """
    動きのあるテキスト表示用クラス
    """

    def __init__(self, font, text: str, pos: ta_pos, movePos: ta_pos = (0, 0), lastAddPos: ta_pos = (0, 0), time: int = 10, color: Optional[ta_color] = None, *, isTyping: bool = False, noMove: bool = False) -> None:
        self._font = font
        self._text = text
        self.pos = Vector2(*Vector2.convert(pos).pos())
        self._movePos = Vector2.convert(movePos)
        self._lastAddPos = Vector2.convert(lastAddPos)
        self._time = time

        self._nowAddPos = Vector2()

        # 色コード変換
        _col = Colors.auto_tuple(color)
        if _col == None:
            self._color: Tuple[int, int, int] = (255, 255, 255)
        else:
            self._color = _col

        self.alpha = 128

        self.noMove = noMove
        if (self.noMove):
            self._basePos_cache = self._basePos.copy()
        else:
            self._basePos_cache = self._basePos

        self._isTyping = isTyping
        if self._isTyping:
            self.typing = TypingAnim(
                self._text,
                animSpeed=1,
                debug=True,
            )

        self._textOri = self._font.render(self._text, False, self._color)

    def update(self, isDraw: bool = True) -> bool:
        """
        更新処理
        """
        if self._time <= 0:
            return True

        # データ更新
        self._nowAddPos += self._movePos
        self._time -= 1

        if self._isTyping:
            ty = self.typing.update()
            if ty == 1:
                self._textOri = self._font.render(
                    str(self.typing), False, self._color)
            elif ty == -1:
                self._text = str(self.typing)
                self._isTyping = False
                self._textOri = self._font.render(
                    str(self.typing), False, self._color)

        if isDraw:
            self.draw()

        return False

    def draw(self) -> None:
        """
        描画処理
        """
        tmpPos = self.pos - self._basePos_cache
        tmpPos += self._addPos
        tmpPos *= self._impPos
        tmpPos += self._lastAddPos
        tmpPos += self._nowAddPos
        self._screen.blit(
            self._textOri,
            tmpPos.pos()
        )


class Particle(EffectBase):
    """
    パーティクル表示用クラス
    """

    def __init__(self, pos: ta_pos, vel: Tuple[int, int], radius: float = 1.0, time: int = 10, color: ta_color = (0, 0, 0)) -> None:
        self.pos = Vector2(*Vector2.convert(pos).pos())
        self._nowAddPos = Vector2()
        self.vx, self.vy = vel

        self.radius = radius

        self.time = time

        # 色コード変換
        _col = Colors.auto_tuple(color)
        if _col == None:
            self._color: Tuple[int, int, int] = (255, 255, 255)
        else:
            self._color = _col

        self.dt = 0.8
        self.gy = 0.5

    def update(self, isDraw: bool = True) -> bool:
        """
        更新処理
        """
        if self.time <= 0:
            return True
        self.time -= 1

        self.vy += self.gy * self.dt
        self._nowAddPos.x += int(self.vx * self.dt)
        self._nowAddPos.y += int(self.vy * self.dt)

        if isDraw:
            self.draw()

        return False

    def draw(self) -> None:
        """
        描画処理
        """
        tmpPos = self.pos - self._basePos
        tmpPos += self._addPos
        tmpPos *= self._impPos
        tmpPos += (self._world._fCOL, self._world._fROW)
        tmpPos += self._nowAddPos
        self._pg.draw.circle(self._screen, self._color,
                             tmpPos.pos(), self.radius)


@dataclass
class Colors:
    """
    色定義
    """

    WHITE: Final[ta_tuple_color] = (255, 255, 255)
    GRAY: Final[ta_tuple_color] = (128, 128, 128)
    RED: Final[ta_tuple_color] = (255, 0, 0)
    GREEN: Final[ta_tuple_color] = (0, 255, 0)

    BLOOD: Final[ta_tuple_color] = (211, 9, 19)
    MONSTER_BLOOD: Final[ta_tuple_color] = (17, 186, 8)

    LIGHT_YELLOW_GREEN: Final[ta_tuple_color] = (181, 255, 20)
    LIGHT_BLUE: Final[ta_tuple_color] = (157, 204, 224)

    @final
    @classmethod
    def auto_tuple(cls, obj: Optional[ta_color]) -> Optional[Tuple[int, int, int]]:
        """
        自動で色コード(hex)をTupleに変換する
        """
        if isinstance(obj, str):
            return cls.hex2Tuple(obj)
        elif isinstance(obj, tuple):
            return obj
        return None

    @final
    @classmethod
    def auto_hex(cls, obj: Optional[ta_color]) -> Optional[str]:
        """
        自動で色コード(Tuple)をhexに変換する
        """
        if isinstance(obj, tuple):
            return cls.tuple2Hex(obj)
        elif isinstance(obj, str):
            return obj
        return None

    @final
    @staticmethod
    def hex2Tuple(hex: str) -> Optional[Tuple[int, int, int]]:
        """
        カラーコードをタプルに
        """

        if hex[0] == "#":
            hex = hex[1:]

        # 16進数を10進数に
        try:
            return (int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))
        except:
            return None

    @final
    @staticmethod
    def tuple2Hex(tup: Tuple[int, int, int]) -> Optional[str]:
        """
        タプルをカラーコードに
        """

        # 10進数を16進数に
        try:
            return f"#{hex(tup[0])}{hex(tup[1])}{hex(tup[2])}".upper()
        except:
            return None

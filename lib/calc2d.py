# coding: utf-8
"""
2D計算用ライブラリ
"""


from typing import Any, Dict, Tuple, List, Set, Optional, Union, final
from dataclasses import dataclass
from copy import deepcopy
from math import sqrt, atan2

# type aliases
ta_opInt = Optional[int]
ta_pos = Optional[Union["Vector2", Union[Tuple[int, int], List[int]]]]

# ここまで


@final
@dataclass
class classControl:
    @staticmethod
    def formatOrthop(name: str, *args: Any) -> str:
        """
        classデバッグ用format出力
        """
        return f"<{name} [{', '.join(map(str, args))}]>"

    @staticmethod
    def typeofError(val: Any, _type: type, valName: str) -> None:
        """
        型チェック
        (エラーで停止)
        """
        if type(val) is not _type:
            raise TypeError(f"{valName} must be {_type.__name__}")


class Vector2:
    """
    2d上での座標情報
    """

    def __init__(self, x: int = 0, y: int = 0, maxX: ta_opInt = None, minX: ta_opInt = None, maxY: ta_opInt = None, minY: ta_opInt = None) -> None:
        self._x = x
        self._y = y
        self._max_x = maxX
        self._min_x = minX
        self._max_y = maxY
        self._min_y = minY

        self._overCheck()

    def update(self, x: ta_opInt = None, y: ta_opInt = None, maxX: Union[ta_opInt, str] = "", minX: Union[ta_opInt, str] = "", maxY: Union[ta_opInt, str] = "", minY: Union[ta_opInt, str] = "") -> "Vector2":
        """
        座標更新
        """
        if x != None:
            self._x = x
        if y != None:
            self._y = y

        if not isinstance(maxX, str):
            self._max_x = maxX
        if not isinstance(minX, str):
            self._min_x = minX
        if not isinstance(maxY, str):
            self._max_y = maxY
        if not isinstance(minY, str):
            self._min_y = minY

        self._overCheck()
        return self

    def add(self, x: ta_opInt = None, y: ta_opInt = None) -> "Vector2":
        """
        座標の増分
        """
        if x != None:
            self._x += x
        if y != None:
            self._y += y

        self._overCheck()
        return self

    def pos(self) -> Tuple[int, int]:
        """
        座標返却(x, y)
        """
        return (self.x, self.y)

    def copy(self) -> "Vector2":
        """
        座標位置等deepCopy
        """
        return deepcopy(self)

    def reverse(self) -> "Vector2":
        return Vector2(self.y, self.x, self._max_y, self._min_y, self._max_x, self._min_x)

    @staticmethod
    def convert(pos: ta_pos) -> "Vector2":
        if isinstance(pos, Vector2):
            return pos
        elif pos == None:
            return Vector2()
        else:
            if 1 <= len(pos) <= 6:
                return Vector2(*pos)
        return Vector2()

    def __eq__(self, oth: ta_pos) -> bool:
        v = self.convert(oth)
        return self.x == v.x and self.y == v.y

    def __add__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        return Vector2(self.x + v.x, self.y + v.y)

    def __iadd__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        return self.add(v.x, v.y)

    def __sub__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        return Vector2(self.x - v.x, self.y - v.y)

    def __isub__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        return self.add(-v.x, -v.y)

    def __mul__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        return Vector2(self.x * v.x, self.y * v.y)

    def __imul__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        self._x *= v.x
        self._y *= v.y
        self._overCheck()
        return self

    def __truediv__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        return Vector2(self._x // v._x, self._y // v._y)

    def __itruediv__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        self._x //= v.x
        self._y //= v.y
        self._overCheck()
        return self

    def __floordiv__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        return Vector2(self._x // v._x, self._y // v._y)

    def __ifloordiv__(self, oth: Union[ta_pos, int]) -> "Vector2":
        if isinstance(oth, int):
            v = Vector2(oth, oth)
        else:
            v = self.convert(oth)
        self._x //= v.x
        self._y //= v.y
        self._overCheck()
        return self

    def __abs__(self) -> "Vector2":
        return Vector2(abs(self._x), abs(self._y))

    def __format__(self, spec: str) -> str:
        if spec == "x":
            return str(self._x)
        if spec == "y":
            return str(self._x)
        return classControl.formatOrthop("Vector2", self._x, self._y)

    def __str__(self) -> str:
        return classControl.formatOrthop("Vector2", self._x, self._y)

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    def __call__(self) -> Tuple[int, int]:
        """
        座標取得(x,y)
        """
        return self.pos()

    def _overCheck(self) -> None:
        """
        座標位置を正常に
        """
        if self._max_x != None and self._x > self._max_x:
            self._x = self._max_x
        if self._min_x != None and self._x < self._min_x:
            self._x = self._min_x
        if self._max_y != None and self._y > self._max_y:
            self._y = self._max_y
        if self._min_y != None and self._y < self._min_y:
            self._y = self._min_y

    @final
    @property
    def x(self) -> int:
        return self._x

    @final
    @x.setter
    def x(self, val: int) -> None:
        classControl.typeofError(val, int, "Vector2.x")
        self._x = val
        self._overCheck()

    @final
    @property
    def y(self) -> int:
        return self._y

    @final
    @y.setter
    def y(self, val: int) -> None:
        classControl.typeofError(val, int, "Vector2.y")
        self._y = val
        self._overCheck()


@final
@dataclass
class Calc2d:
    """
    2d計算用
    """

    @classmethod
    def getCircleList(cls, lst: List[List[Any]], basePos: ta_pos, r: int) -> List[Tuple[int, int]]:
        ansList = []
        bPos = Vector2.convert(basePos)
        mx = [max(bPos.x-r-1, 0), min(bPos.x+r+1, len(lst[0]))]
        my = [max(bPos.y-r-1, 0), min(bPos.y+r+1, len(lst[1]))]
        for x in range(*mx):
            for y in range(*my):
                if cls.innerCircle(basePos, r, (x, y)):
                    ansList.append((x, y))
        return ansList

    @staticmethod
    def pos2distance(pos1: ta_pos, pos2: ta_pos) -> float:
        """
        2点間の距離
        """
        v1 = Vector2.convert(pos1)
        v2 = Vector2.convert(pos2)
        dx = abs(v2.x - v1.x)
        dy = abs(v2.y - v1.y)
        return sqrt(dx**2 + dy**2)

    @staticmethod
    def getRadian(pos1: ta_pos, pos2: ta_pos) -> float:
        """
        2点間の角度
        """
        v1 = Vector2.convert(pos1)
        v2 = Vector2.convert(pos2)
        return atan2(v2.y - v1.y, v2.x - v1.x)

    @staticmethod
    def innerCircle(basePos: ta_pos, r: int, getPos: ta_pos) -> bool:
        """
        円の内側かどうか
        """
        bp = Vector2.convert(basePos)
        gp = Vector2.convert(getPos)
        return ((gp.x - bp.x)**2 + (gp.y - bp.y)**2) < r**2

    class DirectDistance:
        """
        2点+(X or Y)で(Y or X)を返却するclass
        """

        def __init__(self, pos1: ta_pos, pos2: ta_pos) -> None:
            self._pos1 = Vector2.convert(pos1)
            self._pos2 = Vector2.convert(pos2)

            diffX = self._pos2.x - self._pos1.x
            diffY = self._pos2.y - self._pos1.y
            self._a = diffY / diffX
            self._b = self._pos1.y - self._a * self._pos1.x

        def __call__(self, *, x: float = 0, y: float = 0):
            """
            X or Y 取得
            """
            if x == 0:
                return (y - self._b) / self._a
            elif y == 0:
                return self._a * x + self._b
            else:
                raise ValueError("xとyを同時に指定は出来ません")

    class BresenhamLine:
        """
        Bresenham法による直線計算
        及び、可視範囲の取得
        """

        def __init__(self, map_2d: List[List[int]]) -> None:
            # キャッシュ辞書の初期化
            self.visibility_cache: Dict[
                Tuple[Tuple[int, int], int], Set[Tuple[int, int]]] = {}
            self.map_2d = map_2d
            self.map_height = len(map_2d)
            self.map_width = len(map_2d[0])

        @final
        def innerCells(self, base_pos: ta_pos, max_distance: int, get_pos: ta_pos) -> bool:
            if Calc2d.innerCircle(base_pos, max_distance, get_pos):
                lst = self.get_visible_cells(base_pos, max_distance)[1]
                return Vector2.convert(get_pos).pos() in lst
            return False

        @final
        def get_visible_cells(self, player_pos: ta_pos, max_distance: int) -> Tuple[bool, Set[Tuple[int, int]]]:
            """
            可視範囲の取得
            """
            p = Vector2.convert(player_pos)

            # キャッシュキーの生成
            cache_key = (p.pos(), max_distance)

            # キャッシュが存在する場合は結果を返す
            if cache_key in self.visibility_cache:
                return (False, self.visibility_cache[cache_key])

            max_distance_squared = max_distance ** 2
            visible_cells: Set[Tuple[int, int]] = set()

            for x in range(self.map_width):
                for y in range(self.map_height):
                    dx = x - p.x
                    dy = y - p.y
                    distance_squared = dx ** 2 + dy ** 2

                    if distance_squared <= max_distance_squared:
                        line_of_sight = self.bresenham_line(p.x, p.y, x, y)
                        in_sight = True

                        for cx, cy in line_of_sight:
                            if (
                                cx < 0
                                or cx >= self.map_width
                                or cy < 0
                                or cy >= self.map_height
                                or self.map_2d[cy][cx] == 1
                            ):
                                in_sight = False
                                break

                        if in_sight:
                            visible_cells.add((x, y))

            # 結果をキャッシュに保存
            self.visibility_cache[cache_key] = visible_cells

            return (True, visible_cells)

        @final
        @staticmethod
        def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
            """
            Bresenham法による直線計算
            """
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = -1 if x0 > x1 else 1
            sy = -1 if y0 > y1 else 1
            err = dx - dy

            line: List[Tuple[int, int]] = []
            x, y = x0, y0

            while True:
                line.append((x, y))

                if x == x1 and y == y1:
                    break

                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x += sx
                if e2 < dx:
                    err += dx
                    y += sy

            return line

    @staticmethod
    def listReplace(lst: List[Any], repList: dict = {}) -> List[Any]:
        """
        1次元配列の中身を置換
        """
        if len(repList) == 0:
            return lst

        for i in range(len(lst)):
            for k, v in repList.items():
                if lst[i] == k:
                    lst[i] = v
        return lst

    @staticmethod
    def convert_1dTo2d(lst: List[Any], w: int) -> List[List[Any]]:
        """
        1次元配列を2次元に変換
        """
        return [lst[i:i + w] for i in range(0, len(lst), w)]

    @staticmethod
    def lerp(a: Vector2, b: Vector2, f: float) -> Vector2:
        """
        線形補間
        """
        return Vector2(
            round(a.x * (1. - f) + b.x * f),
            round(a.y * (1. - f) + b.y * f)
        )

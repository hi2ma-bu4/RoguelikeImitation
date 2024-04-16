# coding: utf-8
"""
ローグライク - マップ関連
"""

from typing import Any, Tuple, List, Final, Optional, final
from copy import deepcopy
from random import Random, randint
from math import sqrt

from lib.A_star import astar
from lib.calc2d import Calc2d

# type aliases
ta_Size = Tuple[int, int]


# 定数
RANDOM_SEED_MAX_NUM: Final[int] = 9999999999


@final
class Layer2D:
    """
    2dマップを作成する為の基盤
    """

    def __init__(self, size: ta_Size) -> None:
        self._tmpMap = []

        self._size = size

    def toInd(self, x: int, y: int) -> int:
        """
        配列index取得
        """
        return y * self._size[0] + x

    def isOutOfRange(self, x: int, y: int) -> bool:
        """
        範囲外判定
        """
        return not (0 < x < self._size[0] and 0 < y < self._size[1])

    def get(self, x: int, y: int) -> int:
        """
        座標位置取得
        """
        if self.isOutOfRange(x, y):
            return -1
        return self._tmpMap[self.toInd(x, y)]

    def set(self, x: int, y: int, val: int) -> None:
        """
        座標位置更新
        """
        if not self.isOutOfRange(x, y):
            self._tmpMap[self.toInd(x, y)] = val

    def fill(self, val: int) -> None:
        """
        配列全埋め立て
        """
        self._tmpMap = [val]*(self._size[0] * self._size[1])

    def fillRect(self, x: int, y: int, w: int, h: int, val: int) -> None:
        """
        配列長方形埋め立て
        """
        for j in range(h):
            for i in range(w):
                self.set(x+i, y+j, val)

    def fillRectLTRB(self, left: int, top: int, right: int, bottom: int, val: int) -> None:
        """
        配列長方形埋め立て
        (4点指定)
        """
        self.fillRect(left, top, right - left, bottom - top, val)

    @property
    def get_map(self) -> List[int]:
        """
        map取得
        """
        return self._tmpMap


class _RlmRect:
    """
    長方形の範囲座標保持
    """

    def __init__(self) -> None:
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    def set(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @final
    @property
    def width(self) -> int:
        return self.right - self.left

    @final
    @property
    def height(self) -> int:
        return self.bottom - self.top

    @final
    @property
    def center(self) -> Tuple[int, int]:
        return (
            int(self.left + (self.right - self.left)/2),
            int(self.top + (self.bottom - self.top)/2)
        )


@final
class _RlmDiv:
    """
    区画と部屋情報保持
    """

    def __init__(self) -> None:
        self.rect = _RlmRect()
        self.room = _RlmRect()


@final
class RogueLikeMap:
    """
    ローグライクのマップ生成
    """

    CHIP_EMPTY: Final[int] = 0
    CHIP_ROAD: Final[int] = 1
    CHIP_WALL: Final[int] = 5
    STEPUP: Final[int] = 10
    STEPDOWN: Final[int] = 11

    def __init__(self, size: ta_Size, seed: int = randint(1, RANDOM_SEED_MAX_NUM), *, roomMaxSize: ta_Size = (5, 5), roomMinSize: ta_Size = (3, 3)) -> None:
        """
        ローグライクのマップを自動生成
        (初期設定)
        """
        self._size = size
        self._seed = seed
        self._roomMaxSize = roomMaxSize
        self._roomMinSize = roomMinSize

    def createMap(self) -> List[int]:
        """
        map作成
        """
        self.roomR = Random()
        self.roomR.seed(self._seed)

        # 本体初期化
        self._layer = Layer2D(self._size)
        self._layer.fill(self.CHIP_WALL)

        self._divList: List[_RlmDiv] = []

        # 初期区画生成
        self._createRect(0, 0, self._size[0]-1, self._size[1]-1)

        # 区画分割
        self._splitRect(not self.roomR.randint(0, 1))

        # 区画に部屋作成 & 結合
        self._createRoom()
        self._connectRooms()

        return self._layer.get_map

    def _createRect(self, left: int, top: int, right: int, bottom: int) -> None:
        """
        区画情報登録
        """
        div = _RlmDiv()
        div.rect.set(left, top, right, bottom)
        self._divList.append(div)

    def _splitRect(self, isVertical: bool, spInd: int = 0) -> None:
        """
        区画分割
        """
        parent = self._divList[spInd]

        if isVertical:
            # 列

            # 区分可能かチェック
            if parent.rect.width < (self._roomMinSize[0]+4)*2+1:
                return
            a = parent.rect.left + self._roomMinSize[0] + 3
            b = parent.rect.right + self._roomMinSize[0] - 3

            ab = b - a
            if self._roomMaxSize[0] < ab:
                ab = self._roomMaxSize[0]

            p = a + self.roomR.randint(1, ab)

            self._createRect(p, parent.rect.top,
                             parent.rect.right, parent.rect.bottom)

            parent.rect.right = p
        else:
            # 行

            # 区分可能かチェック
            if parent.rect.height < (self._roomMinSize[1]+4)*2+1:
                return
            a = parent.rect.top + self._roomMinSize[1] + 3
            b = parent.rect.bottom + self._roomMinSize[1] - 3

            ab = b - a
            if self._roomMaxSize[1] < ab:
                ab = self._roomMaxSize[1]

            p = a + self.roomR.randint(1, ab)

            self._createRect(parent.rect.left, p,
                             parent.rect.right, parent.rect.bottom)

            parent.rect.bottom = p

        if self.roomR.randint(0, 1):
            self._divList[-1], self._divList[-2] = self._divList[-2], self._divList[-1]

        # 再帰的に処理
        self._splitRect(not isVertical, len(self._divList)-1)
        self._splitRect(not isVertical, spInd)

    def _createRoom(self) -> None:
        """
        部屋作成
        """

        upStepRect = self.roomR.randint(
            0, max(len(self._divList)-3, len(self._divList)))

        for i in range(len(self._divList)):
            div = self._divList[i]
            w = div.rect.width - 3
            h = div.rect.height - 3

            cw = max(1, w - self._roomMinSize[0])
            ch = max(1, h - self._roomMinSize[1])

            sw = self.roomR.randint(0, cw-1) + self._roomMinSize[0]
            sh = self.roomR.randint(0, ch-1) + self._roomMinSize[1]
            if sw > self._roomMaxSize[0]:
                sw = self._roomMaxSize[0]
            if sh > self._roomMaxSize[1]:
                sh = self._roomMaxSize[1]

            rw = max(1, w - sw)
            rh = max(1, h - sh)

            rx = self.roomR.randint(1, rw) + 1
            ry = self.roomR.randint(1, rh) + 1
            left = div.rect.left + rx
            right = left + sw
            top = div.rect.top + ry
            bottom = top + sh

            div.room.set(left, top, right, bottom)

            self._layer.fillRectLTRB(
                div.room.left, div.room.top, div.room.right, div.room.bottom, self.CHIP_EMPTY)

            if i == upStepRect:
                x = self.roomR.randint(1, sw-2)
                y = self.roomR.randint(1, sh-2)
                mx = div.room.left + x
                my = div.room.top + y
                self._layer.set(mx, my, self.STEPUP)
            if i == len(self._divList)-1:
                x = self.roomR.randint(1, sw-2)
                y = self.roomR.randint(1, sh-2)
                mx = div.room.left + x
                my = div.room.top + y
                self._layer.set(mx, my, self.STEPDOWN)

    def _fillHLine(self, left: int, right: int, y: int, chipId: int) -> None:
        """
        横道(横)を接続
        """
        if left > right:
            left, right = right, left
        for x in range(left, right+1):
            self._layer.set(x, y, chipId)

    def _fillVLine(self, top: int, bottom: int, x: int, chipId: int) -> None:
        """
        横道(縦)を接続
        """
        if top > bottom:
            top, bottom = bottom, top
        for y in range(top, bottom+1):
            self._layer.set(x, y, chipId)

    def _createRoad(self, rectAInd: int, rectBInd: int) -> bool:
        """
        横道(部屋に垂直)を生成
        """
        divA = self._divList[rectAInd]
        divB = self._divList[rectBInd]

        if divA.rect.bottom == divB.rect.top or divA.rect.top == divB.rect.bottom:
            x1 = self.roomR.randint(0, divA.room.width-1) + divA.room.left
            x2 = self.roomR.randint(0, divB.room.width-1) + divB.room.left

            if divA.rect.top > divB.rect.top:
                y = divA.rect.top
                self._layer.fillRectLTRB(
                    x1, y+1, x1+1, divA.room.top, self.CHIP_ROAD)
                self._layer.fillRectLTRB(
                    x2, divB.room.bottom, x2+1, y, self.CHIP_ROAD)
            else:
                y = divB.rect.top
                self._layer.fillRectLTRB(
                    x1, divA.room.bottom, x1+1, y, self.CHIP_ROAD)
                self._layer.fillRectLTRB(
                    x2, y, x2+1, divB.room.top, self.CHIP_ROAD)

            # 横道生成
            self._fillHLine(x1, x2, y, self.CHIP_ROAD)

        elif divA.rect.left == divB.rect.right or divA.rect.right == divB.rect.left:
            y1 = self.roomR.randint(0, divA.room.height-1) + divA.room.top
            y2 = self.roomR.randint(0, divB.room.height-1) + divB.room.top

            if divA.rect.left > divB.rect.left:
                x = divA.rect.left
                self._layer.fillRectLTRB(
                    divB.room.right, y2, x, y2+1, self.CHIP_ROAD)
                self._layer.fillRectLTRB(
                    x+1, y1, divA.room.left, y1+1, self.CHIP_ROAD)
            else:
                x = divB.rect.left
                self._layer.fillRectLTRB(
                    divA.room.right, y1, x, y1+1, self.CHIP_ROAD)
                self._layer.fillRectLTRB(
                    x+1, y2, divB.room.left, y2+1, self.CHIP_ROAD)

            # 横道生成
            self._fillVLine(y1, y2, x, self.CHIP_ROAD)
        else:
            return False
        return True

    def _roomDistance(self, aInd: int, bInd: int) -> float:
        """
        部屋間の距離
        """
        aPos = self._divList[aInd].room.center
        bPos = self._divList[bInd].room.center

        return sqrt((aPos[0] - bPos[0])**2 + (aPos[1] - bPos[1])**2)

    def _connectRooms(self) -> None:
        """
        全体の通路接続
        """
        # [接続道本数, 最短ind, 最短距離]
        dl = len(self._divList)
        distList = [[0, -1, 99999.0, True] for i in range(dl)]

        # 最も近い部屋と接続
        for i in range(dl-1):
            renewal = False
            if distList[i][0] < 3:
                for j in range(i+1, dl):
                    dist = self._roomDistance(i, j)
                    if dist < distList[i][2] and distList[j][0] < 2:
                        distList[i][1] = j
                        distList[i][2] = dist
                        renewal = True
            if renewal:
                distList[i][0] += 1
                distList[distList[i][1]][0] += 1

        for i in range(dl-1):
            isCreate = self._createRoad(i, distList[i][1])

            # ボッチ部屋を救出
            if not isCreate:
                tmpDistList = []
                for j in range(dl-1):
                    if i != j:
                        tmpDistList.append([self._roomDistance(i, j), j])
                tmpDistList.sort()
                for t in tmpDistList:
                    if self._createRoad(i, t[1]):
                        break

        # for i in range(len(self._divList)-1):
        #    self._createRoad(i, i+1)


@final
class RouteSearch:
    """
    経路探索
    """

    @staticmethod
    def search(map: List[int], w: int) -> Optional[List[Any]]:
        """
        A* で経路探索
        0[道],1[壁],2[スタート],3[ゴール]
        """
        tmpMap = deepcopy(map)

        # 経路探索用の座標取得
        endFlag = 0
        start = (0, 0)
        end = (0, 0)
        for y in range(len(tmpMap)//w):
            for x in range(w):
                n = tmpMap[x + y * w]
                if n == 2:
                    start = (y, x)
                    endFlag += 1
                elif n == 3:
                    end = (y, x)
                    endFlag += 1
                if endFlag >= 2:
                    break
            if endFlag >= 2:
                break

        # 2,3を0に変換
        repDict = {2: 0, 3: 0}
        tmpMap = Calc2d.listReplace(tmpMap, repDict)

        # 2次元配列に変換
        tmpMap = Calc2d.convert_1dTo2d(tmpMap, w)

        # A* で経路探索
        return astar(tmpMap, start, end)

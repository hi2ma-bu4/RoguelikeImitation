# coding: utf-8
"""
ローグライク - キャラ関連
"""

from typing import Any, Callable, List, Tuple, Final, Optional, final
from abc import abstractmethod
from random import randint
from json import dumps, loads
from math import log

from lib.calc2d import ta_pos, classControl, Vector2, Calc2d
from lib.A_star import astar

# type aliases
ta_opInt = Optional[int]

# ここまで


def flattenMap(map: List[List[int]]) -> List[List[int]]:
    """
    mapの余計な情報を削除
    """
    tmpMap = []

    for y in range(len(map)):
        tmpMap.append([])
        for x in range(len(map[0])):
            d = map[y][x]
            if d == 1 or d == 10 or d == 11:
                a = 0
            elif d == 5:
                a = 1
            else:
                a = d
            tmpMap[y].append(a)
    return tmpMap


class Status:
    """
    ステータスデータ保存用
    """

    LEVEL_IMPORTANCE: Final[float] = 1.1
    LEVEL_EARLY_EXP: Final[int] = 12

    # レベル→経験値
    #

    def __init__(self, maxHP: int, speed: int, attack: int, *, nowHP: ta_opInt = None, exp: int = 0) -> None:
        self.maxHP = maxHP
        if nowHP == None:
            self._nowHP = self.maxHP
        else:
            self._nowHP = nowHP

        self.speed = speed
        self.attack = attack

        self.totalExp = exp

    def __format__(self, spec: str) -> str:
        return classControl.formatOrthop(f"Status", f"{self.hp}/{self.maxHP}", self.speed, self.attack, self.totalExp)

    @final
    def out(self) -> str:
        dic = {
            "nowHP": self._nowHP,
            "maxHP": self.maxHP,
            "speed": self.speed,
            "attack": self.attack,
            "exp": self.totalExp
        }
        return dumps(dic)

    @final
    def load(self, sd: str) -> None:
        dic = loads(sd)

        self._nowHP: int = dic["nowHP"]
        self.maxHP: int = dic["maxHP"]
        self.speed: int = dic["speed"]
        self.attack: int = dic["attack"]
        self.totalExp: int = dic["exp"]

    @final
    @property
    def hp(self) -> int:
        return self._nowHP

    @final
    @hp.setter
    def hp(self, val: int) -> None:
        classControl.typeofError(val, int, "Status.hp")
        self._nowHP = val
        if self.maxHP < val:
            self._nowHP = self.maxHP
        elif 0 > val:
            self._nowHP = 0

    @final
    def totalExpGet(self, level: int, exp: int = 0) -> int:
        return int(self.LEVEL_EARLY_EXP * ((1-self.LEVEL_IMPORTANCE**level)/(1-self.LEVEL_IMPORTANCE)) + exp)

    @final
    @property
    def level(self) -> int:
        return int(log((self.LEVEL_EARLY_EXP+(self.LEVEL_IMPORTANCE - 1)*self.totalExp)/self.LEVEL_EARLY_EXP, self.LEVEL_IMPORTANCE))

    @final
    @property
    def exp(self) -> int:
        return self.totalExp - self.totalExpGet(self.level)

    @final
    def addExp(self, val: int) -> bool:
        oldL = self.level
        self.totalExp += val
        return oldL < self.level

    @final
    @property
    def nextExp(self) -> int:
        return self.totalExpGet(self.level) - self.totalExpGet(self.level-1)


class mapObject():
    """
    マップ上にあるやつら
    """

    def __init__(self, pos: ta_pos, nameId: str) -> None:
        # Vector2に変換
        self.pos = Vector2.convert(pos)
        self.pos.update(minX=0, minY=0)

        self._nameId = nameId


class Item(mapObject):
    def __init__(self, pos: ta_pos, nameId: str) -> None:
        super().__init__(pos, nameId)

        self.death = False


class Entity(mapObject):
    """
    マップ上にいるやつら(動く)
    """

    # 向いている方向
    DIRECT_DOWN: Final[int] = 0
    DIRECT_LEFT: Final[int] = 1
    DIRECT_RIGHT: Final[int] = 2
    DIRECT_UP: Final[int] = 3

    # アニメーションコマ数
    ANIM_COUNT: Final[int] = 3

    MAX_TURN: Final[int] = 100

    def __init__(self, pos: ta_pos, nameId: str, status: Status) -> None:
        super().__init__(pos, nameId)
        self.direction = self.DIRECT_UP

        self.status = status

        self._passageTurn = 0
        self.animSpeed = 400
        self._animSpeedCou = 0
        self.nowAnimCou = 0

        self.death = False

        self.tiedTogether = True

    @classmethod
    def mapDataSet(cls, lst: List[List[Any]], bresenhamLine: Calc2d.BresenhamLine) -> None:
        cls.mapData = flattenMap(lst)
        cls.bresenhamLine = bresenhamLine

    @classmethod
    def textPopupSet(cls, textPopupFunc: Callable[..., None]) -> None:
        cls.createTextPopup = textPopupFunc

    @classmethod
    def enemyListSet(cls, lst: List["Enemy"]):
        cls.enemyList = lst

    def doTurn(self) -> bool:
        """
        1ターンごとに実行
        """

        # 失職した場合実行させない
        if not self.tiedTogether:
            if not self.death and self.status.hp <= 0:
                self.death = True
            return False

        self._passageTurn += 1

        # 自身のターンになった時
        if self._passageTurn > self.MAX_TURN - self.status.speed:
            self._passageTurn = 0

            self.playMyTurn()

            return True
        return False

    def animTurn(self) -> bool:
        """
        アニメーションコマ
        """

        # 失職した場合実行させない
        if not self.tiedTogether:
            return False

        self._animSpeedCou += 1
        if self._animSpeedCou > self.animSpeed:
            self._animSpeedCou = 0
            self.nowAnimCou += 1
            if self.nowAnimCou > self.ANIM_COUNT:
                self.nowAnimCou = 0
            return True
        return False

    @abstractmethod
    def playMyTurn(self) -> None:
        """
        自身のターンになった時の処理
        """
        pass

    def move(self, x: int = 0, y: int = 0, *, notMove: bool = False) -> None:
        """
        指定分移動
        """
        if not notMove:
            self.pos.add(x, y)

        # x == y == 0 はスキップ
        if y == 0 or abs(x) > abs(y):
            if x > 0:
                self.direction = self.DIRECT_RIGHT
            else:
                self.direction = self.DIRECT_LEFT
        elif x == 0:
            if y > 0:
                self.direction = self.DIRECT_DOWN
            else:
                self.direction = self.DIRECT_UP

    def __format__(self, spec: str) -> str:
        return classControl.formatOrthop(f"Entity.{self._nameId}", self.direction)


class Player(Entity):
    """
    プレイヤー
    """

    def __init__(self, pos: ta_pos, status: Status) -> None:
        super().__init__(pos, "man", status)
        Enemy.playerPosSet(self.pos)

        self.turnStop = False

    def move(self, x: int = 0, y: int = 0, *, notMove: bool = False) -> None:
        super().move(x, y, notMove=notMove)
        Enemy.playerPosSet(self.pos)

    def doTurn(self) -> bool:
        # 何か操作があるまで待機

        if self.turnStop:
            return True

        if super().doTurn():
            self.turnStop = True
            return True
        return False

    def turnMove(self) -> None:
        self.turnStop = False


class Enemy(Entity):
    """
    敵
    """

    def __init__(self, pos: ta_pos, nameId: str, status: Status, discoveryRange: int = 5, animSpeed: int = 100, ind: int = 0) -> None:
        super().__init__(pos, nameId, status)

        self.discoveryRange = discoveryRange
        self.animSpeed = animSpeed

        self._ind = ind

        self.lastPlayerPos: Optional[Vector2] = None
        self.pathList: Optional[List[Tuple[int, int]]] = []

        self.nowMove = False
        self.isDiscovery = False
        self._beginningTiedTogether = True

    @classmethod
    def playerPosSet(cls, pos: Vector2) -> None:
        """
        計算用プレイヤー座標設定
        """
        cls.playerPos = pos

    @classmethod
    def enemyAttackSet(cls, func) -> None:
        cls.enemyAttack = func

    def out(self) -> str:
        dic = {
            "pos": self.pos.pos(),
            "status": self.status.out(),
            "pathList": self.pathList,
            "isDiscovery": self.isDiscovery,
        }
        return dumps(dic)

    def load(self, sd: str) -> None:
        dic = loads(sd)

        self.pos = Vector2(*dic["pos"])
        self.status.load(dic["status"])
        self.pathList = dic["pathList"]
        self.isDiscovery = dic["isDiscovery"]

    def playMyTurn(self) -> None:

        if self.status.hp <= 0:
            self.death = True
            return

        # 行き先決定
        self._routeSearch()
        # 移動
        self._movePos()

    def doAttack(self) -> None:
        self.enemyAttack(self)

    def _movePos(self) -> None:
        """
        道に沿って移動
        """
        if self.pathList == None or len(self.pathList) == 0:
            self.nowMove = False
            return

        # 移動先座標
        mPos = Vector2(*self.pathList[0]).reverse()

        # 他の敵(プレイヤー)に被らないようにする
        if self.playerPos == mPos:
            self.doAttack()
            self.move(*(mPos - self.pos).pos(), notMove=True)
            return
        for e in self.enemyList:
            if not e.death and e.pos == mPos:
                self.nowMove = False
                self.move(*(mPos - self.pos).pos(), notMove=True)
                return

        self.move(*(mPos - self.pos).pos())
        # 削除
        self.pathList.pop(0)

    def _routeSearch(self) -> None:
        """
        行き先決定
        """

        # 無駄な参照防止用
        if self.tiedTogether:
            # 無駄な参照防止用(初期計算)
            if self._beginningTiedTogether:
                self._beginningTiedTogether = False
                route = astar(
                    self.mapData, self.pos.reverse().pos(),
                    self.playerPos.reverse().pos()
                )
                if route == None:
                    self.tiedTogether = False
                    print("失職")

            # 指定距離より遠くは時間停止
            if Calc2d.innerCircle(self.pos, 30, self.playerPos):
                # プレイヤーが感知範囲にいるか
                if self.bresenhamLine.innerCells(self.pos, self.discoveryRange, self.playerPos):
                    self.nowMove = True
                    self.pathList = astar(
                        self.mapData, self.pos.reverse().pos(), self.playerPos.reverse().pos())
                    if self.pathList != None:
                        self.pathList.pop(0)
                        # 発見時ポップアップ生成
                        if not self.isDiscovery:
                            self.isDiscovery = True
                            self.createTextPopup("!", self.pos, "#FFA500")
                        return

                if not self.nowMove:
                    # 見失った場合ポップアップ生成
                    if self.isDiscovery:
                        self.isDiscovery = False
                        self.createTextPopup("?", self.pos, "#ffffff")
                    self.nowMove = True
                    # 感知範囲取得
                    chList = Calc2d.getCircleList(
                        self.mapData, self.pos, self.discoveryRange)
                    # ランダムに行き先決定
                    moList: List[Vector2] = []
                    for i in range(len(chList)):
                        p = Vector2(*chList[i])
                        if self.mapData[p.y][p.x] == 0:
                            moList.append(p)
                    if len(moList) == 0:
                        print("何故か積み")
                    else:
                        p = moList[randint(0, len(moList)-1)]
                        self.pathList = astar(
                            self.mapData, self.pos.reverse().pos(), p.reverse().pos())
                        if self.pathList != None:
                            self.pathList.pop(0)
                            return
                        print("ルート検索できず")
                    self.nowMove = False
                    self.pathList = []

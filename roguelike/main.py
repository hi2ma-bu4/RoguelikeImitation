# coding: utf-8
"""
ローグライク - 本体
"""
from typing import List, Optional, final
from random import random, randint

from roguelike.draw import RoguelikeDraws, Vector2, Colors, ta_Size
from roguelike.menu import RoguelikeMenu


@final
class Roguelike(RoguelikeDraws):
    """
    ローグライクをpygameで動かす為のclass
    """

    def __init__(self, pygame, windowSize: ta_Size = (15, 20), chipSize: int = 16, *, fontPath: List[Optional[str]] = [None]*2) -> None:
        super().__init__(pygame, windowSize, chipSize, fontPath=fontPath)

        # *初期値
        self.worldSeed = randint(1, self.RANDOM_SEED_MAX_NUM)
        self.nowFloor = 0
        self.floorName = "なぞのばしょ"
        self.passageTurn = 0

        self.Menu = RoguelikeMenu(self)

    def downFloor(self, pos: Vector2 = Vector2()) -> None:
        """
        1階層下る
        """

        self.darkMap2DataList()
        self.enemyKillSave()
        self.nowFloor += 1
        self.load_floorData()

        if pos == Vector2():
            for y in range(self.mapHeight):
                for x in range(self.mapWidth):
                    if self.floorMap[y][x] == 10:
                        self.player.pos.update(
                            x, y, maxX=self.mapWidth, maxY=self.mapHeight)
        else:
            self.player.pos.update(
                *pos.pos(), maxX=self.mapWidth, maxY=self.mapHeight
            )
        self.lightMap()
        self.viewFloorNum()
        self.changeDrawing = True

    def upFloor(self) -> None:
        """
        1階層上る
        """
        # 地上には逃がさない

        self.darkMap2DataList()
        self.enemyKillSave()
        if self.nowFloor <= 1:
            return
        self.nowFloor -= 1
        self.load_floorData()

        for y in range(self.mapHeight):
            for x in range(self.mapWidth):
                if self.floorMap[y][x] == 11:
                    self.player.pos.update(
                        x, y, maxX=self.mapWidth, maxY=self.mapHeight)
        self.lightMap()
        self.viewFloorNum()
        self.changeDrawing = True

    def playTurn(self) -> None:
        """
        ターン処理実行
        """

        # アニメーション関係
        p = self.player

        doAnim = 0
        if not self.isGameOver:
            doAnim += p.animTurn()

        miX = self.world.mapInX
        miY = self.world.mapInY

        for e in self.enemyList:
            t = e.animTurn()
            if 0 <= e.pos.x-miX < self.world.COL and 0 <= e.pos.y-miY < self.world.ROW:
                doAnim += t

        for tp in self.textPopupList:
            if tp._movePos != (0, 0):
                self.changeDrawing = True
        if doAnim or len(self.particleList) > 0:
            self.changeDrawing = True

        # ゲームオーバー時停止
        if self.isGameOver:
            self.stopTurn = True
            return

        # プレイヤー行動まで待機
        if self.player.doTurn():
            return
        self.stopTurn = True

        # 敵行動
        doTurn = False
        for e in self.enemyList:
            if e.doTurn():
                doTurn = True

        if doTurn:
            self.changeDrawing = True
        self.stopTurn = False

    def playerMove(self, x: int = 0, y: int = 0, *, notMove: bool = False) -> bool:
        """
        主人公行動
        """

        if self.doTurn():
            return False

        p = self.player
        if not notMove:
            p.turnMove()

        co = self.chipOptGet(x+p.pos.x, y+p.pos.y)
        if notMove or co["passage"] == 1:
            self.changeDrawing = True

            p.move(x, y, notMove=True)
            return False
        elif co["passage"] == 0:
            self.changeDrawing = True

            for e in self.enemyList:
                if not e.death and e.pos == (x+p.pos.x, y+p.pos.y):
                    p.move(x, y, notMove=True)
                    self.playerAttack(notTurn=True)
                    return False

            p.move(x, y)
            self.lightMap()
            return True
        raise RuntimeError("不明な通行id")

    def playerAttack(self, shortDistance: bool = True, *, notTurn: bool = False) -> None:
        """
        敵に攻撃
        """

        if self.doTurn():
            return

        p = self.player
        if not notTurn:
            p.turnMove()

        # 向き算出
        d = p.direction
        dPos = Vector2()
        if d == p.DIRECT_LEFT:
            dPos.x -= 1
        elif d == p.DIRECT_UP:
            dPos.y -= 1
        elif d == p.DIRECT_RIGHT:
            dPos.x += 1
        elif d == p.DIRECT_DOWN:
            dPos.y += 1

        # 対象の敵を羅列
        atkList = []

        if shortDistance:
            # 近距離
            tmpPos = dPos + p.pos
            for e in self.enemyList:
                if tmpPos == e.pos and not e.death:
                    atkList.append(e)
        else:
            # 遠距離
            pass

        for e in atkList:
            damage = int(p.status.attack * random())
            if e.status.hp <= damage:
                self.tmpKillEnemyList[e._ind] = 0
                if p.status.addExp(e.status.totalExp):
                    p.status.maxHP = int(p.status.maxHP * 1.1)
                    p.status.hp = p.status.maxHP
                    self.createLevelUpPopup()
            e.status.hp -= damage
            if self.createDamagePopup(str(damage), e.pos, Colors.WHITE):
                self.createParticles(e.pos, Colors.MONSTER_BLOOD, 10)

    def doTurn(self) -> bool:
        """
        ターン経過
        """
        if self.stopTurn or not self.player.turnStop:
            return True

        if self.player.status.hp <= 0:
            self.isGameOver = True
            self.changeDrawing = True
            return True
        return False

    def checkEvent(self) -> None:
        """
        決定キーでのイベント処理
        """
        p = self.player.pos
        fmi = self.floorMap[p.y][p.x]
        if fmi == 10:
            self.upFloor()
        elif fmi == 11:
            self.downFloor()

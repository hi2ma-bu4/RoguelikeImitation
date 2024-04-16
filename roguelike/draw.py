# coding: utf-8
"""
ローグライク - 描画
"""

from typing import Any, Tuple, List, Dict, Optional

from roguelike.base import RoguelikeBase, Colors, ta_Size, ta_entity
from lib.calc2d import Vector2, ta_pos


class RoguelikeDraws(RoguelikeBase):
    """
    ローグライクをpygameで描画する為のclass
    """

    def __init__(self, pygame, windowSize: ta_Size = (15, 20), chipSize: int = 16, *, fontPath: List[Optional[str]] = [None]*2) -> None:
        super().__init__(pygame, windowSize, chipSize, fontPath=fontPath)

        self.hideMap: List[List[Any]]

        self.hpBarList = []

        # *描画管理
        self.changeDrawing = True

    def allDrawing(self) -> bool:
        """
        全体一括描画
        """

        # 描画回数を減らして軽量化
        if self.changeDrawing:
            self.changeDrawing = False
            # print("描画")

            # 画面リセット
            self.screen.fill((0, 0, 0))

            # ゲーム開始まで待機
            if self.isPlayGame:
                # マップ描画
                self.drawMap()
                # エンティティ描画
                self.drawEntity()
                # 敵HPバー表示
                self.drawEnemyHPBar()
                # パーティクル描画
                self.drawParticle()
                # 暗闇描画
                self.drawDarkness()
                # ポップアップ描画
                self.drawPopup()
                # プレイヤーHPバー表示
                self.drawPlayerBar()

                # ゲームオーバー時処理
                if self.isGameOver:
                    self.drawGameover()
            return True
        return False

    def drawMap(self) -> None:
        """
        ダンジョンマップを描画
        """
        self._mapImageSetter()
        # 描画
        miX = self.world.mapInX
        miY = self.world.mapInY
        for r in range(self.world.ROW):
            for c in range(self.world.COL):
                mx = c + miX
                my = r + miY
                if 0 <= mx < self.mapWidth and 0 <= my < self.mapHeight:
                    imageData = self.chipNameMap[my][mx]
                elif -1 <= mx <= self.mapWidth and -1 <= my <= self.mapHeight:
                    imageData = self._setChipData(
                        self.floorChipData["ceiling"])
                else:
                    imageData = []
                if imageData:
                    self.drawChip(
                        self.chipNameMap,
                        imageData[0],
                        c, r, mx, my,
                        imageData[1],
                        [*imageData[2:]]
                    )

    def drawEntity(self) -> None:
        """
        entityを描画
        """
        miX = self.world.mapInX
        miY = self.world.mapInY
        # enemy描画
        for e in self.enemyList:
            if not (
                0 <= e.pos.x-miX < self.world.COL
                and 0 <= e.pos.y-miY < self.world.ROW
            ) or e.death:
                continue
            if e.pos.pos() not in self.playerViewCell[1]:
                continue
            self.screen.blit(
                self.imageDict[e._nameId][0],
                ((e.pos.x-miX)*self.world.GS, (e.pos.y-miY)*self.world.GS-10),
                (*self._entityDrawDataGet(e), self.world.GS, self.world.CHARA_HEIGHT)
            )
            self._drawEnemyHP(e.pos, miX, miY, e.status.maxHP, e.status.hp)
        # プレイヤー描画
        self.screen.blit(
            self.imageDict[self.player._nameId][0],
            (self.world._fCOL*self.world.GS, self.world._fROW*self.world.GS-10),
            (
                *self._entityDrawDataGet(self.player),
                self.world.GS, self.world.CHARA_HEIGHT
            )
        )

    def _drawEnemyHP(self, pos: ta_pos, mx: int, my: int, maxHP: int, nowHP: int) -> None:
        """
        敵のHP描画
        """
        ep = Vector2.convert(pos)
        # 割合
        if nowHP > maxHP:
            nowHP = maxHP
        par = int(nowHP / maxHP*100)/100

        bx = (ep.x-mx)*self.world.GS+self.world.GS*0.1
        by = (ep.y-my+1)*self.world.GS-self.world.CHARA_HEIGHT
        maxX = self.world.GS*0.8
        # HPバー描画
        self.hpBarList.append([
            (bx+maxX*par, by, maxX*(1-par), 2),
            (bx, by, maxX*par, 2)
        ])

    def drawEnemyHPBar(self) -> None:
        """
        敵HPバー表示
        """
        for hb in self.hpBarList:
            self.screen.fill(Colors.RED, hb[0])
            self.screen.fill(Colors.LIGHT_YELLOW_GREEN, hb[1])
        self.hpBarList = []

    def drawPlayerBar(self) -> None:
        """
        プレイヤーバー表示
        """
        s = self.player.status

        # *経験値バー
        # 割合
        par = int(s.exp / s.nextExp*200)/200

        expY = self.world.GS*0.1
        # 描画
        self.screen.fill(
            Colors.GRAY, (0, self.world.WINDOW_HEIGHT-expY, self.world.WINDOW_WIDTH, expY))
        self.screen.fill(Colors.LIGHT_BLUE, (
            0, self.world.WINDOW_HEIGHT - expY,
            self.world.WINDOW_WIDTH*par, expY)
        )

        # *HPバー
        # 割合
        par = int(s.hp / s.maxHP*200)/200

        maxX = self.world.GS*4
        maxY = self.world.GS*0.5
        # 描画
        self.screen.fill(
            Colors.RED, (0, self.world.WINDOW_HEIGHT-maxY-expY, maxX, maxY))
        self.screen.fill(Colors.LIGHT_YELLOW_GREEN, (
            0,
            self.world.WINDOW_HEIGHT-maxY-expY,
            maxX*par, maxY)
        )
        # テキスト
        text = self.damageFont.render(f"{s.hp} / {s.maxHP}", True, (0, 0, 0))
        self.screen.blit(text, (10, self.world.WINDOW_HEIGHT-maxY-expY))

    def drawDarkness(self) -> None:
        """
        暗闇を描画
        """

        miX = self.world.mapInX
        miY = self.world.mapInY

        # 半透明
        for r in range(self.world.ROW):
            for c in range(self.world.COL):
                mx = c + miX
                my = r + miY
                if 0 <= mx < self.mapWidth and 0 <= my < self.mapHeight:
                    imageData = self._setChipData(self.hideMap[r][c][2])
                elif -2 <= mx < self.mapWidth+2 and -2 <= my < self.mapHeight+2:
                    imageData = self._setChipData("dark2")
                else:
                    imageData = []
                if imageData:
                    self.drawChip(
                        self.hideMap,
                        imageData[0],
                        c, r, c, r,
                        imageData[1],
                        [*imageData[2:]]
                    )

        # 不透過
        for r in range(self.world.ROW):
            for c in range(self.world.COL):
                mx = c + miX
                my = r + miY
                if 0 <= mx < self.mapWidth and 0 <= my < self.mapHeight:
                    imageData = self._setChipData(self.darkMap[my][mx][2])
                elif -2 <= mx < self.mapWidth+2 and -2 <= my < self.mapHeight+2:
                    imageData = self._setChipData("dark1")
                else:
                    imageData = []
                if imageData:
                    self.drawChip(
                        self.darkMap,
                        imageData[0],
                        c, r, mx, my,
                        imageData[1],
                        [*imageData[2:]]
                    )

    def drawPopup(self) -> None:
        """
        textPopup描画
        """
        miX = self.world.mapInX
        miY = self.world.mapInY

        for i in range(len(self.textPopupList)-1, -1, -1):
            tp = self.textPopupList[i]
            isDraw = False
            if tp.noMove \
                    or -1 <= tp.pos.x-miX <= self.world.COL \
                    and -1 <= tp.pos.y-miY <= self.world.ROW:
                isDraw = True
            flag = tp.update(isDraw)
            # 用済みは削除
            if flag:
                self.textPopupList.pop(i)

    def drawParticle(self):
        """
        パーティクルの描画
        """
        miX = self.world.mapInX
        miY = self.world.mapInY

        for i in range(len(self.particleList)-1, -1, -1):
            pa = self.particleList[i]
            isDraw = False
            if -1 <= pa.pos.x-miX <= self.world.COL and -1 <= pa.pos.y-miY <= self.world.ROW:
                isDraw = True
            flag = pa.update(isDraw)
            # 用済みは削除
            if flag:
                self.particleList.pop(i)

    def drawChip(self, mapList: list, image, x: int, y: int, mx: int, my: int, imageType="auto", opt: list = []) -> None:
        """
        1マスを描画
        """
        xGS = x * self.world.GS
        yGS = y * self.world.GS
        if imageType == "index":
            self.screen.blit(
                image, (xGS, yGS), (opt[0]*self.world.GS, opt[1]*self.world.GS+1, self.world.GS, self.world.GS))
        elif imageType == "auto":
            tmpPos = self._autoChipPosGet(mapList, mx, my, opt[0])

            # オートchip描画
            for dx in range(2):
                for dy in range(2):
                    self.screen.blit(image, (xGS + dx * self.world._fGS, yGS + dy * self.world._fGS), (dx * self.world._fGS,
                                     tmpPos[dy * 2 + dx] + dy * self.world._fGS - dy + 1, self.world._fGS, self.world._fGS))
        else:
            print(f"不明な形式:{imageType}")

    def drawGameover(self) -> None:
        """
        ゲームオーバー描画
        """
        goText = self.gameOverFont.render("Game Over", True, Colors.RED)
        self.screen.blit(goText, goText.get_rect(
            center=(self.world.WINDOW_WIDTH//2, self.world.WINDOW_HEIGHT//2)))

    def chipOptGet(self, x: int, y: int) -> Dict[str, Any]:
        """
        マップチップオプション取得
        """
        if 0 <= x < self.mapWidth and 0 <= y < self.mapHeight:
            return self.CHIP_OPT[str(self.floorMap[y][x])]
        return self.CHIP_OPT["etc"]

    def lightMap(self) -> None:
        """
        マップを照らす
        """
        self.hideMap = [
            [
                ['none', 'none', 'dark2'] for j in range(self.world.COL)
            ] for i in range(self.world.ROW)
        ]

        p = self.player.pos
        self.playerViewCell = self.bresenhamLine.get_visible_cells(
            p, self.floorMapSetting["lightRange"])

        for l in self.playerViewCell[1]:
            if self.playerViewCell[0]:
                self.darkMap[l[1]][l[0]][2] = "none"
            self.hideMap[l[1]-self.world.mapInY][
                l[0] - self.world.mapInX][2] = "none"

    def _entityDrawDataGet(self, ent: ta_entity) -> Tuple[int, int]:
        """
        entityの描画用座標取得
        """
        animCou = ent.nowAnimCou
        if animCou >= 3:
            animCou = animCou - 2
        direction = ent.direction

        ret_pos = (animCou*self.world.GS, self.world.CHARA_HEIGHT*direction)
        return ret_pos

    def _replaceChip(self, x: int, y: int) -> str:
        """
        画像を1マスごとに振り分け
        """
        nc = self.floorMap[y][x]
        co = self.CHIP_OPT[str(nc)]
        if co["name"] == "wall":
            # 壁
            wca = self._wallChipAssort(x, y, 5)
            if wca != "etc":
                return self.floorChipData[wca]
        elif co["name"] in ["upStep", "downStep"]:
            # 出入口
            return self.floorDict["設定"][co["name"]]
        else:
            # その他
            return self.floorChipData[co["name"]]

        # 未設定なchip
        return "forestSnow"

    def _mapImageSetter(self) -> None:
        """
        マップ配列上にchip画像path設定
        """
        self.chipNameMap = []
        for r in range(self.mapHeight):
            self.chipNameMap.append([])
            for c in range(self.mapWidth):
                chipData = self._replaceChip(c, r)
                self.chipNameMap[r].append([])
                self.chipNameMap[r][c] = self._setChipData(chipData)

    def _setChipData(self, name: str) -> List[Any]:
        """
        chipデータ設定
        """
        tmpData = name.split("-")
        if len(tmpData) == 3:
            return [*self.imageDict[tmpData[0]], int(tmpData[1]), int(tmpData[2])]
        else:
            if name in self.imageDict:
                return [*self.imageDict[name], name]
        return []

    def _chipIdEqual(self, x: int, y: int, id: int, outRet: int = 0) -> int:
        """
        chipがidと一致しているか
        """
        if 0 <= x < self.mapWidth and 0 <= y < self.mapHeight:
            if self.floorMap[y][x] == id:
                return 1
            return 0
        return outRet

    def _chipNameEqual(self, mapList: list, x: int, y: int, name: str, outRet: int = 0) -> int:
        """
        chipがpathと一致しているか
        """
        # if 0 <= x < self.mapWidth and 0 <= y < self.mapHeight:
        if 0 <= x < len(mapList[0]) and 0 <= y < len(mapList):
            if mapList[y][x][2] == name:
                return 1
            return 0
        return outRet

    def _wallChipAssort(self, x: int, y: int, id: int) -> str:
        """
        壁のchipを正確に組み合わせる
        """
        if not self._chipIdEqual(x, y, id):
            return "etc"

        if not self._chipIdEqual(x, y+1, id, 1):
            if self._chipIdEqual(x-1, y, id, 1):
                if self._chipIdEqual(x+1, y, id, 1):
                    return "bottomMid"
                return "bottomRight"
            else:
                if self._chipIdEqual(x+1, y, id, 1):
                    return "bottomLeft"
                return "bottomPillar"
        elif not self._chipIdEqual(x, y+2, id, 1):
            if self._chipIdEqual(x-1, y+1, id, 1):
                if self._chipIdEqual(x+1, y+1, id, 1):
                    return "topMid"
                return "topRight"
            else:
                if self._chipIdEqual(x+1, y+1, id, 1):
                    return "topLeft"
                return "topPillar"
        return "ceiling"

    def _autoChipNameAssort(self, mapList: list, x: int, y: int, name: str) -> int:
        """
        自身のchipの周りのchipで自身と同じ名前の位置を出力
        """
        company = 0
        company |= self._chipNameEqual(mapList, x, y-1, name, 1)
        company |= self._chipNameEqual(mapList, x-1, y, name, 1) << 1
        company |= self._chipNameEqual(mapList, x+1, y, name, 1) << 2
        company |= self._chipNameEqual(mapList, x, y+1, name, 1) << 3
        company |= self._chipNameEqual(mapList, x-1, y-1, name, 1) << 4
        company |= self._chipNameEqual(mapList, x+1, y-1, name, 1) << 5
        company |= self._chipNameEqual(mapList, x-1, y+1, name, 1) << 6
        company |= self._chipNameEqual(mapList, x+1, y+1, name, 1) << 7
        return company

    def _autoChipPosGet(self, mapList: list, x: int, y: int, name: str):
        bitFlag = self._autoChipNameAssort(mapList, x, y, name)

        renderPos: List[int] = [0]*4
        # 左上
        bitTmp = bitFlag & 0b10011
        if bitTmp in [0b0, 0b10000]:
            # コーナー
            renderPos[0] = 0
        elif bitTmp in [0b1, 0b10001]:
            # 縦方向の道
            renderPos[0] = self.world.GS
        elif bitTmp in [0b10, 0b10010]:
            # 横方向の道
            renderPos[0] = self.world.GS * 2
        elif bitTmp == 0b11:
            # 交差
            renderPos[0] = self.world.GS * 3
        else:
            # 境界なし
            renderPos[0] = self.world.GS * 4

        # 右上
        bitTmp = bitFlag & 0b100101
        if bitTmp in [0b0, 0b100000]:
            renderPos[1] = 0
        elif bitTmp in [0b1, 0b100001]:
            renderPos[1] = self.world.GS
        elif bitTmp in [0b100, 0b100100]:
            renderPos[1] = self.world.GS * 2
        elif bitTmp == 0b101:
            renderPos[1] = self.world.GS * 3
        else:
            renderPos[1] = self.world.GS * 4

        # 左下
        bitTmp = bitFlag & 0b1001010
        if bitTmp in [0b0, 0b1000000]:
            renderPos[2] = 0
        elif bitTmp in [0b1000, 0b1001000]:
            renderPos[2] = self.world.GS
        elif bitTmp in [0b10, 0b1000010]:
            renderPos[2] = self.world.GS * 2
        elif bitTmp == 0b1010:
            renderPos[2] = self.world.GS * 3
        else:
            renderPos[2] = self.world.GS * 4

        # 右下
        bitTmp = bitFlag & 0b10001100
        if bitTmp in [0b0, 0b10000000]:
            renderPos[3] = 0
        elif bitTmp in [0b1000, 0b10001000]:
            renderPos[3] = self.world.GS
        elif bitTmp in [0b100, 0b10000100]:
            renderPos[3] = self.world.GS * 2
        elif bitTmp == 0b1100:
            renderPos[3] = self.world.GS * 3
        else:
            renderPos[3] = self.world.GS * 4
        return renderPos

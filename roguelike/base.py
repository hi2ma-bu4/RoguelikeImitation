# coding: utf-8
"""
ローグライク - コア
"""

from typing import Any, Tuple, List, Dict, Callable, Final, Union, Optional, final
from dataclasses import dataclass
from pygame.locals import Rect, RLEACCEL
from random import Random, random, randint, uniform
from copy import deepcopy

from lib.files import FileCSV, FileJSON, SqlManager
from lib.compress import Comp
from lib.stringLib import Base
from roguelike.map import RogueLikeMap, RouteSearch
from roguelike.char import Status, Entity, Enemy, Player, Calc2d, Vector2, ta_pos
from roguelike.effect import Colors, EffectBase, TextPopup, Particle, ta_color

# type aliases
ta_Size = Tuple[int, int]
ta_entity = Union[Player, Enemy]

# ここまで


class RoguelikeBase:
    """
    ローグライクをpygameで実行する為の基底class
    """

    RANDOM_SEED_MAX_NUM: Final[int] = 9999999999

    CHIP_OPT: Final[Dict[str, Dict[str, Union[str, int]]]] = {
        # 例外処理用
        "etc": {
            "name": "wall",
            "passage": 1
        },
        # 文字で指定(int→str)
        "0": {
            "name": "floor",
            "passage": 0
        },
        "1": {
            "name": "passage",
            "passage": 0
        },
        "5": {
            "name": "wall",
            "passage": 1
        },
        "10": {
            "name": "upStep",
            "passage": 0
        },
        "11": {
            "name": "downStep",
            "passage": 0
        }
    }

    def __init__(self, pygame, windowSize: ta_Size = (15, 20), chipSize: int = 16, *, fontPath: List[Optional[str]] = [None]*2) -> None:
        self.pg = pygame

        # *キャラ等管理
        self.player = Player((0, 0), Status(20, 20, 3))
        self.enemyList: List[Enemy] = []

        self.fontPath = fontPath

        self.userName = ""

        # *定数(動的)設定
        RoguelikeBase.world = World(*windowSize, chipSize, self.player.pos)

        self.screen = self.pg.display.set_mode(self.world.SCR_RECT.size)
        self.gameOverFont = self.pg.font.Font(None, 60)
        self.damageFont = self.pg.font.Font(None, 25)
        self.FloorNumFont = self.pg.font.Font(self.fontPath[0], 25)

        self._img = Image(self.pg, 1)

        EffectBase.set_baseInit(
            self.pg,
            self.screen,
            self.world,
            self.player.pos,
            (self.world.GS, self.world.GS),
            (self.world._fCOL, self.world._fROW)
        )
        self.textPopupList: List[TextPopup] = []
        self.particleList: List[Particle] = []

        self.killEnemyDict: List[str] = []
        self.tmpKillEnemyList: List[int] = []
        self.nowFloorEnemyDataDict: Dict[str, str] = dict()
        self.darkMap: List[List[List[Any]]] = []
        self.darkDataList = []

        # *ゲーム管理
        self.isPlayGame = False
        self.isGameOver = False

        # *文字列圧縮用
        self.lzw = Comp()

        # *キャッシュを使用して計算を高速化
        self.binaryMap: List[List[int]] = []
        self.bresenhamLine: Calc2d.BresenhamLine
        self.baseIns = Base(
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

        # プレイヤーダメージポップアップゴリ押し
        Enemy.enemyAttackSet(_enemyAttackBase(
            self.player.status,
            lambda x: self.createDamagePopup(x, self.player.pos, Colors.RED),
            lambda: self.createParticles(self.player.pos, Colors.BLOOD, 8)
        ))
        Enemy.textPopupSet(self.createPopup)

    @final
    def fileInit(self, imageCSVPath: str, floorJSONPath: str, enemyJSONPath: str, itemJSONPath: str) -> None:
        """
        構成ファイル読み込み
        """
        self.imageDict = self._img.loadImages(imageCSVPath, "image/")
        self.floorDict: Dict[str, Any] = FileJSON(floorJSONPath).get()
        self.enemyDict: Dict[str, Any] = FileJSON(enemyJSONPath).get()
        self.itemDict: Dict[str, Any] = FileJSON(itemJSONPath).get()

    @final
    def db_setting(self, userDataBase: str) -> None:
        """
        構成db読み込み
        """
        # セーブデータ読み込み
        self.userSaveDB = SqlManager(userDataBase, "saveData", """
    userName TEXT,
    seed TEXT,
    posData TEXT,
    status TEXT,
    killEnemy TEXT,
    floorEnemyData TEXT,
    darkData TEXT,
    PRIMARY KEY (userName)
""")

    @final
    def game_save(self) -> None:
        """
        データをセーブ
        """

        name = self.userName
        if name == "":
            return

        self.nowFloorEnemyDataDict = dict()
        for enemy in self.enemyList:
            self.nowFloorEnemyDataDict[str(enemy._ind)] = enemy.out()
        self.darkMap2DataList()
        self.enemyKillSave()

        where = f'userName="{name}"'
        saveData = self.userSaveDB.select(select="userName", where=where)
        if len(saveData) > 0:
            self.userSaveDB.update({
                "posData": self.lzw.json_compress([self.nowFloor, *self.player.pos.pos()]),
                "status": self.lzw.compress(self.player.status.out()),
                "killEnemy": self.lzw.json_compress(self.killEnemyDict),
                "floorEnemyData": self.lzw.json_compress(self.nowFloorEnemyDataDict),
                "darkData": self.lzw.json_compress(self.darkDataList),
            },
                where=where)
            print("セーブデータを上書き保存しました")
        else:
            self.userSaveDB.insert((
                name,
                str(self.worldSeed),
                self.lzw.json_compress(
                    [self.nowFloor, *self.player.pos.pos()]),
                self.lzw.compress(self.player.status.out()),
                self.lzw.json_compress(self.killEnemyDict),
                self.lzw.json_compress(self.nowFloorEnemyDataDict),
                self.lzw.json_compress(self.darkDataList),
            ))
            print("セーブデータを新規作成しました")

    @final
    def game_load(self) -> bool:
        """
        データをロード
        """

        name = self.userName
        if name == "":
            return False
        saveData = self.userSaveDB.select(
            select="seed, posData, status, killEnemy, floorEnemyData, darkData", where=f'userName="{name}"')

        if len(saveData) > 0:
            print(f"ユーザー名「{name}」でロード")
            self.worldSeed = int(saveData[0][0])
            posData = self.lzw.json_decompress(saveData[0][1])
            self.nowFloor = posData[0] - 1
            self.player.pos.update(*posData[1:3])
            self.player.status.load(self.lzw.decompress(
                saveData[0][2]
            ))
            self.killEnemyDict = self.lzw.json_decompress(
                saveData[0][3]
            )
            self.nowFloorEnemyDataDict = self.lzw.json_decompress(
                saveData[0][4]
            )
            self.darkDataList = self.lzw.json_decompress(
                saveData[0][5]
            )
            return True

        print("ユーザーが見つかりませんでした")
        return False

    @final
    def load_floorData(self) -> None:
        """
        階層データを読み込み
        """
        print(f"{self.nowFloor}階層目")

        for k, v in self.floorDict.items():
            if k == "設定":
                continue
            if v["floorMin"] <= self.nowFloor <= v["floorMax"]:
                self.floorName = k
                self.tpFloorName = v["typing"]
                self.floorChipData = v["mapChip"]
                self.floorMapSetting = {
                    "roomMinSize": v["roomMinSize"],
                    "roomMaxSize": v["roomMaxSize"],
                    "minStep": v["minStep"],
                    "lightRange": v["lightRange"],
                    "mapSize": (v["mapSizeX"], v["mapSizeY"]),
                    "spawnProbability": v["spawnProbability"],
                    "enemy": v["enemy"],
                }
                break
        self.floorMap = self.rogueLikeMapCreator(
            self.floorMapSetting["mapSize"],
            self.worldSeed+self.nowFloor,
            roomMaxSize=self.floorMapSetting["roomMaxSize"],
            roomMinSize=self.floorMapSetting["roomMinSize"],
            minStep=self.floorMapSetting["minStep"]
        )
        self.mapWidth = len(self.floorMap[0])
        self.mapHeight = len(self.floorMap)
        Entity.mapDataSet(self.floorMap, self.bresenhamLine)
        self.enemyEstablishment(self.worldSeed+self.nowFloor)
        Entity.enemyListSet(self.enemyList)
        self.nowFloorEnemyDataDict = dict()

        self.textPopupList = []

        # 暗闇マップ読み込み
        self.loadDarkDataList2Map()

        self.hideMap = []

    def viewFloorNum(self):
        """
        階層番号表示
        """
        self.textPopupList.append(TextPopup(
            self.FloorNumFont,
            f"{self.tpFloorName}//e//j≪ - ≫{self.nowFloor}かいそう≪階層≫め≪目≫",
            self.player.pos - (self.world._fCOL, self.world._fROW),
            (0, 0),
            (0, 0),
            70,
            Colors.WHITE,
            noMove=True,
            isTyping=True
        ))

    def rogueLikeMapCreator(self, size: ta_Size, seed: int = randint(1, 999), *, roomMaxSize: ta_Size = (5, 5), roomMinSize: ta_Size = (3, 3), minStep: int = 60) -> List[List[Any]]:
        """
        ローグライクのマップ生成
        (ゴール出来るマップのみ生成)
        """

        r = Random()
        r.seed(seed)

        repDict = {1: 0, 5: 1, 10: 2, 11: 3}

        while True:
            # マップ生成
            print("Map生成開始...", end="")
            rlMap = RogueLikeMap(
                size, seed, roomMaxSize=roomMaxSize, roomMinSize=roomMinSize)
            mapData = rlMap.createMap()

            print("完了！")

            # ちゃんとゴールできるか
            tmp = Calc2d.listReplace(deepcopy(mapData), repDict)
            route = RouteSearch.search(tmp, size[0])
            if route and len(route) > minStep:
                self.binaryMap = Calc2d.convert_1dTo2d(
                    Calc2d.listReplace(tmp, {2: 0, 3: 0}), size[0])
                self.bresenhamLine = Calc2d.BresenhamLine(self.binaryMap)
                return Calc2d.convert_1dTo2d(mapData, size[0])

            # 再生成
            seed = r.randint(1, self.RANDOM_SEED_MAX_NUM)
            print(f"経路未開通 再生成seed: {seed}")

    def enemyEstablishment(self, seed: int) -> None:
        """
        敵設置
        """

        self.enemyKillLoad()
        t_kel = self.tmpKillEnemyList
        eCou = 0

        self.enemyList = []
        rnd = Random()
        rnd.seed(seed)
        sp = self.floorMapSetting["spawnProbability"]
        for r in range(self.mapHeight):
            for c in range(self.mapWidth):
                if self.floorMap[r][c] == 0:
                    if rnd.randint(0, sp) == 0:
                        ri = rnd.randint(0, 100)
                        if len(t_kel) <= eCou:
                            t_kel.append(1)
                        if t_kel[eCou] == 1:
                            for k, v in self.floorMapSetting["enemy"].items():
                                if v >= ri:
                                    ed = self.enemyDict[k]

                                    eo = Enemy((c, r), ed["image"], Status(
                                        ed["hp"], ed["speed"], ed["attack"], exp=ed["exp"]), animSpeed=ed["animSpeed"], ind=eCou)

                                    if str(eCou) in self.nowFloorEnemyDataDict.keys():
                                        eo.load(self.nowFloorEnemyDataDict[
                                            str(eCou)
                                        ])
                                    self.enemyList.append(eo)
                                    break
                                ri -= v
                        eCou += 1

    def enemyKillSave(self) -> None:
        if len(self.tmpKillEnemyList) <= 0:
            return
        tmp = self.baseIns.n2m(
            2, "".join(map(str, self.tmpKillEnemyList)), 62
        )
        maxL = self.baseIns.dec2n(len(self.tmpKillEnemyList), 62)
        if tmp == -1 or maxL == -1:
            print("敵討伐数保存失敗")
            tmp = "0,1"
        else:
            tmp = f"{maxL},{tmp}"
        if len(self.killEnemyDict) < self.nowFloor:
            self.killEnemyDict.append(tmp)
        else:
            self.killEnemyDict[self.nowFloor-1] = tmp

    def enemyKillLoad(self) -> None:
        if len(self.killEnemyDict) <= 0:
            return

        if len(self.killEnemyDict) < self.nowFloor:
            self.killEnemyDict.append("0,1")
        tmpS = self.killEnemyDict[self.nowFloor-1].split(",")
        tmp = self.baseIns.n2m(62, tmpS[1], 2)
        if tmp == -1:
            print("敵討伐数読み込み失敗")
            tmp = ""
        tmp = tmp.zfill(int(self.baseIns.n2dec(2, tmpS[0])))
        self.tmpKillEnemyList = [int(v) for v in tmp]

    def darkMap2DataList(self) -> None:
        """
        暗闇マップを保存用リストに変換、格納
        """

        if len(self.darkMap) <= 0:
            return

        m2d = self.bresenhamLine.map_2d

        ret = ""
        for r in range(self.mapHeight):
            for c in range(self.mapWidth):
                if m2d[r][c] == 0:
                    if self.darkMap[r][c][2] == "dark1":
                        ret += "1"
                    else:
                        ret += "0"
        if len(self.darkDataList) < self.nowFloor:
            self.darkDataList.append("")
        self.darkDataList[self.nowFloor-1] = \
            f"{self.baseIns.dec2n(len(ret), 62)},{self.baseIns.n2m(2, ret, 62)}"

    def loadDarkDataList2Map(self) -> None:
        """
        暗闇マップを読み込み
        """

        self.darkMap = [
            [
                ['none', 'none', 'dark1'] for j in range(self.mapWidth)
            ] for i in range(self.mapHeight)
        ]
        if len(self.darkDataList) < self.nowFloor:
            return

        tmp = self.darkDataList[self.nowFloor-1].split(",")

        mLen = self.baseIns.n2dec(62, tmp[0])
        ret = self.baseIns.n2m(62, tmp[1], 2)
        if ret == -1 or mLen == -1:
            print("暗闇マップデータ復元失敗！！")
            return
        ret = ret.zfill(mLen)

        m2d = self.bresenhamLine.map_2d

        t = 0
        for r in range(self.mapHeight):
            for c in range(self.mapWidth):
                if m2d[r][c] == 0:
                    if ret[t] == "0":
                        self.darkMap[r][c][2] = "none"
                    t += 1

    def createDamagePopup(self, text: str, pos: ta_pos, color: ta_color) -> bool:
        """
        ダメージポップアップ生成
        """
        tmpPos = Vector2.convert(pos)

        isP = True
        if text == "0":
            text = "miss"
            isP = False

        self.textPopupList.append(TextPopup(
            self.damageFont,
            text,
            tmpPos - (0, 1),
            (0, -2),
            (randint(2, self.world.GS-2), randint(2, self.world.GS-2)),
            20,
            color
        ))
        return isP

    def createPopup(self, text: str, pos: ta_pos, color: ta_color) -> None:
        """
        普通のポップアップ生成
        """
        tmpPos = Vector2.convert(pos)
        self.textPopupList.append(TextPopup(
            self.damageFont,
            text,
            tmpPos - (0, 1),
            (0, 0),
            (self.world._fGS, self.world._fGS),
            20,
            color
        ))

    def createParticle(self, pos: ta_pos, color: ta_color) -> None:
        """
        パーティクル生成
        """
        tmpPos = Vector2.convert(pos)

        self.particleList.append(Particle(
            tmpPos,
            (int(uniform(-8, 8)), int(uniform(-8, 8))),
            3,
            8,
            color
        ))

    def createParticles(self, pos: ta_pos, color: ta_color, cou: int) -> None:
        """
        パーティクル群生成
        """
        tmpPos = Vector2.convert(pos)

        for i in range(cou):
            self.createParticle(tmpPos, color)

    def createLevelUpPopup(self) -> None:
        """
        レベルアップダメージポップ生成
        """
        self.textPopupList.append(TextPopup(
            self.damageFont,
            "Level Up!",
            self.player.pos + (
                -self.world._fCOL,
                self.world.WINDOW_HEIGHT - self.world._fROW
            ),
            (0, 0),
            (0, -self.world._fGS),
            80,
            Colors.LIGHT_YELLOW_GREEN,
            noMove=True
        ))


def _enemyAttackBase(playerStatus: Status, damagePopup: Callable[..., bool], damageParticle: Callable[..., None]) -> Callable[..., None]:
    """
    プレイヤーのステータスをキャッシュ
    """

    def _enemyAttack(self, e: Enemy) -> None:
        """
        プレイヤーのhpを減らす
        """
        damage = int(e.status.attack * random())
        playerStatus.hp -= damage

        if damagePopup(str(damage)):
            damageParticle()

    return _enemyAttack


@final
@dataclass
class World:
    """
    世界の情報
    """

    def __init__(self, row: int, col: int, chipSize: int, plPos: Vector2) -> None:

        # *定数(動的)
        World.ROW: Final[int] = row
        World.COL: Final[int] = col
        World.GS: Final[int] = chipSize
        World.WINDOW_WIDTH: Final[int] = self.COL*self.GS
        World.WINDOW_HEIGHT: Final[int] = self.ROW*self.GS
        World.CHARA_HEIGHT: Final[int] = 40

        World._fROW: Final[int] = self.ROW//2
        World._fCOL: Final[int] = self.COL//2
        World._fGS: Final[int] = self.GS//2
        World.SCR_RECT: Final = Rect(
            0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self._plPos = plPos

    @property
    def mapInX(self) -> int:
        return self._plPos.x - self._fCOL

    @property
    def mapInY(self) -> int:
        return self._plPos.y - self._fROW


@final
class Image:
    """
    pygame画像読み込み
    """

    def __init__(self, pygame, GS_SIZE: int) -> None:
        self._pygame = pygame
        self._GS_SIZE = GS_SIZE

    def load(self, filename, *, colorKey=None):
        """
        pygameに使用できる形式で画像読み込み
        """
        try:
            image = self._pygame.image.load(filename)
        except self._pygame.error as e:
            print("Cannot load image:", filename)
            raise SystemExit(e)
        image = self._pygame.transform.rotozoom(image, 0, self._GS_SIZE)
        image = image.convert_alpha()
        if colorKey is not None:
            if colorKey == -1:
                colorKey = image.get_at((0, 0))
            image.set_colorkey(colorKey, RLEACCEL)
        return image

    def loadImages(self, path: str, basePath: str = "") -> Dict[str, List[Any]]:
        csv = FileCSV(path).get()
        return {r[0]: [self.load(basePath + r[1]), r[2]] for r in csv}

# coding: utf-8
"""
ローグライク - メニュー
"""

from typing import List, Final, final
from pygame.locals import QUIT, KEYDOWN, KEYUP, TEXTEDITING, TEXTINPUT, \
    K_ESCAPE, K_RETURN, K_BACKSPACE, K_DELETE, \
    K_LEFT, K_UP, K_RIGHT, K_DOWN, \
    K_a, K_d, K_e, K_m, K_s, K_w

from lib.jp_input import JpText
from lib.eastAsianWidthOverride import slen


class RoguelikeMenu:
    """
    ローグライクでメニュー画面を管理するクラス
    """

    K_LEFT: Final[List[int]] = [K_LEFT, K_a]
    K_UP: Final[List[int]] = [K_UP, K_w]
    K_RIGHT: Final[List[int]] = [K_RIGHT, K_d]
    K_DOWN: Final[List[int]] = [K_DOWN, K_s]
    K_ATTACK: Final[List[int]] = [K_e]
    K_MENU: Final[List[int]] = [K_ESCAPE, K_m]
    K_RETURN: Final[List[int]] = [K_RETURN]

    def __init__(self, par) -> None:
        self.par = par

        # *定数(動的)
        self.WINDOW_WIDTH: Final[int] = self.par.world.WINDOW_WIDTH
        self.WINDOW_HEIGHT: Final[int] = self.par.world.WINDOW_HEIGHT

        self.pg = self.par.pg

        # *キー入力設定
        self._keyFlags = {
            "UP": True,
            "DOWN": True,

            "MENU": True,
            "ATTACK": True,
            "RETURN": True,
        }

        # *jp_input設定
        self.jpt = JpText()
        self.jpt_inputText = format(self.jpt)
        self.event_trigger = {
            K_BACKSPACE: self.jpt.delete_left_of_cursor,
            K_DELETE: self.jpt.delete_right_of_cursor,
            K_LEFT: self.jpt.move_cursor_left,
            K_RIGHT: self.jpt.move_cursor_right,
            K_RETURN: self.jpt.enter,
        }

        # *メニュー描画用
        self.menuFont = self.pg.font.Font(self.par.fontPath[0], 24)
        self.inputFont = self.pg.font.Font(self.par.fontPath[1], 24)
        self.inputFont.set_bold(True)

        self.menuItems = ["セーブ", "セーブして終了", "セーブせずに終了", "もどる"]
        self.selectMenuItem = 0

        # 名前を変更中か
        self.editName = True
        self.pg.key.start_text_input()
        # メニューを開いているか
        self.openMenu = False

    def getEvent(self) -> int:
        """
        イベント取得
        """
        for event in self.pg.event.get():
            if event.type == QUIT:
                return -2

            if event.type == KEYDOWN:
                if self.editName:
                    # 名前編集時
                    if not self.jpt.is_editing:
                        if event.key in self.event_trigger.keys():
                            self.jpt_inputText = self.event_trigger[event.key](
                            )
                        if event.unicode in ("\r", "") and event.key == K_RETURN:
                            # 名前確定

                            # 設定変更
                            self.pg.key.stop_text_input()
                            self.pg.event.clear()
                            self._keyFlags["RETURN"] = False

                            print(f"ユーザー名「{self.jpt_inputText}」で実行")
                            # 名前設定
                            self.par.userName = self.jpt_inputText
                            self.jpt_inputText = format(self.jpt)
                            self.editName = False

                            # セーブデータ呼び出し
                            self.par.game_load()
                            # 上位の階層から降りてきた体
                            self.par.downFloor(self.par.player.pos)

                            # ゲームスタート
                            self.par.isPlayGame = True
                            break
                else:
                    # ゲーム実行時
                    km = self.pg.key.get_mods()
                    onShift = bool(
                        km & self.pg.KMOD_LSHIFT or km & self.pg.KMOD_RSHIFT)

                    # 特殊行動
                    if event.key in self.K_MENU:
                        if self._keyFlags["MENU"]:
                            self._keyFlags["MENU"] = False
                            self.openMenu = not self.openMenu
                            self.changeDrawing = True

                    # メニューが開いているか
                    if self.openMenu:
                        # 変更
                        if event.key in self.K_UP:
                            if self._keyFlags["UP"]:
                                self._keyFlags["UP"] = False
                                self.selectMenuItem = (
                                    self.selectMenuItem - 1) % len(self.menuItems)
                                self.par.changeDrawing = True
                        elif event.key in self.K_DOWN:
                            if self._keyFlags["DOWN"]:
                                self._keyFlags["DOWN"] = False
                                self.selectMenuItem = (
                                    self.selectMenuItem + 1) % len(self.menuItems)
                                self.par.changeDrawing = True

                        # 決定
                        elif event.key in self.K_RETURN:
                            if self._keyFlags["RETURN"]:
                                self._keyFlags["RETURN"] = False
                                if self.selectMenuItem == 0:
                                    self.openMenu = False
                                    return 1
                                elif self.selectMenuItem == 1:
                                    return -1
                                elif self.selectMenuItem == 2:
                                    return -2
                                elif self.selectMenuItem == 3:
                                    self.openMenu = False
                    else:
                        # 特殊行動
                        if event.key in self.K_ATTACK:
                            if self._keyFlags["ATTACK"]:
                                self._keyFlags["ATTACK"] = False
                                self.par.playerAttack(True)
                        elif event.key in self.K_RETURN:
                            if self._keyFlags["RETURN"]:
                                self._keyFlags["RETURN"] = False
                                self.par.checkEvent()

                        # 移動
                        elif event.key in self.K_LEFT:
                            self.par.playerMove(x=-1, notMove=onShift)
                        elif event.key in self.K_UP:
                            self.par.playerMove(y=-1, notMove=onShift)
                        elif event.key in self.K_RIGHT:
                            self.par.playerMove(x=1, notMove=onShift)
                        elif event.key in self.K_DOWN:
                            self.par.playerMove(y=1, notMove=onShift)

            elif event.type == KEYUP:
                if event.key in self.K_UP:
                    self._keyFlags["UP"] = True
                elif event.key in self.K_DOWN:
                    self._keyFlags["DOWN"] = True

                elif event.key in self.K_MENU:
                    self._keyFlags["MENU"] = True
                elif event.key in self.K_ATTACK:
                    self._keyFlags["ATTACK"] = True
                elif event.key in self.K_RETURN:
                    self._keyFlags["RETURN"] = True

            if self.editName:
                # 全角入力
                if event.type == TEXTEDITING:
                    self.jpt_inputText = self.jpt.edit(event.text, event.start)

                # 半角入力 or 全角入力確定
                elif event.type == TEXTINPUT:
                    self.jpt_inputText = self.jpt.input(event.text)

                    # オーバーに対処
                    if slen(self.jpt_inputText) > 21:
                        cp = self.jpt.cursor_pos
                        for i in range(len(format(self.jpt))):
                            self.jpt.move_cursor_right()
                        for i in range(len(self.jpt_inputText)):
                            if slen(format(self.jpt)) <= 21:
                                break
                            self.jpt.delete_left_of_cursor()
                        for i in range(len(format(self.jpt))):
                            if cp >= self.jpt.cursor_pos:
                                break
                            self.jpt.move_cursor_left()
                        self.jpt_inputText = format(self.jpt)

                # 再描画
                if event.type in [KEYDOWN, TEXTEDITING, TEXTINPUT]:
                    self.par.changeDrawing = True

        return 0

    @final
    def drawAll(self, chDr: bool) -> None:
        """
        このクラスにおける描画管理
        """

        if chDr:
            # メニュー描画
            if self.editName:
                self.draw_editName()
            else:
                if self.openMenu:
                    self.draw_menu()

    @final
    def draw_editName(self) -> None:
        """
        名前入力欄描画
        """
        # 背景
        rect = self.pg.Rect(200, 200, self.WINDOW_WIDTH -
                            400, self.WINDOW_HEIGHT-400)
        self.pg.draw.rect(self.par.screen, (72, 135, 181), rect)
        text = self.menuFont.render("名前を入力", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WINDOW_WIDTH//2, 250))
        self.par.screen.blit(text, text_rect)

        # 入力欄
        rect = self.pg.Rect(300, 300, self.WINDOW_WIDTH-600, 40)
        self.pg.draw.rect(self.par.screen, (255, 255, 255), rect)
        # 入力された文字
        text = self.inputFont.render(self.jpt_inputText, True, (0, 0, 0))
        self.par.screen.blit(text, (310, 300))

    @final
    def draw_menu(self) -> None:
        """
        メニュー画面描画
        """
        # 背景
        rect = self.pg.Rect(200, 150, self.WINDOW_WIDTH -
                            400, self.WINDOW_HEIGHT-300)
        self.pg.draw.rect(self.par.screen, (72, 135, 181), rect)
        text = self.menuFont.render("Menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WINDOW_WIDTH//2, 175))
        self.par.screen.blit(text, text_rect)
        # 項目
        for i, item in enumerate(self.menuItems):
            if i == self.selectMenuItem:
                # 選択した項目に長方形を描画
                if (self.par.isGameOver or self.par.userName == "") and i < 2:
                    text_color = (128, 128, 128)
                else:
                    text_color = (102, 191, 255)
                rect = self.pg.Rect(300, 220 + i * 50,
                                    self.WINDOW_WIDTH-600, 40)
                self.pg.draw.rect(self.par.screen, text_color, rect)

            # メニューのテキスト表示
            if i == self.selectMenuItem:
                text_color = (255, 255, 255)
            else:
                if (self.par.isGameOver or self.par.userName == "") and i < 2:
                    text_color = (128, 128, 128)
                else:
                    text_color = (102, 191, 255)
            text = self.menuFont.render(item, True, text_color)
            self.par.screen.blit(text, (350, 225 + i * 50))

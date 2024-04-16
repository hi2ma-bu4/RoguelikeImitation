# coding: utf-8

from typing import Optional, cast
import os

from tkinterJSON import TkJson, TkJSONFunc
from tkinterControl.hyperlinkManager import HyperlinkManager

jsonPath = "data/organization.json"


def main() -> None:
    tkj = TkJson(jsonPath)
    tkf = TkFunc(tkj.tkc)

    tkj.loadFunctionClass(tkf)
    tkj.runConfiguration()

    tkj.drawStart()


class TkFunc(TkJSONFunc):

    urls = {
        "python_arr": [
            "https://qiita.com/maru_maruo/items/78da1545ce84014abca9",
            "https://tech.motex.co.jp/entry/2022/06/30/083000",
            "https://zenn.dev/turing_motors/articles/8b9a2c4d3e8882"
        ],
        "python_oth": [
            "https://atmarkit.itmedia.co.jp/ait/articles/2002/18/news007.html",
            "https://uxmilk.jp/39845",
            "https://blog.codecamp.jp/python-class-code",
            "https://hitoriit.blog/archives/2607",
            "https://note.nkmk.me/python-math-exp-log/#mathlog-mathlog10-mathlog2",
            "https://qiita.com/chankane/items/3909e9f2d1c5910cc60b",
            "https://qiita.com/fumitoh/items/60f181695844daf72450",
            "https://qiita.com/nicco_mirai/items/5591c1c48b1422c324c9",
            "https://qiita.com/suin/items/b15f908aaf8023a8a1fc",
            "https://qiita.com/y518gaku/items/07961c61f5efef13cccc",
            "https://scrapbox.io/kembo/Python_%E3%81%A7%E3%82%A4%E3%83%B3%E3%82%B9%E3%82%BF%E3%83%B3%E3%82%B9%E5%A4%89%E6%95%B0%E3%81%AB%E5%86%8D%E4%BB%A3%E5%85%A5%E3%81%95%E3%81%9B%E3%81%9F%E3%81%8F%E3%81%AA%E3%81%84%E6%99%82",
            "https://vaaaaaanquish.hatenablog.com/entry/2018/12/02/210647",
            "https://yiskw713.hatenablog.com/entry/2023/05/05/182048",
            "https://ytyaru.hatenablog.com/entry/2018/10/29/000000",
            "https://ytyaru.hatenablog.com/entry/2018/11/01/000000"
        ],
        "pygame_oth": [
            "https://algorithm.joho.info/programming/python/pygame-rpg-map/",
            "https://dygv.github.io/blog/post/2021/01/pygame%E3%81%AE%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E5%85%A5%E5%8A%9B/",
            "https://news.mynavi.jp/techplus/article/zeropython-90/",
            "https://www.hiro877.com/entry/2019/02/19/221123",
            "https://www.isc.meiji.ac.jp/~ri03037/ICTappli2/step06.html",
            "https://teratail.com/questions/264900"
        ],
        "rogue_map": [
            "http://rudora7.blog81.fc2.com/blog-entry-152.html",
            "http://www.rcc.ritsumei.ac.jp/2019/1201_10216/",
            "https://befool.co.jp/blog/ayumegu/unity-study-create-dungeon/",
            "https://donichi-game.com/howto-roguelike00/",
            "https://kt2525family.com/rogue-development-5/",
            "https://qiita.com/2dgames_jp/items/00ee2ad52914753bfbb7"
        ],
        "rogue_pat": [
            "https://stone-program.com/python/algorithm/a-star-introduction/"
        ],
        "rogue_col": [
            "https://frog.raindrop.jp/knowledge/archives/001607.html",
            "https://qiita.com/Hoshi_7/items/d04936883ff3eb1eed2d",
            "https://talavax.com/isinsidecircle.html#gsc.tab=0",
            "https://teratail.com/questions/359086",
            "https://www.shuei-yobiko.co.jp/labo/jh-math-byousatsu09/"
        ],
        "rogue_lay": [
            "https://elosove.com/?p=248",
            "https://whitewell.sakura.ne.jp/OpenCV/Notebook/epipolar_geometry.html",
            "https://zenn.dev/msakuta/articles/d37ab5cd6498f9"
        ],
        "rogue_lev": [
            "https://qiita.com/yuji_yasuhara/items/83a67a784d4d6152a2de"
        ],
        "rogue_eff": [
            "https://web.tohoku.ac.jp/kc_kyomu/computer_seminar1/py/textbook_ja/oop.html"
        ],
        "rogue_oth": [
            "https://qiita.com/2dgames_jp/items/1730e7c4822091c3c320"
        ],
        "tkinter_pla": [
            "https://imagingsolution.net/program/python/tkinter/widget_layout_grid/",
            "https://kuroro.blog/python/UuvLfIBIEaw98BzBZ3FJ/",
            "https://pymori.xyz/25v4qip54o/",
            "https://teratail.com/questions/312901",
            "https://watlab-blog.com/2020/07/18/tkinter-frame-pack-grid/",
            "https://www.delftstack.com/ja/howto/python-tkinter/how-to-hide-recover-and-delete-tkinter-widgets/",
            "https://www.shido.info/py/tkinter2.html"
        ],
        "tkinter_fra": [
            "https://kuroro.blog/python/vcVtKO69wSxuyhp2a8GS/",
            "https://python-work.com/tkinter-frame/",
            "https://qiita.com/junkmd/items/1623025afb56a8731f8d",
            "https://qiita.com/R1nY1x1/items/6c7139fb0967408b16c0",
            "https://teratail.com/questions/221734",
            "https://www.whitetaro-blog.com/tkinter-%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%82%B5%E3%82%A4%E3%82%BA%E3%82%92%E8%87%AA%E5%8B%95%E3%81%A7%E5%A4%89%E6%9B%B4%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/"
        ],
        "tkinter_wid": [
            "http://blog.eszett-design.com/2022/03/python-tkinter-combobox.html",
            "https://blog.teclado.com/tkinter-placeholder-entry-field/",
            "https://getech-lab.toniemon.com/tkinter-listbox/",
            "https://hhsprings.pinoko.jp/site-hhs/2020/10/%E4%B8%96%E7%95%8C%E4%B8%80%E4%BD%BF%E3%81%84%E3%81%AB%E3%81%8F%E3%81%84%E3%83%AA%E3%82%B9%E3%83%88%E3%83%9C%E3%83%83%E3%82%AF%E3%82%B9%E3%82%92%E4%BD%9C%E3%82%8C%E3%81%A1%E3%82%83%E3%81%86%E3%81%9C/",
            "https://imagingsolution.net/program/python/tkinter/radiobutton/",
            "https://tomtom-stock.com/2023/02/12/tkinter-spinbox/",
            "https://mulberrytassel.com/tkinter-start-10/",
            "https://office54.net/python/tkinter/ttk-treeview-widget",
            "https://qiita.com/nnahito/items/f85274ced64757235816",
            "https://tomtom-stock.com/2022/02/27/tkinter-progressbar/",
            "https://yuta0306.github.io/tk-entry-default",
            "https://www.delftstack.com/ja/howto/python-tkinter/how-to-change-tkinter-button-state/",
            "https://www.python-beginners.com/entry/20210517/1621242000",
            "https://www.stjun.com/entry/2019/07/15/224705",
            "https://www.whitetaro-blog.com/tkinter-%E3%82%A6%E3%82%A3%E3%82%B8%E3%82%A7%E3%83%83%E3%83%88%E3%81%AE%E5%B9%85%E3%82%92%E8%87%AA%E5%8B%95%E5%A4%89%E6%9B%B4/",
            "https://www.python-beginners.com/entry/20181229/1546061264",
            "https://www.python-beginners.com/entry/20181230/1546124400",
            "https://www.python-beginners.com/entry/20190312/1552389696",
            "https://www.python-beginners.com/entry/20190424/1556111932",
            "https://www.python-beginners.com/entry/20210517/1621242000",
            "https://www.python-beginners.com/entry/20210522/1621616008",
            "https://www.python-beginners.com/entry/20210607/1623057987",
            "https://www.python-beginners.com/entry/20210719/1626623421"
        ],
        "tkinter_msg": [
            "https://cercopes-z.com/Python/stdlib-tkinter-messagebox-py.html#options",
            "https://pg-chain.com/python-messagebox",
            "https://tomtom-stock.com/2022/02/17/tkinter-messagebox/#%E3%83%BBaskquestion"
        ],
        "tkinter_ttk": [
            "https://office54.net/python/tkinter/tkinter-ttk-difference",
            "https://python.keicode.com/advanced/tkinter-style.php",
            "https://python.keicode.com/advanced/tkinter-theme.php"
        ],
        "tkinter_var": [
            "https://daeudaeu.com/control-variable/",
            "https://python-man.club/tinter_textvariable/",
            "https://qiita.com/ab-boy_ringo/items/51242a3150365ec81106"
        ],
        "tkinter_sty": [
            "https://imagingsolution.net/program/python/tkinter/tkinter_relief_style/",
            "https://mulberrytassel.com/tkinter-start-43/",
            "https://qiita.com/ab-boy_ringo/items/cdd45230d90024b05b09"
        ],
        "tkinter_eve": [
            "https://daeudaeu.com/tkinter_event/",
            "https://memopy.hatenadiary.jp/entry/2017/06/13/214928",
            "https://office54.net/python/tkinter/window-close-catch",
            "https://tomtom-stock.com/2023/02/03/tkinter-enter-return/",
            "https://www.python-beginners.com/entry/20210729/1627491799"
        ],
        "tkinter_foc": [
            "https://nayutari.com/tkinter-focusset",
            "https://teratail.com/questions/362208"
        ],
        "tkinter_oth": [
            "https://ancient-v.hatenadiary.org/entry/20081005/1223202729",
            "https://office54.net/python/tkinter/screen-size",
            "https://pg-chain.com/python-gui-tkinter",
            "https://python.keicode.com/advanced/tkinter-widget-sizegrip.php",
            "https://qiita.com/ara_kyo/items/77d9e6d7fe9b5e3ede7e",
            "https://teratail.com/questions/233750"
        ],
        "raw_ima": [
            "https://pipoya.net/sozai/"
        ],
        "raw_fon": [
            "https://creator.levtech.jp/tips/article/66/",
            "https://github.com/adobe-fonts/source-han-code-jp/releases",
            "https://itouhiro.hatenablog.com/entry/20140917/font"
        ],
        "oth_god": [
            "https://chat.openai.com/",
            "https://translate.google.com/",
            "https://www.deepl.com/ja/translator"
        ],
        "oth_com": [
            "https://note.com/omiyayimo/n/n1436bcc9b0dd",
            "https://py-py.hatenablog.com/entry/2019/02/15/161943"
        ]
    }

    def __init__(self, tkc: TkJson.Tkc) -> None:
        self.tkc = tkc

    def showTreeData(self, event: TkJson.Tkc.tk.Event, *args) -> None:
        tree: TkJson.Tkc.ttk.Treeview = event.widget

        selectData = tree.item(tree.focus())
        if "child" in selectData["tags"]:
            text: TkJson.Tkc.tk.Text = cast(
                TkJson.Tkc.tk.Text,
                self.tkc.fra.getFrameWidgets(
                    "dataShowFrame"
                ).getWidget("dataShow"))
            text["state"] = "normal"
            text.delete("0.0", "end")
            ht = HyperlinkManager(text)

            dataPath = selectData["tags"][1]
            spPath = dataPath.split("/")[1:]
            if spPath[0] == "実行について":
                if spPath[1] == "実行ファイル":
                    text.insert("end", """実行について

実行はinit.pyを実行するとゲームが起動します。
pygameがinstallされていない場合自動installします。

pipがエラーを出力する場合は
python3 -m pip install --force-reinstall --upgrade pip
をcmdで実行して下さい。
""")
                elif spPath[1] == "起動オプション":
                    text.insert("end", """起動オプションについて

game.py実行時に引数に指定すると動作が変更されます。
引数は以下の通りです。
・load
-> ゲームを確認無しに実行
・control
-> ゲームのセーブデータを確認する用のデバッグ起動
・manual
-> このマニュアルを起動

！！注意！！
python3 game.py control
を使用する場合、vscode標準ターミナルではなく、cmd.exeを使用して下さい。

※vscode標準ターミナルでも実行出来ますが表示が崩れます。
""")
                elif spPath[1] == "起動後コマンド":
                    text.insert("end", """起動後コマンドについて

game.pyを引数無しで実行すると入力画面が表示されます。
入力画面には以下の入力で実行動作が変更されます。
・[Ctrl+Z→Enter]
-> ゲームを強制実行
・control
-> ゲームのセーブデータを確認する用のデバッグ起動
・manual
-> このマニュアルを起動

！！注意！！
controlオプション
を使用する場合、vscode標準ターミナルではなく、cmd.exeを使用して下さい。

※vscode標準ターミナルでも実行出来ますが表示が崩れます。
""")
            elif spPath[0] == "roguelike":
                if spPath[1] == "ゲーム概要":
                    text.insert("end", """ゲーム概要について

このゲームのゲームジャンルはRoguelikeです。
気分でローグライクを作りたいと思ったので作成しました。

最下層(25層)まで遊んで下さるとありがたいです。

難易度はローグライクとは思えないほどイージーにしたので、
恐らく簡単に25層まで下れると思います。

こまめなセーブを忘れず、今日もご安全に！
""")
                elif spPath[1] == "操作方法":
                    text.insert("end", """操作方法について

キー入力でゲームを操作することができます。
※マウスは使用出来ません！
W, ↑ : 上に移動
A, ← : 左に移動
S, ↓ : 下に移動
D, → : 右に移動

E     : 前方に攻撃
ESC,M : メニューを開く
Enter : 決定(選択)
""")
                elif spPath[1] == "探索範囲":
                    text.insert("end", """探索範囲について

このゲームの探索可能範囲は
25層までです。
一応100層まで生成されますが、
代わり映えしなくなります。

100層以降も実は生成されますが、
100層より下の層でセーブを実行すると、
設定ファイルが100層までしか対応していないので、
ロードの際にエラーが発生します。
一応、100層まで戻ってセーブすると問題は発生しません。
""")
            elif spPath[0] == "control":
                if spPath[1] == "プログラム概要":
                    text.insert("end", """プログラム概要について

control.pyはゲームのセーブデータを確認するための
プログラムです。

実行はgame.pyから実行して下さい。

game.pyで遊んだ人のデータが閲覧できます。
デバッグ用なので、見易さは考慮されていません。

ターミナルでの表示をするためだけに
terminalDrawライブラリは作成されました。
""")
                elif spPath[1] == "操作方法":
                    text.insert("end", """操作方法について


キー入力でターミナルを操作することができます。
※マウスは使用出来ません！
↑    : 上に選択を移動
↓    : 下に選択を移動

Tab   : 入力モード時に英字、ひらがな、カタカナを切り替える
ESC   : 1つページを戻る
Enter : 決定(確定)
""")
            elif spPath[0] == "manual":
                if spPath[1] == "プログラム概要":
                    text.insert("end", """プログラム概要について

manual.pyはプログラムの説明を確認するための
プログラムです。

実行はgame.pyからでもMANUAL.pyからでも、
実行できます。

tkinterでなにか表示をしたいが為に作成されました。
この為、README.txtはリストラされました。

tkinterをローコードで扱えるように
tkinterControlライブラリは作成されました。
また、tkinterControlライブラリの画面設定を
ノーコードで扱えるように
tkinterJSONライブラリは作成されました。
""")
                elif spPath[1] == "操作方法":
                    text.insert("end", """操作方法について

マウス操作！！単純明快！
・横の断層構造
-> クリックで選択
・ハイパーリンク
-> Ctrl+クリックでブラウザで開く
""")
            elif spPath[0] == "採点":
                if spPath[1] == "プログラム":
                    text.insert("end", """プログラムの採点について

どうやらこのプログラムは合計で442681行あるらしいので
しっかり全部読んでいただければありがたいです。
(linuxの「find . -type f |xargs cat | wc -l」使用)
非常に残念ながらvscodeの拡張機能によると、
このプログラムは7320行のようです(悲)
""")
            elif spPath[0] == "参考URL":
                if spPath[1] == "Python":
                    if spPath[2] == "並列処理":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["python_arr"])
                    elif spPath[2] == "その他":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["python_oth"])
                elif spPath[1] == "pygame":
                    if spPath[2] == "その他":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["pygame_oth"])
                elif spPath[1] == "ローグライク":
                    if spPath[2] == "マップ生成":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["rogue_map"])
                    elif spPath[2] == "経路探索":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["rogue_pat"])
                    elif spPath[2] == "当たり判定":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["rogue_col"])
                    elif spPath[2] == "レイキャスト":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["rogue_lay"])
                    elif spPath[2] == "レベル":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["rogue_lev"])
                    elif spPath[2] == "エフェクト":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["rogue_eff"])
                    elif spPath[2] == "その他":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["rogue_oth"])
                elif spPath[1] == "tkinter":
                    if spPath[2] == "設置・配置":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_pla"])
                    elif spPath[2] == "Frame":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_fra"])
                    elif spPath[2] == "Widget":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_wid"])
                    elif spPath[2] == "Messagebox":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_msg"])
                    elif spPath[2] == "tk・ttk":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_ttk"])
                    elif spPath[2] == "Variable":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_var"])
                    elif spPath[2] == "Style・Font":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_sty"])
                    elif spPath[2] == "Event":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_eve"])
                    elif spPath[2] == "Focus":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_foc"])
                    elif spPath[2] == "その他":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["tkinter_oth"])
                elif spPath[1] == "素材":
                    if spPath[2] == "Image":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["raw_ima"])
                    elif spPath[2] == "Font":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["raw_fon"])
                elif spPath[1] == "その他":
                    if spPath[2] == "神":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["oth_god"])
                    elif spPath[2] == "文字列圧縮":
                        text.insert("end", "参考URL")
                        self._addUrls(text, ht, self.urls["oth_com"])

            text["state"] = "disabled"

    def _addUrls(self, text, ht, lst) -> None:
        for l in lst:
            text.insert("end", "\n・")
            text.insert("end", *ht.add(l))


if __name__ == "__main__":
    # カレントディレクトリ修正
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    main()

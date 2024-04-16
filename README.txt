########################################
ローグライク
########################################

【お知らせ】READMEの内容はMANUAL.pyに移植されました

ゲーム　　起動は init.py   を、
マニュアル起動は MANUAL.py を起動して下さい。

########################################
☆ファイル構成

◇RoguelikeImitation/
┣◇data/
┃┣◆enemyData.json
┃┣◆floorData.json
┃┣◆imageList.csv
┃┣◆itemData.json
┃┣◆organization.json
┃┗◆userData.db
┣◇font/
┃┣◆Nasu-Regular.ttf
┃┗◆SourceHanCodeJP.ttc
┣◇image/
┃┗◆...
┣◇lib/
┃┣◆A_star.py
┃┣◆auto_pip.py
┃┣◆calc2d.py
┃┣◆compress.py
┃┣◆eastAsianWidthOverride.py
┃┣◆files.py
┃┣◆jp_input.py
┃┣◆romaji.py
┃┣◆stringLib.py
┃┣◆terminalDraw.py
┃┣◆typingAnim.py
┃┗◆windowsColor.py
┣◇LICENSE/
┃┗◆...
┣◇roguelike/
┃┣◆__init__.py
┃┣◆base.py
┃┣◆char.py
┃┣◆draw.py
┃┣◆effect.py
┃┣◆main.py
┃┣◆map.py
┃┗◆menu.py
┣◇tkinterControl/
┃┣◆__init__.py
┃┣◆hyperlinkManager.py
┃┣◆main.py
┃┣◆messagebox.py
┃┣◆variable.py
┃┗◆widgets.py
┣◇tkinterJSON/
┃┣◆__init__.py
┃┣◆func.py
┃┗◆main.py
┣◆control.py
┣◆game.py
┣◆init.py
┣◆MANUAL.py
┗◆README.txt


############################################################
☆ファイル参照構成

◆init
┣◆auto_pip
┗◆game
 ┣◆control
 ┃┣◆compress
 ┃┣◆files
 ┃┣◆stringLib
 ┃┃┗◆eastAsianWidthOverride
 ┃┣◆terminalDraw
 ┃┃┣◆romaji
 ┃┃┣◆stringLib
 ┃┃┃┗◆eastAsianWidthOverride
 ┃┃┗◆windowsColor
 ┃┣◆windowsColor
 ┃└◇userData.db
 ┣◆MANUAL.py
 ┣◆hyperlinkManager
 ┃┣◆tkinterJSON.__init__
 ┃│┗◆tkinterJSON.main
 ┃│ ┣◆func.py
 ┃│ ┗◆tkinterControl.__init__
 ┃│  ┗◆tkinterControl.main
 ┃│   ┣◆messagebox.py
 ┃│   ┗◆widgets.py
 ┃│    ┣◆calc2d.py
 ┃│    ┣◆stringLib.py
 ┃│    ┃┗◆eastAsianWidthOverride
 ┃│    ┗◆variable.py
 ┃│     ┗◆calc2d.py
 ┃└◇organization.json
 ┣◆roguelike.__init__
 ┃┗◆roguelike.main
 ┃ ┣◆draw
 ┃ ┃┣◆base
 ┃ ┃┃┣◆char
 ┃ ┃┃┃┣◆A_star
 ┃ ┃┃┃┗◆calc2d
 ┃ ┃┃┣◆compress
 ┃ ┃┃┣◆effect
 ┃ ┃┃┃┣◆calc2d
 ┃ ┃┃┃┗◆typingAnim
 ┃ ┃┃┃ ┗◆romaji
 ┃ ┃┃┣◆files
 ┃ ┃┃┣◆map
 ┃ ┃┃┃┣◆A_star
 ┃ ┃┃┃┗◆calc2d
 ┃ ┃┃┣◆stringLib
 ┃ ┃┃┃┗◆eastAsianWidthOverride
 ┃ ┃┃├◇itemData.json
 ┃ ┃┃│├◇enemyData.json
 ┃ ┃┃││├◇floorData.json
 ┃ ┃┃│││└◇imageList.csv
 ┃ ┃┃││└◇imageList.csv
 ┃ ┃┃│└◇imageList.csv
 ┃ ┃┃└◇userData.db
 ┃ ┃┗◆calc2d
 ┃ ┗◆menu
 ┃  ┣◆eastAsianWidthOverride
 ┃  ┗◆jp_input
 ┗◆windowsColor



############################################################
☆使用import一覧

・abc
    char
    func
・base64
    compress
・bz2
    compress
・copy
    base
    calc2d
    compress
    map
・csv
    files
・dataclasses
    base
    calc2d
    effect
    windowsColor
・importlib
    auto_pip
・inspect
    func
・json
    auto_pip
    char
    compress
    control
    files
    tkinterJSON.main
・math
    calc2d
    char
    map
    terminalDraw
・os
    control
    game
    MANUAL
    terminalDraw
・pip
    auto_pip
・platform
    tkinterControl.main
・pygame(非標準)
    base
    game
    menu
・random
    base
    char
    effect
    map
    roguelike.main
・re
    compress
    eastAsianWidthOverride
    romaji
    terminalDraw
    typingAnim
・readchar(非標準)
    control
・shutil
    terminalDraw
・sqlite3
    files
・subprocess
    auto_pip
・sys
    game
・time
    terminalDraw
・tkinter
    messagebox
    variable
    widgets
・typing
    auto_pip
    base
    calc2d
    char
    compress
    control
    draw
    effect
    files
    func
    jp_input
    map
    menu
    messagebox
    roguelike.main
    romaji
    stringLib
    terminalDraw
    tkinterControl.main
    tkinterJSON.main
    typingAnim
    variable
    widgets
    windowsColor
・unicodedata
    eastAsianWidthOverride
・webbrowser
    hyperlinkManager
・zlib
    compress


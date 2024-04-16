# coding: utf-8
"""
ひらがな、カタカナ、ローマ字変換ライブラリ
"""

from typing import final
from re import compile, escape


class Romaji:
    """
    ローマ字変換
    """

    _kata = {
        'ア': 'あ', 'イ': 'い', 'ウ': 'う', 'エ': 'え', 'オ': 'お',
        'カ': 'か', 'キ': 'き', 'ク': 'く', 'ケ': 'け', 'コ': 'こ',
        'サ': 'さ', 'シ': 'し', 'ス': 'す', 'セ': 'せ', 'ソ': 'そ',
        'タ': 'た', 'チ': 'ち', 'ツ': 'つ', 'テ': 'て', 'ト': 'と',
        'ナ': 'な', 'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の',
        'ハ': 'は', 'ヒ': 'ひ', 'フ': 'ふ', 'ヘ': 'へ', 'ホ': 'ほ',
        'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も',
        'ヤ': 'や', 'ユ': 'ゆ', 'ヨ': 'よ', 'ラ': 'ら', 'リ': 'り',
        'ル': 'る', 'レ': 'れ', 'ロ': 'ろ', 'ワ': 'わ', 'ヲ': 'を',
        'ン': 'ん',

        'ガ': 'が', 'ギ': 'ぎ', 'グ': 'ぐ', 'ゲ': 'げ', 'ゴ': 'ご',
        'ザ': 'ざ', 'ジ': 'じ', 'ズ': 'ず', 'ゼ': 'ぜ', 'ゾ': 'ぞ',
        'ダ': 'だ', 'ヂ': 'ぢ', 'ヅ': 'づ', 'デ': 'で', 'ド': 'ど',
        'バ': 'ば', 'ビ': 'び', 'ブ': 'ぶ', 'ベ': 'べ', 'ボ': 'ぼ',
        'パ': 'ぱ', 'ピ': 'ぴ', 'プ': 'ぷ', 'ペ': 'ぺ', 'ポ': 'ぽ',

        'ァ': 'ぁ', 'ィ': 'ぃ', 'ゥ': 'ぅ', 'ェ': 'ぇ', 'ォ': 'ぉ',
        'ャ': 'ゃ', 'ュ': 'ゅ', 'ョ': 'ょ',
        'ヴ': 'ヴ', 'ッ': 'っ', 'ヮ': 'ゎ', 'ヰ': 'ゐ', 'ヱ': 'ゑ',
    }

    _master = {
        'a': 'ア', 'i': 'イ', 'u': 'ウ', 'e': 'エ', 'o': 'オ',
        'ka': 'カ', 'ki': 'キ', 'ku': 'ク', 'ke': 'ケ', 'ko': 'コ',
        'sa': 'サ', 'shi': 'シ', 'su': 'ス', 'se': 'セ', 'so': 'ソ',
        'ta': 'タ', 'chi': 'チ', 'tu': 'ツ', 'te': 'テ', 'to': 'ト',
        'na': 'ナ', 'ni': 'ニ', 'nu': 'ヌ', 'ne': 'ネ', 'no': 'ノ',
        'ha': 'ハ', 'hi': 'ヒ', 'fu': 'フ', 'he': 'ヘ', 'ho': 'ホ',
        'ma': 'マ', 'mi': 'ミ', 'mu': 'ム', 'me': 'メ', 'mo': 'モ',
        'ya': 'ヤ', 'yu': 'ユ', 'yo': 'ヨ',
        'ra': 'ラ', 'ri': 'リ', 'ru': 'ル', 're': 'レ', 'ro': 'ロ',
        'wa': 'ワ', 'wo': 'ヲ', 'nn': 'ン', 'vu': 'ヴ',
        'ga': 'ガ', 'gi': 'ギ', 'gu': 'グ', 'ge': 'ゲ', 'go': 'ゴ',
        'za': 'ザ', 'ji': 'ジ', 'zu': 'ズ', 'ze': 'ゼ', 'zo': 'ゾ',
        'da': 'ダ', 'di': 'ヂ', 'du': 'ヅ', 'de': 'デ', 'do': 'ド',
        'ba': 'バ', 'bi': 'ビ', 'bu': 'ブ', 'be': 'ベ', 'bo': 'ボ',
        'pa': 'パ', 'pi': 'ピ', 'pu': 'プ', 'pe': 'ペ', 'po': 'ポ',

        'kya': 'キャ', 'kyi': 'キィ', 'kyu': 'キュ', 'kye': 'キェ', 'kyo': 'キョ',
        'gya': 'ギャ', 'gyi': 'ギィ', 'gyu': 'ギュ', 'gye': 'ギェ', 'gyo': 'ギョ',
        'sha': 'シャ',                'shu': 'シュ', 'she': 'シェ', 'sho': 'ショ',
        'ja': 'ジャ',                 'ju': 'ジュ', 'je': 'ジェ', 'jo': 'ジョ',
        'cha': 'チャ',                'chu': 'チュ', 'che': 'チェ', 'cho': 'チョ',
        'dya': 'ヂャ', 'dyi': 'ヂィ', 'dyu': 'ヂュ', 'dhe': 'デェ', 'dyo': 'ヂョ',
        'nya': 'ニャ', 'nyi': 'ニィ', 'nyu': 'ニュ', 'nye': 'ニェ', 'nyo': 'ニョ',
        'hya': 'ヒャ', 'hyi': 'ヒィ', 'hyu': 'ヒュ', 'hye': 'ヒェ', 'hyo': 'ヒョ',
        'bya': 'ビャ', 'byi': 'ビィ', 'byu': 'ビュ', 'bye': 'ビェ', 'byo': 'ビョ',
        'pya': 'ピャ', 'pyi': 'ピィ', 'pyu': 'ピュ', 'pye': 'ピェ', 'pyo': 'ピョ',
        'mya': 'ミャ', 'myi': 'ミィ', 'myu': 'ミュ', 'mye': 'ミェ', 'myo': 'ミョ',
        'rya': 'リャ', 'ryi': 'リィ', 'ryu': 'リュ', 'rye': 'リェ', 'ryo': 'リョ',
        'fa': 'ファ', 'fi': 'フィ',               'fe': 'フェ', 'fo': 'フォ',
        'wi': 'ウィ', 'we': 'ウェ',
        'va': 'ヴァ', 'vi': 'ヴィ', 've': 'ヴェ', 'vo': 'ヴォ',

        'kwa': 'クァ', 'kwi': 'クィ', 'kwu': 'クゥ', 'kwe': 'クェ', 'kwo': 'クォ',
        'kha': 'クァ', 'khi': 'クィ', 'khu': 'クゥ', 'khe': 'クェ', 'kho': 'クォ',
        'gwa': 'グァ', 'gwi': 'グィ', 'gwu': 'グゥ', 'gwe': 'グェ', 'gwo': 'グォ',
        'gha': 'グァ', 'ghi': 'グィ', 'ghu': 'グゥ', 'ghe': 'グェ', 'gho': 'グォ',
        'swa': 'スァ', 'swi': 'スィ', 'swu': 'スゥ', 'swe': 'スェ', 'swo': 'スォ',
        'swa': 'スァ', 'swi': 'スィ', 'swu': 'スゥ', 'swe': 'スェ', 'swo': 'スォ',
        'zwa': 'ズヮ', 'zwi': 'ズィ', 'zwu': 'ズゥ', 'zwe': 'ズェ', 'zwo': 'ズォ',
        'twa': 'トァ', 'twi': 'トィ', 'twu': 'トゥ', 'twe': 'トェ', 'two': 'トォ',
        'dwa': 'ドァ', 'dwi': 'ドィ', 'dwu': 'ドゥ', 'dwe': 'ドェ', 'dwo': 'ドォ',
        'mwa': 'ムヮ', 'mwi': 'ムィ', 'mwu': 'ムゥ', 'mwe': 'ムェ', 'mwo': 'ムォ',
        'bwa': 'ビヮ', 'bwi': 'ビィ', 'bwu': 'ビゥ', 'bwe': 'ビェ', 'bwo': 'ビォ',
        'pwa': 'プヮ', 'pwi': 'プィ', 'pwu': 'プゥ', 'pwe': 'プェ', 'pwo': 'プォ',
        'phi': 'プィ', 'phu': 'プゥ', 'phe': 'プェ', 'pho': 'フォ',
    }

    _romaji_assist = {
        'si': 'シ', 'ti': 'チ', 'hu': 'フ', 'zi': 'ジ',
        'sya': 'シャ', 'syu': 'シュ', 'syo': 'ショ',
        'tya': 'チャ', 'tyu': 'チュ', 'tyo': 'チョ',
        'cya': 'チャ', 'cyu': 'チュ', 'cyo': 'チョ',
        'jya': 'ジャ', 'jyu': 'ジュ', 'jyo': 'ジョ', 'pha': 'ファ',
        'qa': 'クァ', 'qi': 'クィ', 'qu': 'クゥ', 'qe': 'クェ', 'qo': 'クォ',

        'ca': 'カ', 'ci': 'シ', 'cu': 'ク', 'ce': 'セ', 'co': 'コ',
        'la': 'ァ', 'li': 'ィ', 'lu': 'ゥ', 'le': 'ェ', 'lo': 'ォ',
        'lya': 'ャ', 'lyu': 'ュ', 'lyo': 'ョ', 'ltu': 'ッ', 'lwa': 'ヮ',
        'xa': 'ァ', 'xi': 'ィ', 'xu': 'ゥ', 'xe': 'ェ', 'xo': 'ォ',
        'xya': 'ャ', 'xyu': 'ュ', 'xyo': 'ョ', 'xtu': 'ッ', 'xwa': 'ヮ',

        '-': 'ー',
        # 'la': 'ラ', 'li': 'リ', 'lu': 'ル', 'le': 'レ', 'lo': 'ロ',

        # 'mb': 'ム', 'py': 'パイ', 'tho': 'ソ', 'thy': 'ティ', 'oh': 'オウ',
        # 'by': 'ビィ', 'cy': 'シィ', 'dy': 'ディ', 'fy': 'フィ', 'gy': 'ジィ',
        # 'hy': 'シー', 'ly': 'リィ', 'ny': 'ニィ', 'my': 'ミィ', 'ry': 'リィ',
        # 'ty': 'ティ', 'vy': 'ヴィ', 'zy': 'ジィ',

        # 'b': 'ブ', 'c': 'ク', 'd': 'ド', 'f': 'フ', 'g': 'グ', 'h': 'フ', 'j': 'ジ',
        # 'k': 'ク', 'l': 'ル', 'm': 'ム', 'p': 'プ', 'q': 'ク', 'r': 'ル', 's': 'ス',
        # 't': 'ト', 'v': 'ヴ', 'w': 'ゥ', 'x': 'クス', 'y': 'ィ', 'z': 'ズ',
    }

    _kana_assist = {'a': 'ァ', 'i': 'ィ', 'u': 'ゥ', 'e': 'ェ', 'o': 'ォ', }

    @final
    @classmethod
    def _Romaji2Init(cls) -> None:
        """
        初期化
        """

        # ひらがな
        cls._hira = dict([(v, k) for k, v in cls._kata.items()])

        cls._re_hira2kata = compile("|".join(map(escape, cls._hira)))
        cls._re_kata2hira = compile("|".join(map(escape, cls._kata)))

        # カタカナ

        cls._romaji_dict = {}
        for tbl in cls._master, cls._romaji_assist:
            for k, v in tbl.items():
                cls._romaji_dict[k] = v

        romaji_keys = list(cls._romaji_dict.keys())
        romaji_keys.sort(key=lambda x: len(x), reverse=True)

        cls._re_roma2kana = compile("|".join(map(escape, romaji_keys)))
        # m の後ろにバ行、パ行のときは "ン" と変換
        cls._rx_mba = compile(r"m(b|p)([aiueo])")
        # 子音が続く時は "ッ" と変換
        cls._rx_xtu_k = compile(r"([bcdfghjklmpqrstvwxyz])\1")
        # nが単体で残ったら "ン" と変換
        cls._rx_nn_k = compile(r"n(?!$)")

        # ローマ字

        cls._kana_dict = {}
        for tbl in cls._master, cls._kana_assist:
            for k, v in tbl.items():
                cls._kana_dict[v] = k

        kana_keys = list(cls._kana_dict.keys())
        kana_keys.sort(key=lambda x: len(x), reverse=True)

        cls._re_kana2roma = compile("|".join(map(escape, kana_keys)))
        # 小さい "ッ" は直後の文字を２回に変換
        cls._rx_xtu_r = compile(r"ッ([a-z])")
        # 最後の小さい "ッ" は消去(?)
        cls._rx_ltu = compile(r"ッ")
        # n の後ろが バ行、パ行 なら m に修正
        cls._rx_n = compile(r"n(b|p)([aiueo])")
        # nn の後ろが 子音なら n に修正
        cls._rx_nn_r = compile(r"nn([cdfghjklmqrstvwxyz])")
        # 母音繰り返しを消去
        cls._rx_oo = compile(r"([aiueo])\1")

    @classmethod
    def Hira2Kata(cls, text: str) -> str:
        """
        ひらがな → カタカナ
        """
        return cls._re_hira2kata.sub(lambda x: cls._hira[x.group(0)], text)

    @classmethod
    def Kata2Hira(cls, text: str) -> str:
        """
        カタカナ → ひらがな
        """
        return cls._re_kata2hira.sub(lambda x: cls._kata[x.group(0)], text)

    @classmethod
    def Romaji2Kata(cls, text: str) -> str:
        """
        ローマ字 → カタカナ
        """
        result = text.lower()
        result = cls._rx_mba.sub(r"ン\1\2", result)
        result = cls._rx_xtu_k.sub(r"ッ\1", result)
        result = cls._re_roma2kana.sub(
            lambda x: cls._romaji_dict[x.group(0)], result)
        return cls._rx_nn_k.sub("ン", result)

    @classmethod
    def Romaji2Hira(cls, text: str) -> str:
        """
        ローマ字 → ひらがな
        """
        result = cls.Romaji2Kata(text)
        return cls.Kata2Hira(result)

    @classmethod
    def kana2Romaji(cls, text: str) -> str:
        """
        ひらがな(カタカナ) → ローマ字
        """
        result = cls.Hira2Kata(text)
        result = cls._re_kana2roma.sub(
            lambda x: cls._kana_dict[x.group(0)], result)
        result = cls._rx_xtu_r.sub(r"\1\1", result)
        result = cls._rx_ltu.sub(r"ltu", result)
        result = cls._rx_n.sub(r"m\1\2", result)
        result = cls._rx_nn_r.sub(r"n\1", result)
        return result  # cls._rx_oo.sub(r"\1", result)


Romaji._Romaji2Init()

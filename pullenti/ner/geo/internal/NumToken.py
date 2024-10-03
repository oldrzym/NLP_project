﻿# SDK Pullenti Lingvo, version 4.22, february 2024. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken

class NumToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.value = None;
        self.alt_value = None;
        self.has_prefix = False
        self.has_spec_word = False
        self.is_cadaster_number = False
        self.template = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.has_prefix): 
            print("№ ", end="", file=res)
        print(self.value, end="", file=res)
        if (self.alt_value is not None): 
            print(" / {0}".format(self.alt_value), end="", file=res, flush=True)
        if (self.is_cadaster_number): 
            print(" cadaster", end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_parse(t : 'Token', typ : 'GeoTokenType') -> 'NumToken':
        if (t is None): 
            return None
        if (t.is_value("ОТДЕЛЕНИЕ", None) and (t.whitespaces_after_count < 3)): 
            next0__ = NumToken.try_parse(t.next0_, typ)
            if (next0__ is not None): 
                next0__.begin_token = t
                next0__.has_prefix = True
                next0__.has_spec_word = True
                return next0__
        tt = MiscHelper.check_number_prefix(t)
        if (tt is None and (isinstance(t, TextToken)) and t.term.startswith("КАД")): 
            tt1 = t.next0_
            if (tt1 is not None and tt1.is_char('.')): 
                tt1 = tt1.next0_
            tt = MiscHelper.check_number_prefix(tt1)
            if (tt is None): 
                tt = tt1
        if (tt is not None): 
            has_reest = False
            ttt = tt
            first_pass3832 = True
            while True:
                if first_pass3832: first_pass3832 = False
                else: ttt = ttt.next0_
                if (not (ttt is not None)): break
                if (((ttt.is_char_of(":") or ttt.is_hiphen)) and (isinstance(ttt.next0_, NumberToken))): 
                    continue
                if (has_reest): 
                    if (isinstance(ttt.get_referent(), GeoReferent)): 
                        continue
                ter = TerrItemToken.try_parse(ttt, None, None)
                if (ter is not None and ((ter.onto_item is not None or ter.termin_item is not None))): 
                    ttt = ter.end_token
                    continue
                npt = NounPhraseHelper.try_parse(ttt, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
                if (npt is not None): 
                    if (npt.end_token.is_value("ЗАПИСЬ", None) or npt.end_token.is_value("РЕЕСТР", None)): 
                        ttt = npt.end_token
                        has_reest = True
                        continue
                    break
                if (not (isinstance(ttt, NumberToken))): 
                    break
                res = NumToken._new1441(t, ttt, True, "n")
                res.value = ttt.value
                res.__correct(typ)
                return res
        if (tt is None): 
            tt = t
        if (isinstance(tt, NumberToken)): 
            res = NumToken._new1441(t, tt, tt != t, "n")
            res.value = tt.value
            res.__correct(typ)
            return res
        if ((isinstance(tt, ReferentToken)) and (isinstance(tt.get_referent(), UriReferent))): 
            res = NumToken._new1443(t, tt, tt != t)
            res.value = tt.get_referent().get_string_value("VALUE")
            sh = tt.get_referent().get_string_value("SCHEME")
            if (sh == "КАДАСТР"): 
                res.is_cadaster_number = True
            return res
        if ((isinstance(tt, TextToken)) and not t.is_value("C", None)): 
            nt = NumberHelper.try_parse_roman(tt)
            if (nt is not None and nt.value != "100"): 
                res = NumToken._new1441(t, nt.end_token, tt != t, "l")
                res.value = nt.value
                res.__correct(typ)
                return res
        if (BracketHelper.is_bracket(t, True)): 
            next0__ = NumToken.try_parse(t.next0_, typ)
            if (next0__ is not None): 
                if (next0__.end_token.next0_ is not None and BracketHelper.is_bracket(next0__.end_token.next0_, True)): 
                    next0__.begin_token = t
                    next0__.end_token = next0__.end_token.next0_
                    return next0__
        if (((isinstance(t, TextToken)) and t.length_char == 1 and t.chars.is_letter) and typ == GeoTokenType.STRONG): 
            res = NumToken._new1441(t, t, tt != t, "c")
            ch = LanguageHelper.get_cyr_for_lat(t.term[0])
            if ((ord(ch)) == 0): 
                ch = t.term[0]
            res.value = "{0}".format(ch)
            res.__correct(typ)
            return res
        if (((isinstance(t, TextToken)) and t.length_char == 2 and t.chars.is_all_upper) and t.chars.is_letter and typ == GeoTokenType.STRONG): 
            res = NumToken._new1441(t, t, tt != t, "c")
            res.value = t.term
            res.__correct(typ)
            if (res.end_token != t): 
                return res
        return None
    
    def __correct(self, typ : 'GeoTokenType') -> None:
        nt = Utils.asObjectOrNull(self.end_token, NumberToken)
        if ((nt is not None and (isinstance(nt.end_token, TextToken)) and nt.end_token.term == "Е") and nt.end_token.previous == nt.begin_token and not nt.end_token.is_whitespace_before): 
            self.value += "Е"
        t = self.end_token.next0_
        if (t is None or t.whitespaces_before_count > 1): 
            return
        if (t.is_value("ОТДЕЛЕНИЕ", None)): 
            self.end_token = t
            t = t.next0_
            self.has_prefix = True
            self.has_spec_word = True
            if (t is None or t.whitespaces_before_count > 1): 
                return
        if (t.is_value2("ОЧЕРЕДЬ", "ОСВОЕНИЕ")): 
            self.end_token = t.next0_
            t = t.next0_.next0_
            self.has_prefix = True
            self.has_spec_word = True
            if (t is None or t.whitespaces_before_count > 1): 
                return
        if (t.is_hiphen and t.next0_ is not None and ((t.next0_.is_value("Я", None) or t.next0_.is_value("ТИ", None) or t.next0_.is_value("ГО", None)))): 
            self.end_token = t.next0_
            t = self.end_token.next0_
            if (t is None or t.whitespaces_before_count > 1): 
                return
        if ((isinstance(self.end_token, NumberToken)) and self.end_token.length_char == 2): 
            tt = t
            if (tt.is_char_of(".:") and tt.next0_ is not None): 
                tt = tt.next0_
            if (((isinstance(tt, NumberToken)) and tt.typ == NumberSpellingType.DIGIT and tt.length_char == 2) and tt.next0_ is not None): 
                ttt = tt.next0_
                if (ttt.is_char_of(".:") and ttt.next0_ is not None): 
                    ttt = ttt.next0_
                is_kv = False
                tt0 = self.begin_token.previous
                while tt0 is not None: 
                    if (tt0.is_value("КВАРТАЛ", None) or tt0.is_value("КВ", None)): 
                        is_kv = True
                        break
                    elif (tt0.length_char > 1 or not (isinstance(tt0, TextToken))): 
                        break
                    tt0 = tt0.previous
                if ((isinstance(ttt, NumberToken)) and ((ttt.length_char == 6 or ttt.length_char == 7)) and ttt.typ == NumberSpellingType.DIGIT): 
                    self.value = "{0}:{1}:{2}".format(self.value, tt.get_source_text(), ttt.get_source_text())
                    self.end_token = ttt
                    ttt = ttt.next0_
                    self.is_cadaster_number = True
                    if (ttt is not None and ttt.is_char_of(".:") and (isinstance(ttt.next0_, NumberToken))): 
                        self.value = "{0}:{1}".format(self.value, ttt.next0_.get_source_text())
                        self.end_token = ttt.next0_
                elif ((isinstance(ttt, NumberToken)) and is_kv): 
                    tmp = io.StringIO()
                    print("{0}:{1}:{2}".format(self.value, tt.get_source_text(), ttt.get_source_text()), end="", file=tmp, flush=True)
                    t1 = ttt
                    ttt = ttt.next0_
                    first_pass3833 = True
                    while True:
                        if first_pass3833: first_pass3833 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (isinstance(ttt, NumberToken)): 
                            print(ttt.get_source_text(), end="", file=tmp)
                            t1 = ttt
                            continue
                        if (ttt.is_char(':') and (isinstance(ttt.next0_, NumberToken))): 
                            print(":{0}".format(ttt.next0_.get_source_text()), end="", file=tmp, flush=True)
                            t1 = ttt.next0_
                            break
                        break
                    if (tmp.tell() >= 7): 
                        self.value = Utils.toStringStringIO(tmp)
                        self.end_token = t1
                        self.is_cadaster_number = True
        if (self.is_cadaster_number): 
            return
        t = self.end_token.next0_
        first_pass3834 = True
        while True:
            if first_pass3834: first_pass3834 = False
            else: t = t.next0_
            if (not (t is not None)): break
            is_drob = False
            is_hiph = False
            br_after = False
            if (t.is_hiphen and not t.is_whitespace_after and t.next0_ is not None): 
                is_hiph = True
                t = t.next0_
            elif (t.is_char_of("\\/") and not t.is_whitespace_after and t.next0_ is not None): 
                is_drob = True
                t = t.next0_
            elif (t.is_value("ДРОБЬ", None) and t.next0_ is not None): 
                is_drob = True
                t = t.next0_
            elif (BracketHelper.is_bracket(t, False)): 
                if ((((isinstance(t.next0_, NumberToken)) or (((isinstance(t.next0_, TextToken)) and t.next0_.chars.is_letter and t.next0_.length_char == 1)))) and t.next0_.next0_ is not None and BracketHelper.is_bracket(t.next0_.next0_, False)): 
                    t = t.next0_
                    br_after = True
                else: 
                    lat0 = NumberHelper.try_parse_roman(t.next0_)
                    if (lat0 is not None and lat0.end_token.next0_ is not None and lat0.end_token.next0_.is_char(')')): 
                        t = t.next0_
                        br_after = True
            templ0 = self.template[len(self.template) - 1]
            if (isinstance(t, NumberToken)): 
                num = Utils.asObjectOrNull(t, NumberToken)
                if (num.typ != NumberSpellingType.DIGIT): 
                    break
                if (is_hiph and ((templ0 != 'n' or typ == GeoTokenType.ORG))): 
                    pass
                elif (is_drob or br_after): 
                    pass
                elif (not t.is_whitespace_before): 
                    pass
                else: 
                    break
                val = num.value
                if (not num.morph.class0_.is_adjective): 
                    val = num.get_source_text()
                self.value = "{0}{1}{2}".format(self.value, ("/" if is_drob or br_after else ("" if templ0 == 'c' else "-")), val)
                self.template += "n"
                if (br_after): 
                    t = t.next0_
                self.end_token = t
                continue
            if (isinstance(t, TextToken)): 
                nt = NumberHelper.try_parse_roman(t)
                if (nt is not None and nt.value != "100"): 
                    self.value = "{0}{1}{2}".format(self.value, ('/' if is_drob or br_after else '-'), nt.value)
                    self.template += "l"
                    t = nt.end_token
                    if (br_after): 
                        t = t.next0_
                    self.end_token = t
                    continue
            if (((isinstance(t, TextToken)) and t.length_char == 1 and t.chars.is_letter) and ((not t.is_whitespace_before or t.is_newline_after or ((t.next0_ is not None and (isinstance(t.next0_.next0_, NumberToken)) and ((t.next0_.is_comma or t.next0_.is_char_of("\\/")))))))): 
                if (templ0 == 'n'): 
                    pass
                elif (templ0 == 'l' and ((is_hiph or is_drob))): 
                    pass
                else: 
                    break
                ch = LanguageHelper.get_cyr_for_lat(t.term[0])
                if ((ord(ch)) == 0): 
                    ch = t.term[0]
                self.value = "{0}{1}".format(self.value, ch)
                self.template += "c"
                if (br_after): 
                    t = t.next0_
                self.end_token = t
                continue
            break
    
    @staticmethod
    def _correct_char(v : 'char') -> 'char':
        if (v == 'A' or v == 'А'): 
            return 'А'
        if (v == 'Б' or v == 'Г'): 
            return v
        if (v == 'B' or v == 'В'): 
            return 'В'
        if (v == 'C' or v == 'С'): 
            return 'С'
        if (v == 'D' or v == 'Д'): 
            return 'Д'
        if (v == 'E' or v == 'Е'): 
            return 'Е'
        if (v == 'H' or v == 'Н'): 
            return 'Н'
        if (v == 'K' or v == 'К'): 
            return 'К'
        return chr(0)
    
    @staticmethod
    def __correct_char_token(t : 'Token') -> str:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        v = tt.term
        if (len(v) == 1): 
            corr = NumToken._correct_char(v[0])
            if (corr != (chr(0))): 
                return "{0}".format(corr)
            if (t.chars.is_cyrillic_letter): 
                return v
        if (len(v) == 2): 
            if (t.chars.is_cyrillic_letter): 
                return v
            corr = NumToken._correct_char(v[0])
            corr2 = NumToken._correct_char(v[1])
            if (corr != (chr(0)) and corr2 != (chr(0))): 
                return "{0}{1}".format(corr, corr2)
        return None
    
    @staticmethod
    def _new1441(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : str) -> 'NumToken':
        res = NumToken(_arg1, _arg2)
        res.has_prefix = _arg3
        res.template = _arg4
        return res
    
    @staticmethod
    def _new1443(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NumToken':
        res = NumToken(_arg1, _arg2)
        res.has_prefix = _arg3
        return res
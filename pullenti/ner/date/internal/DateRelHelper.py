# SDK Pullenti Lingvo, version 4.22, february 2024. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import operator
import datetime
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.date.internal.DateExToken import DateExToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent

class DateRelHelper:
    
    @staticmethod
    def create_referents(et : 'DateExToken') -> typing.List['ReferentToken']:
        if (not et.is_diap or len(et.items_to) == 0): 
            li = DateRelHelper.__create_refs(et.items_from)
            if (li is None or len(li) == 0): 
                return None
            return li
        li_fr = DateRelHelper.__create_refs(et.items_from)
        li_to = DateRelHelper.__create_refs(et.items_to)
        ra = DateRangeReferent()
        if (len(li_fr) > 0): 
            ra.date_from = Utils.asObjectOrNull(li_fr[0].tag, DateReferent)
        if (len(li_to) > 0): 
            ra.date_to = Utils.asObjectOrNull(li_to[0].tag, DateReferent)
        res = list()
        res.extend(li_fr)
        res.extend(li_to)
        res.append(ReferentToken(ra, et.begin_token, et.end_token))
        if (len(res) == 0): 
            return None
        res[0].tag = (ra)
        return res
    
    @staticmethod
    def __create_refs(its : typing.List['DateExItemToken']) -> typing.List['ReferentToken']:
        res = list()
        own = None
        i = 0
        first_pass3738 = True
        while True:
            if first_pass3738: first_pass3738 = False
            else: i += 1
            if (not (i < len(its))): break
            it = its[i]
            d = DateReferent()
            if (it.is_value_relate): 
                d.is_relative = True
            if (own is not None): 
                d.higher = own
            if (it.typ == DateExToken.DateExItemTokenType.DAY): 
                d.day = it.value
                if (it.is_last and ((it.value == 0 or it.value == -1)) and i > 0): 
                    it0 = its[i - 1]
                    day = 0
                    if (it0.typ == DateExToken.DateExItemTokenType.MONTH and not it0.is_value_relate): 
                        m = d.month
                        if (((m == 1 or m == 3 or m == 5) or m == 7 or m == 8) or m == 10 or m == 12): 
                            day = 31
                        elif (m == 2): 
                            day = 28
                        elif (m > 0): 
                            day = 30
                    elif (it0.typ == DateExToken.DateExItemTokenType.QUARTAL and not it0.is_value_relate): 
                        m = 1 + (((it0.value - 1)) * 4)
                        dm = DateReferent()
                        dm.month = m
                        if (own is not None): 
                            dm.higher = own
                        res.append(ReferentToken(dm, it.begin_token, it.end_token))
                        d.higher = dm
                        own = d.higher
                        if (((m == 1 or m == 3 or m == 5) or m == 7 or m == 8) or m == 10 or m == 12): 
                            day = 31
                        elif (m == 2): 
                            day = 28
                        elif (m > 0): 
                            day = 30
                    elif (it0.typ == DateExToken.DateExItemTokenType.YEAR): 
                        dm = DateReferent()
                        dm.month = 12
                        if (own is not None): 
                            dm.higher = own
                        res.append(ReferentToken(dm, it.begin_token, it.end_token))
                        d.higher = dm
                        own = d.higher
                        day = 31
                    elif (it0.typ == DateExToken.DateExItemTokenType.CENTURY): 
                        dy = DateReferent()
                        dy.year = 99
                        dy.is_relative = True
                        if (own is not None): 
                            dy.higher = own
                        res.append(ReferentToken(dy, it.begin_token, it.end_token))
                        own = dy
                        dm = DateReferent()
                        dm.month = 12
                        dm.higher = own
                        res.append(ReferentToken(dm, it.begin_token, it.end_token))
                        d.higher = dm
                        own = d.higher
                        day = 31
                    if ((day + it.value) > 0): 
                        d.is_relative = False
                        d.day = day + it.value
            elif (it.typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                d.day_of_week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.HOUR): 
                d.hour = it.value
                if (((i + 1) < len(its)) and its[i + 1].typ == DateExToken.DateExItemTokenType.MINUTE and not its[i + 1].is_value_relate): 
                    d.minute = its[i + 1].value
                    i += 1
            elif (it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                d.minute = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.MONTH): 
                d.month = it.value
                if (it.is_last and ((it.value == 0 or it.value == -1)) and i > 0): 
                    it0 = its[i - 1]
                    m = 0
                    if (it0.typ == DateExToken.DateExItemTokenType.QUARTAL and not it0.is_value_relate): 
                        m = (1 + (((it0.value - 1)) * 4) + it.value)
                    elif (it0.typ == DateExToken.DateExItemTokenType.YEAR or it0.typ == DateExToken.DateExItemTokenType.DECADE or it0.typ == DateExToken.DateExItemTokenType.CENTURY): 
                        m = (12 + it.value)
                    if (m > 0): 
                        d.is_relative = False
                        d.month = m
            elif (it.typ == DateExToken.DateExItemTokenType.QUARTAL): 
                d.quartal = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.SEASON): 
                d.season = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.WEEK): 
                d.week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.HALFYEAR): 
                d.halfyear = (2 if it.is_last else it.value)
            elif (it.typ == DateExToken.DateExItemTokenType.YEAR): 
                d.year = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.CENTURY): 
                d.century = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.DECADE): 
                d.decade = it.value
            else: 
                continue
            res.append(ReferentToken(d, it.begin_token, it.end_token))
            own = d
            it.src = d
        if (len(res) > 0): 
            res[0].tag = (own)
        return res
    
    @staticmethod
    def __create_date_ex(dr : 'DateReferent') -> typing.List['DateExItemToken']:
        res = list()
        while dr is not None: 
            n = 0
            for s in dr.slots: 
                it = DateExToken.DateExItemToken._new850(None, None, DateExToken.DateExItemTokenType.UNDEFINED)
                if (dr.get_string_value(DateReferent.ATTR_ISRELATIVE) == "true"): 
                    it.is_value_relate = True
                if (s.type_name == DateReferent.ATTR_YEAR): 
                    it.typ = DateExToken.DateExItemTokenType.YEAR
                    wrapn851 = RefOutArgWrapper(0)
                    inoutres852 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn851)
                    n = wrapn851.value
                    if (inoutres852): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DECADE): 
                    it.typ = DateExToken.DateExItemTokenType.DECADE
                    wrapn853 = RefOutArgWrapper(0)
                    inoutres854 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn853)
                    n = wrapn853.value
                    if (inoutres854): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_CENTURY): 
                    it.typ = DateExToken.DateExItemTokenType.CENTURY
                    wrapn855 = RefOutArgWrapper(0)
                    inoutres856 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn855)
                    n = wrapn855.value
                    if (inoutres856): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_HALFYEAR): 
                    it.typ = DateExToken.DateExItemTokenType.HALFYEAR
                    wrapn857 = RefOutArgWrapper(0)
                    inoutres858 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn857)
                    n = wrapn857.value
                    if (inoutres858): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_QUARTAL): 
                    it.typ = DateExToken.DateExItemTokenType.QUARTAL
                    wrapn859 = RefOutArgWrapper(0)
                    inoutres860 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn859)
                    n = wrapn859.value
                    if (inoutres860): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_SEASON): 
                    it.typ = DateExToken.DateExItemTokenType.SEASON
                    wrapn861 = RefOutArgWrapper(0)
                    inoutres862 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn861)
                    n = wrapn861.value
                    if (inoutres862): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MONTH): 
                    it.typ = DateExToken.DateExItemTokenType.MONTH
                    wrapn863 = RefOutArgWrapper(0)
                    inoutres864 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn863)
                    n = wrapn863.value
                    if (inoutres864): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_WEEK): 
                    it.typ = DateExToken.DateExItemTokenType.WEEK
                    wrapn865 = RefOutArgWrapper(0)
                    inoutres866 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn865)
                    n = wrapn865.value
                    if (inoutres866): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAYOFWEEK): 
                    it.typ = DateExToken.DateExItemTokenType.DAYOFWEEK
                    wrapn867 = RefOutArgWrapper(0)
                    inoutres868 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn867)
                    n = wrapn867.value
                    if (inoutres868): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAY): 
                    it.typ = DateExToken.DateExItemTokenType.DAY
                    wrapn869 = RefOutArgWrapper(0)
                    inoutres870 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn869)
                    n = wrapn869.value
                    if (inoutres870): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_HOUR): 
                    it.typ = DateExToken.DateExItemTokenType.HOUR
                    wrapn871 = RefOutArgWrapper(0)
                    inoutres872 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn871)
                    n = wrapn871.value
                    if (inoutres872): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MINUTE): 
                    it.typ = DateExToken.DateExItemTokenType.MINUTE
                    wrapn873 = RefOutArgWrapper(0)
                    inoutres874 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn873)
                    n = wrapn873.value
                    if (inoutres874): 
                        it.value = n
                if (it.typ != DateExToken.DateExItemTokenType.UNDEFINED): 
                    res.insert(0, it)
            dr = dr.higher
        # PYTHON: sort(key=attrgetter('typ'))
        res.sort(key=operator.attrgetter('typ'))
        return res
    
    @staticmethod
    def calculate_date(dr : 'DateReferent', now : datetime.datetime, tense : int) -> datetime.datetime:
        if (dr.pointer == DatePointerType.TODAY): 
            return now
        if (not dr.is_relative and dr.dt is not None): 
            return dr.dt
        det = DateExToken(None, None)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        return det.get_date(now, tense)
    
    @staticmethod
    def calculate_date_range(dr : 'DateReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        if (dr.pointer == DatePointerType.TODAY): 
            from0_.value = now
            to.value = now
            return True
        if (not dr.is_relative and dr.dt is not None): 
            to.value = dr.dt
            from0_.value = to.value
            return True
        det = DateExToken(None, None)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        inoutres875 = det.get_dates(now, from0_, to, tense)
        return inoutres875
    
    @staticmethod
    def calculate_date_range2(dr : 'DateRangeReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        from0_.value = datetime.datetime.min
        to.value = datetime.datetime.max
        dt0 = None
        dt1 = None
        if (dr.date_from is None): 
            if (dr.date_to is None): 
                return False
            wrapdt0876 = RefOutArgWrapper(None)
            wrapdt1877 = RefOutArgWrapper(None)
            inoutres878 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt0876, wrapdt1877, tense)
            dt0 = wrapdt0876.value
            dt1 = wrapdt1877.value
            if (not inoutres878): 
                return False
            to.value = dt1
            return True
        elif (dr.date_to is None): 
            wrapdt0879 = RefOutArgWrapper(None)
            wrapdt1880 = RefOutArgWrapper(None)
            inoutres881 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0879, wrapdt1880, tense)
            dt0 = wrapdt0879.value
            dt1 = wrapdt1880.value
            if (not inoutres881): 
                return False
            from0_.value = dt0
            return True
        wrapdt0885 = RefOutArgWrapper(None)
        wrapdt1886 = RefOutArgWrapper(None)
        inoutres887 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt0885, wrapdt1886, tense)
        dt0 = wrapdt0885.value
        dt1 = wrapdt1886.value
        if (not inoutres887): 
            return False
        from0_.value = dt0
        dt2 = None
        dt3 = None
        wrapdt2882 = RefOutArgWrapper(None)
        wrapdt3883 = RefOutArgWrapper(None)
        inoutres884 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt2882, wrapdt3883, tense)
        dt2 = wrapdt2882.value
        dt3 = wrapdt3883.value
        if (not inoutres884): 
            return False
        to.value = dt3
        return True
    
    @staticmethod
    def append_to_string(dr : 'DateReferent', res : io.StringIO) -> None:
        dt0 = None
        dt1 = None
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0888 = RefOutArgWrapper(None)
        wrapdt1889 = RefOutArgWrapper(None)
        inoutres890 = DateRelHelper.calculate_date_range(dr, cur, wrapdt0888, wrapdt1889, 0)
        dt0 = wrapdt0888.value
        dt1 = wrapdt1889.value
        if (not inoutres890): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def append_to_string2(dr : 'DateRangeReferent', res : io.StringIO) -> None:
        dt0 = None
        dt1 = None
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt0891 = RefOutArgWrapper(None)
        wrapdt1892 = RefOutArgWrapper(None)
        inoutres893 = DateRelHelper.calculate_date_range2(dr, cur, wrapdt0891, wrapdt1892, 0)
        dt0 = wrapdt0891.value
        dt1 = wrapdt1892.value
        if (not inoutres893): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def __append_dates(cur : datetime.datetime, dt0 : datetime.datetime, dt1 : datetime.datetime, res : io.StringIO) -> None:
        mon0 = dt0.month
        print(" ({0}.{1}.{2}".format(dt0.year, "{:02d}".format(mon0), "{:02d}".format(dt0.day)), end="", file=res, flush=True)
        if (dt0.hour > 0 or dt0.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(dt0.hour), "{:02d}".format(dt0.minute)), end="", file=res, flush=True)
        if (dt0 != dt1): 
            mon1 = dt1.month
            print("-{0}.{1}.{2}".format(dt1.year, "{:02d}".format(mon1), "{:02d}".format(dt1.day)), end="", file=res, flush=True)
            if (dt1.hour > 0 or dt1.minute > 0): 
                print(" {0}:{1}".format("{:02d}".format(dt1.hour), "{:02d}".format(dt1.minute)), end="", file=res, flush=True)
        monc = cur.month
        print(" отн. {0}.{1}.{2}".format(cur.year, "{:02d}".format(monc), "{:02d}".format(cur.day)), end="", file=res, flush=True)
        if (cur.hour > 0 or cur.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(cur.hour), "{:02d}".format(cur.minute)), end="", file=res, flush=True)
        print(")", end="", file=res)
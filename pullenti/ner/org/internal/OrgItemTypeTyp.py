﻿# SDK Pullenti Lingvo, version 4.22, february 2024. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class OrgItemTypeTyp(IntEnum):
    UNDEFINED = 0
    ORG = 1
    PREFIX = 2
    DEP = 3
    DEPADD = 4
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
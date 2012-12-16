"""
Copyright (c) 2012, Christopher Stillson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import exceptions
from pprint import pprint as pp
from copy import deepcopy


class InvalidRange(exceptions.Exception): 
    pass

class InvertedRange(exceptions.Exception): 
    pass

class InvalidInput(exceptions.Exception): 
    pass

class VirtualClassOnly(exceptions.Exception): 
    pass

# is this singular
def isSQ(p):
    return hasattr(p, 'isSingularQ') and p.isSingularQ

def isRQ(p):
    return hasattr(p, 'isSingularQ') and not p.isSingularQ


def enum(**enums):
    return type('Enum', (), enums)

coverType = enum(EXACT_COVER    = 0,
                 UPPER_COVER    = 1,
                 LOWER_COVER    = 2,
                 INNER_COVER    = 3,
                 OUTER_COVER    = 4,
                 BELOW_NO_COVER = -1,
                 ABOVE_NO_COVER = -2,)

ct = coverType

class IntvBase(object):
    def __init__(self):
        raise VirtualClassOnly('This class should not be instatiated')
    
    def rangeCmp(self, other):
        if self.exactCoverQ(other): return ct.EXACT_COVER
        if self.upperCoverQ(other): return ct.UPPER_COVER
        if self.lowerCoverQ(other): return ct.LOWER_COVER
        if self.innerCoverQ(other): return ct.INNER_COVER
        if self.outerCoverQ(other): return ct.OUTER_COVER
        if self < other:            return ct.BELOW_NO_COVER
        if self > other:            return ct.ABOVE_NO_COVER
    
    @property
    def isSingularQ(self):
        return len(self) == 1
    
    def exactCoverQ(self, other):
        "exact match"
        return False
    
    def upperCoverQ(self, other):
        "overlaps above        (3,7) is upperCovered by (6,8)"
        return False
    
    def lowerCoverQ(self, other):
        "overlaps below        (3,7) is lowerCovered by (2,4)"
        return False
    
    def innerCoverQ(self, other):
        "partly covers inside  (3,7) is innerCovered by (4,6) or (3,5)"
        return False
    
    def outerCoverQ(self, other):
        "partly covers outside (3,7) is outerCovered by (1,9) or (2,7)"
        return False
    
    @property
    def lower(self):
        "return lower bound as a singular element"
        return None
    
    @property
    def upper(self):
        "return upper bound as a singular element"
        return None
    
    def __len__(self):
        "number of points covered 1 or 2+ really"
        return 0
    
    def split(self, port):
        "break a non singular element into two elements (if len is 2+)"
        return None
    
    def __add__(self, other):
        "add a point or range to a non singular element"
        return None
    
    def __sub__(self, other):
        "remove a point or range from a non singular element"
        return None
    
    def __contains__(self, other):
        "for in (is the intersection of two objects not null)"
        return False
    
    def __cmp__(self, other):
        "for sorting, only compares lower"
        return -1
    
    def nextToQ(self, other):
        "test adjacency (-1 == right below, 1 right above, 0 not adj)"
        return 0
    
    def coalesce(self, other):
        "if self and other should coalesce, return coalesced as non list, otherwise return None"
        rv = self + other
        if len(rv) = 1:
            return rv[0]
        return None
    
    def copy(self):
        return deepcopy(self)
 
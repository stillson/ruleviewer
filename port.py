#!/usr/bin/env python

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
from intvBase import *


MAXP = 65535
MINP = 1

class Port(IntvBase):
    def __init__(self, val):
        if val < MINP or val > MAXP:
            raise InvalidRange("port must be between 1 and 65535")
        
        if isSQ(val):
            self._val = val.val
        else:
            self._val = val
    
    @property
    def lower(self):
        return self._val
    
    @property
    def upper(self):
        return self._val
    
    @property
    def val(self):
        return self._val
    
    def __str__(self):
        return "p%s" % (self.val,)
    
    def __repr__(self):
        return self.__str__()
    
    def exactCoverQ(self, other):
        if isSQ(other):
            return self == other
        if isRQ(other):
            return False
        raise InvalidInput("must be port or range")
    
    def __add__(self, other):
        # double dispatch
        if isSQ(other):
            sv = self.val
            ov = other.val
            mn = min(sv,ov)
            mx = max(sv,ov)
            if mx - mn == 1:
                return [PortRange(mn,mx)]
            if other == self:
                return [Port(self)]
            return [Port(n), Port(x)]
        if isRQ(other):
            return other + self
        return Port(self.val + other)
    
    def __sub__(self, other):
        if isSQ(other):
            if self == other:
                return []
            else:
                return [Port(self)]
        if isRQ(other):
            if self in other:
                return []
            else:
                return [Port(self.val)]
                
        return Port(self.val - other)
    
    def __cmp__(self,other):
        if isSQ(other):
            return self.val.__cmp__(other.val)
        elif isRQ(other):
            return self.val.__cmp__(other.lower())
        else:
            return self.val.__cmp__(other)
    
    def split(self, port):
        return [Port(self.val)]
    
    def __contains__(self, other):
        if isSQ(other):
            return self == other
        if isRQ(other):
            return self in other
    
    def nextToQ(self, other):
        if isSQ(other):
            return abs(self.val - other.val) == 1
        if isRQ(other):
            return self.val + 1 == other.lower().val or self.val - 1 == other.upper().val
    
    def minQ(self):
        return self.val == MINP
    
    def maxQ(self):
        return self.val == MAXP
    
    def __len__(self):
        return 1
    

class PortRange(IntvBase):
    def __init__(self, start, end):
        if start >= end: raise InvertedRange("start must be less than end")
        self._start = Port(start)
        self._end   = Port(end)
        
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    def __len__(self):
        return self.end.val - self.start.val + 1
    
    def __contains__(self, other):
        if isSQ(other):
            return (other >= self.start) and (other <= self.end)
        
        if isRQ(other):
            if other.start < self.start and other.end > self.end:
                return True
            return (other.start in self) or (other.end in self)
        
        raise InvalidInput("object must be Port or PortRange")
    
    def __str__(self):
        return "|%d-%d|" % (self.start.val, self.end.val)
    
    def __repr__(self):
        return self.__str__()
    
    def rangeCmp(self, other):
        if isSQ(other):
            v = other.__cmp__(self)
            if v == -1:
                return ABOVE_NO_COVER
            if v == 0:
                return OUTER_COVER
            if v == 1:
                return BELOW_NO_COVER
        if isRQ(other):
            if self.end < other.start:
                return BELOW_NO_COVER
            if self.start > other.end:
                return ABOVE_NO_COVER
            if self.lowerCoverQ(other):
                return LOWER_COVER
            if self.upperCoverQ(other):
                return UPPER_COVER
            if self.outerCoverQ(other):
                return OUTER_COVER
            if self.innerCoverQ(other):
                return INNER_COVER
            if self.exactCoverQ(other):
                return EXACT_COVER
    
    def split(self, port):
        # port becomes the end of the lesser (unless it's the same as self.end)
        if not port in self:
            return [self.copy()]
        
        if port == self.start:
            if len(self) == 2:
                return [port + 0, self.start + 1]
            else:
                return [port + 0, PortRange(self.start + 1, self.end)]
        
        if port == self.end:
            return [self.copy()]
        
        if not port.maxQ() and port + 1 == self.end:
            return [PortRange(self.start, port), port + 1] 
        
        return [PortRange(self.start, port), PortRange(port + 1, self.end)] 
    
    def lowerCoverQ(self,other):
        # other lower covers self
        return (self.start in other) and not (self.end in other)
    
    def upperCoverQ(self,other):
        # other upper covers self
        return not (self.start in other) and (self.end in other)
    
    def outerCoverQ(self,other):
        # other outer covers self
        return self.start >= other.start and self.end <= other.end
    
    def innerCoverQ(self,other):
        # other inner covers self
        return other.outerCoverQ(self)
    
    def exactCoverQ(self,other):
        return self.start == other.start and self.end == other.end
    
    def __cmp__(self, other):
        # which one starts first
        return self.start.__cmp__(other.start)
    
    def maxEndQ(self):
        return self.end.val == MAXP
    
    def minStartQ(self):
        return self.start.val == MINP
    
    def __sub__(self, p):
        #remove a port or range
        if isSQ(p): 
            if not p in self:
                return [deepcopy(self)]
            if p == self.start:
                if len(self) == 2:
                    return [Port(self.end)]
                return [PortRange(self.start + 1, self.end)]
            if p == self.end:
                if len(self) == 2:
                    return [Port(self.start)]
                return [PortRange(self.start, self.end - 1)]
            if not p.minQ() and p - 1 == self.start:
                return [self.start, PortRange(self.start + 2, self.end)]
            if not p.maxQ() and p + 1 == self.end:
                return [PortRange(self.start, self.end - 2), self.end]
            split_range = self.split(p)
            split_range[0] = (split_range[0] - p)[0]
            return split_range
        
        if isRQ(p):
            if self.exactCoverQ(p) or self.outerCoverQ(p):
                return []
            if self.lowerCoverQ(p):
                split_range = self.split(p.end)
                return [split_range[1]]
            if self.upperCoverQ(p):
                split_range = self.split(p.start - 1)
                return [split_range[0]]
            if self.innerCoverQ(p):
                sr_low = self.split(p.start - 1)
                sr_hi  = self.split(p.end)
                return [sr_low[0], sr_hi[1]]
            #disjoint
            return [deepcopy(self)]
        
        raise InvalidInput("object must be Port or PortRange")
    
    def __add__(self,p):
        # add a port or range
        if isSQ(p):
            if p in self:
                return [deepcopy(self)]
            if p < self.start:
                if p + 1 == self.start:
                    return [PortRange(p, self.end)]
                else:
                    return [p + 0, deepcopy(self)]
            if self.end + 1 == p:
                return [PortRange(self.start, p)]
            else:
                return [deepcopy(self), p + 0]
        if isRQ(p):
            if self.exactCoverQ(p) or self.innerCoverQ(p):
                return [self.copy()]
            if self.outerCoverQ(p):
                return [p.copy()]
            if self.lowerCoverQ(p):
                return [PortRange(p.start, self.end)]
            if self.upperCoverQ(p):
                return [PortRange(self.start, p.end)]
            if self < p:
                if not self.maxEndQ() and self.end + 1== p.start:
                    return [PortRange(self.start, p.end)]
                else:
                    return [self.copy(), p.copy()]
            if not self.minStartQ() and self.start -1 == p.end:
                return [PortRange(p.start, self.end)]
            else:
                return [p.copy(), self.copy()]
        
        raise InvalidInput("object must be Port or PortRange")
    
    def upper(self):
        return self.start
    
    def lower(self):
        return self.end
    
    def nextToQ(self,other):
        if isSQ(other):
            return other.nextToQ(self)
        if isRQ(other):
            return self.end.val + 1 == other.start.val or other.end.val + 1 == self.start.val
    


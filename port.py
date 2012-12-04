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

import numbers
import exceptions
from pprint import pprint as pp
from copy import deepcopy


class InvalidPort(exceptions.Exception): 
    pass

class InvertedRange(exceptions.Exception): 
    pass

class InvalidInput(exceptions.Exception): 
    pass

class VirtualClassOnly(exceptions.Exception): 
    pass


MAXP = 65535
MINP = 1

def isP(p):
    return (hasattr(p, 'singularQ') and p.singularQ)

def isPR(p):
    return (hasattr(p, 'singularQ') and not p.singularQ)

EXACT_COVER    = 0
UPPER_COVER    = 1
LOWER_COVER    = 2
INNER_COVER    = 3
OUTER_COVER    = 4
BELOW_NO_COVER = -1
ABOVE_NO_COVER = -2

class PortBase(object):
    def __init__(self):
        raise VirtualClassOnly('This class should not be instatiated')
    
    def rangeCmp(self, other):
        if self.exactCoverQ(other): return EXACT_COVER
        if self.upperCoverQ(other): return UPPER_COVER
        if self.lowerCoverQ(other): return LOWER_COVER
        if self.innerCoverQ(other): return INNER_COVER
        if self.outerCoverQ(other): return OUTER_COVER
        if self < other:            return BELOW_NO_COVER
        if self > other:            return ABOVE_NO_COVER
    
    def exactCoverQ(self, other):
        # exact match
        return False
    
    def upperCoverQ(self, other):
        # overlaps above        (3,7) is upperCovered by (6,8)
        return False
    
    def lowerCoverQ(self, other):
        # overlaps below        (3,7) is lowerCovered by (2,4)
        return False
    
    def innerCoverQ(self, other):
        # partly covers inside  (3,7) is innerCovered by (4,6) or (3,5)
        return False
    
    def outerCoverQ(self, other):
        #partly covers outside (3,7) is outerCovered by (1,9) or (2,7)
        return False
    
    def lower(self):
        #return lower bound as a singular element
        return None
    
    def upper(self):
        #return upper bound as a singular element
        return None
    
    def __len__(self):
        #number of points covered 1 or 2+ really
        return 0
    
    def split(self, port):
        #break a non singular element into two elements (if len is 2+)
        return None
    
    def __add__(self, other):
        #add a point or range to a non singular element
        return None
    
    def __sub__(self, other):
        #remove a point or range from a non singular element
        return None
    
    def __contains__(self, other):
        #for in
        return False
    
    def __cmp__(self, other):
        #for sorting
        return -1
    
    def nextToQ(self, other):
        #test adjacency (-1 == right below, 1 right above, 0 not adj)
        return 0
    
    def copy(self):
        return deepcopy(self)
    

class Port(PortBase):
    def __init__(self, val):
        if val < MINP or val > MAXP:
            raise InvalidPort("port must be between 1 and 65535")
        
        self.singularQ = True
        
        if isP(val):
            self._val = val.val
        else:
            self._val = val
    
    @property
    def val(self):
        return self._val
    
    def __str__(self):
        return "p%s" % (self.val,)
    
    def __repr__(self):
        return self.__str__()
    
    def exactCoverQ(self, other):
        if isP(other):
            return self == other
        if isPR(other):
            return False
        raise InvalidInput("must be port or range")
    
    def __add__(self, other):
        # double dispatch
        if isP(other):
            if other > self:
                return [Port(self.val), Port(other.val)]
            if other < self:
                return [Port(other.val), Port(self.val)]
            if other == self:
                return [Port(self.val)]
        if isPR(other):
            return other + self
        return Port(self.val + other)
    
    def __sub__(self, other):
        if isP(other):
            if self == other:
                return []
            else:
                return [Port(self.val)]
        if isPR(other):
            if self in other:
                return []
            else:
                return [Port(self.val)]
                
        return Port(self.val - other)
    
    def __cmp__(self,other):
        if isP(other):
            return self.val.__cmp__(other.val)
        elif isPR(other):
            return self.val.__cmp__(other.lower())
        else:
            return self.val.__cmp__(other)
    
    def split(self, port):
        return [Port(self.val)]
    
    def __contains__(self, other):
        if isP(other):
            return self == other
        if isPR(other):
            return self in other
    
    def nextToQ(self, other):
        if isP(other):
            return self.val == other.val -1 or self.val == other.val + 1
        if isPR(other):
            return self.val + 1 == other.lower().val or self.val - 1 == other.upper().val
    
    def lower(self):
        return self.copy()
    
    def upper(self):
        return self.copy()
    
    def minQ(self):
        return self.val == MINP
    
    def maxQ(self):
        return self.val == MAXP
    
    def __len__(self):
        return 1
    

class PortRange(PortBase):
    def __init__(self, start, end):
        if start >= end: raise InvertedRange("start must be less than end")
        self._start = Port(start)
        self._end   = Port(end)
        
        self.singularQ = False
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    def __len__(self):
        return self.end.val - self.start.val + 1
    
    def __contains__(self, other):
        if isP(other):
            return (other >= self.start) and (other <= self.end)
        
        if isPR(other):
            return (self.start in other) or (self.end in other)
        
        raise InvalidInput("object must be Port or PortRange")
    
    def __str__(self):
        return "|%d-%d|" % (self.start.val, self.end.val)
    
    def __repr__(self):
        return self.__str__()
    
    def rangeCmp(self, other):
        if isP(other):
            v = other.__cmp__(self)
            if v == -1:
                return ABOVE_NO_COVER
            if v == 0:
                return OUTER_COVER
            if v == 1:
                return BELOW_NO_COVER
        if isPR(other):
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
        if isP(p): 
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
        
        if isPR(p):
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
        if isP(p):
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
        if isPR(p):
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
        if isP(other):
            return other.nextToQ(self)
        if isPR(other):
            return self.end.val + 1 == other.start.val or other.end.val + 1 == self.start.val
    

if __name__ == "__main__":
    
    if True:
        p = Port(80)
        q = Port(8080)
        p1 = Port(1)
        p2 = Port(1024)
        pa = Port(2)
        pb = Port(3)
        r = PortRange(1,1024)
        
        print( p in r )
        print( q in r )
        pp(r.split(p))
        pp(r.split(q))
        pp(r - p)
        pp(r - q)
        pp(r - p1)
        pp(r - p2)
        pp(r - pa)
        pp(r - pb)
    
    r1 = PortRange(100,200)
    lc = PortRange(50,150)
    uc = PortRange(150,250)
    ic = PortRange(125, 175)
    oc = PortRange(50, 250)
    lc1= PortRange(100,125)
    uc1= PortRange(175,200)
    dj1= PortRange(300,400)
    dj2= PortRange(30,40)
    
    def testsub(tr1,tr2):
        print "_"* 10
        print tr1,"-",tr2
        pp(tr1 -tr2)
    
    if True:
        testsub(r1, lc)
        testsub(r1, uc)
        testsub(r1, ic)
        testsub(r1, oc)
        testsub(r1, lc1)
        testsub(r1, uc1)
        testsub(r1, dj1)
        testsub(r1, dj2)
        testsub(r1, r1)
    
    def testadd(tr1,tr2):
        print "_"* 10
        print tr1,"+",tr2
        pp(tr1 + tr2)
    
    if True:
        testadd(r1, lc)
        testadd(r1, uc)
        testadd(r1, ic)
        testadd(r1, oc)
        testadd(r1, lc1)
        testadd(r1, uc1)
        testadd(r1, dj1)
        testadd(r1, dj2)
        testadd(r1, r1)
    
    
    all = PortRange(1,65535)
    low = PortRange(1,1023)
    mid = PortRange(1024, 49151)
    hi  = PortRange(49152,65535)
    
    if True:
        testsub(all, low) 
        testsub(all, mid) 
        testsub(all, hi) 
        testsub(all, all) 
        
        testadd(all, low) 
        testadd(all, mid) 
        testadd(all, hi) 
        testadd(all, all) 
    
    sr1=PortRange(1,2)
    sr2=PortRange(2,3)
    sr3=PortRange(3,4)
    sr4=PortRange(4,5)
    sp1=Port(1)
    sp2=Port(2)
    sp3=Port(3)
    sp4=Port(4)
    sp5=Port(5)
    
    srlist = [sr1,sr2,sr3,sr4]
    splist = [sp1,sp2,sp3,sp4,sp5]
    
    for tsr in srlist:
        for tsp in splist:
            print '+=' * 20
            testsub(tsr, tsp)
            testadd(tsr, tsp)
    
    print "^" * 40
    print "^" * 40
    
    for tsr1 in srlist:
        for tsr2 in srlist:
            print '+=' * 20
            testsub(tsr1, tsr2)
            testadd(tsr1, tsr2)
    
    rr1=PortRange(MAXP - 1, MAXP - 0)
    rr2=PortRange(MAXP - 2, MAXP - 1)
    rr3=PortRange(MAXP - 3, MAXP - 2)
    rr4=PortRange(MAXP - 4, MAXP - 3)
    rp1=Port(MAXP - 5)
    rp2=Port(MAXP - 4)
    rp3=Port(MAXP - 3)
    rp4=Port(MAXP - 2)
    rp5=Port(MAXP - 1)
    rp6=Port(MAXP - 0)
    
    rrlist = [rr1,rr2,rr3,rr4]
    rplist = [rp1,rp2,rp3,rp4,rp5, rp6]
    
    for rsr in rrlist:
        for rsp in rplist:
            print '+=' * 20
            testsub(rsr, rsp)
            testadd(rsr, rsp)
    
    print "^" * 40
    print "^" * 40
    
    for rsr1 in rrlist:
        for rsr2 in rrlist:
            print '+=' * 20
            testsub(rsr1, rsr2)
            testadd(rsr1, rsr2)
    
    
    #list1 = [all,low,mid,hi]
    list1 = [r1,lc,uc,ic,oc,lc1,uc1,dj1,dj2]
    
    if False:
        for tr1 in list1:
            for tr2 in list1:
                print '+=' * 20
                testsub(tr1,tr2)
                testadd(tr1,tr2)

#!/usr/bin/env python

import numbers
import exceptions
from pprint import pprint as pp


class InvalidPort(exceptions.Exception): pass
class InvertedRange(exceptions.Exception): pass
class InvalidInput(exceptions.Exception): pass

MAXP = 65535
MINP = 1

def isP(p):
    return hasattr(p, 'val')

def isPR(p):
    return hasattr(p, 'start')

class Port(object):
    def __init__(self, val):
        if val < MINP or val > MAXP:
            raise InvalidPort("port must be between 1 and 65535")

        if isP(val):
            self.val = val.val
        else:
            self.val = val

    def __call__(self):
        return self.val 

    def __str__(self):
        return "p%s" % (self.val,)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return Port(self.val + other)

    def __sub__(self, other):
        return Port(self.val - other)

    def __cmp__(self,other):
        if isP(other):
            return self.val.__cmp__(other.val)
        else:
            return self.val.__cmp__(other)

    def minQ(self):
        return self.val == MINP

    def maxQ(self):
        return self.val == MAXP

    def __len__(self):
        return 1

    def singularQ(self):
        return True

class PortRange(object):
    def __init__(self, start, end):
        if start >= end: raise InvertedRange("start must be less than end")
        if isP(start):
            self.start = start
        else:
            self.start = Port(start)

        if isP(end):
            self.end   = end
        else:
            self.end   = Port(end)

    def singularQ(self):
        return False

    def __len__(self):
        return self.end.val - self.start.val + 1

    def __contains__(self, other):
        if isP(other):
            return (other >= self.start) and (other <= self.end)

        if isPR(other):
            return (self.start in other) or (self.end in other)

        raise InvalidInput("object must be Port or PortRange")

    def __str__(self):
        return "|%d-%d|" % (self.start(), self.end())

    def __repr__(self):
        return self.__str__()

    # port becomes the end of the lesser (unless it's the same as self.end)
    def split(self, port):
        if not port in self:
            return [self]

        if self.start + 1 == self.end:
            return [self.start, self.end]
        if port == self.start:
            if len(self) == 2:
                return [port, self.start + 1]
            else:
                return [port, PortRange(self.start + 1, self.end)]

        if port == self.end:
            return [self]
        
        if not port.maxQ() and port + 1 == self.end:
            return [PortRange(self.start, port), port + 1] 

        return [PortRange(self.start, port), PortRange(port + 1, self.end)] 

    def lowerCoverQ(self,other):
        return (self.start in other) and not (self.end in other)

    def upperCoverQ(self,other):
        return not (self.start in other) and (self.end in other)

    def outerCoverQ(self,other):
        return self.start >= other.start and self.end <= other.end

    def innerCoverQ(self,other):
        return other.outerCoverQ(self)

    def exactCoverQ(self,other):
        return self.start == other.start and self.end == other.end

    # which one starts first
    def __cmp__(self, other):
        return self.start.__cmp__(other.start)

    def maxEndQ(self):
        return self.end.val == MAXP

    def minStartQ(self):
        return self.start.val == MINP

    #remove a port or range
    def __sub__(self, p):
        if isP(p): 
            if not p in self:
                return [self]
            if p == self.start:
                if len(self) == 2:
                    return [Port(self.end)]
                return [PortRange(self.start + 1, self.end)]
            if p == self.end:
                if len(self) == 2:
                    return [Port(self.start)]
                return [PortRange(self.start, self.end -1)]
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
            return [self]

        raise InvalidInput("object must be Port or PortRange")

    # add a port or range
    def __add__(self,p):
        if isP(p):
            if p in self:
                return [self]
            if p < self.start:
                if p + 1 == self.start:
                    return [PortRange(p, self.end)]
                else:
                    return [p, self]
            if self.end + 1 == p:
                return [PortRange(self.start, p)]
            else:
                return [self, p]
        if isPR(p):
            if self.exactCoverQ(p) or self.innerCoverQ(p):
                return [self]
            if self.outerCoverQ(p):
                return [p]
            if self.lowerCoverQ(p):
                return [PortRange(p.start, self.end)]
            if self.upperCoverQ(p):
                return [PortRange(self.start, p.end)]
            if self < p:
                if not self.maxEndQ() and self.end + 1== p.start:
                    return [PortRange(self.start, p.end)]
                else:
                    return [self,p]
            if not self.minStartQ() and self.start -1 == p.end:
                return [PortRange(p.start, self.end)]
            else:
                return [p,self]

        raise InvalidInput("object must be Port or PortRange")

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

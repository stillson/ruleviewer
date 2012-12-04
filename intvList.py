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

# value responds to: (*CoverQ() for len = 2+_)
# exactCoverQ() interval match        (3,7) == (3,7)
# upperCoverQ() overlaps above        (3,7) is upperCovered by (6,8)
# lowerCoverQ() overlaps below        (3,7) is lowerCovered by (2,4)
# innerCoverQ() partly covers inside  (3,7) is innerCovered by (4,6) or (3,5)
# outerCoverQ() partly covers outside (3,7) is outerCovered by (1,9) or (2,7)
# lower()       return lower bound as a singular element
# upper()       return upper bound as a singular element
# __len__       number of points covered 1 or 2+ really
# split()       break a non singular element into two elements (if len is 2+)
# +             add a point or range to a non singular element
# -             remove a point or range from a non singular element
# __contains__  for in
# __cmp__       for sorting
# nextToQ()     test adjacency (-1 == right below, 1 right above, 0 not adj)

import bisect

class IntvList(object):
    def __init__(self):
        self.list = []
    
    def add(self, v):
        if not self.list:
            self.list = [v]
            return self
        
        if len(self) == 1:
            self.list = self.list[0] + v
            return self
            
        print "--s-->", self
        print "--v-->", v
        l = self.find_below(v)
        print "--l-->", l
        u = self.find_above(v)
        print "--u-->", u

        if l > u:
            print "l > u: bad"
            return
        
        if l == u and l == len(self):
            self.list.append(v)
            return self
        if l == u:
            if self.list[l - 1].nextToQ(v):
                self.list[l - 1] = (self.list[l - 1] + v)[0]
                return self
            if self.list[u].nextToQ(v):
                self.list[u] = (self.list[u] + v)[0]
                return self
            self.list.insert(l, v)
            return self
        else:
            if l != 0:
                before = self.list[:l - 1] 
            else:
                before = []
            if u != len(self):
                after = self.list[u + 1:]
            else: 
                after = []
            
            if l - u == 1:
                middle = self.list[l] + v
            else:
                middle = self.list[l] + v
                print "middle", middle
                print "self", self
                if u < len(self):
                    middle = self.list[u] + middle[0]
                else:
                    middle = [middle[0]]

            if len(before) and before[-1].nextToQ(middle[0]):
                middle[0] = (middle[0] + before[-1])[0]
                before = before[:-1]
            if len(after) and after[0].nextToQ(middle[-1]):
                middle[-1] = (after[0] + middle[-1])[0]
                after = after[1:]
            self.list = before + middle + after
            return self
                    
    
    def remove(self, v):
        if not self.list:
            return self
    
    def __str__(self):
        rstr ="["
        for i in self.list:
            rstr += str(i)
            rstr += ","
        if len(rstr) > 1: rstr = rstr[:-1]
        rstr += ']'
        return rstr
    
    def __iter__(self):
        return self.list.__iter__
    
    def __contains__(self,v):
        #is v in any of the elements of this list
        
        if len(self) < 2:
            testList = self.list
        else:
            lower = self.find_below(v)
            upper = self.find_above(v)
            testList = self.list[lower:upper]
        
        print "==v==>", v
        for e in testList:
            print "==e==>", e
            if v in e: return True
        return False
    
    def __len__(self):
        return len(self.list)
    
    def find_above(self, other):
        # leftmost element with upper() < other.lower
        lo=0
        hi = len(self)

        while lo < hi:
            mid = (lo+hi)//2
            if self.list[mid].upper() < other.lower(): 
                lo = mid+1
            else: 
                hi = mid
        return lo

    
    def find_below(self, other):
        # rightmost element with lower() > other.upper
        lo = 0
        hi = len(self)
        while lo < hi:
            mid = (lo+hi)//2
            if other.upper() < self.list[mid].lower(): 
                hi = mid
            else: 
                lo = mid+1
        return lo
    

if __name__ == '__main__':
    from port import *
    ALL = PortRange(MINP, MAXP)
    r1  = PortRange(1,1024)
    r2  = PortRange(500,1500)
    r3  = PortRange(1025, 2000)
    r4  = PortRange(2000,3000)
    r5  = PortRange(4000,5000)
    r6  = PortRange(6000,7000)
    r7  = PortRange(8000,9000)
    p1  = Port(80)
    p2  = Port(1025)
    p3  = Port(8080)

    lall = [r1,r2,r3,r4,r5,r6,r7,p1,p2,p3]

    print "TEST1"
    i = IntvList()
    print i
    print i.add(r1)
    print i.add(r3)
    print i.add(r2)
    print i.add(ALL)
    print

    print "TEST2"
    i = IntvList()
    print i
    print i.add(r1)
    print i.add(r4)
    print i.add(p2)
    print i.add(p3)
    print i.add(r4)
    print i.add(r5)
    print i.add(r6)
    print i.add(ALL)

    print "TEST3"
    i = IntvList()
    print i
    print i.add(r1)
    print i.add(r4)
    print i.add(p2)
    print i.add(p3)
    print i.add(r4)
    print i.add(r5)
    print i.add(r6)
    print i.add(r7)

    print "test4"

    import itertools
    perm = itertools.permutations(lall, len(lall))

    for lv in perm:
        print
        print perm
        i = IntvList()
        for v in lv:
            print i
            print v
            print i.add(v)
            print


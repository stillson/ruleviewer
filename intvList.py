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

import exceptions
import bisect
import collections
from ilDebug import dbP,dbPn
import itertools

class UpperLowerCross(exceptions.Exception):
    pass

class IntvList(collections.MutableSequence):
    "init"
    def __init__(self):
        self.list = []
    
    "ABC related functions"
    def __setitem__(self, index, value):
        self.list[index] = value

    def __delitem__(self, index):
        self.list.__delitem__(index)

    def insert(self, index, val):
        self.list.insert(index,val)

    def insert_(self, index, val):
        self.list.insert(index,val)
        return self

    def __getitem__(self, index):
        return self.list[index]

    def __str__(self):
        rstr ="["
        for i in self.list:
            rstr += str(i)
            rstr += ","
        if len(rstr) > 1: rstr = rstr[:-1]
        rstr += ']'
        return rstr
    
    def __iter__(self):
        return self.list.__iter__()
    
    def __contains__(self,v):
        #is the intersection of self an v not the empty set
        
        if len(self) == 0:
            return False
        
        if len(self) < 1:
            # otimized because it's not worth it to find lower/upper
            # for a short list
            # set to 1 for debugging
            testList = self.list
        else:
            lower = self.find_below(v)
            upper = self.find_above(v)
            testList = self[lower:upper]
        
        #print "==v==>", v
        for e in testList:
            #print "==e==>", e
            if v in e: 
                return True

        #print "False"
        return False
    
    def __len__(self):
        return len(self.list)
    
    def __cmp__(self, other):
        pairlist = itertools.izip(self,other)
        for p in pairlist:
            rv =  p[0].__cmp__(p[1])
            if rv != 0:
                return rv
        return 0

    "useful internal funcs"
    def find_above(self, other):
        # leftmost (first) element with self[i].upper() <= other.lower
        lo=0
        hi = len(self)

        while lo < hi:
            mid = (lo+hi)//2
            if self[mid].upper() < other.lower():
                lo = mid+1
            else:
                hi = mid
        return lo

    
    def find_below(self, other):
        # rightmost (last) element with self[i].lower() >= other.upper
        lo = 0
        hi = len(self)
        while lo < hi:
            mid = (lo+hi)//2
            if other.upper() < self[mid].lower(): 
                hi = mid
            else: 
                lo = mid+1
        return lo
    
    "MEAT"
    def add_(self, v):
        
        # empty list
        if not self.list:
            self.list = [v]
            return self
        
        # 1 elment
        if len(self) == 1:
            self.list = self.list[0] + v
            return self
        
        l = self.find_below(v)
        u = self.find_above(v)
        
        if l > u:
            if v.isSingularQ:
                #we are trying to put a port on top of an identical port
                return self
            else:
                raise UpperLowerCross("lower greather than upper")
        
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
                #print "middle", middle
                #print "self", self
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
    
    def remove_(self, v):
        pf = False
        dbP(pf, '')
        dbP(pf, 'pre')
        if not self.list or not v in self:
            dbP(pf, 'x',str(self))
            return self
        
        if len(self) == 1:
            dbP(pf, 'a')
            self.list = self.list[0] - v
            return self
        
        l = self.find_below(v)
        u = self.find_above(v)
        dbP(pf, "l: %d" % l)
        dbP(pf, "u: %d" % u)
        dbP(pf, "len: %d" % len(self))
        
        if u < l:
            dbP(pf, 'c')
            if len(v) == 1:
                # port to port
                self.remove(v)
                return self
            else:
                raise UpperLowerCross("lower greater than upper")
        
        if u == len(self):
            u = u - 1
        
        if l == u:
            dbP(pf, 'd')
            self[l:u+1] = self[l] - v
            return self
        
        if u - l == 1:
            dbP(pf, 'f')
            self[u:u+1] = self[u] - v
            self[l:l+1] = self[l] - v
        else:
            dbP(pf, 'g')
            self[u:u+1] = self[u] - v
            del self[l+1,u]
            self[l:l+1] = self[l] - v
        
        return self
    

if __name__ == '__main__':
    i = IntvList()
    print dir(i)

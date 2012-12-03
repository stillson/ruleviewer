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
        
        if not v in self:
            l = self.find_below(v)
            u = self.find_above(v)
            
            if l == u:
                pass
            else:
                pass
    
    def remove(self, v):
        if not self.list:
            return self
    
    def __str__(self):
        rstr ="["
        for i in self.list:
            rstr += str(i)
            rstr += ","
        rstr = rstr[:-1]
        rstr += ']'
    
    def __iter__(self):
        return self.list.__iter__
    
    def __contains__(self,v):
        #is v in any of the elements of this list
        
        if len(self) < 5:
            testList = self.list
        else:
            lower = find_below(val)
            upper = find_above(val)
            testList = self.list[lower:upper]
        
        for e in testList:
            if v in e return True
        return False
    
    def __len__(self):
        return len(self.list)
    
    def find_below(self, val):
        return bisect_right(self.list,val.lower())
    
    def find_above(self, val):
        return bisect_right(self, val.upper())
    


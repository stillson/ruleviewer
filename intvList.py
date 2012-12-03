#!/usr/bin/env python

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
    


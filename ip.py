
import ipaddr
from intvBase import *
from copy import deepcopy as dCopy

# V4 only right now

class IpAddress(IntvBase):
    """represents a single ip address"""
    def __init__(self, arg):
        # use a sing host network
        self._addr = ipaddr.IPNetwork(arg, version=4)
        self._arg = arg
        
    @property
    def copy(self):
        return dCopy(self)
    
    @property
    def lower(self):
        return dCopy(self)
    
    @property
    def upper(self):
        return dCopy(self)
    
    @property
    def val(self):
        return dCopy(self._addr)
    
    def __str__(self):
        return str(self._addr)
    
    def __repr__(self):
        return repr(self._addr)
    
    def exactCoverQ(self, other):
        if isSQ(other):
            return self.val == other.val
        if isRQ(other):
            return False
        raise InvalidInput('Must be IpAddress or IpNetwork')
    
    def __add__(self, other):
        if isSQ(other):
            if self == other:
                return [self.copy()]
            if abs(int(self._addr) - int(other._addr)) == 1:
                # return a very small address range....
                args = [self._addr.network, other._addr.network]
                args.sort()
                return summarize_address_range(*args)
            args = [self, other]
            args.sort()
            return args
        if isRQ(other):
            #double dispatch
            return other + self
        raise InvalidInput('Must be IpAddress or IpNetwork')
        
    def __sub__(self, other):
        if isSQ(other):
            if self == other:
                return []
            else:
                return [self.copy()]
        if isRQ(other):
            if self in other:
                return []
            else:
                return [self.copy()]
        raise InvalidInput('Must be IpAddress or IpNetwork')
        
    def __cmp__(self, other):
        if isSQ(other):
            if self._addr <  other._addr: return -1
            if self._addr == other._addr: return 0
            if self._addr >  other._addr: return 1
        if isRQ(other):
            if self._addr <  other.lower: return -1
            if self._addr == other.lower: return 0
            if self._addr >  other.lower: return 1
        raise InvalidInput('Must be IpAddress or IpNetwork')
    
    def nextToQ(self):
        if isSQ(other):
            if abs(int(self._addr) - int(other._addr)) == 1:
                return True
            else:
                return False
        if isRQ(other):
            if int(other.lower) - int(self._addr) == 1:
                return True
            if int(self._addr) - int(other.upper) == 1:
                return True
            else:
                return False
        
        raise InvalidInput('Must be IpAddress or IpNetwork')
    
    def split(self, ipaddr):
        return [self.copy()]
    
    def __contains__(self, other):
        if isSQ(other):
            return self == other
        if isRQ(other):
            return self in other
        raise InvalidInput('Must be IpAddress or IpNetwork')
        
    def __len__(self):
        return 1
    
class IpNetwork(IntvBase):
    """an ipv4 range (not really a netowrk)"""
    def __init__(self, arg):
        self._arg = arg
        self._net = IPNetwork(arg, version=4)
    
    @property
    def lower(self):
        return IpAddress(int(self._net.network))
    
    @property
    def upper(self):
        return IpAddress(int(self._net.broadcast))
        
    @property
    def val(self):
        return dCopy(self._net)
    
    def __len__(self):
        return self._net.numhosts
    
    def __contains__(self, other):
        if isSQ(other):
            return other.val in self._net
        if isRQ(other):
            return self._net.overlaps(other.val)
        
        raise InvalidInput('Must be IpAddress or IpNetwork')
    
    def __str__(self):
        return str(self._net)
    
    def __repr__(self):
        return str(self)
    
    def lowerCoverQ(self,other):
        # other lower covers self
        return (self.lower in other) and not (self.upper in other)
    
    def upperCoverQ(self,other):
        # other upper covers self
        return not (self.lower in other) and (self.upper in other)
    
    def outerCoverQ(self,other):
        # other outer covers self
        return self.lower >= other.lower and self.upper <= other.upper
    
    def innerCoverQ(self,other):
        # other inner covers self
        return other.outerCoverQ(self)
    
    def exactCoverQ(self,other):
        return self.lower == other.lower and self.upper == other.upper
    
    def __cmp__(self,other):
        self.start.__cmp__(other.start)
    
    def nextToQ(self,other):
        if isSQ(other):
            return other.nextToQ(self)
        if isRQ(other):
            return self.lower.nextToQ(other.lower) or self.upper.nextToQ(other.upper)
        
        raise InvalidInput('Must be IpAddress or IpNetwork')
    
    def __add__(self, other):
        if isSQ(other):
            if other in self:
                return [self.copy()]
            if other < self.lower:
                return [other.copy(), self.copy()]
            if other > self.upper:
                return [self.copy(), other.copy()]
        if isRQ(other):
            def mapper(x):
                return IpNetwork(str(x))
            new_addrs = collapse_address_list(self.val, other.val)
            new_addrs = map(mapper, new_addrs)
            return new_addrs
        
        raise InvalidInput('Must be IpAddress or IpNetwork')
        
    def __sub__(self, other):
        if not self.overlaps(other):
            return [self.copy()]
        def mapper(x):
            return IpNetwork(str(x))
        rv = self._net.address_exclude_ab(other._net)
        rv_list = []
        for i in rv:
            rv_list.append(map(mapper, i))
        return rv_list

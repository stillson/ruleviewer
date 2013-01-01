
import ipaddr
from intvBase import *

# V4 only right now

class ipAddress(IntvBase):
    """represents a single ip address"""
    def __init__(self, arg):
        addr = ipaddr.IPAddress(arg, version=4)
        self.arg = arg
        


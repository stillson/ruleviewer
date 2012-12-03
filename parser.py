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

from  pyparsing import Keyword
import pyparsing as P
#from pprint import pprint as pp
import pprint
import collections

pp = pprint.PrettyPrinter(indent=4, width=20).pprint

"""
RULE-BODY:      check-state [PARAMS] | ACTION [PARAMS] ADDR [OPTION_LIST]
ACTION: check-state | allow | count | deny | unreach{,6} CODE |
               skipto N | {divert|tee} PORT | forward ADDR |
               pipe N | queue N | nat N | setfib FIB
PARAMS:         [log [logamount LOGLIMIT]] [altq QUEUE_NAME]
ADDR:           [ MAC dst src ether_type ]
                [ ip from IPADDR [ PORT ] to IPADDR [ PORTLIST ] ]
                [ ipv6|ip6 from IP6ADDR [ PORT ] to IP6ADDR [ PORTLIST ] ]
IPADDR: [not] { any | me | ip/bits{x,y,z} | table(t[,v]) | IPLIST }
IP6ADDR:        [not] { any | me | me6 | ip6/bits | IP6LIST }
IP6LIST:        { ip6 | ip6/bits }[,IP6LIST]
IPLIST: { ip | ip/bits | ip:mask }[,IPLIST]
OPTION_LIST:    OPTION [OPTION_LIST]
OPTION: bridged | diverted | diverted-loopback | diverted-output |
        {dst-ip|src-ip} IPADDR | {dst-ip6|src-ip6|dst-ipv6|src-ipv6} IP6ADDR |
        {dst-port|src-port} LIST |
        estab | frag | {gid|uid} N | icmptypes LIST | in | out | ipid LIST |
        iplen LIST | ipoptions SPEC | ipprecedence | ipsec | iptos SPEC |
        ipttl LIST | ipversion VER | keep-state | layer2 | limit ... |
        icmp6types LIST | ext6hdr LIST | flow-id N[,N] | fib FIB |
        mac ... | mac-type LIST | proto LIST | {recv|xmit|via} {IF|IPADDR} |
        setup | {tcpack|tcpseq|tcpwin} NN | tcpflags SPEC | tcpoptions SPEC |
        tcpdatalen LIST | verrevpath | versrcreach | antispoof
"""


# test function
def ppp(tok):
    pp(tok[0])

def ip_from(tok):
    print "from :", tok[0]
    
def ip_to(tok):
    print "to   :", tok[0]

# rule holder. basically a dict
class Rule(collections.MutableMapping):
    def __init__(self):
        self.i_dict = {}

    def __getitem__(self, key):
        return self.i_dict[key]
        
    def __setitem__(self, key, val):
        self.i_dict[key] = val
        
    def __delitem__(self, key):
        del(self.i_dict[key])
        
    def keys(self):
        return self.i_dict.keys()
        
    def __len__(self):
        return len(self.i_dict)
        
    def __iter__(self):
        return self.i_dict.__iter__()
        
    def __contains__(self, k):
        return self.i_dict.__contains__(k)
    
    def dump(self):
        pp(self.i_dict)
        
# holder for G_RULE
class RuleFactory(object):
    G_RULE = None
    def __init__(self):
        if not RuleFactory.G_RULE:
            RuleFactory.G_RULE = Rule()

    def popRule(self):
        old_rule = RuleFactory.G_RULE
        RuleFactory.G_RULE = Rule()
        return old_rule

    @staticmethod
    def getParseAction(tok_name, level=1):
        def iFunc(token):
            if level == 0:
                t = token
            else:
                t = token[0]
            if tok_name in RuleFactory.G_RULE:
                RuleFactory.G_RULE[tok_name].append(t)
            else:
                RuleFactory.G_RULE[tok_name] = [t]
        return iFunc
    

# various numbers
LINENO              = P.Word(P.nums, max=5)
SKIPNO              = P.Word(P.nums)
IPPART              = P.Word(P.nums, max=3)
TABLENO             = P.Word(P.nums, max=2)
PORTNO              = P.Word(P.nums, max=5)
CIDR                = P.Word(P.nums, max=2)
UIDNO               = P.Word(P.nums, max=6)

# various literals
DOT                 = P.Literal('.')
STAR                = P.Literal('*')
LBRACE              = P.Literal('{')
RBRACE              = P.Literal('}')
LPAREN              = P.Suppress('(')
RPAREN              = P.Suppress(')')
SLASH               = P.Literal('/')
COLON               = P.Literal(':')
COMMA               = P.Literal(',')
DASH                = P.Literal('-')

# keywords
ALLOW               = Keyword("allow")
ALTQ                = Keyword("altq")
ANTISPOOF           = Keyword("antispoof")
ANY                 = Keyword("any")
BRIDGED             = Keyword("bridged")
CHECK_STATE         = Keyword("check-state")
COUNT               = Keyword("count")
DENY                = Keyword("deny")
DIVERTED            = Keyword("diverted")
DIVERTED_LOOPBACK   = Keyword("diverted-loopback")
DIVERTED_OUTPUT     = Keyword("diverted-output")
DST_IP              = Keyword("dst-ip")
DST_IP6             = Keyword("dst-ip6")
DST_IPV6            = Keyword("dst-ipv6")
DST_PORT            = Keyword("dst-port")
ESTAB               = Keyword("estab")
ETHER_TYPE          = Keyword("ether_type")
EXT6HDR             = Keyword("ext6hdr")
FIB                 = Keyword("fib")
FLOW_ID             = Keyword("flow-id")
FORWARD             = Keyword("forward")
FRAG                = Keyword("frag")
FROM                = Keyword("from")
FWD                 = Keyword("fwd")
GUID                = Keyword("guid")
ICMP6TYPES          = Keyword("icmp6types")
ICMPTYPES           = Keyword("icmptypes")
IN                  = Keyword("in")
IP6                 = Keyword("ip6")
IPID                = Keyword("ipid")
IPLEN               = Keyword("iplen")
IPOPTIONS           = Keyword("ipoptions")
IPPRECEDENCE        = Keyword("ipprecedence")
IPSEC               = Keyword("ipsec")
IPTOS               = Keyword("iptos")
IPTTL               = Keyword("ipttl")
IPV6                = Keyword("ipv6")
IPVERSION           = Keyword("ipversion")
KEEP_STATE          = Keyword("keep-state")
LAYER2              = Keyword("layer2")
LIMIT               = Keyword("limit")
LOG                 = Keyword("log")
LOGAMOUNT           = Keyword("logamount")
MAC                 = Keyword("mac")
MAC_TYPE            = Keyword("mac-type")
ME                  = Keyword("me")
ME6                 = Keyword("me6")
NAT                 = Keyword("nat")
NOT                 = Keyword("not")
OR                  = Keyword("or")
OUT                 = Keyword("out")
PIPE                = Keyword("pipe")
QUEUE               = Keyword("queue")
REJECT              = Keyword("reject")
RESET               = Keyword("reset")
RECV                = Keyword("recv")
SOCKARG             = Keyword("sockarg")
SETFIB              = Keyword("setfib")
SETUP               = Keyword("setup")
SKIPTO              = Keyword("skipto")
SRC                 = Keyword("src")
SRC_IP              = Keyword("src-ip")
SRC_IP6             = Keyword("src-ip6")
SRC_IPV6            = Keyword("src-ipv6")
SRC_PORT            = Keyword("src-port")
TABLE               = Keyword("table")
TABLEARG            = Keyword("tablearg")
TCPACK              = Keyword("tcpack")
TCPDATALEN          = Keyword("tcpdatalen")
TCPFLAGS            = Keyword("tcpflags")
TCPOPTION           = Keyword("tcpoption")
TCPSEQ              = Keyword("tcpseq")
TCPWIN              = Keyword("tcpwin")
TEE                 = Keyword("tee")
TO                  = Keyword("to")
UID                 = Keyword("uid")
UNREACH             = Keyword("unreach")
UNREACH6            = Keyword("unreach6")
VERREVPATH          = Keyword("verrevpath")
VERSRCREACH         = Keyword("versrcreach")
VIA                 = Keyword("via")
XMIT                = Keyword("xmit")
IP                  = Keyword("ip")
TCP                 = Keyword("tcp")
UDP                 = Keyword("udp")
DIVERT              = Keyword("divert")

# start of the language
TABLEID             = P.Group(TABLE + LPAREN + TABLENO + RPAREN) # group
#TABLEID.setParseAction(RuleFactory.getParseAction('tableid', 1)) # PA

#in the real world, you would have to parse/import /etc/protocols
PROTO               = P.oneOf("""ip icmp igmp ggp ipencap st2 tcp cbt egp igp 
bbn-rcc nvp pup argus emcon xnet chaos udp mux dcn hmp prm xns-idp trunk-1
trunk-2 leaf-1 leaf-2 rdp irtp iso-tp4 netblt mfe-nsp merit-inp sep 3pc idpr xtp
ddp idpr-cmtp tp++ il ipv6 sdrp ipv6-route ipv6-frag idrp rsvp gre mhrp bna esp
ah i-nlsp swipe narp mobile tlsp skip ipv6-icmp ipv6-nonxt ipv6-opts cftp
sat-expak kryptolan rvd ippc sat-mon visa ipcv cpnx cphb wsn pvp br-sat-mon
sun-nd wb-mon wb-expak iso-ip vmtp secure-vmtp vines ttp nsfnet-igp dgp tcf eigrp
ospf sprite-rpc larp mtp ax.25 ipip micp scc-sp etherip encap gmtp ifmp pnni pim
aris scps qnx a/n ipcomp snp compaq-peer ipx-in-ip vrrp pgm l2tp ddx iatp st srp
uti smp sm ptp isis fire crtp crdup sscopmce iplt sps pipe sctp fc divert
 """)
PORTCOM             = PORTNO + P.ZeroOrMore( COMMA + PORTNO)
PORTRNG             = PORTNO + DASH + PORTNO
PORT                = PORTRNG | PORTCOM #g

PROTO.setParseAction(RuleFactory.getParseAction('proto')) # PA
# ip and ports
#DOTTED              = IPPART + DOT + IPPART + DOT + IPPART + DOT + IPPART # group
DOTTED              = P.Regex("\d+\.\d+\.\d+\.\d+")
DOTTED.Name = "Dotted"
MASK                = (SLASH + CIDR) | (COLON + DOTTED) | (COMMA + PORTNO)
MASK.Name = "Mask"
IPLISTP              = P.Group(DOTTED + P.Optional(MASK)) # group
IPLIST              = IPLISTP + P.ZeroOrMore(COMMA + IPLISTP)
IPADDR              = P.Group(P.Optional(NOT) + (ANY + P.Optional(PORT)| ME | TABLEID('tableid') | IPLIST('iplist') | TABLEARG)) #group
IPADDR.Name = "Ipaddr"

#PORT.setParseAction(RuleFactory.getParseAction('port'))

# address skip MAC and v6 for now
ADDRPORTN = P.Group((IPADDR + P.Optional(COMMA + PORTNO)) | PORTNO)
FROMADDR = P.Group(ADDRPORTN | LBRACE + ADDRPORTN + P.ZeroOrMore(OR + ADDRPORTN) + RBRACE)
FROMADDR.setParseAction(RuleFactory.getParseAction('from'))
ADDRPORT = P.Group((IPADDR + P.Optional(PORT)) | PORT )
ADDRPORT.setParseAction(RuleFactory.getParseAction('to'))
ADDR = PROTO + FROM + FROMADDR('from')  + TO + ADDRPORT('to') #g
#ADDR.setParseAction(RuleFactory.getParseAction('fulladdr', 0))
# interfaces right now, only em* and gre* : final system will have to be more clever
IFNUM               = P.Word(P.nums)
EM                  = P.Regex("em(\d+|\*)")
GRE                 = P.Regex("gre(\d+|\*)")
IFACE               = EM | GRE

# ICMPTYPES list
ICMLIST  = PORTNO + P.ZeroOrMore( COMMA + PORTNO)
IPIDLIST = PORTNO + P.ZeroOrMore( COMMA + PORTNO)

# skipping a bunch of options for now
OPTION = BRIDGED | DIVERTED | DIVERTED_LOOPBACK | DIVERTED_OUTPUT | (DST_IP | SRC_IP) + IPADDR | \
(DST_PORT | SRC_PORT) + PORT | ESTAB | FRAG | (GUID | UID) + UIDNO | ICMPTYPES + ICMLIST | IN | OUT | \
IPID + IPIDLIST | KEEP_STATE | LAYER2 | (RECV | XMIT | VIA) + (IFACE | IPADDR) | SETUP #g

OPTIONP = P.Group(P.Optional(NOT) + OPTION)
OPTIONP2 = LBRACE + OPTIONP + P.ZeroOrMore(OR + OPTIONP) + RBRACE
OPTFULL = OPTIONP | OPTIONP2

OPTION_LIST = P.Group(P.OneOrMore(OPTFULL('option')))
OPTION_LIST.setParseAction(RuleFactory.getParseAction('options')) # PA


LOGAMMOUNTNO = P.Word(P.nums, max=10)
LOGP = LOG + P.Optional(LOGAMOUNT + LOGAMMOUNTNO)
ALTQP = ALTQ + P.Word(P.alphanums)
PARAMS = P.Each(P.Optional(LOGP) + P.Optional(ALTQP))
PARAMS.setParseAction(RuleFactory.getParseAction('params'))

N = P.Word(P.nums)
XNAME = P.Word(P.alphanums)

ACTION = P.Group(CHECK_STATE | ALLOW | COUNT | DENY | UNREACH + P.Word(P.nums, max=3) | \
SKIPTO + LINENO | RESET | (DIVERT | TEE) + PORTNO | (FORWARD | FWD) + IPADDR | \
PIPE + (N | TABLEARG) | QUEUE + N | NAT + N | SETFIB + XNAME | REJECT)
ACTION.setParseAction(RuleFactory.getParseAction('action'))

RULE_BODY = CHECK_STATE + P.Optional(PARAMS) | ACTION('action') + P.Optional(PARAMS) + ADDR + P.Optional(OPTION_LIST)

ROOT = P.Group(LINENO + RULE_BODY)
#ROOT.setParseAction(RuleFactory.getParseAction('root'))

def parse_a_rule(a_line):
    factory = RuleFactory()
    res = ROOT.searchString(a_line)
    return factory.popRule()

if __name__ == "__main__":
    #with open('test.list') as f:
    with open('ipfw2.list') as f:
        test_lines = f.readlines()

    #test_lines = ['01242 deny ip from { 10.1.1.1 or not table(4) } to any']

    factory = RuleFactory()

    for a_line in test_lines:
        print "-"* 60
        print a_line.strip()
        res = ROOT('root').searchString(a_line)
        #pp(res)
        print
        #pp(res.copy().asList())
        #pp(res.copy().asDict())
        #pp(res.copy().items())
        a_rule = factory.popRule()
        print
        a_rule.dump()
        print


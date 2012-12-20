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

import sys
import os
import pygraphviz as gv
import bisect
from pprint import pprint as pp
import warnings
import networkx as nx
import parser
import ipaddr

END = 100000
ruleTable = [None] * (END + 1)

TERMINAL_VERBS = ['reject', 'allow', 'accept', 'pass', 'permit', 'deny', 'drop', 'divert','pipe','reset','reset6','unreach','unreach6']
VERB_COLOR = {
    'deny': 'crimson',
    'reject': 'crimson',
    'reset': 'deeppink',
    'check-state': 'blueviolet',
    'count': 'blueviolet',
    'allow': 'springgreen',
    'divert': 'yellow',
    'skipto': 'orange',
    'fwd': 'palegreen3',
    }

RULE_ENDERS = ["ip from any to any", "ip from any to any keep-state"]

class RuleTable:
    def __init__(self, name):
        self.g = gv.AGraph(directed=True, name=name)
        self.rules = {}
        self.rule_list = []

    # for debugging
    def DUMP(self):
        pp(self.rules)
        pp(self.rule_list)

    def add(self, aRule):
        # hack to deal with repeated rules
        while aRule.rule_num in self.rules:
            aRule.rule_num += 1
        self.rules[aRule.rule_num] = aRule
        self.rule_list.append(aRule.rule_num)

        # set node color
        color = VERB_COLOR.get(aRule.verb, 'black')
        if aRule.all_packets and aRule.terminal:
            # this ends all traffic
            self.g.add_node(aRule.rule_num, label=aRule.raw_line, color=color, fontname='Courier', penwidth='4.0', shape='box')
        elif aRule.terminal:
            # this might end some traffic
            self.g.add_node(aRule.rule_num, label=aRule.raw_line, color=color, fontname='Courier', penwidth='2.0')
        elif aRule.all_packets:
            # this Probably catches all packets
            self.g.add_node(aRule.rule_num, label=aRule.raw_line, color=color, fontname='Courier', penwidth='2.0')
        else:
            self.g.add_node(aRule.rule_num, label=aRule.raw_line, color=color, fontname='Courier', penwidth='1.0')

    def nextRule(self,aRuleNum):
        # find the next rule number after aRuleNum
        nr = bisect.bisect_left(self.rule_list, aRuleNum)
        return self.rule_list[nr]

    def reparse(self):
        # sort the rule list, add the edges
        # green for misses, black for matches
        self.rule_list.sort()
        END = self.rule_list[-1]
        for k,v in self.rules.items():
            v.reparse()
            if v.next: self.g.add_edge(k,v.next, color='black')
            if v.skip: self.g.add_edge(k, v.skip, color='green')

def bottom(listlike):
    if len(listlike) == 1:
        return bottom(listlike[0])
    else:
        return listlike

class PRule(object):
    # parsed rule
    def __init__(self, a_line):
        self.raw_line = a_line
        self.parsedRule = parser.parse_a_rule(a_line)
        self.processPR()

    def DUMP(self):
        print "-" * 60
        print self.raw_line
        for k,v in self.__dict__.items():
            if k[0] == 'P' and k[1] == '_':
                print k,v

    def processPR(self):
        for k,v in self.parsedRule.iteritems():
            fName = "do_" + k
            self.__getattribute__(fName)(v)
        self.findMatchOut()
        self.findMissOut()

    def findMatchOut(self):
        if 'P_action' not in self.__dict__:
            return
        if type(self.P_action) == list:
            verb = self.P_action[0]
        else:
            verb = self.P_action

        if verb in TERMINAL_VERBS:
            self.P_match_out = None
            return

        if not 'P_to' in self.__dict__:
            return

        if self.P_to == 'any':
            self.P_destip = ipaddr.IPNetwork("0.0.0.0/0")

        if self.P_from == 'any':
            self.P_srcip = ipaddr.IPNetwork("0.0.0.0/0")
        #in
        #srcip
        #srcports
        #destip
        #destport
        #ifaces

        #out
        #srcip
        #srcports
        #destip
        #destport
        #ifaces

    def findMissOut(self):
        pass

    def do_proto(self, tok):
        self.P_proto = tok[0]

    def do_from(self, tok):
        self.P_from = bottom(tok)

    def do_to(self, tok):
        self.P_to = bottom(tok)

    def do_options(self, tok):
        self.P_options = bottom(tok)

    def do_params(self, tok):
        self.P_params = bottom(tok)

    def do_action(self, tok):
        self.P_action = bottom(tok)

class Rule(object):
    def __init__(self, a_line, a_rule_table):
        self.raw_line = a_line
        self.rule_table = a_rule_table
        self.last = False
        self.parse()
        self.rule_table.add(self)
        self.prule = PRule(a_line)
        self.prule.DUMP()


    def parse(self):
        split_line = self.raw_line.split()
        self.rule_num = int(split_line[0])
        self.verb = split_line[1]
        self.next = None
        self.skip = None
        if self.verb == 'skipto': self.skip = int(split_line[2])
        if self.rule_num == END: self.last = True
        self.all_packets = self.allPacketsQ()
        self.terminal = self.terminalQ()

    def allPacketsQ(self):
        r0 = self.raw_line[-len(RULE_ENDERS[0]):] == RULE_ENDERS[0]
        r1 = self.raw_line[-len(RULE_ENDERS[1]):] == RULE_ENDERS[1]
        return r0 or r1

    def terminalQ(self):
        return self.verb in TERMINAL_VERBS

    def nextRule(self):
        if self.last: return None
        return self.rule_table.nextRule(self.rule_num)
        
    def reparse(self):
        if self.last: return
        
        if self.all_packets and self.terminal:
            self.next = None
        else:
            self.next = self.rule_table.nextRule(self.rule_num + 1)

        if self.skip and self.all_packets:
            self.next = None

        if self.skip:
            self.skip = self.rule_table.nextRule(self.skip)

        if not self.skip and not self.next:
            self.next = END

def help():
    print """
usage: ipfw-graph.py [rule-list-file]

rule-list-file is the result of:
ipfw -list > rule-list-file

outputs a png of the rules (very large) and a dot file, which can be fed
into a variety of graph viewing software (graphviz works well)
"""

def main(args):
    if len(args) < 2:
        print "please supply file name"
        return
        

    f_name = args[1]

    if f_name[-5:] == ".list":
        f_name = f_name[:-5]

    with open(f_name + ".list") as f:
        lines = f.readlines()

    rl = RuleTable(f_name)
    # add fake start and end
    #Rule('00000 allow ip from any to any',rl)
    #Rule('100000 deny ip from any to any',rl)
    for a_line in lines:
        Rule(a_line.strip(), rl)
    rl.reparse()

    #rl.g.string()
    rl.g.write(f_name + ".dot")
    #rl.g.layout('dot')
    #rl.g.draw(f_name + '.png')

    os.system("dotty " + f_name + ".dot")

    #rl.g.name = f_name
    #nxg = nx.from_agraph(rl.g)
    #foo = nxg.nodes()
    #foo.sort()
    #print foo
    #paths = find_all_paths(nxg,'0', '100000')
    #pp(paths)
    #print
    #print len(paths)

    #return rl.g

def find_all_paths(graph, start, end):
    path  = []
    paths = []
    queue = [(start, end, path)]
    while queue:
        start, end, path = queue.pop()
        #print 'PATH', path

        path = path + [start]
        if start == end:
            paths.append(path)
        for node in set(graph[start]).difference(path):
            queue.append((node, end, path))
    return paths

if __name__ == '__main__':
    # ignore Graphviz warning messages
    warnings.simplefilter('ignore', RuntimeWarning)

    main(sys.argv)

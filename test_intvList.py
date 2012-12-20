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

from intvList import *

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

    if False:
        print "TEST1"
        i = IntvList()
        print i
        print i.add_(r1)
        print i.add_(r3)
        print i.add_(r2)
        print i.add_(ALL)
        print

    if 0:
        print "TEST2"
        i = IntvList()
        print i
        print i.add_(r1)
        print i.add_(r4)
        print i.add_(p2)
        print i.add_(p3)
        print i.add_(r4)
        print i.add_(r5)
        print i.add_(r6)
        print i.add_(ALL)

    if 0:
        print "TEST3"
        i = IntvList()
        print i
        print i.add_(r1)
        print i.add_(r4)
        print i.add_(p2)
        print i.add_(p3)
        print i.add_(r4)
        print i.add_(r5)
        print i.add_(r6)
        print i.add_(r7)


    import itertools
    pr = PortRange
    p  = Port
    
    if 0:
        print "test4"
        r1 = pr(1,20)
        r2 = pr(10,30)
        r3 = pr(21,40)
        r4 = pr(31, 35)
        p1 = p(11)
        p2 = p(30)
        p3 = p(29)
        lall = [r1,r2,r3,r4,p1,p2,p3]
        perm = itertools.permutations(lall, len(lall))
        
        for lv in perm:
            print
            print lv
            i = IntvList()
            for v in lv:
                print i , "plus ", v,
                print "---->",i.add_(v)
                print
            
    import random
    ri = random.randint

    if 0:
        minp = MINP
        maxp = 4 
        for i in range(100):
            def randos():
                start = ri(minp, maxp - 2)
                end   = ri(start + 1, maxp)
                return (start, end)
            start,end = randos()
            r1 = pr(start,end)
            start,end = randos()
            r2 = pr(start,end)
            start,end = randos()
            r3 = pr(start,end)
            start,end = randos()
            r4 = pr(start,end)
            p1 = p(ri(minp,maxp))
            p2 = p(ri(minp,maxp))
            p3 = p(ri(minp,maxp))
            p4 = p(ri(minp,maxp))


            lall = [r1,r2,r3,r4,p1,p2,p3,p4]
            perm = itertools.permutations(lall, len(lall))

            for lv in perm:
                print
                print lv
                i = IntvList()
                for v in lv:
                    print i , "plus ", v,
                    print "---->",i.add_(v)

    if 0:
        i = IntvList()
        p1 = p(10)
        p2 = p(2)
        p3 = p(8)
        lv = [p1,p2,p2]
        for v in lv:
            print i , "plus ", v,
            print "---->",i.add_(v)

    def testadd(a,b):
        print a , "plus ", b,
        print "---->",a.add_(b)

    def testrem(a,b):
        print a , "remove ", b,
        print "---->",a.remove_(b)

    if 1:
        #actual targetted tests
        r1 =  pr(100,  200)
        r2 =  pr(300,  400)
        r3 =  pr(500,  600)
        r4 =  pr(700,  800)
        r5 =  pr(900,  1000)
        r6 =  pr(1100, 1200)

        r7 =  pr(150,  250)
        r8 =  pr(500,  600)
        r9 =  pr(700,  1000)
        r10 = pr(1000, 1100)

        
        i = IntvList()
        testadd(i, r1)
        testadd(i, r1)
        testadd(i, r2)
        testadd(i, r3)
        testadd(i, r4)
        testadd(i, r5)
        testadd(i, r6)
        testadd(i, r7)
        testadd(i, r8)
        testadd(i, r9)
        testadd(i, r10)

    if 0:

        r1 =  pr(100,  200)
        r2 =  pr(300,  400)
        r3 =  pr(500,  600)
        r4 =  pr(700,  800)
        r5 =  pr(900,  1000)
        r6 =  pr(1100, 1200)

        r7 =  pr(150,  250)
        r8 =  pr(500,  600)
        r9 =  pr(700,  1000)
        r10 = pr(1000, 1100)

        i = IntvList()
        i.add_(r1).add_(r2).add_(r3).add_(r4).add_(r5).add_(r6)
        print i
        print i[2:4]
        print i[2]
        print i[4]
        i[2:4] = [i[2]]
        print i


    if 0:
        #actual targetted tests
        rall = pr(1,1500)
        r1 =  pr(100,  200)
        r2 =  pr(300,  400)
        r3 =  pr(500,  600)
        r4 =  pr(700,  800)
        r5 =  pr(900,  1000)
        r6 =  pr(1100, 1200)

        r7 =  pr(150,  250)
        r8 =  pr(500,  600)
        r9 =  pr(700,  1000)
        r10 = pr(1000, 1100)

        
        i = IntvList()
        i.add_(rall)
        print i
        testrem(i, r1)
        testrem(i, r2)
        testrem(i, r3)
        testrem(i, r4)
        testrem(i, r5)
        testrem(i, r6)
        testrem(i, r7)
        testrem(i, r8)
        testrem(i, r9)
        testrem(i, r10)

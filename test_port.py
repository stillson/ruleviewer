#!/usr/bin/env python


from port import *
from pprint import pprint as pp

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

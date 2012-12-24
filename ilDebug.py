import pprint

pp = pprint.pprint
formatter = pprint.PrettyPrinter()
def pformit(*v):
    def myppf(x):
        fval = formatter.pformat(x)
        return fval + " "

    return reduce(lambda x,y: x+y, map(myppf, v))

def formit(*v):
    def myppf(x):
        fval = str(x)
        return fval + " "

    return reduce(lambda x,y: x+y, map(myppf, v))

def dbP(flag, *v):
    if flag: print formit(*v)

def dbPn(flag, *v):
    if flag: print formit(*v),

def dbPP(flag, *v):
    if flag: print pformit(*v)

def dbPPn(flag, *v):
    if flag: print pformit(*v),

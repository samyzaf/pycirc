from .util import *

# Logic Operators to be used for building Logic Cells
# a = an Assign object with input name like: x1, x2, ..., xn
# o = an Assign object with input name like: x1, x2, ..., xn
# but it can be changed to whatever key names a client user chooses

def ZERO(a=None, output="y"):
    o = Assign(output)
    for y in o: o[y] = 0
    return o

def ONE(a=None, output="y"):
    o = Assign(output)
    for y in o: o[y] = 1
    return o

def NOT(a=Assign("x"), output="y"):
    o = Assign(output)
    for x,y in zip(a.names, o.names):
        o[y] = 1 - a[x]
    return o

def AND(a, output="y"):
    o = Assign(output)
    for x in a:
        if a[x] == 0:
            for y in o: o[y] = 0
            return o
    for y in o: o[y] = 1
    return o

def OR(a, output="y"):
    o = Assign(output)
    for x in a:
        if a[x] == 1:
            for y in o: o[y] = 1
            return o
    for y in o: o[y] = 0
    return o

def NOR(a, output="y"):
    o = OR(a, "y")
    b = Assign("x", o["y"])
    return NOT(b, output)

def NAND(a, output="y"):
    o = AND(a, "y")
    b = Assign("x", o["y"])
    return NOT(b, output)

def XOR(a, output="y"):
    o = Assign(output)
    if sum(a[x] for x in a) == 1:
        for y in o: o[y] = 1
        return o
    else:
        for y in o: o[y] = 0
        return o

def XNOR(a, output="y"):
    o = XOR(a, "y")
    b = Assign("x", o["y"])
    return NOT(b, output)

def MUX(a, output="y"):
    sel = [name for name in a if name[0]=="s"]
    bits = [name for name in a if name[0]=="x"]
    sel.sort(key=lambda x: int(x[1:]))
    bits.sort(key=lambda x: int(x[1:]))
    s = [str(a[k]) for k in sel]
    s = "".join(s)
    i = int(s, 2)
    o = Assign(output, a[bits[i]])
    return o


import os
from .logops import *
from .pycirc import *
from urllib.request import urlopen, Request
from collections import deque
#import requests

# A client code must define the library path
# The library path consists of a list of directories or URL's
# from which PyCirc can find a cell.
# Example:
#   set_libpath([os.path.join(os.path.realpath("."), "lib"), "https://samyzaf.com/pycirc/lib", "d:/eda/pycirc/lib"]

libpath = deque()

def set_libpath(pathlist):
    global libpath
    libpath.clear()
    for p in pathlist:
        libpath.append(p)

def libpath_append(path):
    global libpath
    if not path in libpath:
        libpath.append(p)

def list_lib_circs():
    global libpath
    circs = []
    for d in libpath:
        if "https://" in d:
            files = list_url_files(url)
        else:
            files = os.listdir(d)
        for file in files:
            if fnmatch(file, '*.py'):
                circ = file[:-3]
                circs.append(circ)
    return circs

# Load cell file to libraries libs.
# Usually a file contains one cell definition,
# but may contain multiple cells as well.
def load(cell, libs=[pycircLib]):
    global libpath
    try:
        libpath
    except:
        print("Cell library path not defined")
        print("Please define cell library path: set_libpath([dir1, dir2, url1, ...])")
        #raise Exception("Cell library path not defined")
        
    print("libpath =", libpath)
    foundfile = False
    for dir in libpath:
        dir = dir.rstrip("/")
        libfile = "%s/%s.py" % (dir, cell)
        if "https://" in libfile:
            try:
                u = urlopen(libfile)
                code = u.read().decode('utf-8')
                foundfile = True
                break
            except:
                pass
                #print("Failed to load %s" % (libfile,)
        else:
            if os.path.isfile(libfile):
                with open(libfile) as f:
                    code = f.read()
                    foundfile = True
                    break
    if foundfile:
        exec(code)
        print("Loaded cell %s from: %s" % (cell,libfile))
    #elif pycircLib.exists(cell):
    #    return pycircLib.get(cell)
    #else:
    #    raise Exception("Cell %s not found in library path: %s" % (cell,libpath))

def need(cellname):
    if pycircLib.exists(cellname):
        return
    load(cellname)

def logcirc(name, gates, wires, register=True):
    circ = PyCirc(name, gates, wires)
    if register:
        pycircLib.add_circ(circ)
    return circ

# Start definition of a Logic Circuit
def Define(cellname):
    global active_cell
    if "active_cell" in globals() and active_cell is not None:
        raise Exception("You must complete a definition before starting a new one!")
    active_cell = cellname
    Gate.markers[0] = Gate.id
    Wire.markers[0] = Wire.id

# Finalize PyCirc object and add it to libraries in list libs
# Use libs = [] to not add it to any library
# Currently we have only one library pycircLib but future dev may have multiple ...
def EndDef(libs=[pycircLib]):
    global active_cell
    Gate.markers[1] = Gate.id
    Wire.markers[1] = Wire.id
    a,b = Gate.markers
    gates = list()
    for obj in gc.get_objects():
        if isinstance(obj, Gate) and a <= obj.id < b:
            gates.append(obj)
    wires = list()
    a,b = Wire.markers
    for obj in gc.get_objects():
        #if isinstance(obj, Wire) and obj.gate1 in gates and obj.gate2 in gates:
        if isinstance(obj, Wire) and a <= obj.id < b:
            wires.append(obj)
    circ = PyCirc(active_cell, gates, wires)
    for lib in libs:
        lib.add_circ(circ)
    #print("active_cell =", active_cell)
    active_cell = None
    return circ

#-------------------------------------------------------------------------

# These are standard logical cells which we add to pycircLib first:
pycircLib.add_box(name="zero", operator=ZERO, input=[], output=["y"], type="const", depth=0)
pycircLib.add_box(name="one",  operator=ONE,  input=[], output=["y"], type="const", depth=0)
pycircLib.add_box(name="not",  operator=NOT,  input=["x"], output=["y"])
pycircLib.add_box(name="and2", operator=AND,  input="x<1:2>", output=["y"])
pycircLib.add_box(name="and3", operator=AND,  input="x<1:3>", output=["y"])
pycircLib.add_box(name="and4", operator=AND,  input="x<1:4>", output=["y"])
pycircLib.add_box(name="and5", operator=AND,  input="x<1:5>", output=["y"])
pycircLib.add_box(name="and6", operator=AND,  input="x<1:6>", output=["y"])
pycircLib.add_box(name="and7", operator=AND,  input="x<1:7>", output=["y"])
pycircLib.add_box(name="and8", operator=AND,  input="x<1:8>", output=["y"])

# We can also use loops to add cells to our cell library
for k in range(2,9):
    inp = "x<1:%s>" % (k,)
    name = "or" + str(k)
    pycircLib.add_box(name, operator=OR, input=inp, output=["y"])
    name = "xor" + str(k)
    pycircLib.add_box(name, operator=XOR, input=inp, output=["y"])
    name = "nor" + str(k)
    pycircLib.add_box(name, operator=NOR, input=inp, output=["y"])
    name = "nand" + str(k)
    pycircLib.add_box(name, operator=NAND, input=inp, output=["y"])

pycircLib.add_box(name="mux1", operator=MUX, input=["s1", "x0", "x1"], output=["y"], depth=3)
# The following will be defined by a PyCirc circuit:
#pycircLib.add_box(name="mux2", operator=MUX, input=["s1", "s2", "x0", "x1", "x2", "x3"], output=["y"], depth=4)
#pycircLib.add_box(name="mux3", operator=MUX, input=["s1", "s2", "s3", "x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7"], output=["y"], depth=5)

# We can can many more MUX cells with the following loop
# for k in range(1,10):
#     name = "mux" + str(k)
#     inp = "x<0:%s> ; s<1:%s>" % (2**k - 1, k)
#     pycircLib.add_box(name=name, operator=MUX, input=inp, output=["y"])


def list_url_files(url):
    urlpath = urlopen(url)
    string = urlpath.read().decode('utf-8')
    pattern = re.compile('[a-zA-Z0-9_]+.py') #the pattern actually creates duplicates in the list
    filelist = list(set(pattern.findall(string)))
    return filelist

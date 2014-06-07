import os.path
import shutil
import math

class Vec:
    def __init__(self, x=0, y=None, z=None):
        if (y and z) is None:
            self.x, self.y, self.z, = (x, x, x)
        else:
            self.x, self.y, self.z, = (x, y, z)

    def str(self):
        return "{0} {1} {2}".format(self.x, self.y, self.z)

    def __add__(self, other):
        v = Vec()
        if type(other) is Vec:
            v.x = self.x + other.x
            v.y = self.y + other.y
            v.z = self.z + other.z
        elif type(other) is int:
            v.x = self.x + other
            v.y = self.y + other
            v.z = self.z + other
        return v

    def __sub__(self, other):
        v = Vec()
        if type(other) is Vec:
            v.x = self.x - other.x
            v.y = self.y - other.y
            v.z = self.z - other.z
        elif type(other) is int:
            v.x = self.x - other
            v.y = self.y - other
            v.z = self.z - other
        return v

    def __mul__(self, other):
        v = Vec()
        if type(other) is Vec:
            v.x = self.x * other.x
            v.y = self.y * other.y
            v.z = self.z * other.z
        elif type(other) is int:
            v.x = self.x * other
            v.y = self.y * other
            v.z = self.z * other
        return v

    def __div__(self, other):
        v = Vec()
        if type(other) is Vec:
            v.x = self.x / other.x
            v.y = self.y / other.y
            v.z = self.z / other.z
        elif type(other) is int:
            v.x = self.x / other
            v.y = self.y / other
            v.z = self.z / other
        return v

    def __truediv__(self, other):
        return self.__div__(other)

    def rotate(self, origin, axis, angle):
        angle = math.radians(angle)
        if (axis == 'x'):
            x = self.x
            y = ((self.y - origin.y) * math.cos(angle)) - ((origin.z - self.z) * math.sin(angle)) + origin.y
            z = ((self.z - origin.z) * math.cos(angle)) + ((origin.y - self.y) * math.sin(angle)) + origin.z
        elif (axis == 'y'):
            x = ((self.x - origin.x) * math.cos(angle)) - ((origin.z - self.z) * math.sin(angle)) + origin.x
            y = self.y
            z = ((self.z - origin.z) * math.cos(angle)) + ((origin.x - self.x) * math.sin(angle)) + origin.z
        elif (axis == 'z'):
            x = ((self.x - origin.x) * math.cos(angle)) - ((origin.y - self.y) * math.sin(angle)) + origin.x
            y = ((self.y - origin.y) * math.cos(angle)) + ((origin.x - self.x) * math.sin(angle)) + origin.y
            z = self.z

        self.x = x
        self.y = y
        self.z = z
        return self

    def magnitude(self):
        mag = math.sqrt(pow(self.x,2) + pow(self.y,2) + pow(self.z,2))
        return mag

    def normalize(self):
        nvec = Vec()

        mag = self.magnitude()

        nvec.x = self.x/mag
        nvec.x = self.y/mag
        nvec.x = self.z/mag

        return nvec


class CfgBuilder:
    fnum = 0
    fnames = list()
    lines = list()

    def __init__(self, name, wait=200):
        self.name = name
        self.wait = wait
        return

    def appendLine(self, line):
        self.lines.append(line+"\n")
        return

    def rawCmd(self, cmd):
        self.appendLine(cmd)
        return

    def build(self):
        def filename():
            fname = "{0}/gen{1}.cfg".format(self.name, self.fnum)
            self.fnames.append(fname)
            return fname

        if not os.path.exists(self.name):
            os.makedirs(self.name)
        else:
            shutil.rmtree("{0}/".format(self.name), True)
            os.makedirs(self.name)

        f = open(filename(), "w")

        for lc, line in enumerate(self.lines):
            # if 30 lines were read, open new file for writing
            if ((lc+1)%30 == 0):
                f.close()
                self.fnum += 1
                f = open(filename(), "w")

            # write line to file
            f.write(line)

        wait = 0
        f = open("pycfg_{0}.cfg".format(self.name), "w")
        for name in self.fnames:
            f.write("wait {0}; exec {1}\n".format(wait, name))
            wait += self.wait
        f.write("wait {0}; echo done!\n".format(wait))
        f.close()
        return


class Entity:
    flags = 0

    def __init__(self, cfg, entname, name, kvs=dict()):
        self.cfg = cfg
        self.entname = entname
        self.name = name
        self.__kvs = kvs
        return

    def out(self, line):
        if (self.cfg):
            self.cfg.appendLine(line)
        else:
            print(line)
        return

    def create(self):
        cname = self.name
        if (self.cfg):
            cname = self.cfg.name

        line = "ent_create {0} targetname \"{1}\" classname \"{2}\" spawnflags {3}".format(self.entname, self.name, cname, self.flags)
        if (len(self.__kvs) > 0):
            for key, value in self.__kvs.items():
                line += " {0} \"{1}\"".format(key, value)
        self.out(line)
        return

    def fireInput(self, iput, args=None):
        line = "ent_fire {0} {1}".format(self.name,iput)
        if args != None:
            line += " \"{0}\"".format(args)
        self.out(line);
        return

    def setKeyvalue(self, key, value):
        self.fireInput("addoutput", "{0} {1}".format(key, value))
        return

    def setSpawnflags(self, flags):
        self.flags = flags
        self.setKeyvalue("spawnflags", self.flags)
        return

    def buildOPstring(self, otarg, action, args, delay, refiretime):
        return "{0},{1},{2},{3},{4}".format(otarg, action, args, delay, refiretime)

    def addOutput(self, output, otarg, action, args=None, delay="0.0", refiretime="-1"):
        if args is None:
            args = ""
        s = self.buildOPstring(otarg, action, args, delay, refiretime)
        self.setKeyvalue(output, s)
        return

    def parentTo(self, targ=None):
        if issubclass(type(targ), Entity):
            targ = targ.name

        self.fireInput("setparent", targ)
        return


class Sprite(Entity):
    def __init__(self, cfg, name, texture, kvs=dict()):
        kvs["model"] = texture
        Entity.__init__(self, cfg, "env_sprite", name, kvs)
        return


class Spritetrail(Entity):
    def __init__(self, cfg, name, texture, kvs=dict()):
        kvs["spritename"] = texture
        Entity.__init__(self, cfg, "env_spritetrail", name, kvs)
        return


class Prop(Entity):
    def __init__(self, cfg, proptype, name, model, kvs=dict()):
        kvs["model"] = kvs
        if "solid" not in kvs:
            kvs["solid"] = 6
        Entity.__init__(self, cfg, "prop_{0}".format(proptype), name, kvs)
        return


class Brush(Entity):
    def __init__(self, cfg, entname, name, maxs, mins=None, kvs=dict()):
        # if we omited mins, make us a cube
        if (mins == None):
            mins=Vec(-maxs.x,
                    -maxs.y,
                    -maxs.z)

        # fill the keyvalues
        kvs["solid"] = 2

        # store our dimensions
        self.__mins = mins
        self.__maxs = maxs

        Entity.__init__(self, cfg, entname, name, kvs)
        return

    def create(self):
        Entity.create(self)
        self.setKeyvalue("mins", self.__mins.str())
        self.setKeyvalue("maxs", self.__maxs.str())
        return


class Trigger(Brush):
    def __init__(self, cfg, triggertype, name, maxs, mins=None, kvs=dict()):
        Brush.__init__(self, cfg, "trigger_{0}".format(triggertype), name, maxs, mins)
        return

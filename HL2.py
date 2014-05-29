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

    def add(self, val):
        self.x += val.x
        self.y += val.y
        self.z += val.z
        return self

    def sub(self, val):
        self.x -= val.x
        self.y -= val.y
        self.z -= val.z
        return self

    def mul(self, val):
        self.x *= val.x
        self.y *= val.y
        self.z *= val.z
        return self

    def div(self, val):
        self.x /= val.x
        self.y /= val.y
        self.z /= val.z
        return self

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


class CfgBuilder:
    fnum = 0
    fnames = list()
    lines = list()

    def __init__(self, name, wait=200):
        self.name = name
        self.wait = wait

    def appendLine(self, line):
        self.lines.append(line+"\n")

    def rawCmd(self, cmd):
        self.appendLine(cmd)

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

        lc = 1
        for line in self.lines:
            # if 30 lines were read, open new file for writing
            if (lc%30 == 0):
                f.close()
                self.fnum += 1
                f = open(filename(), "w")
            lc += 1

            # write line to file
            f.write(line)

        wait = 0
        f = open("pycfg_{0}.cfg".format(self.name), "w")
        for name in self.fnames:
            f.write("wait {0}; exec {1}\n".format(wait, name))
            wait += self.wait
        f.write("wait {0}; echo done!\n".format(wait))
        f.close()


class Entity:
    def __init__(self, cfg, entname, name, spawnkvs=dict()):
        self.cfg = cfg
        self.entname = entname
        self.name = name
        self.spawnkvs = spawnkvs

    def out(self, line):
        if (self.cfg):
            self.cfg.appendLine(line)
        else:
            print(line)

    def create(self):
        cname = self.name
        if (self.cfg):
            cname = self.cfg.name

        line = "ent_create {0} targetname \"{1}\" classname \"{2}\"".format(self.entname, self.name, cname)
        if (len(self.spawnkvs) > 0):
            for key, value in self.spawnkvs.items():
                line += " {0} \"{1}\"".format(key, value)
        self.out(line)

    def fireInput(self, iput, args=None):
        line = "ent_fire {0} {1}".format(self.name,iput)
        if args != None:
            line += " \"{0}\"".format(args)
        self.out(line);

    def setKeyvalue(self, key, value):
        self.fireInput("addoutput", "{0} {1}".format(key, value))

    def buildOPstring(self, otarg, action, args, delay, refiretime):
        return "{0},{1},{2},{3},{4}".format(otarg, action, args, delay, refiretime)

    def addOutput(self, output, otarg, action, args="", delay="0.0", refiretime="-1"):
        s = self.buildOPstring(otarg, action, args, delay, refiretime)
        self.setKeyvalue(output, s)

    def parentTo(self, targ=None):
        if issubclass(type(targ), Entity):
            targ = targ.name

        self.fireInput("setparent", targ)


class Sprite(Entity):
    def __init__(self, cfg, name, texture):
        Entity.__init__(self, cfg, "env_sprite", name, {
            "model": texture})


class Spritetrail(Entity):
    def __init__(self, cfg, name, texture):
        Entity.__init__(self, cfg, "env_spritetrail", name, {
            "spritename": texture})


class Prop(Entity):
    def __init__(self, cfg, proptype, name, model):
        Entity.__init__(self, cfg, "prop_{0}".format(proptype), name, {
            "model": model,
            "solid": 6})


class Brush(Entity):
    def __init__(self, cfg, entname, name, maxs, mins=None):
        if (mins == None):
            mins=Vec(-maxs.x,
                    -maxs.y,
                    -maxs.z)

        Entity.__init__(self, cfg, entname, name, {
            "solid": "2",
            "maxs": maxs.str(),
            "mins": mins.str()})


class Trigger(Brush):
    def __init__(self, cfg, triggertype, name, maxs, mins=None):
        Brush.__init__(self, cfg, "trigger_{0}".format(triggertype), name, maxs, mins)

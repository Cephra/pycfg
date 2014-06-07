import cfgfile
import cfgmath

class Entity:
    flags = 0

    def __init__(self, cfg, entname, name, kvs=dict()):
        self.__cfg = cfg
        self.entname = entname
        self.name = name
        self.__kvs = kvs
        return

    def out(self, line):
        if (self.__cfg):
            self.__cfg.appendLine(line)
        else:
            print(line)
        return

    def create(self):
        cname = self.name
        if (self.__cfg):
            cname = self.__cfg.name

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
            mins=cfgmath.Vec(-maxs.x,
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

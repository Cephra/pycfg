import os.path
import shutil

class Vec:
    def __init__(self, x=0, y=None, z=None):
        self.x = x
        if (y and z) is None:
            self.y = x
            self.z = x
        else:
            self.y = y
            self.z = z
        return

    def str(self):
        return "{0} {1} {2}".format(self.x, self.y, self.z)

<<<<<<< Updated upstream
=======
    #TODO: This introduces rounding errors faster than expected. Find and fix.
    def rotate(self, origin, axis, angle):
        angle = math.radians(angle)
        if (axis == 'x'):
            self.y = ((self.y - origin.y) * math.cos(angle)) - ((origin.z - self.z) * math.sin(angle)) + origin.y
            self.z = ((self.z - origin.z) * math.cos(angle)) + ((origin.y - self.y) * math.sin(angle)) + origin.z
        elif (axis == 'y'):
            self.x = ((self.x - origin.x) * math.cos(angle)) - ((origin.z - self.z) * math.sin(angle)) + origin.x
            self.z = ((self.z - origin.z) * math.cos(angle)) + ((origin.x - self.x) * math.sin(angle)) + origin.z
        elif (axis == 'z'):
            self.x = ((self.x - origin.x) * math.cos(angle)) - ((origin.y - self.y) * math.sin(angle)) + origin.x
            self.y = ((self.y - origin.y) * math.cos(angle)) + ((origin.x - self.x) * math.sin(angle)) + origin.y
        return
>>>>>>> Stashed changes

class CfgBuilder:
    fnum = 0
    fnames = list()
    lines = list()

    def __init__(self, name, wait=200):
        self.name = name
        self.wait = wait
        return

    def appendLine(self, line):
        self.lines.append(line)

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
<<<<<<< Updated upstream
        f.write("wait {0};echo done!\n".format(wait))
=======
        f.write("wait {0};echo {1}\n".format(wait,self.name))
>>>>>>> Stashed changes
        f.close()


class Entity:
    def __init__(self, cfg, entname, name, prekeyvals=dict()):
        self.cfg = cfg
        self.entname = entname
        self.name = name
        self.prekeyvals = prekeyvals

    def out(self, line):
        if (self.cfg):
            self.cfg.appendLine(line+"\n")
        else:
            print(line)


    def create(self):
        line = "ent_create {0} targetname \"{1}\" classname \"{2}\"".format(self.entname, self.name, self.cfg.name)
        if (len(self.prekeyvals) > 0):
            for key, value in self.prekeyvals.items():
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


class Prop(Entity):
    def __init__(self, cfg, entname, name, model):
        Entity.__init__(self, cfg, "prop_{0}".format(entname), name,{
            "model": model,
            "solid": 6})

import os.path
import shutil

class Vector:
    def __init__(self, x=0, y=None, z=None):
        return


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
        f = open("exec_{0}.cfg".format(self.name), "w")
        f.write("alias {0} \"ent_fire {0} kill;setinfo {0} off\"\n".format(self.name))
        f.write("{0}\n\n".format(self.name))
        for name in self.fnames:
            f.write("wait {0}; exec {1}\n".format(wait, name))
            wait += self.wait
        f.write("\nwait {0};setinfo {1} on\n".format(wait,self.name))
        f.write("wait {0};echo {1}\n".format(wait,self.name))
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
        line = "ent_create {0} classname \"{1}\" targetname \"{2}\"".format(self.entname, self.cfg.name, self.name)
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


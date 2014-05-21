class CfgBuilder:
    def __init__(self):
        self.lines = list()

    def appendLine(self, line):
        self.lines.append(line)

    def build(self):
        self.fnum = 0 # number of files

        f = open("gen{0}".format(self.fnum), "w")

        lc = 0 # line count
        for line in self.lines:
            lc += 1 # increment lines by 1

            # if 30 lines were read, open new file for writing.
            if (lc%30 == 0):
                f.close()
                self.fnum += 1
                f = open("gen{0}".format(self.fnum), "w")

            # write line to file
            f.write(line)

class Entity:
    def __init__(self, cfgfile, name, tname, model = ""):
        self.cfg = cfgfile
        self.name = name
        self.tname = tname
        self.model = model

    def out(self, line):
        if (self.cfg):
            self.cfg.appendLine(line+"\n")
        else:
            print(line)


    def create(self):
        line = "ent_create {0} targetname \"{1}\"".format(self.name, self.tname)
        if (self.model != ""):
            line += " model \"{0}\"".format(self.model)
            line += " solid 6"
        self.out(line)

    def fireInput(self, iput, args = ""):
        line = "ent_fire {0} {1} \"{2}\"".format(self.tname,iput,args)
        self.out(line);

    def setKeyvalue(self, key, value):
        self.fireInput("addoutput", "{0} {1}".format(key, value))

    def buildOPstring(self, otarg, action, args, delay, refiretime):
        return "{0},{1},{2},{3},{4}".format(otarg, action, args, delay, refiretime)

    def addOutput(self, output, otarg, action, args = "", delay = "0.0", refiretime = "-1"):
        s = self.buildOPstring(otarg, action, args, delay, refiretime)
        self.setKeyvalue(output, s)

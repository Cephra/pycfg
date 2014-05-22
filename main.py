import math
import HL2

cfg = HL2.CfgBuilder()

#ent = HL2.Entity(cfg, "prop_dynamic_override", "rotti", "models/props_junk/wood_crate001a.mdl")
#ent.create()
#
#for x in range(1,360):
#    ent.addOutput("onuser1", "!self", "addoutput",
#            "angles 0 {0} 0".format(x),
#            "{0:.6f}".format(0.001*x))
#
#ent.addOutput("onuser1", "!self", "fireuser1", 0, 0.001*360)
#ent.fireInput("fireuser1")
f = 1000
for x in range(0, 18, 1):
    for y in range(1,360, 15):
        ent = HL2.Entity(cfg,
                "prop_dynamic",
                "circ_{0}_{1}".format(x, y),
                "models/props_lab/blastdoor001c.mdl")
        ent.create()

        m = 600
        r = math.radians(y)
        coords = "{0} {1} ".format(
                500+math.cos(r)*m,
                math.sin(r)*m) + str(1200-53)
        ent.setKeyvalue("origin", coords)
        ent.setKeyvalue("angles", "0 {0} 0".format(y))
    ent = HL2.Entity(cfg,
            "info_target",
            "circm{0}".format(x))
    ent.create()
    ent.setKeyvalue("origin", "500 0 1200")
    ent.addOutput("onuser1", "circ_{0}_*".format(x), "setparent", "circm{0}".format(x), 0.1, 1)
    ent.addOutput("onuser1", "!self", "addoutput", "angles 0 0 {0}".format(10*x), 0.2, 1)
    ent.fireInput("fireuser1", "")

cfg.build()

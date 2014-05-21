import math
import HL2

cfg = HL2.CfgBuilder()

ent = HL2.Entity(cfg, "prop_dynamic_override", "rotti", "models/props_junk/wood_crate001a.mdl")
ent.create()

for x in range(1,73):
    ent.addOutput("onuser1", "!self", "addoutput",
            "angles 0 {0} 0".format(x*5),
            "{0:.6f}".format(0.001*x))

ent.addOutput("onuser1", "!self", "fireuser1", 0, 0.001*360)
ent.fireInput("fireuser1")

cfg.build()

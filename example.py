import HL2
import math

cfg = HL2.CfgBuilder("test")

for i in range(0,10):
    for x in range(0,36):
        prop = HL2.Prop(cfg,
                "dynamic",
                "preep{0}{1}".format(x,i),
                "models/roller.mdl")

        prop.create()

        rads = math.radians(x*10)
        prop.setKeyvalue("origin", "{0} {1} {2}".format(
            i*20,
            math.cos(rads)*100,
            200+math.sin(rads)*100))
        prop.setKeyvalue("rendercolor", "{0} {0} {0}".format(
            255*(i/10)))

ent = HL2.Entity(0, "env_spark", "asd")
ent.create()
ent.parentTo("bullshit")

cfg.build()

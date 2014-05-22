import HL2
import math

cfg = HL2.CfgBuilder("manysparks")

for x in range(0,36,1):
    ent = HL2.Entity(cfg,
            "env_spark",
            "spark{0}".format(x))
    ent.create()

    rad = 100
    rads = math.radians(x*10)
    coords = "{0} {1} 0".format(
                math.cos(rads)*rad,
                math.sin(rads)*rad
            )
    ent.setKeyvalue("origin", coords)

    ent.fireInput("startspark")

cfg.build()

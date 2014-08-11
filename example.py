import cfgents
import cfgfile
import cfgmath

# Create a script by the name "manysparks".
cfg = cfgfile.CfgBuilder("manysparks")

# Define the Origin and the Point we want to rotate.
o = cfgmath.Vec(0,0,0)
v = cfgmath.Vec(100,0,0)

# Rotate by 10 degrees every 36 times => 360 degrees.
for x in range(0,36,1):
    # Create a new file every 4 entities so we don't mess up our game.
    if ((x%4)==0):
        cfg.newFile();

    ent = cfgents.Entity(cfg,
            "env_spark",
            "spark{0}".format(x))
    ent.create()

    ent.setKeyvalue("origin", v.rotate(o,"z",10).str())

    ent.fireInput("startspark")

# Builds the script into the current working directory.
cfg.build()

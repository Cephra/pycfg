import HL2

# Create a script by the name "manysparks". 
cfg = HL2.CfgBuilder("manysparks")

# Define the Origin and the Point we want to rotate.
o = HL2.Vec(0,0,0)
v = HL2.Vec(100,0,0)

# Rotate by 10 degrees every 36 times => 360 degrees.
for x in range(0,36,1):
    ent = HL2.Entity(cfg,
            "env_spark",
            "spark{0}".format(x))
    ent.create()
    
    ent.setKeyvalue("origin", v.rotate(o,"z",10).str())

    ent.fireInput("startspark")

# Builds the script into the current working directory.
cfg.build()

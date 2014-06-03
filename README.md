pycfg - A script generator for HL2DM
=====

This tool is designed to lower the amount of work you have to do for console scripts in HL2DM.

Now one might say: "What is this all about!?!"

I will show you just now.

```
ent_create env_spark targetname sparky
ent_fire sparky startspark
```

This ain't a lot of code, true. But what if you want to create sparks aligned in a circle? Yes. Correct. Way too many lines. Now this is where <b>pycfg</b> comes in handy. Instead of having to write all those lines, you can take advantage of for loops in python. Like so:

```python
import HL2
import math

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
```

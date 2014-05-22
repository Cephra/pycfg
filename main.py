import HL2

cfg = HL2.CfgBuilder("testscript")

ent = HL2.Entity(cfg,
"prop_dynamic_override",
"targetnamegoeshere",
"models/props_junk/wood_crate001a.mdl")
ent.create()

cfg.build()

clear @s minecraft:bucket 1
summon item ~ ~1 ~ {Item:{id:"minecraft:milk_bucket",count:1}}
particle minecraft:cloud ~ ~1 ~ 0.4 0.6 0.4 0.02 40 force @s
particle minecraft:splash ~ ~1 ~ 0.3 0.5 0.3 0.01 25 force @s
playsound minecraft:entity.cow.milk player @s ~ ~ ~ 1 1
effect give @s minecraft:hunger 3 100 false
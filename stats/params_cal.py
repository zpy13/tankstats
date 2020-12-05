import json

stats_file = open("tankstats_stats.json","r")
stats_contents = stats_file.read()
stats_dict = json.loads(stats_contents)
stats_file.close()
total =  0
for tank_dic in stats_dict.values():
    s = len(tank_dic)
    total += s
print(total)

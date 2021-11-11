result_dict = {}
with open("wanted_commands.txt") as f:
    result = f.readlines()
    for i, r in enumerate(result): 
        result_dict[r.strip("\n").split(",")[0]] = r.strip("\n").split(",")[1]
    print(result_dict.get("RPM"))
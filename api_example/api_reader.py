
import requests
import statistics, re
import json
import os

url = "https://api.thecatapi.com/v1/breeds"

response = requests.get(url)

content = response.json()

print(content)

def get_weight(arg):
    weight = list()

    def get_median(var):
        tmp_var = re.findall(r"\d+", var)
        tmp_var = (int(tmp_var[0]) + int(tmp_var[1])) / 2
        return tmp_var

    weight = list(map(get_median, map(lambda x: x["weight"]["metric"], arg)))
    minim = min(weight)
    maxim = max(weight)
    mean = statistics.mean(weight)
    median = statistics.median(weight)
    deviation = statistics.stdev(weight)
    return minim, maxim, mean, median, deviation


def get_lifespans(arg):
    lifespans = list()
    tmp = list()
    for i in arg:
        tmp.append(i["life_span"])
    for i in tmp:
        tmp_var = re.findall(r"\d+", i)
        tmp_var = (int(tmp_var[0]) + int(tmp_var[1])) / 2
        lifespans.append(tmp_var)
    minim = min(lifespans)
    maxim = max(lifespans)
    mean = statistics.mean(lifespans)
    median = statistics.median(lifespans)
    deviation = statistics.stdev(lifespans)
    return minim, maxim, mean, median, deviation


print("CATS WEIGHT DATA (kg) \n" "MINIMUM, MAXIMUM, MEAN, MEDIAN, DEVIATION")
print(get_weight(content))
print("CATS LIFESPAN DATA (years) \n" "MINIMUM, MAXIMUM, MEAN, MEDIAN, DEVIATION")
print(get_lifespans(content))

script_dir = str(os.path.dirname(__file__))
files_dir = script_dir + "\\data\\"

if not os.path.exists(files_dir):
    os.makedirs(files_dir)

with open(files_dir + "cats.csv", 'w', newline='') as file:
    json.dump(content,file, indent=4)
import csv
import os
import sys

outfile_name = "all_measurements.csv"
path_default = "default_polling"
path_1ms = "1ms_polling"
all_files_default = sorted(os.listdir(path_default))
all_files_1ms = sorted(os.listdir(path_1ms))
all_files = []

for filename in all_files_default:
    all_files.append(path_default + "/" + filename)

for filename in all_files_1ms:
    all_files.append(path_1ms + "/" + filename)

#all_files = (os.listdir(path_default).sort() + os.listdir(path_1ms).sort())
#print(all_files)

header = ["counter", "latency", "delayTime", "device", "polling", "pollingRate"]

with open(outfile_name, "w") as outfile:
    for item in header:
        outfile.write(",")
        outfile.write(item)
    for filename in all_files:
        print(filename)
        polling_rate = filename.split("_")[-2].split("ms")[0]
        print(polling_rate)
        #with open(filename, "r") as file:

        with open(filename, "r") as f:
            content = f.readlines()
            device_name = content[1].split(";")[1]
            print(device_name)

# no need to complete this script, as the jupyter notebook can do all this

"""

import csv
import os
import sys
import fileinput

outfile_name = "all_measurements.csv"

header = ["counter", "latency", "delayTime", "device", "polling", "pollingRate"]

with open(outfile_name, "w") as outfile:
    for item in header:
        outfile.write(",")
        outfile.write(item)
    for filename in fileinput.input():
        filename = filename.split("\n")[0]
        print(filename)
        polling_rate = filename.split("_")[2].split("ms")[0]
        print(polling_rate)
        with open(filename, "r") as f:
            content = f.readlines()
            device_name = content[1].split(";")[1]
            print(device_name)
            """

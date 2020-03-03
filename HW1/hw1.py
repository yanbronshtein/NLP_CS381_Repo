import os
import shutil

# Get Working directory from user
path = input("Please enter the file path to a chosen working directory containing files test.txt and train.txt\n"
             "This can be achieved by typing pwd in a linux shell if you are already in that directory\n")

# Source and destination paths
sources = [path + "/test.txt", path + "/train.txt"]
destinations = [path + "/test_mod.txt", path + "/train_mod.txt"]

# Extract raw data from test.txt
file0_old = open(sources[0], 'r')
lines0_old = file0_old.readlines()
file0_old.close()

# Extract raw data from training.txt
file1_old = open(sources[1], 'r')
lines1_old = file1_old.readlines()
file1_old.close()

# Pad each sentence in test.txt with <s> and </s> for the start and end tags
file0 = open(destinations[0], 'w')
for line0 in lines0_old:
    new_line0 = "<s> " + str(line0).replace("\n", " </s>\n")
    # print("*********************************************************************")
    # print(new_line0)
    # print("*********************************************************************")
    file0.write(new_line0)
file0.close()

# Pad each sentence in training.txt with <s> and </s> for the start and end tags
file1 = open(destinations[0], 'w')
for line1 in lines1_old:
    new_line1 = "<s> " + str(line1).replace("\n", " </s>\n")
    # print("*********************************************************************")
    # print(new_line0)
    # print("*********************************************************************")
    file1.write(new_line1)
file1.close()


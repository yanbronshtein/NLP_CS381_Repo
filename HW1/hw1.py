import os
import shutil

# Get Working directory from user
path = input("Please enter the file path to a chosen working directory containing files test.txt and train.txt\n"
             "This can be achieved by typing pwd in a linux shell if you are already in that directory\n")


# Source paths of train.txt and test.txt
sources = [path + "/test.txt", path + "/train.txt"]


clean_train_data = []
clean_test_data = []

# Extract data from test.txt
file0 = open(sources[0], 'r')
while line := file0.readline():
    new_line0 = "<s> " + str(line).replace("\n", " </s>")
    clean_train_data.append(new_line0)
file0.close()

# Extract data from train.txt
file1 = open(sources[1], 'r')
while line := file1.readline():
    new_line1 = "<s> " + str(line).replace("\n", " </s>\n")
    clean_test_data.append(new_line1)
file1.close()





import os
import shutil

# Get Working directory from user
path = input("Please enter the file path to a chosen working directory containing files train.txt and test.txt\n"
             "This can be achieved by typing pwd in a linux shell if you are already in that directory\n")

# Source paths of train.txt and test.txt
sources = [path + "/train.txt", path + "/test.txt"]

# List of sentences in test.txt padded with <s> and </s>
padded_train_data = []
# List of sentences in test.txt padded with <s> and </s>
padded_test_data = []

# Extract data from train.txt and store in padded_train_data
file0 = open(sources[0], 'r')
while line := file0.readline():
    tokenized_line = line.split()
    paddedLine = ""
    paddedLine += "<s> "
    for token in tokenized_line:
        paddedLine += token.lower() + " "
    paddedLine += "</s>"
    padded_train_data.append(paddedLine)
file0.close()

# Extract data from test.txt and store in padded_test_data
file1 = open(sources[1], 'r')

training_data_dict = {}
while line := file1.readline():
    tokenized_line = line.split()

    paddedLine = ""
    paddedLine += "<s>"
    for token in tokenized_line:
        word = token.lower()
        if word not in training_data_dict:
            training_data_dict.update({word: 1})
        else:
            old_count = training_data_dict.get(word)
            training_data_dict.update({word: old_count + 1})
        paddedLine += word + " "

    paddedLine += "</s>"
    padded_test_data.append(paddedLine)
file1.close()

# key: word ,value: frequency
# Replace all words occurring in the training data once with the token <unk>. Every word in the test data not seen in the
# training data should be treated as <unk>
print("Hello")



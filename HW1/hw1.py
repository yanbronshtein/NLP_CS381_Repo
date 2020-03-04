import os
import shutil

# Get Working directory from user
path = input("Please enter the file path to a chosen working directory containing files train.txt and test.txt\n"
             "This can be achieved by typing pwd in a linux shell if you are already in that directory\n")

# Source paths of train.txt and test.txt
sources = [path + "/test.txt", path + "/train.txt"]

# # List of sentences in test.txt padded with <s> and </s>
# padded_train_data = []
# # List of sentences in test.txt padded with <s> and </s>
# padded_test_data = []

tokenized_test_data = []
# Extract data from test.txt and store in tokenized_test_data
file0 = open(sources[0], 'r')
while line := file0.readline():
    tokenized_line = line.split()
    paddedLine = ""
    paddedLine += "<s> "  # todo: figure out if need to add this to a dictionary also like for train data
    for token in tokenized_line:
        paddedLine += token.lower() + " "
    paddedLine += "</s>"
    tokenized_test_data.append(paddedLine.split())
file0.close()

# Extract data from train.txt and store in tokenized_train_data
file1 = open(sources[1], 'r')
# Store unique words(keys) and their frequencies(values) in train_dict
train_dict = {}
# Count of the number of unique words appearing in training
num_train_words = 0
tokenized_train_data = []  # List of tokenized training data sentences
while line := file1.readline():
    tokenized_line = line.split()
    paddedLine = ""
    paddedLine += "<s> "
    for token in tokenized_line:
        word = token.lower()
        if word not in train_dict:
            train_dict.update({word: 1})
            num_train_words += 1
        else:
            old_count = train_dict.get(word)
            train_dict.update({word: old_count + 1})
        paddedLine += word + " "
    paddedLine += "</s>"
    tokenized_train_data.append(paddedLine.split())
file1.close()



# Create a filtered dictionary from train_dict containing only the words with frequency= 1
new_dict = {key: value for (key, value) in train_dict.items() if value == 1}

# Iterate through each word in each line of tokenized_train_data and replace the word with token "<unk>" if
# that word is also found in the new_dict(filtered dictionary based on words with frequency =1)
for line in tokenized_train_data:
    for i in range(0, len(line)):
        if line[i] in new_dict:
            line[i] = "<unk>"

# Iterate through each word in each line of tokenized_train_data and replace it with token "<unk>" if that word is not
# found in the train_dict (aka training) and increment the number of unknown words
#

num_new_words = 0
for line in tokenized_test_data:
    for i in range(0, len(line)):
        if line[i] not in train_dict and not(line[i] == "<s>" or line[i] == "</s"):
            line[i] = "<unk>"
            num_new_words += 1

print("Hello mofo")
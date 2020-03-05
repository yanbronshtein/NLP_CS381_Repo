import copy

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
# Store unique words(keys) and their frequencies(values) in train_dict_no_padding excluding <s> and </s>
train_dict_no_padding = {}
# Store unique words(keys) and their frequencies(values) including <s> and </s>
train_dict_padding = {}
# Count of the number of unique words appearing in training
tokenized_train_data = []  # List of tokenized training data sentences
total_num_tokens = 0
while line := file1.readline():
    tokenized_line = line.split()
    paddedLine = ""
    paddedLine += "<s> "

    # Add <s> to train_dict_padding dictionary
    if "<s>" not in train_dict_padding:
        train_dict_padding["<s>"] = 1
    else:
        train_dict_padding["<s>"] += 1
    total_num_tokens += 1

    for token in tokenized_line:
        word = token.lower()

        if word not in train_dict_no_padding:
            train_dict_no_padding[word] = 1
        else:
            train_dict_no_padding[word] += 1

        if word not in train_dict_padding:
            train_dict_padding[word] = 1
        else:
            train_dict_padding[word] += 1
            train_dict_no_padding[word] += 1
        paddedLine += word + " "
    paddedLine += "</s>"

    # Add </s> to train_dict_padding dictionary
    if "</s>" not in train_dict_padding:
        train_dict_padding["</s>"] = 1
    else:
        train_dict_padding["</s>"] += 1
    total_num_tokens += 1
    tokenized_train_data.append(paddedLine.split())

file1.close()

# Create a filtered dictionary from train_dict containing only the words with frequency= 1
rare_word_dict = {key: value for (key, value) in train_dict_padding.items() if value == 1}

# Iterate through each word in each line of tokenized_train_data and replace the word with token "<unk>" if
# that word is also found in the new_dict(filtered dictionary based on words with frequency =1)
# Remove a word train_dict_after_unk as soon as it is replaced with <unk> and increment <unk> count
train_dict_after_unk = copy.deepcopy(train_dict_padding)
for line in tokenized_train_data:
    for i in range(0, len(line)):
        if line[i] in rare_word_dict:
            del train_dict_after_unk[line[i]]
            if "<unk>" not in train_dict_after_unk:
                train_dict_after_unk["<unk"] = 1
            else:
                train_dict_after_unk["<unk"] += 1
            line[i] = "<unk>"

# Create a filtered dictionary from train_dict_padding containing words with frequency> 1
# common_word_dict = {key: value for (key, value) in train_dict_padding.items() if value > 1}

# Iterate through each word in each line of tokenized_train_data and replace it with token "<unk>" if that word is not
# found in the train_dict (aka training) and increment the number of unknown words
# num_new_words = 0
# for line in tokenized_test_data:
#     for i in range(0, len(line)):
#         if line[i] not in train_dict_no_padding and not (line[i] == "<s>" or line[i] == "</s>"):
#             line[i] = "<unk>"
#             num_new_words += 1


hw_file_path = path + "/hw_sol.txt"
q1_question_str = "Q1:How many word types (unique words) are there in the training corpus? \n " \
                  "Please include the padding symbols and the unknown token.\n"
q1_answer_str = "A1: " + str(len(train_dict_after_unk)) + "\n"
with open(hw_file_path, "a") as hw_file:
    hw_file.write(q1_question_str + q1_answer_str)





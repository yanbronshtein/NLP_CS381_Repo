# Source paths of train.txt and test.txt

path = "/Users/yanivbronshtein/Coding/QueensCollege/NLP_CS381_Repo/HW1"

# sources = [path + "/test.txt", path + "/train.txt"] //todo: change back to original nigga
sources = [path + "/train_small.txt", path + "/test_small.txt"]


# Extract data from train.txt and store in tokenized_train_data


# This function is used to pre-process both the
def pre_process_data(file_path):
    tokenized_padded_data = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if line:
                line = line.lower()
                tokenized_line = line.split()
                tokenized_line.insert(0, '<s>')  # Prepend start symbol
                tokenized_line.insert(len(tokenized_line), '</s>')  # Append stop symbol
                tokenized_padded_data.append(tokenized_line)
    file.close()

    return tokenized_padded_data


tokenized_train_data = pre_process_data(sources[0])
tokenized_test_data = pre_process_data(sources[0])


def count_unique_word_tokens(tokenized_train_data, tokenized_test_data):
    data_dict = {}
    for line in tokenized_train_data:
        for word in line:
            data_dict[word] = 1 if word not in data_dict else data_dict[word] + 1
    print("Hi")


count_unique_word_tokens(tokenized_train_data,tokenized_test_data)

def count_total_word_tokens(tokenized_data):
    token_count = 0
    for line in tokenized_data:
        token_count += len(line)
    return token_count


total_word_count_training = count_total_word_tokens(tokenized_train_data)

print("Q2: How many word tokens are there in the training corpus?\n" + str(total_word_count_training))

# total_num_tokens = 0
# while line := file1.readline():
#     tokenized_line = line.split()
#     paddedLine = ""
#     paddedLine += "<s> "
#     total_num_tokens += 1
#     # Add <s> to train_dict_padding dictionary
#     if "<s>" not in train_dict_padding:
#         train_dict_padding["<s>"] = 1
#     else:
#         train_dict_padding["<s>"] += 1
#
#     for token in tokenized_line:
#         word = token.lower()
#         total_num_tokens += 1
#         if word not in train_dict_no_padding:
#             train_dict_no_padding[word] = 1
#         else:
#             train_dict_no_padding[word] += 1
#
#         if word not in train_dict_padding:
#             train_dict_padding[word] = 1
#         else:
#             train_dict_padding[word] += 1
#             train_dict_no_padding[word] += 1
#         paddedLine += word + " "
#     paddedLine += " </s>"
#     paddedLine = paddedLine.strip()
#
#     # Add </s> to train_dict_padding dictionary
#     if "</s>" not in train_dict_padding:
#         train_dict_padding["</s>"] = 1
#     else:
#         train_dict_padding["</s>"] += 1
#     total_num_tokens += 1
#     tokenized_train_data.append(paddedLine.split())
#     tokenized_train_data_padding.append(paddedLine.split())
#
# file1.close()
#
# # Create a filtered dictionary from train_dict containing only the words with frequency= 1
# rare_word_dict = {key: value for (key, value) in train_dict_padding.items() if value == 1}
#
# # Iterate through each word in each line of tokenized_train_data and replace the word with token "<unk>" if
# # that word is also found in the new_dict(filtered dictionary based on words with frequency =1)
# # Remove a word train_dict_after_unk as soon as it is replaced with <unk> and increment <unk> count
# train_dict_after_unk = copy.deepcopy(train_dict_padding)
# for line in tokenized_train_data:
#     for i in range(0, len(line)):
#
#         if line[i] in rare_word_dict:
#             train_dict_after_unk[line[i]] = 0
#             if "<unk>" not in train_dict_after_unk:
#                 train_dict_after_unk["<unk"] = 1
#             else:
#                 train_dict_after_unk["<unk"] += 1
#             line[i] = "<unk>"
# # train_dict_after_unk = {key: value for (key, value) in train_dict_after_unk.items() if value == 0}
#
# tokenized_test_data = []
# # Extract data from test.txt and store in tokenized_test_data and unique words into
# test_dict_padding = {}
# file0 = open(sources[0], 'r')
# while line := file0.readline():
#     tokenized_line = line.split()
#     paddedLine = ""
#     paddedLine += "<s> "  # todo: figure out if need to add this to a dictionary also like for train data
#     if "<s>" not in test_dict_padding:
#         test_dict_padding["<s>"] = 1
#     else:
#         test_dict_padding["<s>"] += 1
#     for token in tokenized_line:
#         paddedLine += token.lower() + " "
#         if token not in test_dict_padding:
#             test_dict_padding[token] = 1
#         else:
#             test_dict_padding[token] += 1
#     paddedLine += "</s>"
#
#     if "</s>" not in test_dict_padding:
#         test_dict_padding["</s>"] = 1
#     else:
#         test_dict_padding["</s>"] += 1
#     tokenized_test_data.append(paddedLine.split())
# file0.close()
#
# test_dict_after_unk = copy.deepcopy(test_dict_padding)
# for line in tokenized_test_data:
#
#     for i in range(0, len(line)):
#         if line[i] not in train_dict_after_unk:
#             test_dict_after_unk[line[i]] = 0
#             if "<unk>" not in test_dict_after_unk:
#                 train_dict_after_unk["<unk"] = 1
#             else:
#                 train_dict_after_unk["<unk"] += 1
#             line[i] = "<unk>"
#
# # Create a filtered dictionary from train_dict_padding containing words with frequency> 1
# # common_word_dict = {key: value for (key, value) in train_dict_padding.items() if value > 1}
#
# # Iterate through each word in each line of tokenized_train_data and replace it with token "<unk>" if that word is not
# # found in the train_dict (aka training) and increment the number of unknown words
# # num_new_words = 0
# # for line in tokenized_test_data:
# #     for i in range(0, len(line)):
# #         if line[i] not in train_dict_no_padding and not (line[i] == "<s>" or line[i] == "</s>"):
# #             line[i] = "<unk>"
# #             num_new_words += 1
#
#
#
# # Take all bigrams put in dictionary.
# # Each bigram appeared once
# # Iterate through map and divide
# print("Q2: How many word tokens are there \n" + str(len(tokenized_train_data_padding)))
# # hw_file_path = path + "/hw_sol.txt"
# #
# # hw_file = open(hw_file_path, "a")
# #
# # q1_question_str = "Q1:How many word types (unique words) are there in the training corpus? \n " \
# #                   "Please include the padding symbols and the unknown token.\n"
# # q1_answer_str = "A1: " + str(len(train_dict_after_unk)) + "\n\n"
# # print(q1_answer_str)
# # hw_file.write(q1_question_str + q1_answer_str)
# #
# # q2_question_str = "Q2:How many word tokens are there in the training corpus?.\n"
# # q2_answer_str = "A2: " + str(total_num_tokens) + "\n\n"
# # hw_file.write(q2_question_str + q2_answer_str)
# # print(q2_answer_str)
# # q3_question_str = "Q3:What percentage of word tokens and word types in the test corpus did not occur in training\n " \
# #                   "(before you mapped the unknown words to <unk> in training and test data)?\n " \
# #                   "Please include the padding symbols in your calculations.\n"
# #
# # len(test_dict_padding)
# # # q3_question_answer = "A3:" + str(test_dict_padding["<unk">]) + " / "

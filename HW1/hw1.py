import copy

# Source paths of train.txt and test.txt

path = "/Users/yanivbronshtein/Coding/QueensCollege/NLP_CS381_Repo/HW1"

sources = [path + "/train.txt", path + "/test.txt"]  # todo: change back to original nigga

# sources = [path + "/train_small.txt", path + "/test_small.txt"]


# This function is used to tokenize and path data read from train.txt and test.txt
def pad_and_tokenize_file_data(file_path):
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


def populate_dict(data):
    dictionary = {}
    for line in data:
        for word in line:
            dictionary[word] = 1 if word not in dictionary else dictionary[word] + 1
    return dictionary


tokenized_train_data_before_unk = pad_and_tokenize_file_data(sources[0])
train_data_dict_before_unk = populate_dict(tokenized_train_data_before_unk)
rare_words_dict = {key: value for (key, value) in train_data_dict_before_unk.items() if
                   value == 1 and value != "<s>" and value !=
                   "</s>"}  # rare_words_dict contains only those words that are not start or end symbols that
# appear only once in training
# those words that appear once in training

tokenized_train_data_after_unk = copy.deepcopy(tokenized_train_data_before_unk)
for line in tokenized_train_data_after_unk:
    for i in range(0, len(line)):
        if line[i] in rare_words_dict:
            line[i] = "<unk>"

train_data_dict_after_unk = populate_dict(tokenized_train_data_after_unk)
print("Q1: How many word types (unique words) are there in the training corpus?\n "
      "Please include the padding symbols and the unknown token.\n" + str(len(train_data_dict_after_unk)))


# total_word_count_training = 0
# for line in tokenized_train_data_after_unk:
#     total_word_count_training += len(line)

def count_tokens(tokenized_data):
    token_count = 0
    for sentence in tokenized_data:
        token_count += len(sentence)
    return token_count


print(
    "Q2: How many word tokens are there in the training corpus?\n" + str(count_tokens(tokenized_train_data_after_unk)))

tokenized_test_data_before_unk = pad_and_tokenize_file_data(sources[1])
test_dict_before_unk = populate_dict(tokenized_test_data_before_unk)
tokenized_test_data_after_unk = copy.deepcopy(tokenized_test_data_before_unk)
unk_count_testing = 0
for line in tokenized_test_data_after_unk:
    for i in range(0, len(line)):
        if line[i] not in train_data_dict_before_unk:
            line[i] = "<unk>"
            unk_count_testing += 1

test_dict_after_unk = populate_dict(tokenized_test_data_after_unk)


# def train_unigram_mle():
#     unigram_model = copy.deepcopy(train_data_dict_before_unk)
#
#     for word in unigram_model:
#         unigram_model[word] = unigram_model[word] / total_word_count_training
#
#     return unigram_model
#
#
# unigram_model = train_unigram_mle()

print("Q3: What percentage of word tokens and word types in the test corpus did not occur in training\n"
      " (before you mapped the unknown words to <unk> in training and test data)? \n"
      "Please include the padding symbols in your calculations.")
# percentage_word_tokens in testing not found in training = total_unks_testing_/total_testing_tokens

total_test_token_count = count_tokens(tokenized_test_data_before_unk)
newDict = {key: value for (key, value) in test_dict_after_unk.items() if key == "<unk>"}



# unk_count_testing = len(tokenized_test_data_before_unk)
print("unk_count_testing: " + str(unk_count_testing) + "\n")
percent_word_tokens_testing = (unk_count_testing / total_test_token_count) * 100
print("a). Percentage of word tokens in test corpus not in training \n" + str(unk_count_testing) + "/" +
      str(total_test_token_count) + "\n" + str(percent_word_tokens_testing) + "%\n")


# appear only once in training
# those words that appear once in training

# def train_bigram_mle():
#     bigram_model = copy.deepcopy(train_data_dict_before_unk)
#
#     for word in unigram_model:
#         unigram_model[word] = unigram_model[word] / total_word_count_training
#
#     return unigram_model

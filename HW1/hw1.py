import copy

# Source paths of train.txt and test.txt

path = "/Users/yanivbronshtein/Coding/QueensCollege/NLP_CS381_Repo/HW1" # todo: Use relative path instead

sources = [path + "/train.txt", path + "/test.txt"]  # todo: change back to original nigga

# sources = [path + "/train_small.txt", path + "/test_small.txt"]


# This function is used to tokenize and pad data read from train.txt and test.txt
def pad_and_tokenize_file_data(file_path):
    tokenized_padded_data = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()  # Remove hidden character
            if line:
                line = line.lower()  # Lowercase each line
                tokenized_line = line.split()  # Tokenize the line by spaces
                tokenized_line.insert(0, '<s>')  # Prepend start symbol
                tokenized_line.insert(len(tokenized_line), '</s>')  # Append stop symbol
                tokenized_padded_data.append(tokenized_line)  # Append the cleaned line to tokenized_padded_data
    file.close()  # Close the file
    return tokenized_padded_data  # Return the dictionary


# This function is used to populate a dictionary given data. If a word is not in the dictionary, it receives a count
# of one. Otherwise the previous count is incremented by one. The modified dictionary is returned
def populate_dict(tokenized_data):
    dictionary = {}
    for line in tokenized_data:
        for word in line:
            dictionary[word] = 1 if word not in dictionary else dictionary[word] + 1
    return dictionary


tokenized_train_data_before_unk = pad_and_tokenize_file_data(sources[0]) #
train_data_dict_before_unk = populate_dict(tokenized_train_data_before_unk)
rare_words_dict = {key: value for (key, value) in train_data_dict_before_unk.items() if
                   value == 1 and value != "<s>" and value !=
                   "</s>"}  # rare_words_dict contains only those words that are not start or end symbols that
# appear only once in training
# those words that appear once in training

# Lines 47-51 replace all words in training that appear only once with "<unk>" token
tokenized_train_data_after_unk = copy.deepcopy(tokenized_train_data_before_unk)
for line in tokenized_train_data_after_unk:
    for i in range(0, len(line)):
        if line[i] in rare_words_dict:
            line[i] = "<unk>"

train_data_dict_after_unk = populate_dict(tokenized_train_data_after_unk)  # create the train_data_dict_after_unk using
#cleaned data after "<unk>" modification
print("Q1: How many word types (unique words) are there in the training corpus?\n "
      "Please include the padding symbols and the unknown token.\n" + str(len(train_data_dict_after_unk)))

# This function parses tokenized data(array of tokenized lines) and counts the number of tokens in each line, and
# adds to the total token count
def count_tokens(tokenized_data):
    token_count = 0
    for sentence in tokenized_data:
        token_count += len(sentence)
    return token_count


total_train_token_count = count_tokens(tokenized_train_data_after_unk)
print("Q2:How many word tokens are there in the training corpus?\n" + str(total_train_token_count))

tokenized_test_data_before_unk = pad_and_tokenize_file_data(sources[1])
test_dict_before_unk = populate_dict(tokenized_test_data_before_unk)
tokenized_test_data_after_unk = copy.deepcopy(tokenized_test_data_before_unk)
for line in tokenized_test_data_after_unk:
    for i in range(0, len(line)):
        if line[i] not in train_data_dict_before_unk:
            line[i] = "<unk>"


test_dict_after_unk = populate_dict(tokenized_test_data_after_unk)
print("Q3: What percentage of word tokens and word types in the test corpus did not occur in training\n"
      " (before you mapped the unknown words to <unk> in training and test data)? \n"
      "Please include the padding symbols in your calculations.")

total_test_token_count = count_tokens(tokenized_test_data_before_unk)  # Calculate the number of tokens in test data
percent_word_tokens_testing = (test_dict_after_unk["<unk>"] / total_test_token_count) * 100  # The numerator gives the
# count of "<unk>" in the test data

print("a). Percentage of word tokens in test corpus not in training \n" + str(test_dict_after_unk["<unk>"]) + "/" +
      str(total_test_token_count) + " OR \n" + str(percent_word_tokens_testing) + "%\n")

total_unique_test_token_count = len(test_dict_before_unk)   # Length of test corpus is the number of unique tokens
# found in testing before replacement(test_dict_before_unk) with <unk> for words found in testing but not in training
percent_word_tokens_testing = (test_dict_after_unk["<unk>"] / total_unique_test_token_count) * 100  # The numerator
# should be the same as with part a


print("b). Percentage of word types in test corpus that did not occur in training \n" +
      str(test_dict_after_unk["<unk>"]) + "/" + str(total_unique_test_token_count) +
      " OR \n" + str(percent_word_tokens_testing) + "%\n")



print("Q4: Now replace singletons in the training data with <unk> symbol and map words (in the test corpus)\n "
      "not observed in training to <unk>. \n What percentage of bigrams (bigram types and bigram tokens) in the test "
      "corpus did not occur in training (treat <unk> as a regular token that has been observed).")


# This function is used to train the unigram model after "<unk>" is inserted
def train_unigram_mle():
    unigram_model = copy.deepcopy(train_data_dict_after_unk)

    for word in unigram_model:
        unigram_model[word] = unigram_model[word] / total_train_token_count

    return unigram_model


unigram_model = train_unigram_mle()
print("Hi")
# test_dict_after_unk care about this
# train_data_dict_after_unk care about this

# appear only once in training
# those words that appear once in training

def train_bigram_mle():
    bigram_model = copy.deepcopy(train_data_dict_before_unk)

    for word in unigram_model:
        unigram_model[word] = unigram_model[word] / total_word_count_training

    return unigram_model

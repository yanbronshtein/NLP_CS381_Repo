import copy

# Source paths of train.txt and test.txt

path = "/Users/yanivbronshtein/Coding/QueensCollege/NLP_CS381_Repo/HW1"  # todo: Use relative path instead

# sources = [path + "/train.txt", path + "/test.txt"]  # todo: change back to original man


sources = [path + "/train_small.txt", path + "/test_small.txt"]


# This function is used to tokenize and pad data read from train.txt and test.txt
def pad_and_tokenize_file_data(file_path):
    tokenized_padded_data = []
    with open(file_path) as file:
        for line0 in file:
            stripped_line = line0.strip()  # Remove hidden character
            if stripped_line:
                stripped_line = stripped_line.lower()  # Lowercase each line
                tokenized_line = stripped_line.split()  # Tokenize the line by spaces
                tokenized_line.insert(0, '<s>')  # Prepend start symbol
                tokenized_line.insert(len(tokenized_line), '</s>')  # Append stop symbol
                tokenized_padded_data.append(tokenized_line)  # Append the cleaned line to tokenized_padded_data
    file.close()  # Close the file
    return tokenized_padded_data  # Return the dictionary


# This function is used to populate a dictionary given data. If a word is not in the dictionary, it receives a count
# of one. Otherwise the previous count is incremented by one. The modified dictionary is returned
def populate_dict(tokenized_data):
    dictionary = {}
    for linea in tokenized_data:
        for word in linea:
            dictionary[word] = 1 if word not in dictionary else dictionary[word] + 1
    return dictionary


# This function parses tokenized data(array of tokenized lines) and counts the number of tokens in each line, and
# adds to the total token count
def count_tokens(tokenized_data):
    token_count = 0
    for sentence in tokenized_data:
        token_count += len(sentence)
    return token_count


def replace_singleton_with_unk_train(tokenized_train_data_before_unk, train_data_dict_before_unk):
    tokenized_train_data_after_unk = copy.deepcopy(tokenized_train_data_before_unk)
    rare_words_dict = {key: value for (key, value) in train_data_dict_before_unk.items() if
                       value == 1 and value != "<s>" and value !=
                       "</s>"}  # rare_words_dict contains only those words that are not start or end symbols that
    # appear only once in training
    # those words that appear once in training
    for line in tokenized_train_data_after_unk:
        for i in range(0, len(line)):
            if line[i] in rare_words_dict:
                line[i] = "<unk>"
    return tokenized_train_data_after_unk


def replace_singleton_with_unk_test(tokenized_test_data_before_unk, train_data_dict_before_unk):
    tokenized_test_data_after_unk = copy.deepcopy(tokenized_test_data_before_unk)
    for line in tokenized_test_data_after_unk:
        for i in range(0, len(line)):
            if line[i] not in train_data_dict_before_unk:
                line[i] = "<unk>"
    return tokenized_test_data_after_unk


# This function is used to train the unigram model before "<unk>" is inserted
def train_unigram_mle(tokenized_train_data, total_train_token_count):
    model = {}
    for word in model:
        model[word] = tokenized_train_data[word] / total_train_token_count

    return model


# total_number_of_bigrams_before_unk = 0
def create_bigram_count_dict(tokenized_data):
    count_dict = {}
    for sentence in tokenized_data:
        for i in range(0, len(sentence) - 1):
            bigram_key = sentence[i] + "," + sentence[i + 1]
            count_dict[bigram_key] = 1 if bigram_key not in count_dict else count_dict[bigram_key] + 1
    return count_dict


# Make bigram dictionary
def train_bigram_mle(tokenized_data, train_data_dict):
    model = create_bigram_count_dict(tokenized_data)
    total_number_of_bigrams = 0

    # for sentence in tokenized_train_data_before_unk:
    #     for i in range(0, len(sentence)-1):
    #         bigram_key = sentence[i] + "," + sentence[i + 1]
    #         model[bigram_key] = 1 if bigram_key not in model else model[bigram_key] + 1
    #         total_number_of_bigrams += 1

    # Assign bigram probabilities
    for word in model:
        # Split by comma
        words = word.split(",")  # Get Wi-1 and Wi
        # count(Wi-1, Wi) / count(Wi-1)
        # print("My word:[" + word + "]" + str(type(word)) + "\n")
        # print("words[0]:[" + words[0] + "]" + str(type(words[0])) + "\n")

        model[word] /= train_data_dict[words[0]]
    return model


def main():
    tokenized_train_data_before_unk = pad_and_tokenize_file_data(sources[0])  #

    train_data_dict_before_unk = populate_dict(tokenized_train_data_before_unk)
    # create the train_data_dict_after_unk using
    tokenized_train_data_after_unk = replace_singleton_with_unk_train(tokenized_train_data_before_unk, train_data_dict_before_unk)

    train_data_dict_after_unk = populate_dict(tokenized_train_data_after_unk)

    tokenized_test_data_before_unk = pad_and_tokenize_file_data(sources[1])

    test_dict_before_unk = populate_dict(tokenized_test_data_before_unk)

    total_train_token_count_before_unk = count_tokens(tokenized_train_data_before_unk)

    total_train_token_count_after_unk = count_tokens(tokenized_train_data_before_unk)

    tokenized_test_data_after_unk = replace_singleton_with_unk_test(tokenized_test_data_before_unk, train_data_dict_before_unk)

    test_dict_after_unk = populate_dict(tokenized_test_data_after_unk)

    total_test_token_count = count_tokens(tokenized_test_data_before_unk)  # Calculate the number of tokens in test data

    percent_word_tokens_testing = (test_dict_after_unk[
                                       "<unk>"] / total_test_token_count) * 100  # The numerator gives the
    # count of "<unk>" in the test data
    # cleaned data after "<unk>" modification

    total_unique_test_token_count = len(test_dict_before_unk)  # Length of test corpus is the number of unique tokens
    # found in testing before replacement(test_dict_before_unk) with <unk> for words found in testing but not in training

    percent_word_tokens_testing = (test_dict_after_unk["<unk>"] / total_unique_test_token_count) * 100  # The numerator
    # should be the same as with part a

    unigram_model_before_unk = train_unigram_mle(tokenized_train_data_before_unk, tokenized_train_data_before_unk)

    unigram_model_after_unk = train_unigram_mle(tokenized_train_data_after_unk, tokenized_train_data_before_unk)

    bigram_model_before_unk = train_bigram_mle(tokenized_train_data_before_unk, train_data_dict_before_unk)

    bigram_model_after_unk = train_bigram_mle(tokenized_train_data_after_unk, train_data_dict_after_unk)

    print("Q1: How many word types (unique words) are there in the training corpus?\n "
          "Please include the padding symbols and the unknown token.\n" + str(len(train_data_dict_after_unk)))

    print("Q2:How many word tokens are there in the training corpus?\n" + str(total_train_token_count_after_unk))

    print("Q3: What percentage of word tokens and word types in the test corpus did not occur in training\n"
          " (before you mapped the unknown words to <unk> in training and test data)? \n"
          "Please include the padding symbols in your calculations.")

    print("a). Percentage of word tokens in test corpus not in training \n" + str(test_dict_after_unk["<unk>"]) + "/" +
          str(total_test_token_count) + " OR \n" + str(percent_word_tokens_testing) + "%\n")

    print("b). Percentage of word types in test corpus that did not occur in training \n" +
          str(test_dict_after_unk["<unk>"]) + "/" + str(total_unique_test_token_count) +
          " OR \n" + str(percent_word_tokens_testing) + "%\n")

    print("Q4: Now replace singletons in the training data with <unk> symbol and map words (in the test corpus)\n "
          "not observed in training to <unk>. \n What percentage of bigrams (bigram types and bigram tokens) in the test "
          "corpus did not occur in training (treat <unk> as a regular token that has been observed).")


if __name__ == "__main__":
    main()

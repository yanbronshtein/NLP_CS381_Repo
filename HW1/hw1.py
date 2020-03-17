import copy
import math

# Source paths of train.txt and test.txt

path = "/Users/yanivbronshtein/Coding/QueensCollege/NLP_CS381_Repo/HW1"  # todo: Use relative path instead

sources = [path + "/train.txt", path + "/test.txt"]  # todo: change back to original man


# sources = [path + "/train_small.txt", path + "/test_small.txt"]


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
def count_tokens_old(tokenized_data):
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


# This function is used to train the unigram model
def get_unigram_mle(data_dict):
    model = copy.deepcopy(data_dict)
    for word in model:
        model[word] /= count_tokens(data_dict)
    return model


# total_number_of_bigrams_before_unk = 0
def create_bigram_count_dict(tokenized_data):
    count_dict = {}

    loop_count = 0
    for sentence in tokenized_data:
        for i in range(0, len(sentence) - 1):
            bigram_key = sentence[i] + " " + sentence[i + 1]
            count_dict[bigram_key] = 1 if bigram_key not in count_dict else count_dict[bigram_key] + 1
    return count_dict


# Make bigram dictionary
def get_bigram_mle(tokenized_data, data_dict):
    model = create_bigram_count_dict(tokenized_data)
    # Assign bigram probabilities
    for word in model:
        # Split by comma
        words = word.split()  # Get Wi-1 and Wi
        # print("******k is: " + str(k) + " words are: " + str(words[0]) + " len: " + str(len(words[0])) + " and " +
        #       str(words[1]) + " len: " + str(len(words[1])) + " word is:" + word + "******\n")

        # if len(words[0]) != 0 and len(words[1]) != 0:
        model[word] /= data_dict[words[0]]
    return model


def get_bigram_aos(tokenized_data, data_dict):
    model = create_bigram_count_dict(tokenized_data)
    for word in model:
        words = word.split()
        model[word] = (model[word] + 1) / (data_dict[words[0]] + len(model))
    return model


def count_tokens(data_dict):
    count = 0
    for word in data_dict:
        count += data_dict[word]
    return count


# This function returns a dictionary containing only the words found in test_bigram but not in train_bigram
def filter_test_bigram(train_bigram_counts, test_bigram_counts):
    filtered_test_bigram = copy.deepcopy(test_bigram_counts)
    unknown_test_bigram = {}
    # Every word(word_phrase of two words) found in the test_bigram but not in train_bigram is copied into
    # unknown_test_bigram gets its key and value copied into unknown_test_bigram
    for word in filtered_test_bigram:
        if word not in train_bigram_counts:
            unknown_test_bigram[word] = test_bigram_counts[word]

    return unknown_test_bigram


# log(p1 * p2 * p3 * p4 ) = log p1 + log p2 + log p3 + log p4
def compute_log_probability_unigram_mle(model, sentence: str):
    probability = 0
    solution_string = "p("
    for word in model:
        solution_string += "log( p(" + word + ") + "
        probability += math.log(model[word], 2)
    return probability


def process_sentence(sentence: str):
    tokenized_sentence = sentence.lower().split()
    tokenized_sentence = tokenized_sentence.insert(0, "<s>")
    tokenized_sentence = tokenized_sentence.insert(len(sentence), "</s>")
    return tokenized_sentence






def main():
    tokenized_train_data_before_unk = pad_and_tokenize_file_data(sources[0])  #

    train_data_dict_before_unk = populate_dict(tokenized_train_data_before_unk)
    # create the train_data_dict_after_unk using
    tokenized_train_data_after_unk = replace_singleton_with_unk_train(tokenized_train_data_before_unk, train_data_dict_before_unk)

    train_data_dict_after_unk = populate_dict(tokenized_train_data_after_unk)

    tokenized_test_data_before_unk = pad_and_tokenize_file_data(sources[1])

    test_dict_before_unk = populate_dict(tokenized_test_data_before_unk)

    total_train_token_count_after_unk = count_tokens(train_data_dict_after_unk)

    tokenized_test_data_after_unk = replace_singleton_with_unk_test(tokenized_test_data_before_unk, train_data_dict_before_unk)

    test_dict_after_unk = populate_dict(tokenized_test_data_after_unk)

    total_test_token_count_before_unk = count_tokens(test_dict_before_unk)  # Calculate the number of tokens in test data

    unique_test_token_count = len(test_dict_before_unk)  # Length of test corpus is the number of unique tokens
    # found in testing before replacement(test_dict_before_unk) with <unk> for words found in testing but not in training

    percent_word_tokens_testing = (test_dict_after_unk["<unk>"] / unique_test_token_count) * 100  # The numerator
    # should be the same as with part a

    train_bigram_counts = create_bigram_count_dict(tokenized_train_data_after_unk)

    test_bigram_counts = create_bigram_count_dict(tokenized_test_data_after_unk)

    filtered_test_bigram = filter_test_bigram(train_bigram_counts, test_bigram_counts)

    # Created tokenized sentence(testing data) and the testing corpus
    q5_sentence_tokenized = process_sentence("I look forward to hearing your reply .")
    q5_sentence_dict = populate_dict(q5_sentence_tokenized)

    # Training unigram with maximum likelihood estimation, test it, and calculate log probability
    train_unigram_mle = get_unigram_mle(train_data_dict_after_unk)
    test_unigram_mle = get_unigram_mle(q5_sentence_dict)
    unigram_mle_log_probability = compute_log_probability()

    # Training bigram with maximum likelihood estimation, testing it, and calculate log probability
    train_bigram_mle = get_bigram_mle(tokenized_train_data_after_unk, train_data_dict_after_unk)
    test_bigram_mle = get_bigram_mle(q5_sentence_tokenized, q5_sentence_dict)

    # Training bigram with add-one-smoothing
    train_bigram_aos = get_bigram_aos(tokenized_train_data_after_unk,
                                      train_data_dict_after_unk)

    test_bigram_aos = get_bigram_aos(q5_sentence_tokenized, q5_sentence_dict)




    print("Q1: How many word types (unique words) are there in the training corpus?\n "
          "Please include the padding symbols and the unknown token.\n" + str(len(train_data_dict_after_unk)))

    print("Q2:How many word tokens are there in the training corpus?\n" + str(total_train_token_count_after_unk))

    print("Q3: What percentage of word tokens and word types in the test corpus did not occur in training\n"
          " (before you mapped the unknown words to <unk> in training and test data)? \n"
          "Please include the padding symbols in your calculations.")

    print("a). Percentage of word tokens in test corpus not in training \n" + str(test_dict_after_unk["<unk>"]) + "/" +
          str(total_test_token_count_before_unk) + " OR \n" + str(percent_word_tokens_testing) + "%\n")

    print("b). Percentage of word types in test corpus that did not occur in training \n" +
          str(test_dict_after_unk["<unk>"]) + "/" + str(unique_test_token_count) +
          " OR \n" + str(percent_word_tokens_testing) + "%\n")

    print("Q4: Now replace singletons in the training data with <unk> symbol and map words (in the test corpus)\n "
          "not observed in training to <unk>. \n What percentage of bigrams (bigram types and bigram tokens) "
          "in the test "
          "corpus did not occur in training (treat <unk> as a regular token that has been observed).")

    print("a). Percentage of bigram tokens in the test corpus that did not occur in training \n " +
          str(count_tokens(filtered_test_bigram)) + "/" + str(count_tokens(test_bigram_counts)) +
          " OR \n" + str((count_tokens(filtered_test_bigram) / count_tokens(test_bigram_counts)) * 100) + "%\n")

    print("b). Percentage of bigram types in the test corpus that did not occur in training \n " +
          str(len(filtered_test_bigram)) + "/" + str(len(test_bigram_counts)) +
          " OR \n" + str((len(filtered_test_bigram) / len(test_bigram_counts)) * 100) + "%\n")

    print("Q5: Compute the log probability of the following sentence under the three models (ignore capitalization\n"
          " and pad each sentence as described above). Please list all of the parameters required to compute the\n"
          "probabilities and show the complete calculation. Which of the parameters have zero values under each "
          "model?\n "
          "Use log base 2 in your calculations. Map words not observed in the training corpus to the <unk> token.\n"
          "I look forward to hearing your reply .\n")





if __name__ == "__main__":
    main()

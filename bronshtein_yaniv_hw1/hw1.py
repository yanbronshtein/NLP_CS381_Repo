import copy
import math
#Code by Yaniv Bronshtein
# Source paths of train.txt and test.txt
path = input("Please enter the directory containing the files 'train.txt' and 'test.txt'.\n"
             "Please note that it will take approximately 15 seconds for the results to display\n")

sources = [path + "/train.txt", path + "/test.txt"]


# sources = [path + "/train_small.txt", path + "/test_small.txt"]

# This function is used to tokenize and pad data read from train.txt and test.txt

tokenized_training_unk_splitted = []
def pad_and_tokenize_file_data(file_path):
    tokenized_padded_data = []
    with open(file_path) as file:
        for line0 in file:
            stripped_line = line0.strip()  # Remove hidden character
            if stripped_line:
                stripped_line = stripped_line.lower()  # Lowercase each line
                tokenized_line = stripped_line.split()  # Tokenize the line by spaces
                tokenized_line.insert(0, "<s>")  # Prepend start symbol
                tokenized_line.insert(len(tokenized_line), '</s>')  # Append stop symbol

                tokenized_padded_data.append(tokenized_line)  # Append the cleaned line to tokenized_padded_data
                for word in tokenized_line:
                    tokenized_training_unk_splitted.append(word)
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


# This function parses tokenized data(array of tokenized lines) and counts the number of tokens in each line, and
# adds to the total token count
def count_tokens_old(tokenized_data):
    token_count = 0
    for sentence in tokenized_data:
        token_count += len(sentence)
    return token_count


# This function is used to create an updated train data dictionary after singletons are replaced with "<unk>"
def replace_singleton_with_unk_train(tokenized_train_data_before_unk, train_data_dict_before_unk):
    tokenized_train_data_after_unk = copy.deepcopy(tokenized_train_data_before_unk) # Copy the training data for modification

    # rare_words_dict contains only those words that are not start or end symbols that
    # appear only once in training
    # those words that appear once in training
    rare_words_dict = {key: value for (key, value) in train_data_dict_before_unk.items() if
                       value == 1 and value != "<s>" and value !=
                       "</s>"}

    for line in tokenized_train_data_after_unk:
        for i in range(0, len(line)):
            if line[i] in rare_words_dict:
                line[i] = "<unk>"
    return tokenized_train_data_after_unk


# This function is used to create an updated test data dictionary after words found in testing but not in training
# are replaced with "<unk>"
def replace_singleton_with_unk_test(tokenized_test_data_before_unk, train_data_dict_after_unk):
    tokenized_test_data_after_unk = copy.deepcopy(tokenized_test_data_before_unk)
    for line in tokenized_test_data_after_unk:
        for i in range(0, len(line)):
            if line[i] not in train_data_dict_after_unk:
                line[i] = "<unk>"
    return tokenized_test_data_after_unk


# This function is used to train the unigram model
def get_unigram_mle(unigram_counts_mle):
    model = copy.deepcopy(unigram_counts_mle)
    denominator = count_tokens(unigram_counts_mle)
    for key in model:
        model[key] /= denominator
    return model


# This function is used to create a bigram by grouping the tokenized_data into
def create_bigram_count_dict(tokenized_data):
    count_dict = {}
    for sentence in tokenized_data:
        for i in range(0, len(sentence) - 1):
            bigram_key = sentence[i] + " " + sentence[i + 1]
            count_dict[bigram_key] = 1 if bigram_key not in count_dict else count_dict[bigram_key] + 1
    return count_dict


#Used to create a bigram for a single sentence
def create_bigram_count_dict_single_sentence(tokenized_sentence):
    count_dict = {}
    for i in range(0, len(tokenized_sentence) - 1):
        bigram_key = tokenized_sentence[i] + " " + tokenized_sentence[i + 1]
        count_dict[bigram_key] = 1 if bigram_key not in count_dict else count_dict[bigram_key] + 1
    return count_dict


# Make bigram dictionary
def get_bigram(bigram_counts, unigram_counts):
    # Assign bigram probabilities
    model = copy.deepcopy(bigram_counts)
    sara = 0
    for bigram_key in model:
        # print(bigram_key + "count is: " + str(sara) + "\n")
        sara += 1
        words = bigram_key.split()  # Get Wi-1 and Wi
        model[bigram_key] /= unigram_counts[words[0]]
    return model

def get_bigram_aos(bigram_counts_aos, unigram_counts):
    model = copy.deepcopy(bigram_counts_aos)
    V = len(unigram_counts)
    for bigram_key in model:
        words = bigram_key.split()
        model[bigram_key] /= (unigram_counts[words[0]] + V)

    return model


def get_bigram_test_sentence_mle(bigram_counts_mle, unigram_counts):
    model = copy.deepcopy(bigram_counts_mle)
    for bigram_key in model:
        words = bigram_key.split()
        model[bigram_key] /= unigram_counts[words[0]]
    return model

def get_bigram_test_sentence_aos(bigram_counts_aos, unigram_counts):
    model = copy.deepcopy(bigram_counts_aos)
    V = len(unigram_counts)
    for bigram_key in model:
        words = bigram_key.split()
        model[bigram_key] /= (unigram_counts[words[0]] + V)
    return model

# This function is used to compute the total number of tokens in data, whether training or testing
# by taking the dictionary formed and adding up all the counts of the unique keys
def count_tokens(data_dict):
    count = 0
    for key in data_dict:
        count += data_dict[key]
    return count


# This function returns a dictionary containing only the words found in test_bigram but not in train_bigram
def filter_test_bigram(train_bigram_counts, test_bigram_counts):
    filtered_test_bigram = copy.deepcopy(test_bigram_counts)
    unknown_test_bigram = {}
    # Every word(word_phrase of two words) found in the test_bigram but not in train_bigram is copied into
    # unknown_test_bigram gets its key and value copied into unknown_test_bigram
    for key in filtered_test_bigram:
        if key not in train_bigram_counts:
            unknown_test_bigram[key] = test_bigram_counts[key]

    return unknown_test_bigram


# This function is used to pad and lowercase the test sentence provided in question 5
def process_sentence(sentence: str):
    tokenized_sentence = sentence.lower().split()
    tokenized_sentence = ["<s>"] + tokenized_sentence
    tokenized_sentence = tokenized_sentence + ["</s>"]
    return tokenized_sentence


# This function is used to calculate the log probability
# log(p1 * p2 * p3 * p4 ) = log p1 + log p2 + log p3 + log p4
# The function returns a tuple because we need the full calculation with all steps as a string and the numeric value
# of the log probability. To get the string do tuple[0] and to get the float value do tuple[1]
def compute_log_probability_unigram_mle(model, tokenized_sentence):
    probability = 0
    solution_string = "P("
    for word in tokenized_sentence:
        solution_string += (word + ", ")
    solution_string = solution_string[0: len(solution_string)-2] + ") = "

    is_undefined = False
    for word in tokenized_sentence:
        solution_string += "log(p(" + word + ")) + "
        if model[word] != 0:
            probability += math.log(model[word], 2)
        else:
            is_undefined = True
            continue

    if not is_undefined:
        solution_string = solution_string[0: len(solution_string) - 1] + " = " + str(probability)
    else:
        solution_string = solution_string[0: len(solution_string) - 2] + " = NaN"
        probability = -math.nan

    return solution_string, probability


# For the bigram models(Maximum Likelihood and Add-One-Smoothing) we need to tokenize first
def compute_log_probability_bigram(train_model, test_model, tokenized_sentence):
    probability = 0
    solution_string = "P("

    for word in tokenized_sentence:
        solution_string += (word + ", ")

    solution_string = solution_string[0: len(solution_string)-2] + ") = "

    is_undefined = False
    for word in test_model:
        words = word.split()
        solution_string += "log(p(" + words[0] + ", " + words[1] + ")) + "
        try:
            probability += math.log(train_model[word], 2)
        except KeyError:
            is_undefined = True
            continue
    if not is_undefined:
        solution_string = solution_string[0: len(solution_string) - 1] + " = " + str(probability)
    else:
        solution_string[0: len(solution_string) - 2] + " = " + str("NaN")
        probability = -math.nan

    return solution_string, probability


# PP(W) = P(W1W2..Wn) ^(-1/n)
def compute_perplexity(log_probability, M):
    L = log_probability / M
    return 2 ** -L



# This is the main function
def main():
    # ****Preprocessing for train.txt****
    tokenized_train_data_before_unk = pad_and_tokenize_file_data(sources[0])
    # Create training data from preprocessed data
    train_data_dict_before_unk = populate_dict(tokenized_train_data_before_unk)
    # Replace all singletons in train data with unk
    tokenized_train_data_after_unk = replace_singleton_with_unk_train(tokenized_train_data_before_unk,train_data_dict_before_unk )

    # create the train_data_dict after replacing all singletons with "<unk>"
    train_data_dict_after_unk = populate_dict(tokenized_train_data_after_unk)
    # create the train_data_dict_after_unk using
    tokenized_train_data_after_unk = replace_singleton_with_unk_train(tokenized_train_data_before_unk, train_data_dict_before_unk)

    # ****Preprocessing for test.txt****
    tokenized_test_data_before_unk = pad_and_tokenize_file_data(sources[1])
    # Create a dictionary before replacement of tokens seen in training but not testing with "<unk>"
    test_dict_before_unk = populate_dict(tokenized_test_data_before_unk)
    # Replace tokens in test data with "<unk>" if the were unseen in training
    tokenized_test_data_after_unk = replace_singleton_with_unk_test(tokenized_test_data_before_unk, train_data_dict_before_unk)
    #create test_dict from preprocessed data
    test_dict_after_unk = populate_dict(tokenized_test_data_after_unk)

    # ************** Used for Q1 **************
    unique_train_token_count_after_unk = len(train_data_dict_after_unk)

    #************** Used for Q2 **************
    total_train_token_count_after_unk = count_tokens(train_data_dict_after_unk)

    #************** Used for Q3 **************
    total_test_token_count_before_unk = count_tokens(test_dict_before_unk)  # Calculate the number of tokens in test data
    unique_test_token_count_before_unk = len(test_dict_before_unk)  # Length of test corpus is the number of unique tokens
    # found in testing before replacement(test_dict_before_unk) with <unk> for words found in testing but not in training

    total_count_tokens_in_test_not_in_train = 0 # Used for Q3a
    count_word_types_testing_not_training = 0 # Used for Q3b
    for key in test_dict_before_unk:
        if key not in train_data_dict_before_unk:
            total_count_tokens_in_test_not_in_train += test_dict_before_unk[key]
            count_word_types_testing_not_training += 1


    #************** Used for Q4 **************
    # This training bigram counts is used for Q4 onwards.
    train_bigram_counts_mle = create_bigram_count_dict(tokenized_train_data_after_unk)
    # This test bigram counts is only used for Q4 because it only applies to data from test.txt
    test_bigram_counts_mle_q4 = create_bigram_count_dict(tokenized_test_data_after_unk)
    #This bigram only contains bigrams in testing but not in training
    filtered_test_bigram_q4 = filter_test_bigram(train_bigram_counts_mle, test_bigram_counts_mle_q4)
    # The count of all the tokens in filtered_test_bigram_q4 gives the number of bigrams in testing but not in training
    # Used for Q4a
    count_total_bigrams_in_test_but_not_train_q4 = count_tokens(filtered_test_bigram_q4)
    # Used for Q4a
    count_total_test_bigram_counts = count_tokens(test_bigram_counts_mle_q4)
    # Used for Q4b
    count_unique_bigrams_in_test_but_not_train = len(filtered_test_bigram_q4)
    # Used for Q4b
    count_total_unique_bigrams = len(test_bigram_counts_mle_q4)

    #***** Question 5 ******
    # Preprocess the given sentence
    q5_sentence_tokenized = process_sentence("I look forward to hearing your reply .")
    q5_sentence_dict = {}
    # Replace any tokens in the new sentence with "<unk>" if they do not appear in training
    q5_sentence_tokenized_after_unk = replace_singleton_with_unk_test(q5_sentence_tokenized, train_data_dict_after_unk)

    #******Create test corpus for q5******
    # Get the parameters
    params_unigram_mle_q5 = []
    for word in q5_sentence_tokenized_after_unk:
        q5_sentence_dict[word] = 1 if word not in q5_sentence_dict else q5_sentence_dict[word] + 1
        params_unigram_mle_q5.append(word)
    #****** Training of unigram_mle, bigram_mle, and bigram_aos models ******
    # Create Unigram counts. This information has already been generated in the train_data_dict_after unk for the
    # previous questions
    train_unigram_counts_mle_q5 = copy.deepcopy(train_data_dict_after_unk)

    # Train the unigram using the counts
    train_unigram_mle_q5 = get_unigram_mle(train_unigram_counts_mle_q5)

    # Create the bigram with add-one-smoothing counts by adding one to all the bigram_mle counts
    train_bigram_counts_aos_q5 = copy.deepcopy(train_bigram_counts_mle)


    for key in train_bigram_counts_aos_q5:
        train_bigram_counts_aos_q5[key] += 1


    # Train the bigram_mle using the unigram counts and the bigram counts_mle
    train_bigram_mle_q5 = get_bigram(train_bigram_counts_mle, train_unigram_counts_mle_q5)
    # Train the bigram_aos using the unigram counts and the bigram counts and the bigram_aos counts
    train_bigram_aos_q5 = get_bigram_aos(train_bigram_counts_aos_q5, train_unigram_counts_mle_q5)

    #****** Creating of testing grams for unigram_mle, bigram_mle, and bigram_aos models ******

    # Create test unigram_mle
    test_unigram_mle_q5 = {}
    test_unigram_counts_mle_q5 = copy.deepcopy(q5_sentence_dict)
    for token in q5_sentence_tokenized_after_unk:
        test_unigram_mle_q5[token] = q5_sentence_dict[token] / len(q5_sentence_tokenized_after_unk)

    # Create test bigram_mle counts
    test_bigram_counts_mle_q5 = create_bigram_count_dict_single_sentence(q5_sentence_tokenized_after_unk)

    # Create test bigram_aos counts
    test_bigram_counts_aos_q5 = copy.deepcopy(test_bigram_counts_mle_q5)
    params_bigram_aos_q5 = []
    params_bigram_mle_q5 = []
    for key in test_bigram_counts_aos_q5:
        test_bigram_counts_aos_q5[key] += 1
        params_bigram_mle_q5.append(key)
        params_bigram_aos_q5.append(key)


    #Create test bigram_mle
    test_bigram_mle_q5 = get_bigram(test_bigram_counts_mle_q5, train_unigram_counts_mle_q5)

    #Create test bigram_aos
    test_bigram_aos_q5 = get_bigram_aos(test_bigram_counts_aos_q5, train_unigram_counts_mle_q5)


    for key in test_unigram_mle_q5:
        test_unigram_mle_q5[key] = test_unigram_mle_q5[key] if key in train_unigram_mle_q5 else 0.0

    for key in test_bigram_mle_q5:
        test_bigram_mle_q5[key] = test_bigram_mle_q5[key] if key in train_bigram_mle_q5 else 0.0

    for key in test_bigram_aos_q5:
        if key in train_bigram_aos_q5:
            test_bigram_aos_q5[key] = test_bigram_aos_q5[key]
        else:
            test_bigram_aos_q5[key] = 1/ (test_unigram_counts_mle_q5[key.split()[0]] + len(q5_sentence_tokenized_after_unk))



    #******Log Probability for unigram_mle******
    log_probability_string_unigram_mle_q5 = ""


    q5_sentence_length = len(q5_sentence_tokenized_after_unk)

    unigram_mle_log_probability_q5 = 0
    log_probability_undefined = False  # Flag needed if we have to take log(0)
    for key in test_unigram_mle_q5:
        if key in train_unigram_mle_q5 and train_unigram_mle_q5[key] != 0:
            unigram_mle_log_probability_q5 += math.log(train_unigram_mle_q5[key])
            log_probability_string_unigram_mle_q5 += " + " + str(math.log(train_unigram_mle_q5[key]))
        else:
            log_probability_undefined = True
            log_probability_string_unigram_mle_q5 += " + log(0)"

    if not log_probability_undefined:
        log_probability_string_unigram_mle_q5 += "\n= " + str(unigram_mle_log_probability_q5) + "\n"
    else:
        log_probability_string_unigram_mle_q5 += "\n= NaN\n"


    # ******Log Probability for bigram_mle******
    log_probability_string_bigram_mle_q5 = ""
    bigram_mle_log_probability_q5 = 0
    log_probability_undefined = False  # Flag needed if we have to take log(0)
    for key in test_bigram_mle_q5:
        if key in train_bigram_mle_q5 and train_bigram_mle_q5[key] != 0:
            bigram_mle_log_probability_q5 += math.log(train_bigram_mle_q5[key])
            log_probability_string_bigram_mle_q5 += " + " + str(math.log(train_bigram_mle_q5[key]))
        else:
            log_probability_undefined = True
            log_probability_string_bigram_mle_q5 += " + log(0)"

    if not log_probability_undefined:
        log_probability_string_bigram_mle_q5 += "\n= " + str(bigram_mle_log_probability_q5) + "\n"
    else:
        log_probability_string_bigram_mle_q5 += "\n= NaN\n"


    # ******Log Probability for bigram_aos******
    log_probability_string_bigram_aos_q5 = ""
    bigram_aos_log_probability_q5 = 0
    log_probability_undefined = False  # Flag needed if we have to take log(0)
    for key in test_bigram_aos_q5:
        if key in train_bigram_aos_q5:
            bigram_aos_log_probability_q5 += math.log(train_bigram_aos_q5[key])
            log_probability_string_bigram_aos_q5 += " + " + str(math.log(train_bigram_aos_q5[key]))

    if not log_probability_undefined:
        log_probability_string_bigram_aos_q5 += "\n= " + str(bigram_aos_log_probability_q5) + "\n"
    else:
        log_probability_string_bigram_aos_q5 += "\n= NaN\n"



    # ******Perplexity Calculations for Question 6******

    M = len(q5_sentence_tokenized_after_unk)
    perplexity_string_unigram_mle_q5 = str(compute_perplexity(unigram_mle_log_probability_q5, M)) if "NaN" not in log_probability_string_unigram_mle_q5 else "NaN"
    perplexity_string_bigram_mle_q5 = str(compute_perplexity(bigram_mle_log_probability_q5, M)) if "NaN" not in log_probability_string_bigram_mle_q5 else "NaN"
    perplexity_string_bigram_aos_q5 = str(compute_perplexity(bigram_aos_log_probability_q5, M)) if "NaN" not in log_probability_string_bigram_aos_q5 else "NaN"

    # ******Question 7******

    # test_dict_after_unk


    # Create test unigram_mle
    test_unigram_mle_q7 = {}
    test_unigram_counts_mle_q7 = copy.deepcopy(test_dict_after_unk)

    num_tokens_q7 = count_tokens(test_dict_after_unk)
    for token in test_unigram_counts_mle_q7:
        test_unigram_mle_q7[token] = test_unigram_counts_mle_q7[token] / num_tokens_q7

    # Create test bigram_mle counts
    test_bigram_counts_mle_q7 = create_bigram_count_dict(tokenized_test_data_after_unk)

    # Create test bigram_aos counts
    test_bigram_counts_aos_q7 = copy.deepcopy(test_bigram_counts_mle_q7)

    for key in test_bigram_counts_aos_q7:
        test_bigram_counts_aos_q7[key] += 1


    # Create test bigram_mle
    test_bigram_mle_q7 = get_bigram(test_bigram_counts_mle_q7, test_unigram_counts_mle_q7)

    # Create test bigram_aos
    test_bigram_aos_q7 = get_bigram_aos(test_bigram_counts_aos_q7, test_unigram_counts_mle_q7)

    # for key in test_unigram_mle_q7:
    #     test_unigram_mle_q7[key] = test_unigram_mle_q7[key] if key in train_unigram_counts_mle_q5 else 0.0

    for key in test_bigram_mle_q7:
        test_bigram_mle_q7[key] = test_bigram_mle_q7[key] if key in train_bigram_counts_mle else 0.0

    for key in test_bigram_aos_q7:
        if key in train_bigram_aos_q5:
            test_bigram_aos_q7[key] = test_bigram_aos_q7[key]
        else:
            test_bigram_aos_q7[key] = 1 / (
                        test_unigram_counts_mle_q7[key.split()[0]] + num_tokens_q7 )

    # ******Log Probability for unigram_mle******
    log_probability_string_unigram_mle_q7 = ""


    unigram_mle_log_probability_q7 = 0
    # log_probability_undefined = False  # Flag needed if we have to take log(0)
    for key in test_unigram_mle_q7:
        if key in train_unigram_mle_q5:
            unigram_mle_log_probability_q7 += math.log(train_unigram_mle_q5[key])
            log_probability_string_unigram_mle_q7 += " + " + str(math.log(train_unigram_mle_q5[key]))

    # if not log_probability_undefined:
    #     log_probability_string_unigram_mle_q7 += "\n= " + str(unigram_mle_log_probability_q7) + "\n"
    # else:
    #     log_probability_string_unigram_mle_q7 += "\n= NaN\n"

    # ******Log Probability for bigram_mle******
    log_probability_string_bigram_mle_q7 = ""
    bigram_mle_log_probability_q7 = 0
    log_probability_undefined = False  # Flag needed if we have to take log(0)
    for key in test_bigram_mle_q7:
        if key in train_bigram_mle_q5 and train_bigram_mle_q5[key] != 0:
            bigram_mle_log_probability_q7 += math.log(train_bigram_mle_q5[key])
            log_probability_string_bigram_mle_q7 += " + " + str(math.log(train_bigram_mle_q5[key]))
        else:
            log_probability_undefined = True
            log_probability_string_bigram_mle_q7 += " + log(0)"

    if not log_probability_undefined:
        log_probability_string_bigram_mle_q7 += "\n= " + str(bigram_mle_log_probability_q7) + "\n"
    else:
        log_probability_string_bigram_mle_q7 += "\n= NaN\n"

    # ******Log Probability for bigram_aos******
    log_probability_string_bigram_aos_q7 = ""
    bigram_aos_log_probability_q7 = 0
    log_probability_undefined = False  # Flag needed if we have to take log(0)
    for key in test_bigram_aos_q7:
        if key in train_bigram_aos_q5:
            bigram_aos_log_probability_q7 += math.log(train_bigram_aos_q5[key])
            log_probability_string_bigram_aos_q7 += " + " + str(math.log(train_bigram_aos_q5[key]))

    if not log_probability_undefined:
        log_probability_string_bigram_aos_q7 += "\n= " + str(bigram_aos_log_probability_q7) + "\n"
    else:
        log_probability_string_bigram_aos_q7 += "\n= NaN\n"

    M = len(test_dict_after_unk)
    perplexity_string_unigram_mle_q7 = str(compute_perplexity(unigram_mle_log_probability_q7,
                                                              M)) if "NaN" not in log_probability_string_unigram_mle_q7 else "NaN"
    perplexity_string_bigram_mle_q7 = str(compute_perplexity(bigram_mle_log_probability_q7,
                                                             M)) if "NaN" not in log_probability_string_bigram_mle_q7 else "NaN"
    perplexity_string_bigram_aos_q7 = str(compute_perplexity(bigram_aos_log_probability_q7,
                                                             M)) if "NaN" not in log_probability_string_bigram_aos_q7 else "NaN"

    print("Q1: How many word types (unique words) are there in the training corpus?\n "
          "Please include the padding symbols and the unknown token.\n" + str(unique_train_token_count_after_unk))

    print("Q2:How many word tokens are there in the training corpus?\n" + str(total_train_token_count_after_unk))

    print("Q3: What percentage of word tokens and word types in the test corpus did not occur in training\n"
          " (before you mapped the unknown words to <unk> in training and test data)? \n"
          "Please include the padding symbols in your calculations.")

    print("a). Percentage of word tokens in test corpus not in training \n" + str(total_count_tokens_in_test_not_in_train) + "/" +
          str(total_test_token_count_before_unk) + " OR \n" +
          str(total_count_tokens_in_test_not_in_train/total_test_token_count_before_unk) + "%\n")

    print("b). Percentage of word types in test corpus that did not occur in training \n" +
          str(count_word_types_testing_not_training) + "/" + str(unique_test_token_count_before_unk) +
          " OR \n" + str(count_word_types_testing_not_training / unique_test_token_count_before_unk) + "%\n")

    print("Q4: Now replace singletons in the training data with <unk> symbol and map words (in the test corpus)\n "
          "not observed in training to <unk>. \n What percentage of bigrams (bigram types and bigram tokens) "
          "in the test "
          "corpus did not occur in training (treat <unk> as a regular token that has been observed).")

    print("a). Percentage of bigram tokens in the test corpus that did not occur in training \n " +
          str(count_total_bigrams_in_test_but_not_train_q4) + "/" + str(count_total_test_bigram_counts) +
          " OR \n" + str(count_total_bigrams_in_test_but_not_train_q4 / count_total_test_bigram_counts * 100) + "%\n")

    print("b). Percentage of bigram types in the test corpus that did not occur in training \n " +
          str(count_unique_bigrams_in_test_but_not_train) + "/" + str(count_total_unique_bigrams) +
          " OR \n" + str((count_unique_bigrams_in_test_but_not_train / count_total_unique_bigrams) * 100) + "%\n")

    print("Q5: Compute the log probability of the following sentence under the three models (ignore capitalization\n"
          " and pad each sentence as described above). Please list all of the parameters required to compute the\n"
          "probabilities and show the complete calculation. Which of the parameters have zero values under each "
          "model?\n "
          "Use log base 2 in your calculations. Map words not observed in the training corpus to the <unk> token.\n"
          "I look forward to hearing your reply .\n")




    print("******Unigram Maximum Likelihood Log Probability******\n" + log_probability_string_unigram_mle_q5)
    print("Parameters needed:\n")
    print(params_unigram_mle_q5)
    print("******Bigram Maximum Likelihood Log Probability******\n" + log_probability_string_bigram_mle_q5)
    print("Parameters needed:\n")
    print(params_bigram_mle_q5)
    print("******Bigram Add One Smoothing Log Probability******\n" + log_probability_string_bigram_aos_q5)
    print("Parameters needed:\n")
    print(params_bigram_aos_q5)

    print("Parameters with 0 probabilities (Notice that only for Bigram MLE:\n")
    print("Unigram MLE:\n")
    for key in params_unigram_mle_q5:
        if test_unigram_mle_q5[key] == 0:
            print("<"+key + ">" + "\n")
    print("Bigram MLE:\n")
    for key in params_bigram_mle_q5:
        if test_bigram_mle_q5[key] == 0:
            print("<"+key.split()[0] + ", " + key.split()[1] + ">" + "\n")
    print("Bigram AOS:\n")
    for key in params_bigram_aos_q5:
        if test_bigram_aos_q5[key] == 0:
            print("<"+key.split()[0] + ", " + key.split()[1] + ">" + "\n")


    print("Q6: Compute the perplexity of the sentence above under each of the models.\n")
    print("******Unigram Maximum Likelihood Perplexity******\n" + perplexity_string_unigram_mle_q5 + "\n")
    print("******Bigram Maximum Likelihood Perplexity******\n" + perplexity_string_bigram_mle_q5 + "\n")
    print("******Bigram Add One Smoothing Perplexity******\n" + perplexity_string_bigram_aos_q5 + "\n")

    print("Q7: Compute the perplexity of the entire test corpus under each of the models.\n"
          "Discuss the differences in the results you obtained.")
    print("******Unigram Maximum Likelihood Perplexity******\n" + perplexity_string_unigram_mle_q7 + "\n")
    print("******Bigram Maximum Likelihood Perplexity******\n" + perplexity_string_bigram_mle_q7 + "\n")
    print("******Bigram Add One Smoothing Perplexity******\n" + perplexity_string_bigram_aos_q7 + "\n")
    print("Like before, the Bigram Maximum Likelihood is susceptible to NaN perplexity because of the susceptibility to"
          "0 probabilities. Bigram with add one smoothing has significantly higher perplexity than the unigram")


if __name__ == "__main__":
    main()

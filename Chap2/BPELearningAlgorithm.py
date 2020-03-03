import re, collections

#The algorithm begins with the set of symbols equal to the set of characters. Each word is represented as a sequence of characters plus a special end-of-word symbol . At each step of the algorithm, we count the number of symbol pairs, find the most frequent pair (‘A’, ‘B’), and replace it with the new merged symbol (‘AB’). We continue to count and merge, creating new longer and longer character strings, until we’ve done k merges; k is a parameter of the algorithm. The resulting symbol set
# will consist of the original set of characters plus k new symbols.
# The algorithm is run inside words (we don’t merge across word boundaries). For this reason, the algorithm can take as input a dictionary of words together with counts. Consider the following tiny input dictionary with counts for each word,
# which would have the starting vocabulary of 11 letters:



def get_stats(vocab):
    pairs = collections.defaultdict(int)

    # Iterate through the vocab dictionary where key = word and value = frequency
    for word, freq in vocab.items():
        symbols = word.split()  # How is symbols split? By space default?

        # For each word, count how often two consecutive symbols occur
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq
    return pairs


def merge_vocab(pair, v_in):
    v_out = {}
    #  escape() Return string with all non-alphanumerics backslashed;
    # this is useful if you want to match an arbitrary literal string that may
    # have regular expression metacharacters in it.
    bigram = re.escape(' '.join(pair)) # The join() method is a string method and returns a string in which the
    # elements of sequence have been joined by str separator.
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        # sub replaces every occurrence of a pattern with a
        # string or the result of a function
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out


# Create vocab dictionary
vocab = {'1 o w </w>': 5, 'l o w e s t </w': 2,
         'n e w e r </w>': 6, 'w i d e r </w>': 3, 'n e w </w>': 2}
# Specify number of merges
num_merges = 8

for i in range(num_merges):
    pairs = get_stats(vocab)  # Call get_stats to create the pair
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    print(best)

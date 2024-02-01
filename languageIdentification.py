import os
import sys
import math

#input: text (str). The training text for a language.
#output: Two dictionaries containing unigram and bigram frequencies.
#purpose: Trains a bigram language model from the text.
def trainBigramLanguageModel(text):

    unigram_frequencies = {}
    bigram_frequencies = {}

    # Iterate through each character in the text
    for i in range(len(text)):
        # Extract and count unigrams (single characters)
        unigram = text[i]
        if unigram not in unigram_frequencies:
            unigram_frequencies[unigram] = 0
        unigram_frequencies[unigram] += 1

        # Extract and count bigrams (pairs of characters)
        if i < len(text) - 1:
            bigram = text[i:i+2]
            if bigram not in bigram_frequencies:
                bigram_frequencies[bigram] = 0
            bigram_frequencies[bigram] += 1
    total_unique_bigrams = len(bigram_frequencies)

    return unigram_frequencies, bigram_frequencies, total_unique_bigrams


    # input: test_string (str we are trying to identify)
    #       language_names 
    #       unigram_dicts (list). list of dictionaries with unigram frequencies for each language.
    #       bigram_dicts (list): list of dictionaries with bigram frequencies for each language.
    # output: The most likely language of the given string.
    # purpose: identifies the most likely language of a given string.
def identifyLanguage(test_string, language_names, unigram_dicts, bigram_dicts, vocab_sizes):
    best_language = None
    max_log_probability = float('-inf')

    # Iterate through each language to find the best match
    for i, language in enumerate(language_names):
        log_probability = 0
        for j in range(len(test_string) - 1):
            bigram = test_string[j:j+2]
            bigram_freq = bigram_dicts[i].get(bigram, 0)
            unigram_freq = unigram_dicts[i].get(test_string[j], 0)

            # smoothing!
            smoothed_probability = (bigram_freq + 1) / (unigram_freq + vocab_sizes[i])
            log_probability += math.log(smoothed_probability)

        #potential match!
        if log_probability > max_log_probability:
            max_log_probability = log_probability
            best_language = language

    return best_language

def main(training_folder, test_file):
    languages = ["English", "French", "Italian"]
    unigram_dicts = []
    bigram_dicts = []
    vocab_sizes = []

    #stole this from somewhere I dont know what it does
    def safe_read(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='ISO-8859-1', errors='replace') as file:
                return file.read()

    # goes through each language in list and trains off of them
    for language in languages:
        text = safe_read(os.path.join(training_folder, language))
        unigrams, bigrams, vocab_size = trainBigramLanguageModel(text)
        unigram_dicts.append(unigrams)
        bigram_dicts.append(bigrams)
        vocab_sizes.append(vocab_size)

    test_text = safe_read(test_file)
    test_lines = test_text.splitlines()  # This handles different types of line endings


    with open('languageIdentification.output', 'w') as output_file:
        for i, line in enumerate(test_lines):
            line = line.strip()
            if line:
                language = identifyLanguage(line, languages, unigram_dicts, bigram_dicts, vocab_sizes)
                output_file.write(f'{i+1} {language}\n')

if __name__ == "__main__":
    training_folder = sys.argv[1]
    test_file = sys.argv[2]
    main(training_folder, test_file)


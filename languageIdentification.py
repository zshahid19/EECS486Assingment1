import os
import sys

def trainBigramLanguageModel(text):
    """
    Trains a bigram language model from the given text.

    Args:
    text (str): The training text for a specific language.

    Returns:
    tuple: Two dictionaries containing unigram and bigram frequencies.
    """
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

    return unigram_frequencies, bigram_frequencies

def identifyLanguage(test_string, language_names, unigram_dicts, bigram_dicts):
    """
    Identifies the most likely language of a given string.

    Args:
    test_string (str): The string to identify the language of.
    language_names (list): List of language names.
    unigram_dicts (list): List of dictionaries with unigram frequencies for each language.
    bigram_dicts (list): List of dictionaries with bigram frequencies for each language.

    Returns:
    str: The most likely language of the given string.
    """
    best_language = None
    max_probability = -1

    # Iterate through each language to find the best match
    for i, language in enumerate(language_names):
        probability = 1
        # Calculate the bigram probability for the test string
        for j in range(len(test_string) - 1):
            bigram = test_string[j:j+2]
            bigram_freq = bigram_dicts[i].get(bigram, 0)
            unigram_freq = unigram_dicts[i].get(test_string[j], 1)  # Avoid division by zero
            probability *= (bigram_freq / unigram_freq)

        # Update the best language based on the highest probability
        if probability > max_probability:
            max_probability = probability
            best_language = language

    return best_language

def main(training_folder, test_file):
    languages = ["English", "French", "Italian"]
    unigram_dicts = []
    bigram_dicts = []

    # Function to safely read text from a file with different encodings
    def safe_read(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().replace('\n', '')
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                return file.read().replace('\n', '')

    # Train language models for each language
    for language in languages:
        text = safe_read(os.path.join(training_folder, language))
        unigrams, bigrams = trainBigramLanguageModel(text)
        unigram_dicts.append(unigrams)
        bigram_dicts.append(bigrams)

    # Process each line in the test file and determine its language
    test_text = safe_read(test_file)
    test_lines = test_text.split('\n')

    with open('languageIdentification.output', 'w') as output_file:
        for i, line in enumerate(test_lines):
            if line:  # Ensure line is not empty
                language = identifyLanguage(line, languages, unigram_dicts, bigram_dicts)
                output_file.write(f'{i+1} {language}\n')

if __name__ == "__main__":
    training_folder = sys.argv[1]
    test_file = sys.argv[2]
    main(training_folder, test_file)


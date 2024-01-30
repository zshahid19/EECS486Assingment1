#!/usr/bin/env python3
import os
import re
"""
Module Docstring
"""

# Questions:
# How should numbers, peroids be handled. Yes to them in abreviations or no spec is confusing
# What exactly should I be adding to my vocabulary just subwords?
# how to handle start before each word? just add a start before every token? or just assume in BPE? Or Start in just start of sentences??
# how am I to return merge rules? number of merge rules or strings of the rules?

#Input: folder_path (path towards the folder with the dataset)
#Output: List containing all the files from the input folder_path
#Purpose: to turn the folder_path and give the user an actual manipultable data
def list_files_in_folder(folder_path):
    #Empty file_path list
    file_paths = []
    
    if not os.path.isdir(folder_path):
        print(f"Path does not exist")
        return file_paths

    #Iterating thorugh folder
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        # If good add it to the list
        if os.path.isfile(full_path):
            file_paths.append(full_path)

    return file_paths

#Input: A string containing the text from a file
#Output: the string with all the SGML tags removed
#Purpose: remove all the SGML tags from the input string
def removeSGML(file_text):
    #removed all SGML tags
    clean_text = re.sub(r'<.*?>', '', file_text)
    # print(clean_text)
    return clean_text


#Input: Take in cleaned text (no SGML text)
#Output: List (of tokens)
#Purpose: Take in the cleaned text, tokenize that text then return list of tokens of that text
def tokenizeText(cleaned_text):
    # Expand contractions
    def expand_contractions(token):
        contractions = { "I'm": "I am", "I'm'a": "I am about to", "I'm'o": "I am going to", "I've": "I have", "I'll": "I will", "I'll've": "I will have", "I'd": "I would", "I'd've": "I would have", "Whatcha": "What are you", "amn't": "am not", "ain't": "are not", "aren't": "are not", "'cause": "because", "can't": "cannot", "can't've": "cannot have", "could've": "could have", "couldn't": "could not", "couldn't've": "could not have", "daren't": "dare not", "daresn't": "dare not", "dasn't": "dare not", "didn't": "did not", "didn’t": "did not", "don't": "do not", "don’t": "do not", "doesn't": "does not", "e'er": "ever", "everyone's": "everyone is", "finna": "fixing to", "gimme": "give me", "gon't": "go not", "gonna": "going to", "gotta": "got to", "hadn't": "had not", "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not", "he've": "he have", "he's": "he is", "he'll": "he will", "he'll've": "he will have", "he'd": "he would", "he'd've": "he would have", "here's": "here is", "how're": "how are", "how'd": "how did", "how'd'y": "how do you", "how's": "how is", "how'll": "how will", "isn't": "is not", "it's": "it is", "'tis": "it is", "'twas": "it was", "it'll": "it will", "it'll've": "it will have", "it'd": "it would", "it'd've": "it would have", "kinda": "kind of", "let's": "let us", "luv": "love", "ma'am": "madam", "may've": "may have", "mayn't": "may not", "might've": "might have", "mightn't": "might not", "mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have", "ne'er": "never", "o'": "of", "o'clock": "of the clock", "ol'": "old", "oughtn't": "ought not", "oughtn't've": "ought not have", "o'er": "over", "shan't": "shall not", "sha'n't": "shall not", "shalln't": "shall not", "shan't've": "shall not have", "she's": "she is", "she'll": "she will", "she'd": "she would", "she'd've": "she would have", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have", "so's": "so is", "somebody's": "somebody is", "someone's": "someone is", "something's": "something is", "sux": "sucks", "that're": "that are", "that's": "that is", "that'll": "that will", "that'd": "that would", "that'd've": "that would have", "'em": "them", "there're": "there are", "there's": "there is", "there'll": "there will", "there'd": "there would", "there'd've": "there would have", "these're": "these are", "they're": "they are", "they've": "they have", "they'll": "they will", "they'll've": "they will have", "they'd": "they would", "they'd've": "they would have", "this's": "this is", "this'll": "this will", "this'd": "this would", "those're": "those are", "to've": "to have", "wanna": "want to", "wasn't": "was not", "we're": "we are", "we've": "we have", "we'll": "we will", "we'll've": "we will have", "we'd": "we would", "we'd've": "we would have", "weren't": "were not", "what're": "what are", "what'd": "what did", "what've": "what have", "what's": "what is", "what'll": "what will", "what'll've": "what will have", "when've": "when have", "when's": "when is", "where're": "where are", "where'd": "where did", "where've": "where have", "where's": "where is", "which's": "which is", "who're": "who are", "who've": "who have", "who's": "who is", "who'll": "who will", "who'll've": "who will have", "who'd": "who would", "who'd've": "who would have", "why're": "why are", "why'd": "why did", "why've": "why have", "why's": "why is", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all're": "you all are", "y'all've": "you all have", "y'all'd": "you all would", "y'all'd've": "you all would have", "you're": "you are", "you've": "you have", "you'll've": "you shall have", "you'll": "you will", "you'd": "you would", "you'd've": "you would have", "to cause": "to cause", "will cause": "will cause", "should cause": "should cause", "would cause": "would cause", "can cause": "can cause", "could cause": "could cause", "must cause": "must cause", "might cause": "might cause", "shall cause": "shall cause", "may cause": "may cause" }
        return contractions.get(token, [token])

    # get the whole date   
    def is_date(char, current_token):
        return char in ['/', '-'] and any(c.isdigit() for c in current_token)
    
    # get the whole acronym
    def is_acronym(i, char, text):
        return char == '.' and i < len(text) - 1 and text[i + 1].isupper()
    
    #  checking for big number digits or commas
    def is_big_number(char, current_token):
        return char.isdigit() or (char == ',' and current_token and current_token.replace(',', '').isdigit())

    tokens = []
    current_token = ''
    word_start = True  # Flag to indicate start of a new word

    for i, char in enumerate(cleaned_text):
        if char.isspace() or char in '.!?':
            word_start = True
            if current_token:
                tokens.extend(expand_contractions(current_token))
                current_token = ''
            continue

        if word_start and current_token:
            # If we are at a word start, finalize the previous token
            tokens.extend(expand_contractions(current_token))
            current_token = ''
        
        word_start = False  # Reset word start flag as we are in the middle of a word

        # logic for handling character addition to tokens
        if (char.isalpha() or char in ['\'', '-'] or 
            is_date(char, current_token) or 
            is_big_number(char, current_token)):
            current_token += char
        elif char == '.' and (is_big_number(char, current_token) or is_acronym(i, char, cleaned_text)):
            current_token += char
        else:
            if current_token:
                tokens.extend(expand_contractions(current_token))
                current_token = ''

        # Handle the final token
    if current_token:
            tokens.extend(expand_contractions(current_token))

    return tokens

    
#Input: tokenized_text list of pre-tokenized text (list of strings)
#Output: Set of unique characters in the tokenized text 
#Purpose: find the vocabulary from the tokenized text
def get_vocab(tokenized_text):
    vocab = set()
    for word in tokenized_text:
        vocab.update(list(word))
    return vocab

#Input: tokenized_text
#Output: dict with pair frequencies
#Purpose: Calculates the frequinces of character pairs
def get_pair_frequencies(tokenized_text):
    pairs = {}
    for tokens in tokenized_text:
        for i in range(len(tokens)-1):
            pair = (tokens[i], tokens[i+1])
            if pair in pairs:
                pairs[pair] += 1
            else:
                pairs[pair] = 1
    return pairs
# Input: pair of two characters, tokenized_text
# Output: merged pair token
# Purpose: merge pair of character
def merge_vocab(pair, tokenized_text):
    merged_text = []
    for tokens in tokenized_text:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
                merged_token = tokens[i] + tokens[i + 1]
                print(f"Merging {tokens[i]} and {tokens[i + 1]} into {merged_token}")  # Debug print
                new_tokens.append(merged_token)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        merged_text.append(new_tokens)
    return merged_text




def flatten_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        if isinstance(sublist, list):
            flat_list.extend(sublist)
        else:
            flat_list.append(sublist)
    return flat_list




#input list( of tokens), vocabSize
#output: list (subword tokens), list (merge rules)
#Purpose: split tokens into subwords to increase vocab count?
def bpe(tokenized_text, target_vocab_size):
    flat_list = flatten_list(tokenized_text)

    # Initialize vocabulary with individual characters from tokens
    vocab = set(''.join(flat_list))  # Create a set of unique characters

    merge_rules = []

    while len(vocab) < target_vocab_size:
        pairs = get_pair_frequencies(flat_list)
        if not pairs:
            break

        best_pair = max(pairs, key=pairs.get)
        merge_rules.append(best_pair)
        
        flat_list = merge_vocab(best_pair, flat_list)
        flat_list = flatten_list(flat_list)  # Flatten the list after each merge

        # Update the vocabulary
        vocab = set(''.join(flat_list))

    # Counting frequencies
    token_frequencies = {}
    for token in flat_list:
        if isinstance(token, list):
            raise ValueError(f"Unexpected list in flat_list: {token}")
        token_frequencies[token] = token_frequencies.get(token, 0) + 1

    return flat_list, vocab, merge_rules, token_frequencies




def main():
    if len(sys.argv) != 3:
        print("Usage: script.py <folder_path> <vocab_size>")
    #     sys.exit(1)
    #folder_path = sys.argv[1]
    #vocab_size = int(sys.argv[2])

    folder_path = "test1/"
    vocab_size = 10000
    file_paths = list_files_in_folder(folder_path)
    token_list = []
    
    #opening each file
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            #Sending each file to removeSGML
            cleaned_content = removeSGML(content)
            # print(f"Revmoed SGL on file: {file_path}")
            #Send each cleaned file to be tokenized
            token_list.append(tokenizeText(cleaned_content))
    # print(len(token_list)) Now we have a list of list of tokens 2d list.
    
    #BPE time
    new_text, new_vocab, merge_rules, token_frequencies = bpe(token_list, vocab_size)

    # Sort tokens and merge rules
    sorted_tokens = sorted(token_frequencies.items(), key=lambda x: x[1], reverse=True)
    sorted_merge_rules = merge_rules[:20]  # First 20 merge rules

    # Write to file
    with open("preprocess.output", "w") as file:
        file.write(f"Tokens [{len(new_vocab)}]\n")
        file.write(f"Merge rules [{len(merge_rules)}]\n")
        
        for rule in sorted_merge_rules:
            file.write(f"({rule[0]}, {rule[1]}) -> {rule[0]}{rule[1]}\n")

        file.write("\nTop 50 tokens\n")
        for token, freq in sorted_tokens[:50]:
            file.write(f"{token} [{freq}]\n")


def open_file(file_name):
    input_file = open(file_name, 'r')
    return input_file



if __name__ == "__main__":
    import sys
    main()

import argparse
from argparse import Namespace
from itertools import combinations, permutations
from typing import List, Iterable, Optional, Tuple, Set

from format_words import FILE_PATH_ENGLISH, FILE_PATH_HEBREW
from probable_phrase import most_probable


def load_words(language: str) -> List[str]:
    if language in ["en", "english"]:
        return _load_words(FILE_PATH_ENGLISH)
    elif language in ["he", "hebrew"]:
        return _load_words(FILE_PATH_HEBREW)
    raise AttributeError("Invalid Language")


def _load_words(file_path: str) -> List[str]:
    with open(file_path) as file:
        lines = [line.rstrip() for line in file]
    return lines


def all_splits(lst: List[str]) -> Set[Tuple[Tuple[str], ...]]:
    result = {(tuple(lst),)}
    if len(lst) <= 3:
        return result
    for i in range(2, len(lst) // 2 + 1):
        combs = list(combinations(lst, i))
        for subset in combs:
            subset_complement = [item for item in lst if item not in subset]
            possible_complements = all_splits(subset_complement)

            for complement in possible_complements:
                split = tuple(sorted([subset, *complement]))
                result.add(split)
    return result


def valid_phrase(letter_groups: Tuple[Tuple[str], ...], word_list: Iterable[str]) -> Optional[List[str]]:
    phrase = []
    for letter_group in letter_groups:
        word = valid_word(list(letter_group), word_list)
        if not word:
            return None
        phrase.append(word)
    return phrase


def valid_word(anagram_letters: List[str], words: Iterable[str]) -> Optional[str]:
    for word in words:
        if len(word) > len(anagram_letters):
            return None
        if sorted(word) == anagram_letters:
            return word
    return None


def generate_phrases(letters_split: Set[Tuple[Tuple[str], ...]], words_list: List[str]) -> List[List[str]]:
    phrases: List[List[str]] = []
    for split in letters_split:
        if phrase := valid_phrase(split, words_list):
            phrases.append(phrase)
    return phrases


def generate_sentences(phrase_list: List[List[str]]) -> List[str]:
    sentences = []
    for phrase in phrase_list:
        sentences.extend(" ".join(s) for s in permutations(phrase))
    return sentences


def main(args: Namespace) -> None:
    if not args.initials.isalpha():
        raise AttributeError("invalid initials")

    anagram_letters: List[str] = list(args.initials)
    anagram_letters.sort()

    words_list = load_words(args.language)

    # Generates all the ways to split anagram letter
    letters_split = all_splits(anagram_letters)

    # Finds all valid word splits
    phrases = generate_phrases(letters_split, words_list)

    if not phrases:
        print("No valid anagram.")
        return

    # Generates all possible sentences
    sentences = generate_sentences(phrases)

    # Ranks sentences by likelihood to be a real english sentence
    probable_phrases = most_probable(sentences)

    print(probable_phrases[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates an Anagram')
    parser.add_argument('initials', type=str,
                        help='letter initials to anagram')
    parser.add_argument('language', type=str, choices=["en", "English", "he", "Hebrew"],
                        help='input language')
    _args = parser.parse_args()
    main(_args)

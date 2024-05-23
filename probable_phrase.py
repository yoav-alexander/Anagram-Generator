from typing import List

import nltk
from nltk.corpus import words
from nltk.tokenize import word_tokenize

# nltk.download('punkt', quiet=True, download_dir="nltk-punkt")
# nltk.download('words', quiet=True,  download_dir="nltk-words" )

# for hebrew:
# nltk.download('averaged_perceptron_tagger')
# nltk.download('perluniprops')

word_list = set(words.words())


def sentence_score(sentence):
    tokens = word_tokenize(sentence.lower())
    return sum(1 for word in tokens if word in word_list)


def most_probable(phrase_list: list[str]) -> List[str]:
    scored_sentences = [(sentence, sentence_score(sentence)) for sentence in phrase_list]
    probable_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)
    return [sentence for sentence, _ in probable_sentences]

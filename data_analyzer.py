import re
import nltk
import os


class DataCleaner:
    def __init__(self):
        self.__stopwords = set()
        self.__Stopword_init()

    def __Stopword_init(self):  # method populating the stopwords set
        directory = 'StopWords'
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                text = None
                with open(path, 'rt') as f:
                    for line in f:
                        self.__stopwords.add(line.split('|')[0].strip().lower())

    # filtering out stopwords and returning filtered words, word count, and avg sentence length
    def RemoveStopwordsAndWordCount(self, text: str):
        words = nltk.word_tokenize(text.lower())
        sentences = nltk.sent_tokenize(text)
        total_sentences = len(sentences)
        # print(sentences)
        filtered_words = [word for word in words if word not in self.__stopwords]
        # print(filtered_words)
        total_words = len(filtered_words)
        avg_sent_len = total_words / total_sentences
        return filtered_words, total_words, avg_sent_len


class DataAnalyzer:
    def __init__(self, stopwords_cleaner: DataCleaner):  # class constructor initializing the pos and neg word sets
        self.__positive_words = None
        self.__negative_words = None
        directory = 'MasterDictionary'
        try:
            with open(os.path.join(directory, 'positive-words.txt'), 'rt') as f:
                self.__positive_words = f.read()

            with open(os.path.join(directory, 'negative-words.txt'), 'rt') as f:
                self.__negative_words = f.read()
        except IOError:
            print(
                'Unable to read files... Kindly check positive-words.txt and negative-words.txt in ' + directory + '.')

        self.__positive_words, __a, __b = stopwords_cleaner.RemoveStopwordsAndWordCount(self.__positive_words)
        self.__negative_words, __a, __b = stopwords_cleaner.RemoveStopwordsAndWordCount(self.__negative_words)
        self.__positive_words, self.__negative_words = set(self.__positive_words), set(self.__negative_words)

    def posneg_score(self, words, total_words):
        """
        Calculation of positive and negative scores.
        :param words: tokenized cleaned words
        :param total_words: count of tokens
        :return: dict containing positive score, negative score, polarity score and subjectivity scores
        """
        pos = 0
        neg = 0
        for word in words:
            if word in self.__positive_words:
                pos += 1
                # print(word)
            if word in self.__negative_words:
                neg += 1
                # print(word)
        polarity_score = (pos - neg) / ((pos + neg) + 0.000001)
        subjectivity_score = (pos + neg) / (total_words + 0.000001)
        return {'POSITIVE SCORE': pos, 'NEGATIVE SCORE': neg,
                'POLARITY SCORE': polarity_score, 'SUBJECTIVITY SCORE': subjectivity_score}

    def words_analysis(self, words, total_words, avg_sent_len):
        """
        method performing text analysis on the basis of words
        :param words:
        :param total_words:
        :param avg_sent_len:
        :return: complex word count, complex words percentage, avg syllable per word, avg word length, fog index
        """
        complex_count = 0
        total_syllables = 0
        total_characters = 0
        for word in words:
            syllable_count = self.__count_syllable(word)
            total_syllables += syllable_count
            if syllable_count > 2:
                complex_count += 1
            total_characters += len(word.strip())
        complex_perc = complex_count / total_words
        return {'COMPLEX WORD COUNT': complex_count, 'PERCENTAGE OF COMPLEX WORDS': complex_perc,
                'SYLLABLE PER WORD': (total_syllables / total_words),
                'AVG WORD LENGTH': (total_characters / total_words),
                'FOG INDEX': self.__fog_index(avg_sent_len, complex_perc)}

    def __fog_index(self, avg_sent_len, complex_perc):
        return 0.4 * (avg_sent_len + complex_perc)

    def __count_syllable(self, word: str):
        syllable_count = 0
        syllable_count += len(re.findall(r'[aeiouy]', word))
        if word.endswith('es') or word.endswith('ed'):
            syllable_count -= 1
        return syllable_count


def PronounCount(text):
    """
    function calculating the personal pronouns mentioned in the text,
    regex (regular expressions) is used to find the counts of words
    such as “I,” “we,” “my,” “ours,” and “us”.
    Special care is taken to exclude instances where the country name “US”
    is mistakenly included in the count.
    :param text:
    :return: count of the occurrences
    """
    count = len(re.findall(r"\b(I|we|my|ours|us)\b", text, flags=re.IGNORECASE))
    count -= len(re.findall(r"\b(US)\b", text))
    # print('COUNT ', count)
    return count


# if __name__ == '__main__':
#
    # # print(dataAnalyzer.positive_words)
    # # print(dataAnalyzer.negative_words)
    # print(dataAnalyzer.posneg_score(w, n))

import pickle
import os
import nltk
from nltk.corpus import stopwords


###############################
#####    Preprocessing    #####
###############################

#TODO - nltk-tokenizer verwendet. Sinnvoll???
def doc_to_tokens(filepath, lower_case, remove_stopwords):
    """ Creates a list of sentences from a document.

    Removes numbers and punctuation. Uses nltk-tokenizer.

    :param filepath: String - The path to the document/file.
    :param lower_case: boolean - iff True, all characters will be lowercased.
    :param remove_stopwords: boolean - iff True, stopwords will be removed.
    :return: List of list of strings - Each String as one token.
        Each inner list is one sentence.
        The outer list is the whole document.
    """
    sents = []

    if remove_stopwords:
        stopw = stopwords.words("german")
    else:
        stopw = []

    with open(filepath) as doc:
        for line in doc:
            for sent in nltk.sent_tokenize(line):
                # Filter and process tokens:
                    # According to parameter (don't) turn to lower case.
                    # According to parameter (don't) remove stopwords.
                    # Remove numbers and punctuation.
                if lower_case:
                    sents.append([token.lower() for token in nltk.word_tokenize(sent)
                                  if (token.isalpha()
                                      and not (token in stopw
                                               or token.lower() in stopw))])    # Remove stopwords also if written upper case
                else:
                    sents.append([token for token in nltk.word_tokenize(sent)
                                  if (token.isalpha()
                                      and not (token in stopw
                                               or token.lower() in stopw))])     # Remove stopwords also if written upper case

                # Skip blank lines
                if len(sents[-1]) == 0:
                    sents = sents[:-1]

    return sents



def get_corpus(folderpath, lower_case, remove_stopwords):
    """ Creates one list of all sentences from all documents of a folder.

    Removes numbers and punctuation. Uses nltk-tokenizer.

    :param folderpath: String - The path to the document/file.
    :param lower_case: boolean - rendered to doc_to_tokens()
    :param remove_stopwords: boolean - rendered to doc_to_tokens()
    :return: List of list of strings - Each String is one token.
        Each inner list is one sentence.
        The outer list contains the sentences from all documents.
    """
    print("BUILD COUPUS")
    corpus = []
    # Hole aus jeden file eine Liste aus sentences (sentence = list if tokens)
    for file in os.listdir(folderpath):
        filepath = os.path.join(folderpath, file)
        doc_sents = doc_to_tokens(filepath, lower_case, remove_stopwords)

        # Hänge die sentences einzeln an das Korpus an
        for sent in doc_sents:
            corpus.append(sent)
    return corpus


# TODO Kommentiere
# Code taken from: https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict/11218504#11218504
# Code modified
def save_corpus(corpus, save_as):
    print("SAVE CORPUS")

    with open(save_as, 'wb') as handle:
        pickle.dump(corpus, handle, protocol=pickle.HIGHEST_PROTOCOL)

# TODO Kommentiere
# Code taken from: https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict/11218504#11218504
# Code modified
def load_corpus(load_from):
    print("LOAD COUPUS")

    with open(load_from, 'rb') as handle:
        return pickle.load(handle)



filepath = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Testkorpus/-1._Das_freundliche_Pfarrhaus.txt"
creat_1750 = "/home/afh/BA/KORPUS - Nur mit Creation Date und ab 1750/Plain Texts from XML"
creat_1650 = "/home/afh/BA/KORPUS - Nur mit Creation Date und ab 1650/Plain Texts from XML"
#folderpath = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Korpus/"
folderpath_testcorpus = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Testkorpus/"

#corpus = get_corpus(creat_1750,
#                    lower_case=False,
#                    remove_stopwords=True)
#save_corpus(corpus, "CORP_DefaultUp")

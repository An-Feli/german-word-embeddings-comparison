# Code taken from https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#
# Code modified.

import gensim
from gensim.models import Word2Vec
from gensim.test.utils import datapath
from gensim import utils
from nltk.probability import FreqDist

#import os
import gensim.models
#import nltk
from collections import defaultdict
from gensim.models.callbacks import CallbackAny2Vec
import EpochSaver
import Preprocessing
#from nltk.corpus import stopwords



#########################################
#####                               #####
#####    EMBEDDINGS FROM SCRATCH    #####
#####                               #####
#########################################

def get_vocab(mdl):
    """ Returns vocabulary of a model both as list and as dictionary.

    :param mdl: Word2Vec-model - The model of which the vocabulary shall be returned.
    :return: List of String - List of all words of the model's vocabulary
        default dict - dictionary of all words of the models vocabulary -> index
    """
    result = defaultdict(lambda: -1)

    for index, word in enumerate(mdl.wv.index_to_key):
        result[word] = index

    return result.keys(), result  # return words only AND dict of words -> index


#############################
#####    Model Setup    #####
#############################

def test_info(mdl, testword):
    """ Saves to file and prints 10 most similar words to a testword and its vector and prints the vocabulary size of a model

    :param mdl: Word2Vec-model - The model of which the vocabulary shall be returned.
    :param testword: String - The word the information is printed about
    :return : List of tuples - 10 most similar words
    """
    print("\nTESTWORD: " + testword)
    #TODO EInkommentieren: print(mdl.wv[testword])

    most_sim = mdl.wv.most_similar(positive = [testword], topn = 10)
    print(most_sim)

    print("\nVOCABUALRY SIZE: ")
    print(len(get_vocab(mdl)[0]))

    return most_sim



def create_train_save(corpus_load_from, vector_size=300, epochs=1, save_as="w2v.model", testword=""):
    """ Creates, trains and saves a new model.

    Includes EpochSaver to log loss.

    :param corpus_load_from: String - rendered to load_corpus()
    :param vector_size: int - rendered to gensim.models.Word2Vec()
    :param epochs: int - rendered to gensim.models.Word2Vec()
    :param save_as: String - model will be saved under this name
    :param testword: String - testword to have some information printed
    """

    # Create Logger
    logger = EpochSaver.EpochSaver()

    # Create and train model
    print("\nCREATE AND TRAIN FROM SCRATCH")
    corpus = Preprocessing.load_corpus(corpus_load_from)
    model = gensim.models.Word2Vec(sentences=corpus,
                                   vector_size = vector_size,
                                   epochs=epochs,
                                   callbacks=[logger],
                                   compute_loss=True,
                                   sg=1,
                                   )

    # Print some info about testword and vocabulary
    try:
        test_info(model, testword)
    except:
        print("The word " + testword + "does not occur in the corpus or it occurs less than min_count")
        pass

    # Save model
    model.save(save_as)
    print("\nModel saved in " + save_as)



#######################################
#####                             #####
#####    PRETRAINED EMBEDDINGS    #####
#####                             #####
#######################################

# TDOD LÖSCHEN WEIL MODELL MANUELL RUNTERLADEN?
def download_save(save_as):
    """ Downloads and saves model trained on word2vec-google-news-300.

    :param save_as: String - model will be saved with this name
    """
    print("LOAD MODEL READY-TO-USE")

    import gensim.downloader as api
    model = api.load('word2vec-ruscorpora-300')
    model.save(save_as)

    print("MODEL SAVED AS " + save_as)


# TODO Kommentieren
def load_train_save(corpus_load_from, model_load_from, epochs=1, save_as="w2v.model", testword=""):

    # Load model and corpus
    model = gensim.models.Word2Vec.load(model_load_from)
    corpus = Preprocessing.load_corpus(corpus_load_from)

    # Create Epoch Saver for logging the loss
    logger= EpochSaver.EpochSaver()

    # Train model
    model.train(corpus_iterable=corpus,
                epochs = epochs,
                callbacks=[logger],
                compute_loss=True,
                total_examples=len(corpus))

    # Print some info about testword and vocabulary
    try:
        test_info(model, testword)
    except:
        print("The word " + testword + " does not occur in the corpus or it occurs less than min_count.")
        pass

    # Save model
    model.save(save_as)


# TODO Kommentieren
def test_word_sims(load_from):

    wv = Word2Vec.load(load_from)
    print(wv["car"])

    print('\nWORD SIMS OF CAR')
    pairs = [
        ('car', 'minivan'),   # a minivan is a kind of car
        ('car', 'bicycle'),   # still a wheeled vehicle
        ('car', 'airplane'),  # ok, no wheels, but still a vehicle
        ('car', 'cereal'),    # ... and so on
        ('car', 'communism'),
    ]
    for w1, w2 in pairs:
        print('%r\t%r\t%.2f' % (w1, w2, wv.similarity(w1, w2)))



    print('\n5 most similar words to “car” or “minivan”')
    print(wv.most_similar(positive=['car', 'minivan'], topn=5))



    print('\nMISMATCH”')
    print(wv.doesnt_match(['fire', 'water', 'land', 'sea', 'air', 'car']))

#download_save("fertiges_modell")


# TODO KOMMENTIEREN (und verschieben :D)
def get_corpuswords_freqDist(corpus_load_from):
    corpus = Preprocessing.load_corpus("CORP_DefaultUp")
    corpus_ONE_list = [token for sentence in corpus for token in sentence]
    return FreqDist(corpus_ONE_list)


# TODO KOMMENTIEREN (und verschieben :D)
def print_most_medium_least_common(mdl):

    dict = defaultdict(lambda:0)

    for index, voc in enumerate(mdl.wv.index_to_key):
        dict[voc] = mdl.wv.get_vecattr(voc, "count")

    sorted_list = sorted(dict, key=dict.get)

    # Low frequency tokens
    print("500 UNCOMMON WORDS")
    for token in sorted_list[50000:50500]:
        print(token + ": " + str(dict[token]), "Index: " + str(sorted_list.index(token)))


    # Medium frequency tokens
    print("\n\n\n100 MEDIUM COMMON WORDS IN")
    center = int(len(sorted_list)*0.99)
    for token in sorted_list[(center-50):(center+50)]:
        print(token + ": " + str(dict[token]), "Index: " + str(sorted_list.index(token)))


    # High frequency tokens
    print("\n\n\n100 MOST COMMON WORDS IN")
    for token in sorted_list[-100:]:
        print(token + ": " + str(dict[token]), "Index: " + str(sorted_list.index(token)))

    print("Vocabulary size: " + str(len(sorted_list)))
#    print("Abfeuern", dict["Abfeuern"])



# TODO REMOVE

# print_most_medium_least_common(gensim.models.Word2Vec.load("MODEL_SCRATCH_DefaultUp"))
# print_most_medium_least_common(gensim.models.Word2Vec.load("MODEL_SCRATCH_1650Up"))


"""
import gensim.downloader as api
import json
info = api.info()
print(json.dumps(info, indent=4))

for model_name, model_data in sorted(info['models'].items()):
    print(
        '%s (%d records): %s' % (
            model_name,
            model_data.get('num_records', -1),
            model_data['description'][:40] + '...',
        )
    )
"""

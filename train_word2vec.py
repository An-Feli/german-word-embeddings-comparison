# Code taken from https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#
# Code modified.

import gensim
from gensim.models import Word2Vec
from nltk.probability import FreqDist

import gensim.models
from collections import defaultdict
import EpochSaver
import preprocessing
import variables


#############################
#####     NEW MODEL     #####
#############################

def test_info(mdl, testword):
    """ Used for Exploring: Saves to file and prints 10 most similar words to a testword and its vector and prints the vocabulary size of a model

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
    corpus = preprocessing.load_corpus(corpus_load_from)
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



#################################
#####                       #####
#####    EXISTING MODELS    #####
#####                       #####
#################################

def load_train_save(corpus_load_from, model_load_from, epochs=1, save_as="w2v.model", testword=""):
    """ Used for further training: Loads a locally saved pretrained model and trains it further.

    :param corpus_load_from: String - filepath where the plain texts for training are (not xml, not yet preprocessed)
    :param model_load_from: String - path from where to load the model from
    :param epochs: int - Number of iterations the model shall be trained
    :param save_as: String - model will be saved under this name
    :param testword: String - a testword for first examination of the  model
    """

    # Load model and corpus
    model = gensim.models.Word2Vec.load(model_load_from)
    corpus = preprocessing.load_corpus(corpus_load_from)

    # Create Epoch Saver for logging the loss
    logger = EpochSaver.EpochSaver()

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

def get_vocab(mdl):
    """ Used for Exploring: Returns vocabulary of a model both as list and as dictionary.

    :param mdl: Word2Vec-model - The model of which the vocabulary shall be returned.
    :return: List of String - List of all words of the model's vocabulary
        default dict - dictionary of all words of the models vocabulary -> index
    """
    result = defaultdict(lambda: -1)

    for index, word in enumerate(mdl.wv.index_to_key):
        result[word] = index

    return result.keys(), result  # return words only AND dict of words -> index



def test_word_sims(load_from):
    """ Used for Exploring: Prints some word similarities and mismatches of testword "car" of a loaded model

    :param load_from: String - path from where to load the model
    """
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



def get_corpuswords_freqDist(corpus_load_from):
    """ Used for Exploring: Returns a FrequencyDistribution of the vocabulary of a loaded corpus

    :param corpus_load_from: String - path from where to load the model
    :return: FreqDist - The FrequencyDistribution
    """
    corpus = preprocessing.load_corpus(corpus_load_from)
    corpus_ONE_list = [token for sentence in corpus for token in sentence]
    return FreqDist(corpus_ONE_list)


def print_most_medium_least_common(mdl):
    """ Used for Exploring: Prints the 500 most uncommon tokens,
    100 tokens with medium frequency and 100 most common tokens
    from the vocabulary of a given model

    :param mdl: Gensim Model - The model which shall be examined

    """

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
    print("Thier", dict["Thier"])
    print("Tier", dict["Tier"])


def train_all_corpora(corpora):
    """ Trains a model for each of the given corpora and
    returns a list of the names as which they are saved.

    :param corpora: list of String - List of names as which the preprocessed corpora are saved
    :return: lost of String - List of names as which the models are saved
    """

    print("***** TRAINING *****")

    # List of all models (will be filled when training)
    models = []

    for corpus in corpora:

        # Train from scratch on all corpora. Save resulting model.
        save_name = "MODEL_SCRATCH" + corpus[4:]
        create_train_save(corpus_load_from=corpus,
                             vector_size=300,
                             epochs=7,
                             save_as=save_name,
                             testword="Abend")

        models.append(save_name)
    return models


def get_neighbourhood(models):
    """ Writes to files the 10 most similar words
    for each testword from variables.py
    and each given model.
    One file for each model.

    :param models: list of String - list of names as which the models are saved
    """

    # Save 10 most similar words: For each testword in each model
    print("***** 10 MOST SIMILAR WORDS FOR EACH TESTWORD IN EACH MODEL *****")
    for model in models:

        # Load model
        mdl = gensim.models.Word2Vec.load(model)

        # Chose relevant testwordlist
        testwords=variables.testwordsLow
        if model[-2:] == "Up":
            testwords=variables.testwordsUp


        # Fetch most similar words and write to file
        with open("10_MOST_SIM_" + model, 'w') as file:
            for word in testwords:
                file.write("\n***** " + word + " *****\n")
                try:
                    sim_lst = mdl.wv.most_similar(positive = [word], topn = 10)
                except:
                    file.write("Word '" + word + "' not present.\n")
                    continue
                for tuple in sim_lst:
                        file.write(tuple[0] + ": " + str(tuple[1]) + "\n")

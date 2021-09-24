import gensim.models

import Preprocessing
import train_word2vec


# TODO relative Pfade
filepath = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Testkorpus/-1._Das_freundliche_Pfarrhaus.txt"
creat_1750 = "/home/afh/BA/KORPUS - Nur mit Creation Date und ab 1750/Plain Texts from XML"
creat_1650 = "/home/afh/BA/KORPUS - Nur mit Creation Date und ab 1650/Plain Texts from XML"
#folderpath = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Korpus/"
folderpath_testcorpus = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Testkorpus/"


"""
# Preprocess Corpora
print("***** PREPROCESSING CORPORA *****")
corpus = Preprocessing.get_corpus(creat_1750,
                                  lower_case=False,
                                  remove_stopwords=True)
Preprocessing.save_corpus(corpus, "CORP_DefaultUp")

corpus = Preprocessing.get_corpus(creat_1750,
                                  lower_case=True,
                                  remove_stopwords=True)
Preprocessing.save_corpus(corpus, "CORP_DefaultLow")

corpus = Preprocessing.get_corpus(creat_1650,
                                  lower_case=False,
                                  remove_stopwords=True)
Preprocessing.save_corpus(corpus, "CORP_1650Up")

corpus = Preprocessing.get_corpus(creat_1650,
                                  lower_case=True,
                                  remove_stopwords=True)
Preprocessing.save_corpus(corpus, "CORP_1650Low")

corpus = Preprocessing.get_corpus(creat_1750,
                                  lower_case=False,
                                  remove_stopwords=False)
Preprocessing.save_corpus(corpus, "CORP_WithStopUp")

corpus = Preprocessing.get_corpus(creat_1750,
                                  lower_case=True,
                                  remove_stopwords=False)
Preprocessing.save_corpus(corpus, "CORP_WithStopLow")

"""
# List of all training corpora
corpora = ["CORP_DefaultUp",
           "CORP_DefaultLow",
           "CORP_1650Up",
           "CORP_1650Low",
           "CORP_WithStopUp",
           "CORP_WithStopLow"]

# List of all models (will be filled when training)
models = []

#TODO LÖSCHEN, WEIL MANUELL?
## Download pretrained model
#train_word2vec.download_save("german.model")

# Train on all copora
print("***** TRAINING *****")
for corpus in corpora:
    """
    # Train from scratch on all corpora. Save resulting model.
    save_name = "MODEL_SCRATCH" + corpus[4:]
    train_word2vec.create_train_save(corpus_load_from=corpus,
                                     vector_size=300,
                                     epochs=7,
                                     save_as=save_name,
                                     testword="Abend")

    models.append(save_name)
    
    # Train and save with pretrained model on all corpora. Save resulting model.
    save_name = "MODEL_PRETRAINED_" + corpus[4:]
    train_word2vec.load_train_save(corpus_load_from=corpus,
                                   model_load_from="german.model",
                                   epochs=7,
                                   save_as=save_name,
                                   testword="")

    models.append(save_name)
    """



# TODO remove!
models = [
    "MODEL_SCRATCH_DefaultUp",
    "MODEL_SCRATCH_DefaultLow",
    "MODEL_SCRATCH_1650Up",
    "MODEL_SCRATCH_1650Low",
    "MODEL_SCRATCH_WithStopUp",
    "MODEL_SCRATCH_WithStopLow"
]
"""
"""
# Lists of words to be compared
testwordsUp = [
             # Polysem
             "gelassen",
             "Recht", "recht",
             "Geliebte", "geliebte",
             "Decke",

             # Nouns
             "Abend",   # high frequency
             "Zeit",    # high frequency
             "Mutter",    # high frequency
             "Erzählung",   # medium frequency
             "Attraktion",  # low frequency

             # Verbs
             "fragte",  # high frequency
             "wußten", "wussten",    # medium frequency, # low frequency
             "abfeuern",    # low frequency
             
             # Adjectives/adverb/participles
             "schon",  # high frequency
             "oft",     # high frequency
             "gnädige",     # medium frequency
             "abnehmende",   # low frequency

             # Other words
             "zwei",    # high frequency
             "Ach", "ach",   # high frequency (but "only" 9641) ,  # medium frequency

             # Stopwords
             "Und", "und",
             "Aber", "aber",
             "Die", "die",
             "Kein", "kein"
             ]

testwordsLow = [ # Polysem
                "gelassen",
                "recht",
                "geliebte",
                "decke",

                # Nouns
                "abend",   # high frequency
                "zeit",    # high frequency
                "mutter",    # high frequency
                "erzählung",   # medium frequency
                "attraktion",  # low frequency

                # Verbs
                "fragte",  # high frequency
                "wußten", "wussten",    # medium frequency, # low frequency
                "abfeuern",    # low frequency

                # Adjectives/adverb/participles
                "schon",  # high frequency
                "oft",     # high frequency
                "gnädige",     # medium frequency
                "abnehmende",   # low frequency

                # Other words
                "zwei",    # high frequency
                "ach",   # medium frequency

                # Stopwords
                "und",
                "aber",
                "die",
                "kein",
             ]


# Print and save 10 most similar words: For each testword in each model
print("***** 10 MOST SIMILAR FOR EACH TESTWORD IN EACH MODEL *****")
for model in models:

    # Load model
    mdl = gensim.models.Word2Vec.load(model)

    # Chose relevant testwordlist
    testwords=testwordsLow
    if model[-2:] == "Up":
        testwords=testwordsUp
    """
      # TODO REMOVE
    # Fetch most similar words and write to file for LaTex
    with open("LATEX_10_MOST_SIM_" + model, 'w') as file:
        for word in testwords:
            file.write("\n***** " + word + " *****\n")
            file.write("\n\\textbf{" + model[14:] + ": " + word + "} \\\\ \n")
            try:
                sim_lst = mdl.wv.most_similar(positive = [word], topn = 10)
            except:
                file.write("Word '" + word + "' not present.\n")
                continue
            for tuple in sim_lst:
                    file.write(tuple[0] + ": " + f"{tuple[1]:.4f}" + "\\\\ \n")

    """
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



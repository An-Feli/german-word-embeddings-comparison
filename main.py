import gensim.models
import preprocessing
import train_word2vec
import variables


# Preprocess corpus from 1750 as well as from 1650
#preprocessing.preprocess_corpora()

# Train on all corpora
models = train_word2vec.train_all_corpora(corpora = variables.corpora)

# Write to file 10 most similar words for each testword in each model
#train_word2vec.get_neighbourhood(models)

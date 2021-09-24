# taken from: https://radimrehurek.com/gensim/models/callbacks.html
# and https://stackoverflow.com/questions/54422810/tracking-loss-and-embeddings-in-gensim-word2vec-model
from gensim.test.utils import get_tmpfile

from gensim.models.callbacks import CallbackAny2Vec

class EpochSaver(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_end(self, model):
        print("Model loss:", model.get_latest_training_loss())  # print loss
        print("Epoch #{} end".format(self.epoch))
        print("\n")
        self.epoch += 1

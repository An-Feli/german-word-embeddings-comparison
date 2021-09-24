# Taken from https://datascience.stackexchange.com/a/81926

import gensim
from gensim.models.callbacks import CallbackAny2Vec

# Your model params:
CONTEXT_WINDOW = 5
NEGATIVES = 5
MIN_COUNT = 5
EPOCHS = 20

class LossLogger(CallbackAny2Vec):
    '''Output loss at each epoch'''
    def __init__(self):
        self.epoch = 1
        self.losses = []

    def on_epoch_begin(self, model):
        print(f'Epoch: {self.epoch}', end='\t')

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        self.losses.append(loss)
        print(f'  Loss: {loss}')
        self.epoch += 1

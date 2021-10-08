# Training And Comparing Word Embeddings with Word2Vec

This repository contains the code for the experimental part of the bachelor thesis "Word Embeddings - Interface Between Computer Science and Linguistics" by Anna-Felicitas Hausmann.

## Usage

Install requirements:

```sh
pip install -r requirements.txt
```

Run main.py
```sh
python main.py
```
Six preprocessed **training corpora** will be derived from the two plain text corpora and will be saved: 
- `CORP_DefaultUp/CORP_DefaultLow`
- `CORP_1650Up/CORP_1650Low`
- `CORP_WithStopUp/CORP_WithStopLow`

Six respective **models** will be trained and saved:
- `MODEL_SCRATCH_DefaultUp/MODEL_SCRATCH_DefaultLow`
- ... 

Six files will be created, one for each model, containing the **10 most similar words** for every testword. They might be different that the ones found in the bachelor thesis (see appendix) due to random in the algorithm (for details, see thesis).
- `10_MOST_SIM_MODEL_SCRATCH_DefaultUp/10_MOST_SIM_MODEL_SCRATCH_DefaultLow`
- ...

### Configuration
#### Testwords
See the two testword lists in `variables.py` in order to change the testword lists. 

#### Training Corpora
Change paths saved in `reprocessing.py`: The variables `creat_1750 = "./1750"` and `creat_1650 = "./1650"` (lines 117 and 118). The directory needs to contain plain text (no xml etc.).

## Exploring
Not all methods are triggered by main.py directly or indirectly. They can be used manually to explore the corpus or the models. They are commented by "Used for..." in the docstring.

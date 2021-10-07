# List of training corpus variants
corpora = ["CORP_DefaultUp",
           "CORP_DefaultLow",
           "CORP_1650Up",
           "CORP_1650Low",
           "CORP_WithStopUp",
           "CORP_WithStopLow"]


# Lists of testwords
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
             "Thier", "Tier",    # medium frequency, # medium frequency
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
                "thier", "tier",    # medium frequency, # medium frequency
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

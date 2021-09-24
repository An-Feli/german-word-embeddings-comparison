# Fetch most similar words and write to file

stopw = []
with open("german.stopwords", 'r') as file:
    for line in file:
        stopw.append(line)

with open("german.stopwords", 'w') as file:
    for w in stopw:
        line = (" \\\\" + w)
        print(line)
        file.write(line)

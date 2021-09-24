# Used to parse xml. Codesnippet from T. Arnold, modified.
import os
import xml.etree.ElementTree as ET
import shutil

# TODO räume Pfade auf
#gibt's nicht mehr path_xmltest = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/XML Testkorpus/"
import nltk.corpus

path_xml = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/XML-Korpus/"
#gibt's nicht mehr path_plaintest = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Testkorpus/"
path_plain = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Plain Korpus/"
path_korpora = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora"

#################################################
############# Get Title, Date, Author ###########
#################################################

def get_title(root):

    for body in root.iter('{http://www.tei-c.org/ns/1.0}title'):
        for maintext in body.iter():
            if maintext.text:
                #print(maintext.text)
                return maintext.text


def get_date_creation(root):
    """ Returns the date of a file, according to its creation.

    :param root: Root of the ElementTree which represents the file
    # TODO String oder int?
    :return: String - Creation date of the file
    """

    date = None

    for profileDescription in root.iter('{http://www.tei-c.org/ns/1.0}profileDesc'):
        for d in profileDescription.iter('{http://www.tei-c.org/ns/1.0}date'):

            # 1. Look for the date (exact year) in "creation" (that is: in profileDescription)
            date = d.get('when')

            # 2. In case date is a span: return lower bound
            if date is None:
                date = d.get('notBefore')

        #    # 3. If date is not in "creation": look for PublicationDate
        #    if date is None:
        #        date = get_date_publication(root)
    return date

def get_date_publication(root):
    """ Returns the date of a file, according to its publictaion.

    :param root: Root of the ElementTree which represents the file
    # TODO String oder int?
    :return: String - Publication date of the file
    """
    date = None

    for fileDescription in root.iter('{http://www.tei-c.org/ns/1.0}fileDesc'):
        for publicationStmt in fileDescription.iter('{http://www.tei-c.org/ns/1.0}date'):

            # 1. Look for the date (exact year) in "publicationStmt"
            date = publicationStmt.get('when')

            # 2. In case date is a span: return lower bound
            if date is None:
                date = publicationStmt.get('notBefore')

        #   # 3. If date is not an xml-attribute but as text:
            if date is None:
                for dat in publicationStmt.iter():
                    date = dat.text
    return date

def test_get_date(folderpath, test_date_creation):
    """ Returns a list of files for which date is None.

    :param folderpath: String - Path to the folder the corpus is in
    :param test_date_creation: boolean - True: creation date will be fetched; False: publication date will be fetched
    :return: List of String - List of filenames for which date is None
    """

    files = os.listdir(folderpath)
    counter = 0
    result = []

    for file in files:
        #print(file)
        if ".meta" not in file and "index" not in file:
            tree = ET.parse(os.path.join(folderpath, file))
            root = tree.getroot()

            # Now, test the correct function
            if test_date_creation:
                date = get_date_creation(root)
            else:
                date = get_date_publication(root)

            if date is None:
                result.append(file)
    return result



def get_author(root):
    for body in root.iter('{http://www.tei-c.org/ns/1.0}author'):
        #print(body.text)
        return body.text


#######################################################################
####### Remove Texts from Corpus Which are Older than Required ########
#######################################################################

#
# TODO: NIMMT GERADE NUR CREATION DATE
def get_old_texts(folderpath, year):
    """ Creates a file with all the filenames
    AND their respective .meta-file
    which are older that given year or None

    :param folderpath: String - Path to corpus files
    :param year: int - files (and .meta-files) which are older than this year will be listed
    """

    files = os.listdir(folderpath)
    file_to_write_to = "Texts older than " + str(year) + ".txt"     # file to write to
    counter = 0

    # Fpr each File ...
    for filename in files:
        # .meta-dateien werden hier übersprungen, weil sie kein Datum enthalten (werden später berücksichtigt)
        if not "meta" in filename:
            tree = ET.parse(os.path.join(folderpath, filename))
            root = tree.getroot()

            # ... get the date.
            date = get_date_creation(root)
            #if date is None:
            #date = get_date_publication(root)

            # If date is None: write filename to resulting File, too
            # Check if date is older than given year. Iff yes: write filename (and its filename.meta) in resulting File.
            if date is None:
                date = "0"
            if int(date) < int(year):
                # TODO Remove
                counter += 1

                line =  filename + ", " + date + "\n"   # what to write to the file
                write_to_file(path_korpora, file_to_write_to, line)     # and now, write
                line =  filename + ".meta " + "\n"   # what to write to the file
                write_to_file(path_korpora, file_to_write_to, line)     # and now, write

                # TODO Remove
                print(str(counter) + ", " + str(date) + ", " + filename)

def write_to_file(folderpath, filename, line):
    file = open (os.path.join(folderpath, filename), "a")
    file.write(line)
    file.close()



# Moves all files from old_folderpath to new_folderpath which name is in given file_old_texts
def move_old_texts(scr_folderpath, dest_folderpath, file_old_texts):
    """ Moves all files from old_folderpath to new_folderpath for which this is true:
    Filename is in given file_old_texts

    :param scr_folderpath: String - Path to move the files FROM
    :param dest_folderpath: String - Path to move the files TO
    :param file_old_texts: String - Path to file with filenames older than required
    """

    files = os.listdir(scr_folderpath)
    counter = 0
    try:
        os.mkdir(dest_folderpath)
    except:
        pass

    # Run through folder file by file...
    for file in files:
        with open(file_old_texts,'r') as old_texts:
            # ...and check every line in old_texts...
            for line in old_texts:
                #... iff filename is in old_texts: move the respective File.
                if file in line:
                    counter += 1
                    # TODO Remove
                    #print(str(counter) + file)
                    src=scr_folderpath + file
                    des=dest_folderpath + file
                    try:
                        os.rename(src, des)
                    except:
                        pass

############################################
##### Create Register of Corpus Texts ######
############################################

# Gets a folderpath
# Writes a register to the same folder (name: "Verzeichnis.txt") of all the files in that folder
def create_register(folderpath, registerpath):
    """ Creates Register of all files in a given folder

    :param folderpath: String - Path to folder with files for the Register
    :param registerpath: String - Path where the Register shall be saved
    """

    files = os.listdir(folderpath)

    # Für jedes File (außer den "...xml.meta"-files):  ...
    for filename in files:
        if not "meta" in filename:
            tree = ET.parse(os.path.join(folderpath, filename))
            root = tree.getroot()

            verz = open(os.path.join(registerpath, "Verzeichnis.txt"),'a')
            verz.write(get_author(filename, root) + ", " + get_title(filename, root) + ", " + get_date(filename, root) + "\n")
            verz.close()


#################################################
### Create Plaintext from Now Filtered Corpus ###
#################################################


def get_corpus_plain(folderpath_scr, folderpath_dest):
    """ Takes the path of the folder where the corpus (xml) is
    and creates a new folder, writing all texts from xml-files to it
    as plain text. Skips .meta-files

    :param folderpath_scr: String - Path to folder from where to take textfiles
    :param folderpath_dest: String - Path to folder where to move textfiles TO
    :return:
    """

    files = os.listdir(folderpath_scr)
    # Create destination folder
    try:
        os.mkdir(folderpath_dest)
    except:
        pass

    # Run through each File (skip .meta-files)...
    for filename in files:
        if ".meta" in filename:
            continue
        tree = ET.parse(os.path.join(folderpath_scr, filename))
        root = tree.getroot()

        # ... extract text from file...
        text = get_plain_text(root)

        # ... and write it to the file in destination folder
        with open(os.path.join( folderpath_dest, filename[:-3] + "txt"),'a') as textfile:
            textfile.write(text)



def get_plain_text(root):
    """ Helper fuction for get_corpus_plain():
    Given an ElementTreeRoot representing an xml-file,
    returns maintext of Element "text"

    :param root: Root - ElementTreeRoot representing an xml-file
    :return: String - Text from xml-file
    """

    textnode = root.find("{http://www.tei-c.org/ns/1.0}text")
    result = ""

    for elm in textnode.iter():
        # Check if eml.text is falsy (that means, there is no text in this Element).
        # If so, do not write it file.
        if elm.text is not None:
            if not elm.text.strip():
                result += "\n"
            else:
                result += elm.text + "\n"
    return result


#print(test_get_date(path_xml, False))
#get_old_texts(path_xml, 1650)
#move_old_texts(path_xml, os.path.join(path_korpora, "Removed from Corpus/"), path_korpora + "/Texts older than 1650.txt")
#get_corpus_plain(path_xml, os.path.join(path_korpora, "AAAPlain Texts from XML"))
#create_register(path_xmltest, path_korpora)

with open ("Stopwords", "w") as file:
    for line in nltk.corpus.stopwords:
        file.write(line)

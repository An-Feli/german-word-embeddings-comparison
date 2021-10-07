# Used to parse xml. Codesnippet from T. Arnold, modified.
import os
import xml.etree.ElementTree as ET


whole_xmlcorpus = "/home/afh/BA/Korpora/XML-Korpus"
path_korpora = "/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/"
path_removed_texts = '/home/afh/DIE Ordner/Uni TUD/6tes Semester/Bachelorarbeit/Korpora/Removed from whole Corpus for 1750/'
creat_1750 = "/home/afh/BA/KORPUS - Nur mit Creation Date und ab 1750/Plain Texts from XML/"
creat_1650 = "/home/afh/BA/KORPUS - Nur mit Creation Date und ab 1650/Plain Texts from XML/"

#################################################
############# Get Title, Date, Author ###########
#################################################

def get_title(root):

    for body in root.iter('{http://www.tei-c.org/ns/1.0}title'):
        for maintext in body.iter():
            if maintext.text:
                return maintext.text


def get_date_creation(root):
    """ Returns the date of a file, according to its creation.

    :param root: Root of the ElementTree which represents the file
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

    return date

def get_date_publication(root):
    """ Returns the date of a file, according to its publictaion.

    :param root: Root of the ElementTree which represents the file
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

            # 3. If date is not an xml-attribute but given as text:
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
    result = []

    for file in files:
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
        return body.text


#######################################################################
####### Remove Texts from Corpus Which are Older than Required ########
#######################################################################


def get_old_texts(folderpath, year):
    """ Creates a file with all the filenames
    AND their respective .meta-file
    which are None or older that given year
    according to their creation date.

    :param folderpath: String - Path to corpus files
    :param year: int - files (and .meta-files) which are older than this year will be listed
    """

    files = os.listdir(folderpath)
    file_to_write_to = "Texts older than " + str(year) + ".txt"     # file to write to
    counter = 0

    # For each File ...
    for filename in files:
        # .meta-files will be skipped here because they do not contain a date
        if not "meta" in filename:
            tree = ET.parse(os.path.join(folderpath, filename))
            root = tree.getroot()

            # ... get the creation date.
            date = get_date_creation(root)

            # If date is None: write filename to resulting File, too
            # Check if date is older than given year. Iff yes: write filename (and its filename.meta) in resulting File.
            if date is None:
                date = "0"
            if int(date) < int(year):
                line =  filename + ", " + date + "\n"   # what to write to the file
                write_to_file(path_korpora, file_to_write_to, line)     # and now, write
                line =  filename + ".meta " + "\n"   # what to write to the file
                write_to_file(path_korpora, file_to_write_to, line)     # and now, write


def write_to_file(folderpath, filename, line):
    """ Writes given line to file.

    :param folderpath: String - path to folder where file is
    :param filename: String - name of the file to be written to
    :param line: String - The line which shall be written
    """
    file = open (os.path.join(folderpath, filename), "a")
    file.write(line)
    file.close()



def move_old_texts(scr_folderpath, dest_folderpath, file_old_texts):
    """ Moves all files from scr_folderpath to dest_folderpath for which this is true:
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
    """ Creates Register of all files in a given folder.

    :param folderpath: String - Path to folder with files for the Register
    :param registerpath: String - Path where the Register shall be saved
    """

    files = os.listdir(folderpath)

    # For each file (except of the "...xml.meta"-files):...
    for filename in files:
        if not "meta" in filename:

            tree = ET.parse(os.path.join(folderpath, filename))
            root = tree.getroot()

            # ...write relevant information to "Verzeichnis.txt"
            verz = open(os.path.join(registerpath, "Verzeichnis.txt"),'a')
            verz.write(get_author(root) + ": " + get_title(root) + ", created " + get_date_creation(root) + "\\\\ \n")
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
    """

    files = os.listdir(folderpath_scr)
    # Create destination folder
    try:
        os.mkdir(folderpath_dest)
    except:
        pass

    # Run through each file (skip .meta-files)...
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
#get_old_texts(path_removed_texts, 1650)
#move_old_texts(path_removed_texts, os.path.join(path_korpora, "Removed texts older than 1750"), path_korpora + "Texts older than 1650.txt")
#get_corpus_plain(path_xml, os.path.join(path_korpora, "AAAPlain Texts from XML"))
#create_register(path_removed_texts, path_korpora)


# Steps used to find out about error in corpora
# (in 1650 corpus, some texts from after 1750 are missing. See Theses appendix for details).

# Create lst with all titles from 1650 corpus
lst1650 = []
files = os.listdir(creat_1650)
for filename in files:
    lst1650.append(filename)

# Create lst with all titles from 1750 corpus
lst1750 = []
files = os.listdir(creat_1750)
for filename in files:
    lst1750.append(filename)

in17butnot16=[]
for item in lst1750:
    if item not in lst1650:
        in17butnot16.append(item)

in16butnot17=[]
for item in lst1650:
    if item not in lst1750:
        in16butnot17.append(item)

with open(os.path.join(path_korpora, "in16butnot17.txt"),'a') as verz:
    xml_files = os.listdir(whole_xmlcorpus)
    for text in in16butnot17:
        for file in xml_files:
           if text[:-4] in file and ".meta" not in file:

               tree = ET.parse(os.path.join(whole_xmlcorpus, file))
               root = tree.getroot()

               verz.write(get_author(root) + ": " + get_title(root) + ", created " + get_date_creation(root) + "\\\\ \n")


with open(os.path.join(path_korpora, "in17butnot16.txt"),'a') as verz:
    xml_files = os.listdir(whole_xmlcorpus)
    for text in in17butnot16:
        for file in xml_files:
           if text[:-4] in file and ".meta" not in file:

               tree = ET.parse(os.path.join(whole_xmlcorpus, file))
               root = tree.getroot()

               verz.write(get_author(root) + ": " + get_title(root) + ", created " + get_date_creation(root) + "\\\\ \n")

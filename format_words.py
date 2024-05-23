
FILE_PATH_ENGLISH = "english-common-words.txt"
FILE_PATH_HEBREW = ""


def reformat_words(file_path: str):
    words = []
    with open(FILE_PATH_ENGLISH, "r") as file:
        for line in file:
            if line.rstrip().isalpha() and len(line) > 2:
                words.append(line.lower())
    words.sort(key=len)
    with open(FILE_PATH_ENGLISH, "w") as file:
        for line in words:
            file.write(line)


reformat_words(FILE_PATH_ENGLISH)
reformat_words(FILE_PATH_HEBREW)
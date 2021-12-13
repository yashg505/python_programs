from string import punctuation  


def find_repeats(fname):
    """
    the function will find if any word is repeated (inadvertently duplicating
    a word). It will print the line number and the repeated word.
    if the word is repeated n number of time, then we will have n-1 number
    of results in the output.

    Assumptions:
    1. space should be after punctuations. ". This is correct,This is not"
       in the above example, "correct,This", cannot be processed correctly,
       while ". This" will be processed corectly.
    2. file needs to be a text file.

    Results will be like:
    #1 : Line - 0, repeated word - entered
    """
    text_file = open(fname, "r")
    rep_words = []  # save repeated words and their position in this list
    l_word = text_file.read().split()  # saving each word in a list
    text_file.close()

    for i in range(len(l_word)-1):
        s_no_punc = l_word[i+1]
        for punc in punctuation:
            s_no_punc = s_no_punc.replace(punc, "")  # remove punctuations
        if l_word[i].lower() == s_no_punc.lower():
            rep_words.append((i+1, l_word[i]))

    for i, element in enumerate(rep_words):
        num = line_num(element[0], fname)
        print("Line: {}, repeated word: {}".format(num, element[1]))


def line_num(char_n, fname):
    """
    The function will return the line number of the word index which is
    provided as input to the function.

    """
    text_file = open(fname, "r")
    lines = text_file.readlines()
    text_file.close()
    num_char = 0
    for k in range(len(lines)):
        num_char += len(lines[k].split())
        if num_char >= char_n:
            return k


FNAME = "file1.txt"
find_repeats(FNAME)

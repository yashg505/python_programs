from string import punctuation


def pig_latin(s):
    """
    The function will take the string and modify it as per below rule:
    words starting with
    vowels : add "way" at the end.
    consonant : all letters before the first vowel placed at end of the
    word and then “ay” added at the end

    Asumptions:
    #1 each word is seperated with space.
    #2 Special characters(if any) are expected to be at
       the end of the word.
    #3 Atleast some text is entered.

    pig_latin("banana") --> "ananabay"
    pig_latin("glove") --> "oveglay"
    pig_latin("eat") --> "eatay"
    pig_latin("Jingle all the way!!")-->"Inglejay allway ethay ayway!!"

    """
    vowels = ("a", "e", "i", "o", "u")
    v_sffx = "way"
    c_sffx = "ay"
    n_word = []
    n_word_capital = []

    if "\n" in s:
        line_s = s.split("\n")
        new_text = []
        for i in line_s:
            new_text.append(pig_latin(i))
        return "\n".join(new_text)

    list_s = s.split(" ")

    for i in list_s:
        if i[0].lower() in vowels:
            s_char = special_char_index(i)
            n_word.append(i[:s_char].lower() + v_sffx + i[s_char:])
        else:
            v_i = vowel_index(i)
            s_char = special_char_index(i)
            if v_i > s_char:
                v_i = 0
            n_word.append(i[v_i:s_char].lower() + i[:v_i].lower()
                          + c_sffx + i[s_char:])

    for i in list_s:
        if i[0].isupper():
            n_word_capital.append(n_word[list_s.index(i)].title())
        else:
            n_word_capital.append(n_word[list_s.index(i)])

    return " ".join(n_word_capital)


def vowel_index(s):
    """
    find the index of the first vowel
    if no vowel, return the length of the string
    vowel_index("yash") --> 1
    vowel_index("why") --> 3
    """
    vowel = ("a", "e", "i", "o", "u")
    for i in s:
        if i in vowel:
            return s.index(i)
    return len(s)


def special_char_index(s):
    """
    find the index of the first special_char
    if no special char, return the length of the string
    special_char_index("yash!") --> 4
    special_char_index("why") --> 3
    """
    for i in s:
        if i in punctuation:
            return s.index(i)
    return len(s)


# user_input = []
# print("Enter the text and press enter two times to input the data\n")
# while True:
#    line = input()
#    if line:
#        user_input.append(line)
#    else:
#        break
# text = '\n'.join(user_input)

text = ("""Jingle bells, jingle bells!
Jingle all the way!!
Oh, what fun it is to ride
In a one horse open sleigh""")


print(pig_latin(text))

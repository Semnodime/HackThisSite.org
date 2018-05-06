"""
Level 1
This level is about unscrambling words.

Find the original (unscrambled) words, which were randomly taken from a wordlist.<--
Send a comma separated list of the original words, in the same order as in the list below.

You have 30 seconds time to send the solution.
List of scrambled words:    	
shorictp
arprosw
6247315
mntnaao
olshnoa
ohtanpm
aaa1dnm
ielenl
natasah
nk1ive

Answer:            (Example:   word1,word2,word3, ... word9,word10)
"""
import fileinput


def read_example():
    example = [
        "shorictp\n",
        "	\n",
        "arprosw\n",
        "	\n",
        "6247315\n",
        "	\n",
        "mntnaao\n",
        "	\n",
        "olshnoa\n",
        "	\n",
        "ohtanpm\n",
        "	\n",
        "aaa1dnm\n",
        "	\n",
        "ielenl\n",
        "	\n",
        "natasah\n",
        "	\n",
        "nk1ive",
    ]


def read_scrambled_input():
    print("Copy paste or pipe the scrambled words into std_in:")
    print('If you copy paste make sure to end the input by EOF (Str+D)')
    for line in fileinput.input():
        line = str(line).strip()
        if line != '':
            yield line


def scrabled_matches_word(scrambled, word):
    """ Check if 'someword' matches 'mrsdoewo' """
    if len(word) != len(scrambled):
        return False

    for letter in scrambled:
        if scrambled.count(letter) != word.count(letter):
            return False

    return True


def unscramble(scrambled, wordlist):
    """ Returns the first word in wordlist that matches the scrambled word"""
    for word in wordlist:
        word = str(word).strip()
        if scrabled_matches_word(scrambled, word):
            return word

    return None


if __name__ == '__main__':
    print('This unscrambler converts words into other words based on ./wordlist.txt')
    with open('./wordlist.txt') as f:
        wordlist = f.readlines()

    result = []
    for scrambled in read_scrambled_input():
        unscrambled = unscramble(scrambled, wordlist)
        if unscrambled:
            result.append(unscrambled)
        else:
            print('Could not unscramble %r' % scrambled)

    answer = ','.join(result)
    print('The answer is the following %d words:\n' % len(result) + answer)

from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter

def make_wordcloud(cmt):

    nlp = Twitter()
    nouns = nlp.nouns(cmt)
    count = Counter(nouns)

    word_cloud = WordCloud(font_path='./HoonWhitecatR.ttf', max_words=20, font_step=5, mode='RGBA',
                          background_color=None).generate_from_frequencies(count)
    # check your font installation
    return word_cloud #need to make save img and return location


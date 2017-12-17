from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter
from .models import Newsanalyzer, Newscomment # later don't commnicate with model on here. move to view

def make_wordcloud(id):
    cmtlist = Newscomment.objects.filter(news_id = id) # later, move to View.
    buff = ""
    for cmt in cmtlist:
        buff += cmt.cmt_text+"\n"

    print(buff)
    print("before nlp")
    nlp = Twitter()
    print("nlp = Twitter()")
    nouns = nlp.nouns(buff)
    print("nouns = nlp.nouns(buff)")
    count = Counter(nouns)
    print("count = Counter(nouns)")

    word_cloud = WordCloud(font_path='./HoonWhitecatR.ttf', max_words=20, font_step=5, mode='RGBA',
                          background_color=None).generate_from_frequencies(count)
    print(word_cloud.words_)
    del(nlp, nouns, count) # to solve memory error, 'nlp' make error when it work more then one time
    return word_cloud #need to make save img and return location


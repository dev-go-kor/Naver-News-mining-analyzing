from naver_crawler import get_ranking_news, get_comment
from cmt_analyzer import make_wordcloud


if __name__ == '__main__':

    news_list = get_ranking_news()
    print(news_list)

    # sample news url is used
    cmt_list = get_comment('http://m.news.naver.com/rankingRead.nhn?oid=421&aid=0003103428&sid1=105&date=20171217&ntype=RANKING')
    print(cmt_list)


    cmt_all = ""
    for row in range(len(cmt_list)):
        cmt_all += cmt_list.iloc[row].text + "\n"
    print(cmt_all)

    wordcloud_img = make_wordcloud(cmt_all).to_image()
    wordcloud_img.show()
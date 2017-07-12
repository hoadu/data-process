# -*-encoding: utf-8 -*-

import pandas as pd
import datetime


def load_data(fpath):
    data = pd.read_excel(fpath)
    return data


if __name__ == '__main__':
    from textrank_zhihu_answer import text_summarization

    # data = load_data("嘉丰瑞德-理财知识.xlsx")
    gonglue_data = load_data("嘉丰瑞德-理财攻略.xlsx")

    replace_words = [i.strip() for i in u'''
    国内知名财富管理机构嘉丰瑞德的资深理财师
    国内知名财富管理机构嘉丰瑞德
    财富管理机构嘉丰瑞德
    嘉丰瑞德的资深理财师
    嘉丰瑞德的理财师
    嘉丰瑞德
    理财师'''.split("\n") if i.strip()]

    print replace_words


    def _replace(text, target):
        for w in replace_words:
            text = text.replace(w, target)
        return text


    # data[u'正文'] = data[u'正文'].map(lambda x: _replace(x, u"叮当"))

    gonglue_data[u'正文'] = gonglue_data[u'正文'].map(lambda x: _replace(x, u"叮当"))
    print datetime.datetime.now()

    # test_data = data.head(5)

    # new_columns_data = data[u'正文'].apply(
    #     lambda x: (pd.Series(dict(zip(["Answer_1", "Answer_2", "Answer_3"], list(text_summarization(x, 3)))))))
    new_columns_data = gonglue_data[u'正文'].apply(
        lambda x: (pd.Series(dict(zip(["Answer_1", "Answer_2", "Answer_3"], list(text_summarization(x, 3)))))))

    print new_columns_data.head(1)
    new_data = gonglue_data.merge(new_columns_data, left_index=True, right_index=True)
    writer = pd.ExcelWriter('fortune_knowledge_strategey.xlsx')


    new_data.to_excel(writer, columns=[u'名称', u'时间', u'页面网址', u'页面标题', u'Answer_1', u'Answer_2'])
    print datetime.datetime.now()
    # for s in summarizations:
    #     print list(s)

    # keys = list(data.columns)

    # dict_list = []
    # for row in data.iterrows():
    #     dict_list.append(dict(zip(keys, row[1:])))
    #
    # print dict_list

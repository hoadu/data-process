# -*-encoding: utf-8 -*-

import pandas as pd

from fortune_management import load_data

data = load_data("格上理财-词典.xlsx")


def remove_title_from_text(d):
    '''

    :param d:
    :return:  remove title in text
    '''
    return d[u'正文'][len(d[u'标题']):]


def remove_company_from_title(d):
    return d[u'页面标题'][:-len(u'_理财辞典_理财学堂_格上财富')]


data[u'正文_2'] = data.apply(remove_title_from_text, axis=1)
data[u'标题_2'] = data.apply(remove_company_from_title, axis=1)

writer = pd.ExcelWriter('invest_dict.xlsx')

data.to_excel(writer, columns=[u'标题_2', u'正文_2'])
writer.save()
writer.close()

# -*-encoding :utf-8 -*-
from __future__ import print_function

import sys
import os
import datetime

from multiprocessing import Pool

# pip install textrank4zh
# cn: pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com textrank4zh


import MySQLdb

connection = MySQLdb.connect(host="localhost", user="root", db="ddfinance")
cursor = connection.cursor()

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Sentence

tr4s = TextRank4Sentence()


def text_summarization(text, summary_count=3):
    tr4s.analyze(text=text, lower=True)
    for item in tr4s.get_key_sentences(num=summary_count):
        yield item.sentence


def load_answers_from_db(fields=None, table=None):
    cursor.execute("""select {} from {}""".format(",".join(fields), table))
    for row in cursor.fetchall():
        yield dict(zip(fields, row))


if __name__ == '__main__':
    start = datetime.datetime.now()

    print(datetime.datetime.now())
    answers = load_answers_from_db(fields=['id', 'question', 'question_link', 'up_count', 'answer'],
                                   table='zhihu_answers')

    answers = list(answers)
    answers = filter(lambda x: int(x['up_count']) > 100 if len(x['up_count']) > 0  else False, answers)
    print(len(answers))

    print("Summarization started!")


    def map_summarization(a):

        summarizations = list(text_summarization(a['answer'], summary_count=3))
        if len(summarizations) == 3:

            a['answer_1'] = summarizations[0]
            a['answer_2'] = summarizations[1]
            a['answer_3'] = summarizations[2]
        else:
            a['answer_1'] = summarizations[0]
            a['answer_2'] = ''
            a['answer_3'] = ''

        print("{} {} ok".format(os.getpid(), a['id']))
        return a


    # import cProfile
    #
    # cProfile.run("map_summarization(answers[1])", filename="text_rank.out")

    total_answers = Pool(15).map(map_summarization, answers)
    # total_answers = map(map_summarization, answers[:100])

    print(len(total_answers))
    print("Summarization finished!")
    total_answers = filter(lambda x: len(x['answer_1']) < 140, total_answers)

    from save_dict_to_excel import ExcelDriver
    from list_helper import slice_list

    for i, ans in enumerate(slice_list(total_answers, 2000)):
        with ExcelDriver("zhihu_answers_{}.xlsx".format(i)) as f:
            f.switch_sheet("zhihu_answers",
                           ["question", "question_link", "up_count", "answer_1", "answer_2", "answer_3"])
            for a in ans:
                f.write(a)
    print("Excel saved!")

    print(datetime.datetime.now())
    print(datetime.datetime.now() - start)

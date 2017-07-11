# -*-encoding:utf-8 -*-
'''
pip install flanker
'''
import poplib
import re
from flanker import mime
from functools import wraps
import traceback

from datetime import datetime, timedelta


def catch_exceptions(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result

        except Exception as e:
            print "!!!COPY ERROR INFO BELOW THEN CONTACT ME!!!"

            print "====" * 20
            print traceback.format_exc()
            print f, args, kwargs
            print str(e)
            print "====" * 20

    return inner


class Inbox(object):
    def __init__(self, email, password, pop3_server, pop3_port, debug=False):
        self.email = email
        self.password = password
        self.server = poplib.POP3_SSL(pop3_server, port=pop3_port)

        if debug:
            self.server.set_debuglevel("DEBUG")

        self.server.user(self.email)
        self.server.pass_(self.password)
        self.latest_index, _ = self.server.stat()

    @catch_exceptions
    def fetch_latest_emails(self, n=100):
        emails = []
        for i in range(self.latest_index - n, self.latest_index + 1):
            _, lines, octets = self.server.retr(i)
            msg_content = '\r\n'.join(lines)
            msg = mime.from_string(msg_content)
            emails.append(msg)

        return emails

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()


find_ABCD = lambda x: re.search('[ABCD]', x).group()


def most_common(lst):
    if len(lst) < 1:
        return ''
    return max(set(lst), key=lst.count)


@catch_exceptions
def extract_dinner_option(email_content):
    email_parts = email_content.parts
    option_list = []
    for p in email_parts:
        option_list.extend(re.findall(" ?[ABCD][^a-zA-Z]", p.body))
    option_list = map(find_ABCD, option_list)

    return most_common(option_list)


@catch_exceptions
def extract_from_email(email_content):
    headers = email_content.headers.items()
    for h in headers:
        if h[0] == 'From':
            from_email = h[1]
            return from_email


@catch_exceptions
def extract_email_date(email_content):
    'Mon, 3 Jul 2017 18:25:49 +0800'
    headers = email_content.headers.items()
    for h in headers:
        if h[0] == 'Date':
            date = h[1]
            weekday, date = date.split(',')
            date = re.search("\d+ \w+ \d{4}", date).group()
            return datetime.strptime(date, "%d  %b %Y")


@catch_exceptions
def test_exception(*args, **kwargs):
    raise ValueError("****")


if __name__ == '__main__':
    email = "wenter.wu@daocloud.io"
    password = ""

    pop3_server = "partner.outlook.cn"
    pop3_port = '995'

    my_inbox = Inbox(email, password, pop3_server, pop3_port)

    with my_inbox as inbox:
        my_emails = inbox.fetch_latest_emails(200)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    today_emails = [e for e in my_emails if extract_email_date(e) >= today - timedelta(hours=1)]
    print "今日邮件数:{}".format(len(today_emails))

    dinner_emails = [e for e in today_emails if u"加班餐" in e.subject]

    print "加班餐邮件数:{}".format(len(dinner_emails))

    for e in dinner_emails:
        print extract_from_email(e), extract_dinner_option(e)

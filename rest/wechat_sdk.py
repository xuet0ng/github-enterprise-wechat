# -*- coding:utf-8 -*-
import datetime
import requests


def token(func):
    def get_newest_token(self, *args, **kwargs):
        if "access_token" not in self.token or self.token['expires_time'] < datetime.datetime.now():
            self.get_token()
        return func(self, *args, **kwargs)
    return get_newest_token


class WeChat(object):

    def __init__(self, url, corp_id, corp_secret):
        self.url = url
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.token = {}

    def get_token(self):
        params = {
            'corpid': self.corp_id,
            'corpsecret': self.corp_secret
        }
        r = requests.get(url=self.url + '/gettoken', params=params)
        t = r.json()
        t['expires_time'] = \
            datetime.datetime.now() + datetime.timedelta(seconds=int(t['expires_in']))
        self.token = t

    @token
    def send_message(self, msg):
        params = {
            'access_token': self.token['access_token']
        }
        data = {
            "touser": "jiangxuetong@tsfinancial.cn",
            "toparty": "",
            "totag": "",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {
                "content": msg
            },
            "safe": 0
        }
        r = requests.post(url=self.url+'/message/send', params=params, json=data)
        return r.json()




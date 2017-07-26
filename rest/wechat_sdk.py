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

    def __init__(self, url, corp_id, corp_secret, agent_id):
        self.url = url
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.token = {}
        self.agent_id = agent_id

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
    def send_message(self, msg, to_user, to_party, msg_type):
        params = {
            'access_token': self.token['access_token']
        }
        data = {
            "touser": to_user,
            "toparty": to_party,
            "totag": '',
            "msgtype": msg_type,
            "agentid": self.agent_id,
            msg_type: msg,
        }
        r = requests.post(url=self.url+'/message/send', params=params, json=data)
        return r.json()

    @token
    def get_agent(self):
        params = {
            'access_token': self.token['access_token'],
            'agentid': self.agent_id
        }
        r = requests.get(url=self.url+'/agent/get', params=params)
        return r.json()

    def auto_send_text_card_message(self, msg):
        agent = self.get_agent()
        allow_users = reduce(
            lambda x, y: y if x == '' and y else '%s|%s' % (x, y),
            map(lambda x: x['userid'], agent['allow_userinfos']['user']),
            ''
        )

        allow_parties = reduce(
            lambda x, y: y if x == '' and y else '%s|%s' % (x, y),
            map(lambda x: str(x), agent['allow_partys']['partyid']),
            ''
        )
        self.send_message(msg=msg, to_user=allow_users, to_party=allow_parties, msg_type='textcard')

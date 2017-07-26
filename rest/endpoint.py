# -*- coding:utf-8 -*-
import json
import os

from flask import Flask, request

from message import pr_msg, ci_failed_msg
from wechat_sdk import WeChat

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if 'GITHUB_WECHAT_CORP_SECRET' in os.environ.keys():

    we_github = WeChat(
        url=os.environ.get('WECHAT_BASE_URL'),
        corp_id=os.environ.get('WECHAT_CORP_ID'),
        corp_secret=os.environ.get('GITHUB_WECHAT_CORP_SECRET'),
        agent_id=os.environ.get('GITHUB_WECHAT_AGENT_ID')
    )


    @app.route('/wechat', methods=['POST'])
    def github():
        payload = json.loads(request.data)

        repo = {
            'full_name': payload['repository']['full_name'],
            'owner': payload['repository']['owner']['login']
        }

        if 'pull_request' in payload:
            if payload['action'] not in ['closed', 'opened', 'reopened']:
                return 'ignore ' + payload['action']
            we_github.auto_send_text_card_message(
                pr_msg(repo, payload)
            )
            return 'yoyoyo'
        elif 'issue' in payload:
            return
        else:
            return 'not support'


if 'CI_WECHAT_CORP_SECRET' in os.environ.keys():

    we_ci = WeChat(
        url=os.environ.get('WECHAT_BASE_URL'),
        corp_id=os.environ.get('WECHAT_CORP_ID'),
        corp_secret=os.environ.get('CI_WECHAT_CORP_SECRET'),
        agent_id=os.environ.get('CI_WECHAT_AGENT_ID')
    )


    @app.route('/jenkins', methods=['POST'])
    def jenkins():

        payload = request.json

        if 'FINALIZED' in payload['build']['phase']:
            we_ci.auto_send_text_card_message(
                ci_failed_msg(payload)
            )
            return 'yoyoyo'
        return 'ignore'


if __name__ == '__main__':
    app.run()

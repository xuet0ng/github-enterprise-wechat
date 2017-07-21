# -*- coding:utf-8 -*-
from jinja2 import Environment, PackageLoader
import time

env = Environment(loader=PackageLoader('templates', ''))


def get_text_card_msg(title, description, url):
    return {
        'title': title,
        'description': description,
        'url': url
    }


def pr_msg(repo, payload):
    pr = {
        'html_url': payload['pull_request']['html_url'],
        'title': payload['pull_request']['title'],
        'time': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
        'action': payload['action'],
        'user_name': payload['pull_request']['user']['login'],
        'user_html': payload['pull_request']['user']['html_url']
    }
    template = env.get_template('pr.txt')
    return get_text_card_msg(
        title='[PR] ' + pr['title'],
        description=template.render(repo=repo, pr=pr),
        url=pr['html_url']
    )

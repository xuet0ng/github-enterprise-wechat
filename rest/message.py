# -*- coding:utf-8 -*-
from jinja2 import Environment, PackageLoader

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
        'assignee': payload['pull_request']['assignee']['login'],
        'title': payload['pull_request']['title'],
        'action': payload['action'],
        'user_name': payload['pull_request']['user']['login'],
        'user_html': payload['pull_request']['user']['html_url']
    }
    template = env.get_template('pr.txt')
    return get_text_card_msg(
        title=pr['title'],
        description=template.render(repo=repo, pr=pr),
        url=pr['html_url']
    )


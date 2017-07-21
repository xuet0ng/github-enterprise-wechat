# -*- coding:utf-8 -*-
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('templates', ''))


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
    return template.render(repo=repo, pr=pr)

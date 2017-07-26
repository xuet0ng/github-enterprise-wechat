# -*- coding:utf-8 -*-
from jinja2 import Environment, PackageLoader
import datetime

env = Environment(loader=PackageLoader('templates', ''))
pr_template = env.get_template('pr.txt')
ci_failed_template = env.get_template('ci_failed.txt')


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
        'time': time_now(),
        'action': payload['action'],
        'user_name': payload['pull_request']['user']['login'],
        'user_html': payload['pull_request']['user']['html_url']
    }
    return get_text_card_msg(
        title='[PR] ' + pr['title'],
        description=pr_template.render(repo=repo, pr=pr),
        url=pr['html_url']
    )


def ci_failed_msg(payload):
    job = {
        'name': payload['name'],
        'status': payload['build']['status'],
        'url': payload['build']['full_url'],
        'time': time_now(),
    }
    return get_text_card_msg(
        title='[CI Failed] ' + job['name'],
        description=ci_failed_template.render(job=job),
        url=job['url']
    )


def time_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

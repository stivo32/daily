# -*- coding: utf-8 -*-
from jira import JIRA


# login='k_eryomenko'
# password='7226981cxzaQ!'
# jira = JIRA(server=servers['sandbox'], basic_auth=(login, password))
# #projects = jira.projects()
# #issue = jira.issue('WOTD-86712')
# print issue
# userstory = jira.search_issues('text ~ "Тестирование 9.19.1. Проведение ежедневных проверок."')
# print userstory
# #print projects
LINK = 'https://confluence.wargaming.net/pages/viewpage.action?pageId=9240613'


def create_task(jira, assignee, dts_type='TRUNK', date='2017-07-07'):
    main_issue = jira.issue('WOTD-76520')
    project = {'id': 10030}
    description = """
    Данный сабтаск предназначен для проведения ежедневных проверок и логирования времени по ним.
    Вся необходимая информация по проведению проверок находится по [ссылке|{}].
    Тестран можно найти по [ссылке|https://testrail.wargaming.net/wot/index.php?/todos/overview/7]
    Билд для проверки рекомендуется предварительно обновить за день до проверки, чтобы минимизировать время на финальный апдейт.
    При нахождении Very High / High бага при Smoke проверке необходимо поставить в известность К. Ерёменко.
    """.format(LINK)
    issuetype = {'name': 'Sub-task'}
    assignee = {'name': assignee}
    priority = {'name': 'High'}
    components = [{'name': 'QA'}]
    due_date = '2017-07-07'

    summary = u'{}. {}. Eжедневная проверка.'.format(dts_type, due_date)
    issue_dict = {
        'project': project,
        'summary': summary,
        'description': description,
        'parent': {'id': main_issue.key},
        'issuetype': issuetype,
        'assignee': assignee,
        #'priority': priority,
        'components': components,
        'duedate': due_date,
    }

    new_issue = jira.create_issue(fields=issue_dict)
    jira.create_issue_link('is included in', new_issue, main_issue, None)
    print("created Task " + new_issue.key)


def parse_schedule():


def main():
    servers = {
        'production': 'https://jira.wargaming.net',
        'sandbox': 'https://sandbox.wargaming.net/jira'
    }
    login = 'k_eryomenko'
    password = '7226981cxzaQ!'
    jira = JIRA(server=servers['sandbox'], basic_auth=(login, password))
    create_task(jira, 'k_eryomenko')
    #project = {'id': 10030}
    # description = 'test information'
    # issuetype = {'name': 'Task'}
    # assignee = {'name': 'a_gorchakov'}
    # priority = {'name': 'High'}
    # components = [{'name': 'QA'}]
    # due_date = '2017-07-07'
    #
    # summary = u'{}. {}. Eжедневная проверка.'.format('Trunk', due_date)
    # issue_dict = {
    #     'project': {'id': 10030},
    #     'issuetype': issuetype,
    #     'duedate': due_date,
    #     'summary': summary,
    #     'description': description,
    #     'priority': priority,
    #     'components': components,
    #     'assignee': assignee,
    # }
    #
    # issue_dict.update({'assignee': assignee})
    # new_issue = jira.create_issue(fields=issue_dict)
    # print("created Task1 " + new_issue.key)


if __name__ == '__main__':
    main()
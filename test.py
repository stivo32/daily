# -*- coding: utf-8 -*-
__author__ = 'd_kachan'
# JIRA_DK Скрипт для создания версионного контейнера

from jira import JIRA


login = 'k_eryomenko'
password = '7226981cxzaQ!'
#jira = JIRA(server='https://jira.wargaming.net', basic_auth=(login, password))
jira = JIRA(server='https://sandbox.wargaming.net/jira', basic_auth=(login, password))






#Константы
BRANCH_CREATE_DATE = '2017-06-05'#юзаем

DueDate1week='2017-06-09'#######
DueDate2week='2017-06-16'#
DueDate3week='2017-06-23'# 5 Недель для дью дейтов
DueDate4week='2017-06-30'#
DueDate5week='2017-07-07'#
DueDate6week='2017-07-14'######

Current_Stable = '9.19'
Previous_Stable = '9.19'
Current_Fix_Versions = 'v0.9.19'
STABLE_SOURCE = 'Trunk'











######SYS_constans!!not for change
Priority_high={'name':'High'}
Component_QA=[{'name': 'QA'}]
Environment_of_creation_dev_cut_from_='{color:red}*метод создания ветки - срез %s.*{color}' %STABLE_SOURCE


#Cоздание ишью в Жире \
EpicStory_RegressAndStabilization = {
    'project': {'id': 10030},
    'issuetype': {'name': 'Epic Story'},
    #'duedate': DueDate5week,
    'customfield_11571': 'Регресс-тестирование и стабилизация svn ветки {}'.format(Current_Stable), #обязателен для эпик стори(Epic Name)
    'summary': 'Регресс-тестирование и стабилизация svn ветки {}'.format(Current_Stable),
    'description': 'Данный контейнер содержит в себе необходимые активности департамента QA Game по проведению'
                   ' регресс-тестов, тестов наличия\отсутствия необходимого контента и функциональности, иные '
                   'сопроводительные процессы на базе ветки: {}'.format(Current_Stable),
    'priority': Priority_high,
    'components': Component_QA,
    'assignee': {'name': 'd_novitsky'},
    'fixVersions': [{'name':'{}'.format(Current_Fix_Versions)}],
    'environment':Environment_of_creation_dev_cut_from_
}
# #Cоздание ишью
EpicStory = jira.create_issue(fields=EpicStory_RegressAndStabilization)
print("Поехали создавать")
print("created Epic " + EpicStory.key)



TASK1_KONTROL = {
    'project': {'id': 10030},
    'issuetype': {'name': 'Task'},
    'duedate': DueDate5week,
    'summary': 'Тестирование {}. Ежедневный контроль производительности по реплеям и бенчмаркам.'.format(Current_Stable),
    'priority': Priority_high,
    'fixVersions': [{'name':'{}'.format(Current_Fix_Versions)}],
    'description': 'Перечень тестов оформлен в виде саб-тасков: \n# Тестирование {}. Ежедневный контроль версии на'
                   ' базе реплеев. \n# Тестирование {}. Ежедневный контроль производительности версии на базе'
                   ' BenchmarkLocations.'.format(Current_Stable,Current_Stable),
    'components': Component_QA,
    'environment': Environment_of_creation_dev_cut_from_,
    'assignee': {'name': 'a_gorchakov'},
}
# #Cоздание ишью
Task1 = jira.create_issue(fields=TASK1_KONTROL)
## Связь двух ишью в эпик включен таск
jira.create_issue_link('is included in', Task1, EpicStory, None)
print("created Task1 " + Task1.key)


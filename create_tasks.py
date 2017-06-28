# -*- coding: utf-8 -*-
from jira import JIRA
import xlrd
from datetime import date, datetime


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


class Schedule(object):
	def __init__(self):
		self.dates = list()

	def __str__(self):
		if not self.dates:
			res_string = 'Schedule is empty now'
		else:
			res_string = ''
			for duty_date in self.dates:
				res_string += str(duty_date)
		return res_string

	def get(self, day):
		try:
			day = datetime.strptime(day, '%Y-%m-%d').date()
		except ValueError:
			print 'Something wrong with your date, please enter date in format YYYY-mm-dd'
			return
		for duty_date in self.dates:
			if duty_date.day == day:
				return duty_date
		print 'There is no such date in schedule'



class Duty(object):
	def __init__(self, day=None, stable=None, trunk=None):
		self.day = day
		self.stable = stable
		self.trunk = trunk

	def __str__(self):
		if self.day is None:
			res_string = 'No duty today'
		else:
			res_string = """
date = {}, Stable: {}, Trunk: {}""".format(str(self.day), str(self.stable), str(self.trunk))
		return res_string


class Daily(object):
	def __init__(self, on_duty=None):
		self.on_duty = on_duty

	def __str__(self):
		if self.on_duty is not None:
			return str(self.on_duty)
		else:
			return 'Nobody1'


class Stable(Daily):
	def __init__(self, on_duty=None):
		super(Stable, self).__init__(on_duty)


class Trunk(Daily):
	def __init__(self, on_duty=None):
		super(Trunk, self).__init__(on_duty)


class OnDuty(object):
	def __init__(self, credentials=None):
		if isinstance(credentials, str):
			self.credentials = credentials.decode('utf-8')
		else:
			self.credentials = credentials
		self.name_in_english = None
		self.name_in_russian = None

	def __str__(self):
		if self.credentials is not None:
			return self.credentials.encode('utf-8')
		else:
			return 'Nobody'


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
	target_schedule = Schedule()
	path = 'schedule.xlsx'
	sched = xlrd.open_workbook(path)
	schedule = sched.sheet_by_index(1).get_rows()
	dates = next(schedule)[1:]
	dates = [xlrd.xldate_as_tuple(day.value, datemode=sched.datemode) for day in dates]
	tmp_matrix = [row for row in schedule]
	people = [row[0].value for row in tmp_matrix]
	onduty_matrix = [row[1:] for row in tmp_matrix]

	for i, row in enumerate(onduty_matrix):
		onduty_matrix[i] = [
			cell.value
			for cell in row
		]
	for i, day in enumerate(dates):
		stable = trunk = None
		for j, row in enumerate(onduty_matrix):
			if row[i] == 'stable':
				stable = j
			if row[i] == 'trunk':
				trunk = j
				if stable and trunk:
					break
		if stable is not None:
			stable = people[stable]
		if trunk is not None:
			trunk = people[trunk]
		duty = Duty(date(*day[:3]), Stable(OnDuty(stable)), Trunk(OnDuty(trunk)))
		target_schedule.dates.append(duty)
	print target_schedule
	return target_schedule


def main():
	# person = OnDuty(u'Милашевский')
	# person3 = OnDuty('A_milashevskiy')
	# person2 = OnDuty()
	# daily_trunk = Trunk(person)
	# daily_stable = Stable(person3)
	# duty = Duty(day=date.today(), trunk=daily_trunk, stable=daily_stable)
	# print duty
	# schedule = Schedule()
	# print schedule
	# schedule.dates.append(duty)
	# print schedule
	# schedule.dates.append(duty)
	# print schedule
	schedule = parse_schedule()
	tmp = schedule.get('2017-06-26')
	if isinstance(tmp, Duty):
		print tmp.stable

if __name__ == '__main__':
	main()
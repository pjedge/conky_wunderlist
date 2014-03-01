'''Peter Edge
a simple script to grab all wunderlist tasks
and display on a crunchbang-style conky display
'''

from datetime import datetime, date, timedelta
from wunderpy import Wunderlist
from os.path import expanduser
import string, time, subprocess, re, argparse

usage ="""
USAGE:
python get_wunderlist_tasks.py [1] [2] [3] [4] [5]

REQUIRED ARGUMENTS:
[1] wunderlist username/email
[2] wunderlist password
[3] name of task list to sync (e.g. 'groceries')
[4] time between updates (seconds)
[5] time between update attempts if ping fails (seconds)
"""

def parseargs():

	parser = argparse.ArgumentParser(description='read input')
	parser.add_argument('username', nargs='?', type = str)
	parser.add_argument('password', nargs='?', type = str)
	parser.add_argument('list_name', nargs='?', type = str)
	parser.add_argument('wait1', nargs='?', type = int)
	parser.add_argument('wait2', nargs='?', type = int)
	args = parser.parse_args()
	return args

# a task object that holds a name and date and is sortable on date
class simple_task:

	def __init__(self, t, d):

		self.task_name = t
		self.due_date = d

	# overload comparison methods to allow sorting.
	# added the clunky None handling because a task might not have a due date
	def __eq__(self, other):
		return (self.due_date == other.due_date) 

	def __lt__(self, other):
		if (self.due_date == None) and (other.due_date != None):
			return True
		elif (self.due_date != None) and (other.due_date == None):
			return False
		else:
			return (self.due_date < other.due_date) 

	def __le__(self, other):
		if (self.due_date == None) and (other.due_date != None):
			return True
		elif (self.due_date != None) and (other.due_date == None):
			return False
		else:
			return (self.due_date <= other.due_date)

	def __gt__(self, other):
		if (self.due_date != None) and (other.due_date == None):
			return True
		elif (self.due_date != None) and (other.due_date == None):
			return False
		else:
			return (self.due_date > other.due_date)

	def __ge__(self, other):
		if (self.due_date != None) and (other.due_date == None):
			return True
		elif (self.due_date != None) and (other.due_date == None):
			return False
		else:
			return (self.due_date >= other.due_date)

def main():

	# get the arguments from the command line
	args = parseargs()
	username = args.username
	password = args.password
	list_name = args.list_name
	wait1 = args.wait1 # time between updates (sec)
	wait2 = args.wait2 # time between reattempting a failed update (sec)

	# require all arguments
	if (username == None) or (password == None) or (list_name == None) or (wait1 == None) or (wait2 == None):
		print(usage)
		return -1
 
 	# run forever as a background process
	while 1:

		# ping google to see if we have an internet connection
		# ping code copied from this stack overflow thread:
		# http://stackoverflow.com/questions/316866/ping-a-site-in-python
		ping = subprocess.Popen(
		    ["ping", "-c", "4", "www.google.com"],
		    stdout = subprocess.PIPE,
		    stderr = subprocess.PIPE
		)

		out, error = ping.communicate()

		# if there is no error then proceed to get tasks from wunderlist
		if (len(error) == 0):

			w = Wunderlist()
			w.login(username, password)
			w.update_lists()  # you have to run this first, before you do anything else
			tasks = w.tasks_for_list(list_name)
			simple_task_list = []

			# step through tasks, crop the name to an appropriate length,
			# put uncompleted tasks into a simple_task object which is actually sortable on date
			for task in tasks:

				task_name = task.title
				if (len(task_name) > 35):
					task_name = task_name[0:32] + '...'
				due_date = task.due_date
				if not task.completed:
					simple_task_list.append(simple_task(task_name, due_date))
				
			# sort the tasks, open up output file where synced list goes
			simple_task_list.sort()
			home = expanduser("~")
			output_file = open(home + '/.conky_wunderlist/task_list', 'w')

			# print out the tasks in conky format
			for task in simple_task_list:
				
				if (task.due_date != None):
					day = str(task.due_date.day) if task.due_date.day > 9 else '0' + str(task.due_date.day) # pad the day string with a zero if needed
					year = (str(task.due_date.year))[2:4] # get just the last two digits of the year
					print ('{}{}{} / {} / {}'.format(task.task_name,'${alignr}', task.due_date.month, day, year), file=output_file) # print conky-style

				else:
					# if due date is None then just print task name
					print (task.task_name, file=output_file)

			output_file.close()

			# have successfully written tasks to file, sleep for wait1 seconds
			time.sleep(wait1)

		# if there was an error then sleep for wait2 seconds and then try again
		else:
			time.sleep(wait2)

if __name__ == '__main__':
	main()
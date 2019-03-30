from smtplib import SMTP 
from email.mime.text import MIMEText
import subprocess
from sys import argv, exit
import os

def get_users():

	#example: users logged in within the past 10 days 
	last_login = subprocess.Popen(['lastlog -t 10'], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
	(out, err) = last_login.communicate()
	filtered_users = out.split('\n') 
	filter_list = []
	for user in filtered_users[1:-2]: 
		need = user.split(" ")
		filter_list.append(need[0])
	
	#extract all users
	passwd = subprocess.Popen(['getent passwd'], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
	(out, err) = passwd.communicate()
	all_users = out.split('\n')
	email_list = []
	
	for user in all_users[:len(users)-1]:
		info = user.split(':')
		if info[0] in filter_list: #if this user is in the filer_list
				email_list.append(info[0] + '@YourCompany.com')
	
	return email_list
	
	#Test with your email addr
	"""
	test = True
	mylist = []
	if test:
		mylist.append('yourAccount@YourCompany.com')
	if not test:
		print('ERROR')
	return mylist 
	"""

def send_email(msgFile, emails): 
	reply_to_address = 'Human Resource <HR@YourCompany.com>' #where will the reply go
	
	with open(msgFile, 'r') as fp:
		msg = MIMEText(fp.read()) 
	
	s = SMTP('YourCompany.com')
	msg['Subject'] = 'Testing Email'
	msg['From'] = '  <HR@YourCompany.com>'
	msg['Bcc'] = ", ".join(emails) #Use 'Bcc' to hide recipients; otherwise use 'To'
	msg.add_header('Reply-To', reply_to_address)
	s.send_message(msg)
	s.send_message(msg['From'],[msg['Bcc']], msg.as_string())
	s.quit()

if (len(argv) < 2):
	exit('please specify input file with message')

send_email(argv[1], get_users())

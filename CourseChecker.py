import urllib2
import os
from time import gmtime, strftime, sleep
from bs4 import BeautifulSoup
from twilio.rest import Client

# Config Setup
_twilioNumber = "<Twilio Phone Number>"
_SID = "<Twilio Secret>"
_ATOKEN = "<Twilio Access Token>"
_myPhoneNumber = "<Your Phone Number>"

_TIME = 600.0
##

timesRan = 0
queuedList = [] # holds all my URLs
importFile = False
isImported = raw_input("Import Courses From File? ")

importFile = True if (isImported == "y") else False



# Populates List to be scraped

def makeList(course, course_number, course_section):
	
	urlFormed = "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=" + course + "&course=" + course_number + "&section=" + course_section

	fullCourse = {'title': course + " " + course_number + " " + course_section, 'url': urlFormed}

	queuedList.append(fullCourse)


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))



def theWholeFunction():
	global timesRan
	timesRan += 1
	isDone = False
	# Grabbing the User Data + Parsing

	while (isDone == False):

	# Manual Implementation

		if not importFile:
			course = raw_input("Which Course? ")
			if not course:
				break;
			course.upper()

			course_number = raw_input("What is the Course Number? ")
			if not course_number:
				break;

			course_section = raw_input("What is the Course Section? ")
			if not course_section:
				break;


			makeList(course, course_number, course_section)


		# Import from File
		else:
			courseListParsed = []

			with open('courses.txt') as f:
				content = f.read().splitlines()
				for i in content:
					courseListParsed.append(i.split())

			for j in courseListParsed:
				makeList(j[0],j[1],j[2])

			isDone = True


	print("-----------------------------------")

	avail = []

	for i in queuedList:

		numbersList = []

		page = urllib2.urlopen(i['url'])

		soup = BeautifulSoup(page, "html.parser")
		theDataInTags = soup.find_all('strong')
		for theData in theDataInTags:
			if theData.get_text().isdigit():
				numbersList.append(theData.get_text())


		# Print All The Course Data
		print("Course: "  + i['title'])
		print("Total Registered: " + numbersList[0])
		print("Currently Registered: " + numbersList[1])
		print("General Remaining: " + numbersList[2])
		print("Restricted Remaining: " + numbersList[3])
		print("-----------------------------------")

		if (numbersList[2] != "0"):
			print("OMG THERES A SEAT IN " + i['title'] + " GO REGISTER!!!!!")
			print("-----------------------------------")
			avail.append(i['title'])
		else:
			print("Still Full :(")
			print("-----------------------------------")
	# Available Handler

	if (len(avail) != 0):
		print("** REGISTER THESE NOW **")
		print("-----------------------------------")

		for course in avail:
			print(course + "\n")

			# Sending SMS Message
			client = Client(_SID,_ATOKEN)
			client.messages.create(to=_myPhoneNumber,from_=_twilioNumber,body=course)

			notify("Course Available", course)


	else: 
		print("All Queries are Still Full :(")



		print("Number of Times Ran: " + str(timesRan))
		print("Last Ran At: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

	print("\n")
	print("\n")

	del queuedList[:]


while(True):
	theWholeFunction()
	sleep(_TIME)






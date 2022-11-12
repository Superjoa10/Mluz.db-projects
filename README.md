# *Mluz.db-projects is a combination of my projects that uses my works Database(debt colletion db)for automations and data science *
as well as automation of some boring tasks i have at my job, such as sending messeges to new debtors, and the ones i've got deals with.

*WORK PC BRANCH - PYAUTOGUI for automating whatsapp messages*

taking in account that selenium opens different pages, something that can take longer with old computers, using a Makro for this negates this problem.

# Python files:

Agenda.py:

(requires list of deals, and database with numbers)
is a python script that uses my old list of deals in excel(not here for obvious reasons), that i've turned into a CSV(acordos.csv, line 73) to send automatic messages taking in considereation time of day, gender, and more particularities of the deal.

It takes the name from the debtor, and uses it to query the number from a csv that was, itself converted from my access work database(Access 2010 runtime, not here for obvios reasons, refereced in line 54) 


get_genderr.py:

Is a group of complementory functions that i've created to avoid making the same functions everytime i detect a gender for exemple, or using regex to extract numbers from the DB.

# ----------------------------------------------------------------
GUI directory: *WORK IN PROGRESS*

Takes the whole concept and turns it into a GUI, for better organization and ease of use, instead of using my list of deals in excel, and turning it to a csv every time i use it

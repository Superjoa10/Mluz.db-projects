# *Mluz.db-projects is a combination of my projects that uses my works Database for debt colletion*
as well as automation of some boring tasks i have at my job, such as sending messeges to new debtors, and the ones i've got deals with.

*Main branch uses Selenium for the whatsapp automation.*

PYAUTOGUI takes control of the computers mouse, making it so that the automation is the only thing your computer is doing. Selenium let's you do other stuff while the automation runs, if the computer can run it smoothly.

# Python Files:

Agenda.py:

(requires list of deals, and database with numbers)
is a python script that uses my old list of deals in excel(not here for obvious reasons), that i've turned into a CSV(acordos.csv, line 67) to send automatic messages taking in considereation time of day, gender, and more particularities of the deal.

It takes the name from the debtor, and uses it to query the number from a csv that was, itself converted from my access work database(Access 2010 runtime, not here for obvios reasons, line 44).  


get_genderr.py:

Is a group of complementory functions that i've created to avoid making the same functions everytime i detect a gender for exemple, or using regex to extract numbers from the DB.

# ----------------------------------------------------------------
GUI directory: *WORK IN PROGRESS*

Takes the whole concept and turns it into a GUI, for better organization and ease of use, instead of using my list of deals in excel, and turning it to a csv every time i use it

# *Mluz.db-projects is a combination of my projects that uses my works Database(debt colletion db)for automations and data science *
This Branch is old, only being kept to demonstrait my abilities with PYAUTOGUI.

# Python files:

Agenda.py:

(requires list of deals, and database that contains the contact information, the ones in this repository being only exemples)
is a python script that uses my old list of deals in excel(not here for privacy reasons), that i've turned into a CSV (acordos.csv, line 73) to send automatic messages taking in considereation time of day, gender, and more particularities of the deal.

It takes the name from the debtor, and uses it to query the number from a csv that was, itself converted from my access work database(Access 2010 runtime, not here for privacy reasons, refereced in line 54)

How to test it:
the agenda.csv file has a few exemples of how the deals would look like. 
the devedores.csv would contain part of the my works database.
To test this python script, all you have to do is to open the devedores.csv and input a valid number in the DevOBS column for each line.
Than run the python script given the files are referenced correctly in the referecend lines.
#Warning:
Take in to concideration that this script was one of my firsts in automations, and PYAUTOGUI is not very good at Whatsapp messege automations, selenium in the main branch being better for this, but PYAUTOGUI being great, this ones being used in an old computer, the infomation about where to click may be out of sync.

get_genderr.py:

Is a group of complementory functions that i've created to avoid making the same functions everytime i detect a gender for exemple, or using regex to extract numbers from the DB.

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

1. First you have to open the devedores.csv and input a valid number in the DevOBS column for each line ( will have **PLACE NUM HERE** in the line ).

2. Open Whatsapp on your browser, when running the script you'll have a few seconds to open the browser. *You may not move the mouse or any keys while the scrit is running to avoid any errors.

3. Run the python script given the files are referenced correctly in the referecend lines, and the makro has the right information of where to click based on the display used.

#Warning:
Take in to concideration that this script was one of my firsts in automations, and PYAUTOGUI is not very good at Whatsapp messege automations, Selenium in the main branch being better for this, but PYAUTOGUI being great in many instances, Selenium is just better for Web automations. The infomation about where to click may be out of sync, becouse the informations is from a very old computer (Windows 7).

get_genderr.py:

Is a group of complementory functions that i've created to avoid making the same functions everytime i detect a gender for exemple, or using regex to extract numbers from the DB.

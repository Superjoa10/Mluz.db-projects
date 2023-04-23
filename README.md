# *Mluz.db-projects is a combination of my projects that uses my works Database for debt colletion*
This Branch is old, only being kept to demonstrait my abilities with PYAUTOGUI.

# *Python files*:

# Agenda CMDL PYAUTOGUI.py:


is a python script that uses my old list of deals in excel(not here for privacy reasons), that i've turned into a CSV (acordos.csv, lesser version for securety reasins, line 73) to send automatic messages taking in considereation time of day, gender, and more particularities of the deal.

It takes the name from the debtor, and uses it to query the number from a csv that was, itself converted from my access work database(Access 2010 runtime, lesser version privacy reasons, refereced in line 54)

*Warning:
Take in to concideration that this script was one of my firsts in automations, and PYAUTOGUI is not very good at Whatsapp messege automations, Selenium in the main branch being better for this, but PYAUTOGUI being great in many instances, Selenium is just better for Web automations. The infomation about where to click may be out of sync, becouse the informations is from a very old computer (Windows 7).


# Agenda CMDL SELENIUM.py:
is a python script that uses my old list of deals in excel(lesser version privacy reasons), that i've turned into a CSV (acordos.csv, line 67) to send automatic messages taking in considereation time of day, gender, and more particularities of the deal. Where one of my first tests using selenium and worked ok for the most part, way faster than PYAUTOGUI for the task.

It takes the name from the debtor, and uses it to query the number from a csv that was, itself converted from my access work database(Access 2010 runtime, lesser version privacy reasons, refereced in line 44)

# How to test it:
the agenda.csv file has a few exemples of how the deals would look like. 
the devedores.csv would contain part of the my works database.

1. First you have to open the devedores.csv and input a valid number in the DevOBS column for each line ( will have **PLACE NUM HERE** in the line ).

2. Check the acordo file, it must be referenced corretly, to test put the date 'data' as the current date, or thre prazo to test in case of the debtor asking a later date

2. 
FOR PYAUTOGUI: Open Whatsapp on your browser, when running the script you'll have a few seconds to open the browser. *You may not move the mouse or any keys while the scrit is running to avoid any errors;

FOR SELENIUM: Have your cellphone at the ready to scan the QRcode.
.

3. Run the python script given that the files are referenced correctly in the lines above for acordos.csv and devedor.csv, and the makro has the right information of where to click based on the display used.


get_genderr.py:

Is a group of complementory functions that i've created to avoid making the same functions everytime i detect a gender for exemple, or using regex to extract numbers from the DB.

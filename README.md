# *Mluz.db-projects is a combination of my projects that uses my works Database for debt colletion*
as well as automation of some boring tasks i have at my job, such as sending messeges to new debtors, and the ones i've got deals with.

*MAIN BRANCH contains the project turned to EXE files / APPS.*
PC-WORK-BRANCH contains Legacy code for the ideas of the automations presented in the main branch.

This files describes the contents of the repository(1), as well as a tutorial on how to test the Apps various functions(2) and a demonstration of the use case cenarious(3).


# 1. Directorie discriptions:
  * Apps:
  
      * Agenda 2023 1.4 FILES: contains the EXE file for the application described in the 'Agenda 2023 1.4 GUI Source code' directory, for more info on how to test it check for the tutorio section on this file(2);

      * Cobrar_setor FILES: contains the EXE file for the application described in the 'Cobrar_setor Source code' directory, for more info on how to test it check for the tutorio section on this file(2).

# 
  * Agenda 2023 1.4 GUI Source code: 
  
  Contains the source code for the EXE APP Agenda 2023 1.4 in the APPS directorie.

     * Config_files: 
     
       Devedor.csv  -  A part of my works Database, where the program takes the numbers, and does general comparing (MUST BE EDITED TO BE USED, PLEASE SEE SECTION 2 FOR THE TUTORIAL WITH MORE INFO); 
       
       agenda_ops.ini  -  contains the configuration options chosen by the user in the main menu options, or in the main month page, like the color theme; 
       
       agenda_2023.db  -  the database for the whole app, if not created, it'll be created in this directory. This is also where i would keep my backups.
       
    * Icons:
     Contains all .ico files for the APP.
     
     * Body.py: 
     Contains the GUI definition, as well as most of the organization of the information containd on the agenda_2023.db and the devedor.csv, that's sent to the helper functions in the Soul.py file.
     
     * Soul.py:
     Contains helper functions for the main aplication, as well as all the messege automation functions that use Selenium.
     
     
# 
  * Cobrar_setor Source code:

  Contains tne source code for the EXE APP Cobrar_setor in the APPS directorie.
  
    * Cobrar_setor.py:
    A command line tool that uses the pre-existing filters (sector / setor) in my works Access 2010 Runtime database, as well as employee id (funcionario), to send automatic messeges to all debtors that match the filters, being Whatsapp, E-mail or both, it also gives the option for general analisys.(more info on the use case cenerous section(3).
    
    * gett_gender.py: 
    Very simular to soul.py in the Agenda application, it contains helper functions like the name of the file, gender detection, as well as all the functions for automating the messeges send by Selenium and email(ssl, smpt).
  
    * Devedor.csv:
    A part of my works Database, where the program takes all the information about a given case with filters, the infomation being numbers, emails, document type and general information for messege generation (MUST BE EDITED TO BE USED, PLEASE SEE SECTION 2 FOR THE TUTORIAL WITH MORE INFO).


# 
  * Sample data:

  Contains some test data to be used in the tutorial section of this file(2), only used in the tutorial for the Agenda application.


PS: The repository contains mostly .TCL files becouse of the heavy imports the APP has, most likely from CUSTOMTKINTER that bring loads of assets in order to make the APP look more modern, or SELENIUM.


# 2. Tutorials:

  * Agenda 2023 1.4:
    1. Install the whole 'Agenda 2023 1.4 FILES' file, and create a shortcut to the 'Agenda 2023 1.4.EXE' APP and 'config_files' for ease of navegation.(OPTIONAL if running the Source code).
    
    2. Open the Devedor.csv file, add a valid phone number (PLEASE USE A PERSONAL OR FAMILY NUMBER) to the sections where it is asked (ROW AD - 'DevOBS'), it'll be asked as * INSERT NUM HERE * . The number MUST contain the country especific code (Brazil being 55), in my version it is not nessesery as i only use it with brasilian numbers.
    
    3. Now you should open the APP or run the body.py file, and click the 'abrir agenda' - open agenda button
   
    4. The current page is where you select which month you'd like to open, if it doesn't exist i'll give a message. Before being able to open any specific agenda follow the next steps
    
    5. Click the 'add mes' - add month button, now you have 2 choices, either use the 'add_sys_sample'
   
# 
  * Cobrar_setor:
    1. Install the whole 'Cobrar_setor FILES' file, and create a shortcut to the 'Cobrar_setor.EXE' APP. (OPTIONAL if running the Source code) 

PS: *Your sistem must be able to run Python 3.10 minimum to run any of the EXE files.* The information in the Sample files, and Devedor.CSV is all fictional and used as exemples only, to protect the information in my works database, but show how it the information is presented in a real world cenario.

# 3. Use case Scenarios:

Disclaimer: *I do not take resposability of any misuse, spaming or abuseve use of my code, this is for demonstrarion and education purposes only.*

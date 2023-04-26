# *Mluz.db-projects is a combination of my projects that uses my works Database for debt colletion*
as well as automation of some boring tasks i have at my job, such as sending messeges to new debtors, and the ones i've got deals with.

*MAIN BRANCH contains the project turned to EXE files / APPS.*
PC-WORK-BRANCH contains Legacy code for the ideas of the automations presented in the main branch.

This files describes the contents of the repository(1), as well as a tutorial on how to test the Apps various functions(2) and a demonstration of the use case cenarious(3).


# 1. Directories:

  * Agenda 2023 1.4 GUI Source code: 
  
  Contains the source code for the EXE APP Agenda 2023 1.4 in the APPS directorie.

     * Config_files: 
     
       Devedor.csv  -  A part of my works Database, where the program takes the numbers, and does general comparing; 
       
       agenda_ops.ini  -  contains the configuration options chosen by the user in the main menu options, or in the main month page, like the color theme; 
       
       agenda_2023.db  -  the database for the whole app, if not created, it'll be created in this directory. This is also where i would keep my backups.
       
    * Icons:
     Contains all .ico files for the APP
     
     * Body.py: 
     Contains the GUI definition, as well as most of the organization of the information containd on the agenda_2023.db and the devedor.csv, that's sent to the helper functions in the Soul.py file.
     
     * Soul.py:
     Contains helper functions for the main aplication, as well as all the messege automation functions that use Selenium

  * Cobrar_setir Source code:

  Contains tne source code for the EXE APP Cobrar_setor in the APPS directorie.
  
    * Cobrar_setor.py:
    A command line tool that uses the pre-existing filters (sector / setor) in my works Access 2010 Runtime database, as well as 
  
    * Devedor.csv:
    A part of my works Database, where the program takes all the information about a given case with filters, the infomation being numbers, emails, document type and general information for messege generation.
    
    
Observarions: The repository contains mostly .TCL files becouse of the heavy imports the APP has, most likely from CUSTOMTKINTER that bring loads of assets in order to make the APP look more modern, or SELENIUM.

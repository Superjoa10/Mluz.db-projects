# *Mluz.db-projects is a combination of my projects that uses my works Database for debt colletion*
as well as automation of some boring tasks i have at my job, such as sending messeges to new debtors(Cob_Setor), and the ones i've got deals with(Agenda 2023).

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
    
    5. Click the 'add mes' - add month button, now you have 2 choices, either add directly or test the comparing of to files to create the file, IF direct click on the use the 'selecionar arquivo a adicionar' - select file to add button, and select the 'add_sys sample' file in the sample data directory (should apear in the treeview), select a month to add (little error in the app here), than click the 'add month' button. If correct it'll show a confirmation messege. It contains a filter in which it skips the dates where it is weekends, and if the weekend is in the last day of the month it detects and does the change accordingly. if you choose this step, skip to step 7 - XII else follow step 6 to test the creation of the file.
    
    6. To test the creation of the add month file (for why i need this logic, and file representantion see use case cenarious(3)) , click on the 'Logistica de arquivo' - File logic button, you'll be presented with a fullscrean page with two treeview and 2 buttons with distinct names. the one with 'Analise 'mes'' you should select the 'analise_sample' file in the Sample data directory (should appear on the respective treeview), and for the 'Devedores por funcionario' you should select the 'Devedores por funcionario sample' om the sample data directory, than click the 'fazer analise' button, if currect i'll ask for an output directory for the file. After that just repeat step 5 - X.
    
    7. Go back to the main page and select the month you just added the data to, after this you can test the various buttons, and dropdown menus for the different actions.
    
    
    8. General functions and features - 
      
      * Click on a record to highlight it on the screen below; 
      * you can un-select it by clicking the 'limpar campos' clear entries button;
      *  You can update any info from a record by highlighting it than clicking on the 'aplicar mudança' aplie change button, most usefull for turning the deal to 'pago' payed from 0 (not payed) to 1 (payed) or * (Past due by more than a month) (for more information on why the need for the filters see use case cenarious(3)); 
      * Lembrete - reminder, right when you open the page, gives a list of cases where the date for the deal is about 3 to 5 days ahead, to send a reminder about the upcoming deal, it skips the weekends. To test just make a deal 3 days after today and when you open the page again the list should apear with a option to send the message.
      *  Pesquisar - search option menu on the top left corner, has the 'pesquisar por nome' search by name option which opens a page where you can search the name and it returns a list sorted by the closest to the name given, than the 'Resetar' reset option which returns the treeview to it's original position; 
      *  Options 'Mostrar pagos' and 'não mostrar pagos' are Show paid, and do not show paid in this order;
      *   'tema do sistema' being the sistem defalt theme, the rest are self explenatorie;
      *   Pegar excel - get excel returns the current table in a excel file, also referenced in the 6/XI step (for more info on why see use case cenarious(3));
      *   Lista de desfeitos - unmade deals list, opens the respective months page for unmade deals (for more info on why see use case cenarious(3)).
    
    8. Cobrar functions - deal options / dropdown menu options - 
 
       This functions share some functinaleties, being, they all prompt you to log in with your phone and whatsapp account via QRcode; they all try to guess the gender of the person, if ambiguious it'll ask for your manual definintion; they all record the most common reasons for errors in sending the message like Selenium not finding the element to click, a lack of a valid phone number or the var for either the program should or not send the messege, so if any errors exist it'll ask if you'd like to open a page where you can visualize or try again, showing the name of the case and the reason.
    
       * Cob. dia - to test this one you should select each one and change the date to the day you are running the test, or the prazo in the same molds as the date. click the button, than the program will search the 'devedor.csv' for the record with the same name, if the 'cob'  variable is 1, meaning you'd like to send the messege, it'll search for the number, and if found it'll send the messege normalie, else if it doesn't find a number it'll prompt separete the reason for the error.After it'll show you how many where succesfull and how many had erros, if any had issues it'll to open a page with the reasons.

       * Cob. selec - Similar to cob dia, but only sends to the ones that are selected via the 'CTRL + LEFT CLICK' command, sending a very similar message.

       * Posição Selec - Similar to cob dia, but only sends to the ones that are selected via the 'CTRL + LEFT CLICK' command, sending a differente message, asking for a answer from the debtor about the deal.
       
    
    9. Opções acordo fuctions / Dropdown menu options -
    
      * Add acordo - Clicking the 'limpar campos' clear entries button, and inserting all the currect information on the entries, than clicking in the button should add the record to the database and show it on the treeview. Take in to consideration the filters present, like the 'valor' should be a Float point integer, without any ',', the prazo is more accepting of errors but if it's not currectly formated the program will not detect it, it also won't add without the cob and pago.
      
      * Cancelar acordo - break deal, deletes the record from the main table and treeview but ads it to a secondary table where all broken deals are separeted for further analysis (for more info on why see use case cenarious(3))
      
      * Del. acordo S/org. - delete deal withou organazing, as the name implies, it deletes the record but without any organazation.
   
# 
  * Cobrar_setor:
     1. Install the whole 'Cobrar_setor FILES' file, and create a shortcut to the 'Cobrar_setor.EXE' APP. (OPTIONAL if running the Source code) 
    
     2. Open the Devedor.csv file, add a valid phone number and email (PLEASE USE A PERSONAL OR FAMILY NUMBER AND EMAIL) to the sections where it is asked (ROW AD - 'DevOBS'), it'll be asked as * INSERT NUM HERE * and * INSERT E-MAIL HERE * . The number MUST contain the country especific code (Brazil being 55), in my version it is not nessesery as i only use it with brasilian numbers.
     
     3. Open the app or run the python file, it'll open the command line with a few options, all of them being variants of the function 'query_mluz_csv' which after running .
     
     4. Cob functions, being any of them, only difference being the metod in which to send the message. If whastapp or all it'll ask for you to login to whatsapp via your phones app QRcode. It'll ask for a few filters before running like the 'setor' sector, and employees, you should chose between 6 and 7, does not matter that much in this demonstration (for more info on the meaning and nessesity of the sector, and separation of emplooyes see use case cenarious(3)). The functions derive from a function in code 'query_mluz_csv' which after running askes if you'd like to get a analysis of what contacts where missing per case for further search (for more info on why see use case cenarious(3)).
     
     5. Continuar function - continue, continues where you left of on a certain filter (sector and employee) given the number in which you stoped, the same being printed out when running any of the cob fuctions. When it reaches the number of the case you have chosen it'll ask which method you like to send the message. Like the cob functions it derives from a function in code 'query_mluz_csv' which after running askes if you'd like to get a analysis of what contacts where missing per case for further search (for more info on why see use case cenarious(3)).
     
     6. Analise - Analysis, passes thrue all cases on a given filter mostly to access the functionality that like all functions derived from a function in code 'query_mluz_csv' which after running askes if you'd like to get a analysis of what contacts where missing per case for further search (for more info on why see use case cenarious(3)).
     
     7. Test_func - askes which method you'd like to test, than it'll ask  for a number and email if method selected sending a message and testing various functionalities like gender guessing, and message sending in general.
     
     8. Ajuda - Help, contains an explanation for the functions in the command line tool, but it's all in portuguese.

PS: *Your sistem must be able to run Python 3.10 minimum to run any of the EXE files.* The information in the Sample files, and Devedor.CSV is all fictional and used as exemples only, to protect the information in my works database, but show how it the information is presented in a real world cenario.

# 3. Use case Scenarios:
General explanations for the concepts presented in the whole reposetory.

  * Agenda 2023 1.4:
     * Filter need - 1 is paid, 0 is not paid, and 2 is past due by more than a month, being needed mostly not mix the paid with not paid, and most important the ones that are way past due, and need more 'atention' per say, being even a different color. the app has the option to not show the paid ones as not to over crownd the scren with information, as it can have up to 100 payments per month. 
  
     * File logic - I need to take a file given by the Access 2010 runtime containing all the deals('Devedores por funcionario sample'), and compare with the past month agenda gotten by the 'get excel' (Month analys) function, this analysis and comparing took a long time, like 3 4 hours and usualy was unefective as i left details out, like from which phone is the contact, or if it has a payment past due, resulting in erros down the line.
     
     * Lista de desfeito - unmade deals list, it's used to separete deals that where unmade, that in general have a bigger chance of later down the line starting the deal over. it's also used as a report to my boss.
     
  * Cobrar_setor:
    * Filter need - Mostly the scructionr of my works database in Access 2010 runtime, sector has various different pourposes, like 'C' being for deals, 'J' being completed deals, 'D' for 'protesto em cartório' which is a method of blocking a persons name, 'B' being  cases where they can't do the 'protesto em cartório' method and vise versa. Its usefull for differentiating cases when generating messages. Emplooye is very self explenatory, my work db has different employees with passwords and all, each having ther own different cases, that giving the need for a separetion.  
    
    * Analysis - most cases require an extensive reasearch to find the persons contact information, it's usefull to know whats missing in any given case, some might have one email and number for one person in the case, but lack all the info for the other one, or have just an email adress. Knowing this information helps me with reasearch later after the sistem runs.


Disclaimer: *I do not take resposability of any misuse, spaming or abuseve use of my code, this is for demonstrarion and education purposes only.*

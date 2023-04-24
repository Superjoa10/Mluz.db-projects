import sqlite3
import sys
import tkinter
import traceback
import datetime
import csv
import customtkinter as custk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from configparser import ConfigParser
import time
import urllib
import webbrowser
from logging import PlaceHolder
from tkinter import *
from tkinter import filedialog, messagebox, ttk

from soul import form, a_form, num_acd, who_acd, cobrar, cob_prazo, cobrar_selected, cobrar_posiçao, cobrar_lem, money_logic, itemgetter, callback

import pandas as pd

#Database location
_Db_ = 'config_files/Agenda_2023.db'

#Read config file, defines theme, and other details
parser = ConfigParser()
parser.read("config_files/agenda_ops.ini")
saved_color = parser.get('colors', 'color')
saved_show = parser.get('colors', 'cleb')

custk.set_appearance_mode(saved_color)
custk.set_default_color_theme('dark-blue')

#Sub levels of ROOT page

def year_agenda():#PAGE
    """ Opens a Custom Tkinter, that gives the option to open a given months list of deals if table exists (by the func 'open_selected'), or deletes the table (by func 'drop_table') or opens a page to add a month using a excel file"""
    global year, options_M
    options_M = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

    year = custk.CTkToplevel()
    year.title("Selecione mês")

    year.geometry("190x180")
    year.minsize(170, 120)
    year.maxsize(190, 180)

    if saved_color == "system":
        icon_primp = ("icons/calendar-white.ico")
    elif saved_color == "light":
        icon_primp = ("icons/email_select.ico")
    elif saved_color == "dark":
        icon_primp = ("icons/calendar-white.ico")
    year.wm_iconbitmap(icon_primp)

    add_monthbt = custk.CTkButton(year, text="Add mês", command=add_month, width=80, fg_color='darkgreen')
    add_monthbt.grid(column = 0, row = 0)

    var_ = custk.StringVar(value='Selecione mês')
    drop = custk.CTkOptionMenu(year, values = options_M, variable= var_, command=callback_)
    drop.grid(column = 0, row = 1, ipadx=10, padx=15, pady=20)

    open_month = custk.CTkButton(year, text="Abrir", command=lambda:open_selected(selec))
    open_month.grid(column = 0, row = 2, pady=10)

    del_month = custk.CTkButton(year, text="Deletar", command=lambda:drop_table(selec), fg_color='darkred')
    del_month.grid(column = 0, row = 3)


def option_page():#PAGE
    """ Opens test page that gives option to test varios functions like Whatsapp or email automation *WORK IN PROGRESS* """
    list_color = 'system', 'light', 'dark'
    list_show = 'Y', 'N'

    global tets
    tets = custk.CTkToplevel()
    tets.title("Options menu")
    tets.geometry("190x180")
    tets.wm_iconbitmap("icons/cogflat_106041.ico")
    tets.minsize(170, 120)
    tets.maxsize(190, 180)

    main_title = custk.CTkLabel(tets, text="Menu de Opções", anchor=CENTER, padx=3, pady=2, font=("Times New Roman", 25))
    main_title.grid(column=0, row=0, padx=10, pady=5)

    color_label = custk.CTkLabel(tets, text="Tema", anchor=CENTER, padx=3, pady=2,  font=("Times New Roman",21))
    color_label.grid(column=0, row=1, padx=10)  

    var_col = custk.StringVar(value=f'{saved_color}', name='var_col')
    color_menu = custk.CTkOptionMenu(tets, values = list_color, variable= var_col, command=color_opt)    
    color_menu.grid(column=0, row=2, padx=10, pady=5)

    show_label = custk.CTkLabel(tets, text="Mostrar pagos", anchor=CENTER, padx=3, pady=2,  font=("Times New Roman",21))
    show_label.grid(column=0, row=3, padx=10)  

    parser = ConfigParser()
    parser.read("config_files/agenda_ops.ini")
    saved_show = parser.get('colors', 'cleb')

    var_show = custk.StringVar(value=f'{saved_show}', name='var_show')
    show_menu = custk.CTkOptionMenu(tets, values = list_show, variable= var_show, command=show_opt)    
    show_menu.grid(column=0, row=4, padx=10, pady=5)    


#Helper functions for options

def color_opt(selection):
    selection_color = selection
    custk.set_appearance_mode(selection_color)

    parser = ConfigParser()
    parser.read('config_files/agenda_ops.ini')
    parser.set('colors', 'color', selection)
    with open('config_files/agenda_ops.ini', 'w') as configfile:
        parser.write(configfile)

def show_opt(selection):
    shown_selec = selection
    parser = ConfigParser()
    parser.read('config_files/agenda_ops.ini')
    if shown_selec == 'Y':
        parser.set('colors', 'cleb', 'Y')
        with open('config_files/agenda_ops.ini', 'w') as configfile:
            parser.write(configfile)
    if shown_selec == 'N':
        parser.set('colors', 'cleb', 'N')
        with open('config_files/agenda_ops.ini', 'w') as configfile:
            parser.write(configfile)
    

#MAIN PAGE - Sub levels of Year Agenda page

def open_selected(mes):#PAGE
    try:
        global main, me
        me = mes
        year.destroy()
        main = custk.CTkToplevel()
        main.state('zoomed')
        main.geometry('1920x1090')
        main.title(f"Agenda do mes de {mes}")

        if saved_color == "system":
            icon_primp = ("icons/agenda_color.ico")
        elif saved_color == "light":
            icon_primp = ("icons/agenda_page.ico")
        elif saved_color == "dark":
            icon_primp = ("icons/agenda_color.ico")
        main.wm_iconbitmap(icon_primp)

        #defining menu
        my_menu = Menu(main)
        main.config(menu=my_menu)
        my_menu.config(background='black', fg='white', borderwidth=5)

        # Search menu
        search_menu = Menu(my_menu, tearoff=False, background='lightgrey')
        my_menu.add_cascade(label="Pesquisar", menu=search_menu)

        search_menu.add_command(label="Pesquisar por nome", command=lambda:lookup_records(mes))
        search_menu.add_separator()
        search_menu.add_command(label="Resetar", command=lambda:query_database(mes))

        # option menu
        main.config(menu=my_menu)
        option_menu = Menu(my_menu, tearoff=False, background='lightgrey')
        my_menu.add_cascade(label="Options", menu=option_menu)
        
        option_menu.add_command(label="Mostrar pagos", command=lambda:most_pag(mes))
        option_menu.add_command(label="Não mostrar pagos", command=lambda:no_most_pag(mes))
        option_menu.add_separator()

        option_menu.add_command(label="Tema do sistema", command=lambda:color_theme('system'))
        option_menu.add_command(label="Light theme", command=lambda:color_theme('light'))
        option_menu.add_command(label="Dark theme", command=lambda:color_theme('dark'))

        #Main frame for treeview
        global my_tree
        tree_frame = custk.CTkFrame(master=main)
        tree_frame.pack()
 
        tree_scroll = custk.CTkScrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        #treeview creation and appending Scrollbar
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=40)
        tree_scroll.configure(command=my_tree.yview)
        my_tree.pack()

        # Define columns
        my_tree['columns'] = ("rowid", "nome", "data", "prazo", "valor","cob", "pago", "obs")

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("rowid", width=0, stretch=NO)
        my_tree.column("nome", anchor=W, width=400)
        my_tree.column("data", anchor=W, width=85)
        my_tree.column("prazo", anchor=CENTER, width=85)
        my_tree.column("valor", anchor=CENTER, width=100)
        my_tree.column("cob", anchor=CENTER, width=50)
        my_tree.column("pago", anchor=CENTER, width=50)
        my_tree.column("obs", anchor=E, width=1000)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("rowid", text="", anchor=W)
        my_tree.heading("nome", text="Nome", anchor=W)
        my_tree.heading("data", text="Data", anchor=W)
        my_tree.heading("prazo", text="Prazo", anchor=CENTER)
        my_tree.heading("valor", text="Valor", anchor=CENTER)
        my_tree.heading("cob", text="Cob", anchor=CENTER)
        my_tree.heading("pago", text="Pago", anchor=CENTER)
        my_tree.heading("obs", text="OBS", anchor=W)
        query_database(mes)
        
        #Frame for editing info.
        data_frame = custk.CTkFrame(master=main, width=1800)
        data_frame.pack(expand=True)

        global rowid_entry, n_entry, val_entry, dt_entry, pz_entry, pg, cbr, obs_entry
        rowid_entry = custk.CTkEntry(data_frame)

        n_label = custk.CTkLabel(data_frame, text="Nome:", font=("defalt", 12), anchor='w')
        n_label.grid(row=0, column=0)
        n_entry = custk.CTkEntry(data_frame)
        n_entry.grid(row=0, column=1, columnspan=7, ipadx=180)

        dt_label = custk.CTkLabel(data_frame, text="Data:", font=("defalt", 12), width=20)
        dt_label.grid(row=1, column=2)
        dt_entry = custk.CTkEntry(data_frame, width=85)
        dt_entry.grid(row=1, column=3)

        pz_label = custk.CTkLabel(data_frame, text="Prazo:", font=("defalt", 12), width=20)
        pz_label.grid(row=1, column=4)
        pz_entry = custk.CTkEntry(data_frame, width=85)
        pz_entry.grid(row=1, column=5)

        val_label = custk.CTkLabel(data_frame, text="Valor:", font=("defalt", 12), width=20)
        val_label.grid(row=1, column=0, pady=2)
        val_entry = custk.CTkEntry(data_frame, width=80)
        val_entry.grid(row=1, column=1, pady=2, ipadx=60)

        # VAR and definition for cob_auto and pago
        global var_cob, var_pag
        options_YN = ['Y','N']
        options_YNS = ['Y','N','*']
        options_cobs =  ['Cob. dia', 'Cob. selec.', 'Posição selec.']
        options_acordo = ['Add. acordo', 'Cancelar acordo', 'Del. acordo S/org.']

        cbr_label = custk.CTkLabel(data_frame, text="Cob. auto.:", font=("defalt", 12))
        cbr_label.grid(row=0, column=8)

        var_cob = custk.StringVar(value='', name='var_cob')
        drop_cob = custk.CTkOptionMenu(data_frame, values = options_YN, variable= var_cob, command=callback_cob, width=60)
        drop_cob.grid(row = 0, column=9)

        pg_label = custk.CTkLabel(data_frame, text="Pago:", font=("defalt", 12))
        pg_label.grid(row=1, column=8)

        var_pag = custk.StringVar(value='', name='var_pag')
        drop_pag = custk.CTkOptionMenu(data_frame, values = options_YNS, variable=var_pag, command=callback_pg, width=60)
        drop_pag.grid(row = 1, column= 9)

        obs_label = custk.CTkLabel(data_frame, text="Obs:", font=("defalt", 12))
        obs_label.grid(row=0, column=10)
        obs_entry = custk.CTkEntry(data_frame, width=350)
        obs_entry.grid(row=0, column=11, columnspan=6, ipadx=280)

        var_cobr = custk.StringVar(value='Opções cobrar')
        drop_cobr = custk.CTkOptionMenu(data_frame, values = options_cobs, variable = var_cobr, command=cobrar_callback, width=100)
        drop_cobr.grid(row=1, column=11)

        var_acords = custk.StringVar(value='Opções acordo')
        drop_cobr = custk.CTkOptionMenu(data_frame, values = options_acordo, variable = var_acords, command=acordo_callback, width=100)
        drop_cobr.grid(row=1, column=12)

        update_btn = custk.CTkButton(data_frame, text="Aplicar mudança", command=lambda: update_record(mes),anchor= CENTER, width=100)
        update_btn.grid(row=1, column=13, pady=5)

        clear_btn = custk.CTkButton(data_frame, text="Limpar campos", command=lambda:clear_entries(), anchor= CENTER, width=100)
        clear_btn.grid(row=1, column=14, pady=5)

        excel_list_btn = custk.CTkButton(data_frame, text="Pegar Excel", command=lambda:get_excel(mes),anchor= CENTER, width=100)
        excel_list_btn.grid(row=1, column=15, pady=5)

        acd_list_btn = custk.CTkButton(data_frame, text="Lista acd. desfeitos", command=lambda:open_list(mes),anchor= CENTER, width=100)
        acd_list_btn.grid(row=1, column=16, pady=5)

        lembrete(mes)
        my_tree.bind("<ButtonRelease-1>", select_record)

    except sqlite3.Error as er:
        main.destroy()
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        messagebox.showerror("Table not diffined", "A agenda desse mes não foi definida, caso queira a defina adicionando um mes na pagina anterior")


def lembrete(mes):#PAGE
    """Takes all deals that are 3 to 5 days ahead, and returns a list of them, thats used to send a reminder to the person about the upcoming date for the deal"""
    
    dia_hj = datetime.datetime.now().strftime("%d/%m/%Y")
    N_cases = list()

    global lembr, tree_lem
    lembr = custk.CTkToplevel()
    lembr.title(f"Lembretes do dia {dia_hj} ")
    lembr.minsize(700, 250)
    lembr.maxsize(700, 250)

    tree_scroll = custk.CTkScrollbar(lembr)
    tree_scroll.pack(side=RIGHT, fill=Y)

    style = ttk.Style()
    style.theme_use("classic")
    style.configure('Treeview', background='silver', foreground='black', fieldbackground='silver')
    style.map('Treeview', background=[('selected', '#009EFF')])

    tree_lem = ttk.Treeview(lembr, yscrollcommand=tree_scroll.set, selectmode="extended", height=10) #25
    tree_lem.pack()
    tree_scroll.configure(command=tree_lem.yview)

    # Define columns
    tree_lem['columns'] = ("rowid", "nome", "data", "prazo", "obs")

    # Format columns
    tree_lem.column("#0", width=0, stretch=NO)
    tree_lem.column("rowid", width=0, stretch=NO)
    tree_lem.column("nome", anchor=W, width=300)
    tree_lem.column("data", anchor=W, width=90)
    tree_lem.column("prazo", anchor=CENTER, width=45)
    tree_lem.column("obs", anchor=E, width=400)

    # Create Headings
    tree_lem.heading("#0", text="", anchor=W)
    tree_lem.heading("rowid", text="", anchor=W)
    tree_lem.heading("nome", text="Nome", anchor=W)
    tree_lem.heading("data", text="Data", anchor=W)
    tree_lem.heading("prazo", text="Prazo", anchor=CENTER)
    tree_lem.heading("obs", text="OBS", anchor=W)

    lem_button = custk.CTkButton(lembr, text="Cobrar selecionados", command=lambda:cob_lembrete())
    lem_button.pack(pady=10)

    conn = sqlite3.connect(_Db_)
    c = conn.cursor()
    c.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, pago , cob, obs FROM {mes} ORDER BY pago ASC")
    records = c.fetchall()
    for record in records:
        if record[4] != 1:
            acd_lem = datetime.datetime.strptime(record[2], "%d/%m/%Y") - datetime.timedelta(days=3)
            weekcheck = acd_lem.strftime("%A")

            #check weekend
            if weekcheck == "Saturday":
                tree_data_ = acd_lem - datetime.timedelta(days=1)
                tree_data = tree_data_.strftime("%d/%m/20%y")
            elif weekcheck == "Sunday":
                tree_data_ = acd_lem - datetime.timedelta(days=2)
                tree_data = tree_data_.strftime("%d/%m/20%y")
            else:
                tree_data = acd_lem.strftime("%d/%m/20%y")


            if dia_hj == tree_data:
                include_lem = True
                N_cases.append(record[1])
            else: 
                include_lem = False

        if include_lem == True:
            tree_lem.insert("", 'end', values=(record[0], record[1], record[2], record[3],  record[6]))

    if len(N_cases) < 1:
        lembr.destroy()


#Helper function for button in 'lembrete' page 

def cob_lembrete():
        """Takes selected options on the Treeview present in the 'lembrete' page, and organizes it to send to the 'cobrar_lem' function, sending a reminder message to the given cases"""
        x_lem = tree_lem.selection()

        response__ = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?
caso sim, tenha o celular em mãos""")
        if response__ == 1:
            
                navegador_lem = webdriver.Chrome()
                navegador_lem.get("https://web.whatsapp.com/")
                while len(navegador_lem.find_elements(By.ID, 'side')) < 1: 
                        time.sleep(1)
                
                for record_re in x_lem:
                    nome_ = (tree_lem.item(record_re, 'values')[1])
                    data_acd = (tree_lem.item(record_re, 'values')[2])
                    obs_ = (tree_lem.item(record_re, 'values')[3])
                    numero = comp(nome_)
                    if numero == None:
                        messagebox.showwarning("Sem numero", f"O caso {nome_} esta sem numero de whatsapp, OBS: {obs_}")
                        pass
                    else:
                        cobrar_lem(nome_, data_acd, numero, navegador_lem)

        elif response__ == 0:
                pass


#Functions for page style, and parsing to config. file

def most_pag(table):
    global saved_show
    saved_show = 'Y'
    query_database(table)
    parser = ConfigParser()
    parser.read('config_files/agenda_ops.ini')
    parser.set('colors', 'cleb', 'Y')
    with open('config_files/agenda_ops.ini', 'w') as configfile:
        parser.write(configfile)

def no_most_pag(table):
    global saved_show
    saved_show = 'N'
    query_database(table)
    parser = ConfigParser()
    parser.read('config_files/agenda_ops.ini')
    parser.set('colors', 'cleb', 'N')
    with open('config_files/agenda_ops.ini', 'w') as configfile:
        parser.write(configfile)

def color_theme(col):
    saved_color = col
    custk.set_appearance_mode(saved_color)
    if col == "system":
            root.wm_iconbitmap("icons/agenda_white.ico")
            main.wm_iconbitmap("icons/agenda_color.ico")

    elif col == "light":
            root.wm_iconbitmap("icons/home_page.ico")
            main.wm_iconbitmap("icons/agenda_page.ico")

    elif col == "dark":
            root.wm_iconbitmap("icons/agenda_white.ico")
            main.wm_iconbitmap("icons/agenda_color.ico")

    parser = ConfigParser()
    parser.read('config_files/agenda_ops.ini')
    parser.set('colors', 'color', col)
    with open('config_files/agenda_ops.ini', 'w') as configfile:
        parser.write(configfile)


#Helper Functions

def return_entry():
    """ Returns a list of all information from the entrie widgets, used only when adding a new deal 'acordo'."""
    if var_cob.get() == 'Y':
                            var_co = 1
    if var_cob.get() == 'N':
                            var_co = 0
    if var_pag.get() == 'Y':
                            var_pa = 1
    if var_pag.get() == 'N':
                            var_pa = 0
    if var_pag.get() == '*':
                            var_pa = 2

    n = n_entry.get()
    clumber = ''.join([x for x in dt_entry.get() if x.isdigit()])
    clomber = str(datetime.datetime.strptime(clumber, '%d%m%Y'))
    dt = clomber
    pz = pz_entry.get()
    val = float(val_entry.get())
    obs = obs_entry.get()

    lonst = list()
    lonst.append(n)
    lonst.append(dt)
    lonst.append(pz)
    lonst.append(val)
    lonst.append(var_pa)
    lonst.append(var_co)
    lonst.append(obs)

    return lonst

def clear_entries():
        rowid_entry.delete(0, END)
        n_entry.delete(0, END)
        dt_entry.delete(0, END)
        pz_entry.delete(0, END)
        val_entry.delete(0, END)
        var_cob.set(value='')
        var_pag.set(value='')
        obs_entry.delete(0, END) 

def select_record(e):
        """Gets information from clicked Treeview element and presents it to Entries"""
        clear_entries()
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        valor_shit = money_logic(values[4])
        try:
            try:
                cleber = values[4].replace('R$', '')
            except:
                valor_shit == False

            rowid_entry.insert(0, values[0]) 
            n_entry.insert(0, values[1])
            dt_entry.insert(0, values[2])
            pz_entry.insert(0, values[3])
            val_entry.insert(0, cleber)
            if int(values[5]) == 1:
                var_cob.set(value='Y')
            if int(values[5]) == 0:
                var_cob.set(value='N')
            if int(values[6]) == 0:
                var_pag.set(value='N')
            if int(values[6]) == 1:
                var_pag.set(value='Y')
            if int(values[6]) == 2:
                var_pag.set(value='*')
            obs_entry.insert(0, values[7])
        except IndexError:
            pass    

def callback_cob(selection):
    global selec1
    selec1 = selection 

def callback_pg(selection):
    global selec2
    selec2 = selection  

def cobrar_callback(selection):
    """Given a selection from the main 'mes' page, returns a action from the 'cobrar' fuctions(being the ones that sort the information to give to the Whatsapp autimation)"""
    selec_x = selection
    if selec_x == 'Cob. dia':
        cob_dia(selec)
    if selec_x == 'Cob. selec.':
        cob_selected(selec)
    if selec_x == 'Posição selec.':
        cob_posicao(selec)

def acordo_callback(selection):
    """Given a selection from the main 'mes' page, returns a action from the 'acordo' fuctions(being the ones that are responsible for doing things for the Database in reagards to the deals present and shown in the Treeview, like deleting records or adding them)"""
    select_h = selection
    if select_h == 'Add. acordo':
        add_acordo(selec)
    if select_h == 'Cancelar acordo':
        del_and_sort(selec)
    if select_h == 'Del. acordo S/org.':
        del_no_sort(selec)


#FUNCTIONS FOR BUTTONS

def update_record(table):
        selected = my_tree.focus()
        clumber = ''.join([x for x in dt_entry.get() if x.isdigit()])
        clomber = str(datetime.datetime.strptime(clumber, '%d%m%Y'))

        if var_pag.get() == 'Y':
            var_pa = 1
        if var_pag.get() == 'N':
            var_pa = 0
        if var_pag.get() == '*':
            var_pa = 2

        if var_cob.get() == 'Y':
            var_co = 1
        if var_cob.get() == 'N':
            var_co = 0
        if var_cob.get() == '*':
            var_co = 2
    
        try:
            valor_float = val_entry.get()
            valor_float = float(valor_float)
        except ValueError:
            messagebox.showwarning("Invalido", "Valor precisa ser um numero")
            raise TypeError("Only integers are allowed")
        
        my_tree.item(selected, text="", values=(rowid_entry.get(), n_entry.get(), clomber, pz_entry.get(), valor_float, var_co, var_pa, obs_entry.get()))

        conn = sqlite3.connect(_Db_)
        c = conn.cursor()
        c.execute(f"""UPDATE {table} SET
            nome = :nome,
            data = :data,
            prazo = :prazo,
            valor = :valor,
            cob = :cob,
            pago = :pago,
            obs = :obs
            WHERE oid = :oid""",
            {
                'nome': n_entry.get(),
                'data': clomber,
                'prazo': pz_entry.get(),
                'valor': val_entry.get(),
                'cob': var_co,
                'pago': var_pa,
                'obs': obs_entry.get(),
                'oid': rowid_entry.get(),})

        conn.commit()
        conn.close()
        clear_entries()
        clear_all()
        query_database(table)

def get_excel(table):
    """Gives a Excel with all the information from given table, input to the asked directory  """
    directory = filedialog.askdirectory()
    pg_lol = []
    normal_lol = []
    columns = ['Nome', 'Data', 'Prazo', 'Valor', 'Pago', 'Obs']

    conn = sqlite3.connect(_Db_)
    c = conn.cursor()
    c.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, valor, cob, pago, obs FROM {table} ORDER BY pago DESC, data")
    records = c.fetchall()
    for record in records:
                important_shit = {'nome': [], 
                    'data': [],
                    'prazo': [],
                    'valor': [],
                    'pago': [],
                    'obs': [],}
                    
                pg_shit = {'nome': [],
                    'data': [],
                    'prazo': [],
                    'valor': [],
                    'pago': [],
                    'obs': []}
                    
                if record[6] == 1:
                        #acordo pago 
                        pg_shit['nome'].append(record[1])
                        pg_shit['data'].append(record[2])
                        pg_shit['prazo'].append(record[3])
                        pg_shit['valor'].append(record[4])
                        pg_shit['pago'].append(1)
                        pg_shit['obs'].append(record[7])
                        pg_lol.append(pg_shit)
                else:
                        important_shit['nome'].append(record[1])
                        important_shit['data'].append(record[2])
                        important_shit['prazo'].append(record[3])
                        important_shit['valor'].append(record[4])
                        important_shit['pago'].append(record[6])
                        important_shit['obs'].append(record[7])
                        normal_lol.append(important_shit)
    conn.commit()
    conn.close()

    nomes = []
    data = []
    prazo = []
    valor = []
    pago = []
    obs = []

    for put in pg_lol:
        nomes.append(put['nome'][0])
        data.append(put['data'][0])
        prazo.append(put['prazo'][0])
        valor.append(put['valor'][0])
        pago.append(put['pago'][0])
        obs.append(put['obs'][0])
        
    for lol in normal_lol:
        nomes.append(lol['nome'][0])
        data.append(lol['data'][0])
        prazo.append(lol['prazo'][0])
        valor.append(lol['valor'][0])
        pago.append(lol['pago'][0])
        obs.append(lol['obs'][0])
        
    dolf = pd.DataFrame(list(zip(nomes,data,prazo,valor,pago,obs)), columns=columns)
    exit_file = str(directory + f"/analise_{table}.xlsx")
    dolf.to_excel(exit_file, index=False)
    messagebox.showinfo("Salvo!", "Arquivo salvo no local selecionado")
    pass


#Dropdown menu options for 'Acordos', referenced in 'acordo_callback' function

def add_acordo(table):
        """Adds new deal, 'acordo' to the current Table."""
        clomber = return_entry()
        clear_entries()
        conn = sqlite3.connect(_Db_)
        l = conn.cursor()
        l.execute(f"INSERT INTO {table} VALUES (:nome, :data, :prazo, :valor, :pago, :cob, :obs)",
            {
                'nome': clomber[0],
                'data': clomber[1],
                'prazo': clomber[2],
                'valor': clomber[3],
                'pago': clomber[5],
                'cob': clomber[4],
                'obs': clomber[6],
                })
        conn.commit()
        conn.close()

        clear_entries()
        my_tree.delete(*my_tree.get_children())
        query_database(table)    

def del_and_sort(table):
            """Deletes a single selected deal from current table, and adds the folowing information to a sub_table to sort the 'broken' deals for later analisys, the page to view such information being open by the function 'open_list'.
            
                'nome': __nome,
                'data': __data,
                'valor': __valor,
                'obs' : __obs
              
             """
            response = messagebox.askyesno("Voce tem certeza?", " Voce tem certerza que quer desfazer acordo e adicionar a lista de desfeitos?")
            if response == 1:
                        acd_dele = str(table + "_unmade")
                        x = my_tree.selection()[0]
                        my_tree.delete(x)

                        conn = sqlite3.connect(_Db_)
                        c_ = conn.cursor()

                        c_.execute(f"SELECT nome, data, valor, obs FROM {table} WHERE rowid =" + rowid_entry.get())
                        record_del = c_.fetchall()
                        for lol in record_del:
                            __nome = lol[0]
                            __data = lol[1]
                            __valor = lol[2]
                            __obs = lol[3]

                        c_.execute(f"INSERT INTO {acd_dele} VALUES (:nome, :data, :valor, :obs)", 
                                {
                                'nome': __nome,
                                'data': __data,
                                'valor': __valor,
                                'obs': __obs
                                })
                        conn.commit()
                        conn.close()

                        conn_db(f"DELETE from {table} WHERE oid=" + rowid_entry.get())
                        messagebox.showinfo("Deleted!", "Caso foi deletado e adicionado a lista de desfeitos do mes!")
                        clear_entries()
            
def del_no_sort(table):
        """Deletes a single selected deal from current table, without the normal analisys, for cases like duplicates"""
        response = messagebox.askyesno("Voce tem certeza?", " Voce tem certerza que quer desfazer acordo sem organizar?")
        if response == 1:
            x = my_tree.selection()[0]
            my_tree.delete(x)
            conn_db(f"DELETE from {table} WHERE oid=" + rowid_entry.get()) 
            clear_entries()
            messagebox.showinfo("Deleted!", "O caso foi deletado sem organizar!")
        else:
            pass


#Dropdown menu options for 'Cobrar', referenced in 'cobrar_callback' function

def cob_dia(table):
        """Deals with all the mind of getting all the deals for the day, plus the ones that asked for more time 'prazo'.
        1. It creates the browser instance 'navegador'
        2. Checks if the deal has already asked for a later date
        3.  If has no later dates and the date is equal to the current one it starts the process
        4. Check in the case was paid, and the 'cob' var(which is if you'd like to send) is 0 or 1 
        5. To get the number 'numero', it call in the 'comp' function that with then name of the person, compares with the 'M-luz' devedor.csv file
        6. If number VAR exits, it checks if there is 'form' being the second person in the case, and from the 2, who is the deal with
        7. Sends messege via the corresponding 'cobrar' func from 'soul.py' recording which where send succesfully and the ones with 'cob' == 0 or if the browser had any errors
        8. After all is done, gives the option wether you'd like to get a list of the cases that where unsuccesfull. Given you'd like, it opens a secondery page with a threeview and a option to retry the selected ones (Only gives the option if there where any unsuccesfull ones) """
        response_dia = messagebox.askyesno("Cobrar dia", """Voce tem certeza que gostaria de cobrar os casos do dia?""")
        if response_dia == 1:

            navegador = webdriver.Chrome()
            navegador.get("https://web.whatsapp.com/")

            while len(navegador.find_elements(By.ID, 'side')) < 1: 
                time.sleep(1)

            acordo_hj = list()
            acordo_cobdesl = list()
            
            global dia_atual
            dia_atual = datetime.datetime.now().strftime("%d/%m/20%y")
            conn = sqlite3.connect(_Db_)
            c = conn.cursor()
            c.execute(f"SELECT nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, pago , cob, obs FROM {table} ORDER BY pago DESC")
            records = c.fetchall()
            for record in records:
                nome = record[0]
                data = record[1]
                prazo = record[2]
                pago = record[3]
                cobrar_ = record[4]
                obs = record[5]
                if dia_atual == data:
                    if str(prazo.casefold()) != str('None'.casefold()):
                        response_prazo = messagebox.askyesno("Possui prazo", f"""Caso {nome} possui prazo para dia {prazo}, deseja cobrar mesmo assim?""")
                        if response_prazo == 1:
                            continue
                        if response_prazo == 0:
                                                        messagebox.showwarning("Prazo", f"O caso {nome} ja possui um prazo para data futura, OBS: {obs}")
                                                        if obs == None:
                                                                obs = 'none'
                                                        obs_ = str(obs + " #PRAZO#")
                                                        if nome not in acordo_cobdesl:
                                                            dicto = {'nome': nome, 'obs': obs_}
                                                            acordo_cobdesl.append(dicto)
                                                            pass
                                                        else:
                                                              pass
                    else:
                        if pago == 0 or pago == 2:
                            if cobrar_ == 1:
                                if nome not in acordo_hj and nome not in acordo_cobdesl:   
                                    numero = comp(nome) 
                                    if numero == None:
                                                        messagebox.showwarning("Sem numero", f"O caso {nome} esta sem numero de whatsapp, OBS: {obs}")
                                                        if obs == None:
                                                                obs = 'none'
                                                        obs_ = str(obs + " #NO NUMBER ERROR#")
                                                        if nome not in acordo_cobdesl:
                                                            dicto = {'nome': nome, 'obs': obs_}
                                                            acordo_cobdesl.append(dicto)
                                                            pass
                                                        else:
                                                              pass
                                    else:
                                        if forms == True:
                                            if who_acd(obs_dev) == True:
                                                    Bo = cobrar(nome, dia_atual, numero, navegador)
                                                    if Bo  == False:
                                                        if obs == None:
                                                            obs = 'none'
                                                        obs_ = str(obs + " #NO SUCH ELEMENT ERROR#")
                                                        messagebox.showwarning("Não possivel", f"O caso {nome} não conseguiu enviar mensagem; OBS: {obs_}")
                                                        dicto = {'nome': nome, 'obs': obs_}
                                                        acordo_cobdesl.append(dicto)
                                                        pass
                                                    else:
                                                        acordo_hj.append(nome) 

                                            elif who_acd(obs_dev) == False:
                                                    Bo = cobrar(formando, dia_atual, numero, navegador)  
                                                    if Bo == False:
                                                        if obs == None:
                                                            obs = 'none'
                                                        obs_ = str(obs + " #NO SUCH ELEMENT ERROR#")
                                                        messagebox.showwarning("Não possivel", f"O caso {nome} com formando {formando} não connseguiu enviar mensage;, OBS: {obs_}")
                                                        dicto = {'nome': nome, 'obs': obs_}
                                                        acordo_cobdesl.append(dicto)
                                                        pass
                                                    else:
                                                        acordo_hj.append(nome)

                                        else:
                                                    Bo = cobrar(nome, dia_atual, numero, navegador)
                                                    if Bo  == False:
                                                        if obs == None:
                                                            obs = 'none'
                                                        obs_ = str(obs + " #NO SUCH ELEMENT ERROR#")
                                                        messagebox.showwarning("Não possivel", f"O caso {nome} não conseguiu enviar mensagem; OBS: {obs_}")
                                                        dicto = {'nome': nome, 'obs': obs_}
                                                        acordo_cobdesl.append(dicto)
                                                        pass
                                                    else:
                                                        acordo_hj.append(nome)
                                else:
                                                        messagebox.showwarning("Ja cobrado", f"O caso {nome} ja foi cobrado referente a outra data, checar prazos ou casos não cobrados por duplicata por motivo, OBS: {obs}")
                                                        if obs == None:
                                                                            obs = 'none'
                                                        obs_ = str(obs + " #DUPLICATE COB#")
                                                        if nome not in acordo_cobdesl:
                                                            dicto = {'nome': nome, 'obs': obs_}
                                                            acordo_cobdesl.append(dicto)
                                                            pass
                                                        else:
                                                              pass
                            elif cobrar_ == 0:
                                                        messagebox.showwarning("Cobrança automatica desligada!", f"O caso {nome} esta com cobrança automatica desligada, OBS: {obs}")
                                                        if obs == None:
                                                                obs = 'none'
                                                        obs_ = str(obs + " #COB. AUTOMATICA DESLIGADA#")
                                                        if nome not in acordo_cobdesl:
                                                            dicto = {'nome': nome, 'obs': obs_}
                                                            acordo_cobdesl.append(dicto)
                                                            pass
                                                        else:
                                                            pass
                        elif pago == 1:
                            pass

                elif dia_atual == prazo:
                    if pago == 0 or pago ==2:
                        if cobrar_ == 1:
                            if nome not in acordo_hj and nome not in acordo_cobdesl:
                                numero = comp(nome) 
                                if numero == None:
                                                        messagebox.showwarning("Sem numero", f"O caso {nome} esta sem numero de whatsapp, OBS: {obs}")
                                                        if obs == None:
                                                                obs = 'none'
                                                        obs_ = str(obs + "; PRAZO - #NO NUMBER ERROR#")
                                                        if nome not in acordo_cobdesl:
                                                            dicto = {'nome': nome, 'obs': obs_}
                                                            acordo_cobdesl.append(dicto)
                                                            pass
                                                        else:
                                                              pass
                                else:
                                    if forms == True:
                                        if who_acd(obs_dev) == True:
                                                bi = cob_prazo(nome, dia_atual, numero, navegador)
                                                if bi  == False:
                                                        if obs == None:
                                                            obs = 'none'
                                                        obs_ = str(obs + "; PRAZO - #NO SUCH ELEMENT ERROR#")
                                                        messagebox.showwarning("Não possivel", f"O caso {nome} não conseguiu enviar mensagem; OBS: {obs_}")
                                                        dicto = {'nome': nome, 'obs': obs_}
                                                        acordo_cobdesl.append(dicto)
                                                        pass
                                                else:
                                                        acordo_hj.append(nome)  
                                        elif who_acd(obs_dev) == False:
                                                bi = cob_prazo(formando, dia_atual, numero, navegador)
                                                if bi  == False:
                                                        if obs == None:
                                                            obs = 'none'
                                                        obs_ = str(obs + "; PRAZO - #NO SUCH ELEMENT ERROR#")
                                                        messagebox.showwarning("Não possivel", f"O caso {nome} não conseguiu enviar mensagem; OBS: {obs_}")
                                                        dicto = {'nome': nome, 'obs': obs_}
                                                        acordo_cobdesl.append(dicto)
                                                        pass
                                                else:
                                                        acordo_hj.append(nome)  
                                    else:
                                                bi = cob_prazo(nome, dia_atual, numero, navegador)
                                                if bi  == False:
                                                        if obs == None:
                                                            obs = 'none'
                                                        obs_ = str(obs + "; PRAZO - #NO SUCH ELEMENT ERROR#")
                                                        messagebox.showwarning("Não possivel", f"O caso {nome} não conseguiu enviar mensagem; OBS: {obs_}")
                                                        dicto = {'nome': nome, 'obs': obs_}
                                                        acordo_cobdesl.append(dicto)
                                                        pass
                                                else:
                                                        acordo_hj.append(nome)
                            else:
                                                        messagebox.showwarning("Ja cobrado", f"O caso {nome} ja foi cobrado referente a outra data, checar prazos, OBS: {obs}")
                                                        if obs == None:
                                                            obs = 'none'
                                                        obs_ = str(obs + " #DUPLICATE COB#")
                                                        if nome not in acordo_cobdesl:
                                                            dicto = {'nome': nome, 'obs': obs_}
                                                            acordo_cobdesl.append(dicto)
                                                            pass
                                                        else:
                                                              pass

                        elif cobrar_ == 0:
                                                        messagebox.showwarning("Cobrança automatica desligada!", f"O caso {nome} , com acordo dia {data} e prazo para hoje, esta com cobrança automatica desligada, OBS: {obs}")
                                                        if obs == None:
                                                                obs = 'none'
                                                        obs_ = str(obs + "; PRAZO - #COB. AUTOMATICA DESLIGADA#")
                                                        if nome not in acordo_cobdesl:
                                                            dicto = {'nome': nome, 'obs': obs_}
                                                            acordo_cobdesl.append(dicto)
                                                            pass
                                                        else:
                                                              pass
                    elif pago == 1:
                        pass

            if len(acordo_cobdesl) >= 1:
                response = messagebox.askyesno("Pronto!", f"""Todos os casos para o dia {dia_atual} foram cobrados!
        foram cobrados {len(acordo_hj)}, gostaria de tentar cobrar novamente?
        casos com cobrança automatica desligada:
        {acordo_cobdesl}""")
                
                if response == 1:
                    global re_cob
                    re_cob = Toplevel()
                    re_cob.title("Lista recobrados")
                    re_cob.geometry("700x300")
                    if saved_color == "system":
                        icon_primp = ("icons/redo_white.ico")
                    elif saved_color == "light":
                        icon_primp = ("icons/recobrar_all.ico")
                    elif saved_color == "dark":
                        icon_primp = ("icons/redo_white.ico")
                    re_cob.wm_iconbitmap(icon_primp)
                    

                    tree_framere = Frame(re_cob)
                    tree_framere.pack(ipady=180, ipadx=450)
                    tree_framere.configure(bg='#bfbfbf')
                    
                    tree_scrollre = Scrollbar(tree_framere)
                    tree_scrollre.pack(side=RIGHT, fill=Y)

                    global my_treere
                    my_treere = ttk.Treeview(tree_framere, selectmode="extended", height=10)
                    my_treere.pack()
                    
                    tree_scrollre.config(command=my_treere.yview)
                    my_treere['columns'] = ("rowid", "nome", "obs")

                    # Format columns
                    my_treere.column("#0", width=0, stretch=NO)
                    my_treere.column("rowid", width=0, stretch=NO)
                    my_treere.column("nome", anchor=W, width=325)
                    my_treere.column("obs", anchor=E, width=325)

                    # Create Headings
                    my_treere.heading("#0", text="", anchor=W)
                    my_treere.heading("rowid", text="", anchor=W)
                    my_treere.heading("nome", text="nome", anchor=W)
                    my_treere.heading("obs", text="obs", anchor=W)

                    for i, res in enumerate(acordo_cobdesl):
                        my_treere.insert("",'end',iid=res,
                        values=(i,res["nome"], res["obs"]))
                    
                    cobsel_btnre = Button(tree_framere, text="Cobrar selecionados", command=lambda:re_cobrar(), anchor= CENTER)
                    cobsel_btnre.pack(pady=10)
                    
                if response == 0:
                    pass

            elif len(acordo_cobdesl) == 0:
                messagebox.showinfo("Pronto!", f"""Todos os casos para o dia {dia_atual} foram cobrados!
                foram cobrados {len(acordo_hj)}
                """) 
        elif response_dia == 0:
            pass

def cob_selected(table):
        """ Skips most filters in 'cob_dia', but using the ones selected in the trwwview, only checking the fallowing steps:
        1. asks if the selected is the original deal or a asked date
        2. To get the number 'numero', it call in the 'comp' function that with then name of the person, compares with the 'M-luz' devedor.csv file
        3. If number VAR exits, it checks if there is 'form' being the second person in the case, and from the 2, who is the deal with
        4. Sends messege via the corresponding 'cobrar' func from 'soul.py' recording which where send succesfully and the ones with 'cob' == 0 or if the browser had any errors
        5. After all is done, gives the option wether you'd like to get a list of the cases that where unsuccesfull. Given you'd like, it opens a secondery page with a threeview and a option to retry the selected ones (Only gives the option if there where any unsuccesfull ones)
        """    
        response = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?caso sim, tenha o celular em mãos""")
        if response == 1:
                response_ = messagebox.askyesno("Escolha tipo de mensagem", "Sim para acordo, não para prazo")
                navegador = webdriver.Chrome()
                navegador.get("https://web.whatsapp.com/")

                while len(navegador.find_elements(By.ID, 'side')) < 1: 
                    time.sleep(1)

                acordos_selec = []
                acords_bruhh = []
                x = my_tree.selection()
                ids_a_cobrar = []
                for record in x:
                    ids_a_cobrar.append(my_tree.item(record, 'values')[0])
                conn = sqlite3.connect(_Db_)
                cunt = conn.cursor()
                nome_list = []
                for rowid in ids_a_cobrar:
                    cunt.execute(f'SELECT rowid, nome, obs FROM {table} WHERE rowid = {rowid}')
                    nomes = cunt.fetchall()
                    nome_list.append(nomes)
                for olo in nome_list:
                    case = olo[0]
                    nome_ = case[1]
                    obs_slc = case[2]
                    numero = comp(nome_)
                    
                    if numero == None:
                                messagebox.showwarning("Sem numero", f"O caso {nome_} esta sem numero de whatsapp, OBS: {obs_slc}")
                                if obs_slc == None:
                                    obs_slc = 'none'
                                obs_slc_ = str(obs_slc + " #NO NUMBER ERROR#")
                                dicto = {'nome': nome_, 'obs': obs_slc_}
                                acords_bruhh.append(dicto)
                    else:
                        if forms == True:
                            if who_acd(obs_dev) == True:
                                Bo = cobrar_selected(nome_, numero, navegador, response_)
                                if Bo  == False:
                                    if obs_slc == None:
                                        obs_slc = 'none'
                                    obs_slc_ = str(obs_slc + " #NO SUCH ELEMENT ERROR#")
                                    messagebox.showwarning("Não possivel", f"O caso {nome_} não conseguiu enviar mensagem; OBS: {obs_slc_}")
                                    dicto = {'nome': nome_, 'obs': obs_slc_}
                                    acordos_selec.append(dicto)
                                    pass
                                else:
                                    acordos_selec.append(nome_)
                            elif who_acd(obs_dev) == False:
                                Bo = cobrar_selected(formando, numero, navegador, response_)
                                if Bo  == False:
                                    if obs_slc == None:
                                        obs_slc = 'none'
                                    obs_slc_ = str(obs_slc + " #NO SUCH ELEMENT ERROR#")
                                    messagebox.showwarning("Não possivel", f"O caso {nome_} não conseguiu enviar mensagem; OBS: {obs_slc_}")
                                    dicto = {'nome': nome_, 'obs': obs_slc_}
                                    acordos_selec.append(dicto)
                                    pass
                                else:
                                    acordos_selec.append(nome_)  
                        else:
                                Bo = cobrar_selected(nome_, numero, navegador, response_)
                                if Bo  == False:
                                    if obs_slc == None:
                                        obs_slc = 'none'
                                    obs_slc_ = str(obs_slc + " #NO SUCH ELEMENT ERROR#")
                                    messagebox.showwarning("Não possivel", f"O caso {nome_} não conseguiu enviar mensagem; OBS: {obs_slc_}")
                                    dicto = {'nome': nome_, 'obs': obs_slc_}
                                    acordos_selec.append(dicto)
                                    pass
                                else:
                                    acordos_selec.append(nome_)  

                if len(acords_bruhh) >= 1:              
                    response__ = messagebox.askyesno("Pronto!", f"""Todos os casos selecionados foram cobrados!
    foram cobrados {len(acordos_selec)}
    casos que não foi possivel cobrar:
    {acords_bruhh}
    Gostaria de tentar cobrar os não cobrados?""")
                    if response__ == 1:
                        global re_cob
                        re_cob = Toplevel()
                        re_cob.title("Lista recobrados")
                        re_cob.geometry("700x300")
                        if saved_color == "system":
                            icon_primp = ("icons/redo_white.ico")
                        elif saved_color == "light":
                            icon_primp = ("icons/recobrar_all.ico")
                        elif saved_color == "dark":
                            icon_primp = ("icons/redo_white.ico")
                        re_cob.wm_iconbitmap(icon_primp)

                        tree_framere = Frame(re_cob)
                        tree_framere.pack(ipady=180, ipadx=450)
                        tree_framere.configure(bg='#bfbfbf')
                        
                        tree_scrollre = Scrollbar(tree_framere)
                        tree_scrollre.pack(side=RIGHT, fill=Y)

                        global my_treere
                        my_treere = ttk.Treeview(tree_framere, selectmode="extended", height=10)
                        my_treere.pack()
                        
                        tree_scrollre.config(command=my_treere.yview)
                        my_treere['columns'] = ("rowid", "nome", "obs")

                        # Format columns
                        my_treere.column("#0", width=0, stretch=NO)
                        my_treere.column("rowid", width=0, stretch=NO)
                        my_treere.column("nome", anchor=W, width=325)
                        my_treere.column("obs", anchor=E, width=325)

                        # Create Headings
                        my_treere.heading("#0", text="", anchor=W)
                        my_treere.heading("rowid", text="", anchor=W)
                        my_treere.heading("nome", text="nome", anchor=W)
                        my_treere.heading("obs", text="obs", anchor=W)

                        for i, res in enumerate(acords_bruhh):
                            my_treere.insert("",'end',iid=res,
                            values=(i,res["nome"], res["obs"]))
                        
                        cobsel_btnre = Button(tree_framere, text="Cobrar selecionados", command=lambda:re_cobrar_selec(response_), anchor= CENTER)
                        cobsel_btnre.pack(pady=10)
                    
                    elif response__ == 0:
                        pass

                elif len(acords_bruhh) == 0:
                    messagebox.showinfo("Pronto!", f"""Todos os acordos selecionados foram cobrados!
                foram cobrados {len(acordos_selec)}
                """)

def cob_posicao(table):
        """ Skips most filters in 'cob_dia',but using the selected cases from the treeview, to ask the person when they'll pay, only checking the fallowing steps:
            1. To get the number 'numero', it call in the 'comp' function that with then name of the person, compares with the 'M-luz' devedor.csv file
            2. If number VAR exits, it checks if there is 'form' being the second person in the case, and from the 2, who is the deal with
            3. Sends messege via the corresponding 'cobrar' func from 'soul.py' recording which where send succesfully and the ones with 'cob' == 0 or if the browser had any errors
            4. After all is done, gives the option wether you'd like to get a list of the cases that where unsuccesfull. Given you'd like, it opens a secondery page with a threeview and a option to retry the selected ones (Only gives the option if there where any unsuccesfull ones)
        """    
        response = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?
    caso sim, tenha o celular em mãos""")
        if response == 1:

                navegador = webdriver.Chrome()
                navegador.get("https://web.whatsapp.com/")

                while len(navegador.find_elements(By.ID, 'side')) < 1: 
                    time.sleep(1)


                acordos_selec = list()
                acords_notcob = list()
                ids_a_cobrar = list()
                nome_list = list()

                x = my_tree.selection()
                for record in x:
                    ids_a_cobrar.append(my_tree.item(record, 'values')[0])

                conn = sqlite3.connect(_Db_)
                cunt = conn.cursor()

                for rowid in ids_a_cobrar:
                    cunt.execute(f'SELECT rowid, nome, obs FROM {table} WHERE rowid = {rowid}')
                    nomes = cunt.fetchall()
                    nome_list.append(nomes)

                for olo in nome_list:
                    case = olo[0]
                    nome_ = case[1]
                    obs_slc = case[2]
                    numero = comp(nome_) 
                    if numero == None:
                                messagebox.showwarning("Sem numero", f"O caso {nome_} esta sem numero de whatsapp, OBS: {obs_slc}")
                                if obs_slc == None:
                                    obs_slc = 'none'
                                obs_slc_ = str(obs_slc + " #NO NUMBER ERROR#")
                                dicto = {'nome': nome_, 'obs': obs_slc_}
                                acords_notcob.append(dicto)
                    else:
                        if forms == True:
                            if who_acd(obs_dev) == True:
                                Bo = cobrar_posiçao(nome_, numero, navegador) 
                                if Bo  == False:
                                    if obs_slc == None:
                                        obs_slc = 'none'
                                    obs_slc_ = str(obs_slc + " #NO SUCH ELEMENT ERROR#")
                                    messagebox.showwarning("Não possivel", f"O caso {nome_} não conseguiu enviar mensagem; OBS: {obs_slc_}")
                                    dicto = {'nome': nome_, 'obs': obs_slc_}
                                    acordos_selec.append(dicto)
                                    pass
                                else:
                                    acordos_selec.append(nome_)   
                            elif who_acd(obs_dev) == False:
                                Bo = cobrar_posiçao(formando, numero, navegador)
                                if Bo  == False:
                                    if obs_slc == None:
                                        obs_slc = 'none'
                                    obs_slc_ = str(obs_slc + " #NO SUCH ELEMENT ERROR#")
                                    messagebox.showwarning("Não possivel", f"O caso {nome_} não conseguiu enviar mensagem; OBS: {obs_slc_}")
                                    dicto = {'nome': nome_, 'obs': obs_slc_}
                                    acordos_selec.append(dicto)
                                    pass
                                else:
                                    acordos_selec.append(nome_)    
                        else:
                                Bo = cobrar_posiçao(nome_, numero, navegador)
                                if Bo  == False:
                                    if obs_slc == None:
                                        obs_slc = 'none'
                                    obs_slc_ = str(obs_slc + " #NO SUCH ELEMENT ERROR#")
                                    messagebox.showwarning("Não possivel", f"O caso {nome_} não conseguiu enviar mensagem; OBS: {obs_slc_}")
                                    dicto = {'nome': nome_, 'obs': obs_slc_}
                                    acordos_selec.append(dicto)
                                    pass
                                else:
                                    acordos_selec.append(nome_)   

                if len(acords_notcob) >= 1:              
                    response__ = messagebox.askyesno("Pronto!", f"""Todos os casos selecionados foram pedidos poosição!
    foram cobrados {len(acordos_selec)}
    casos que não foi possivel cobrar:
    {acords_notcob}
    Gostaria de tentar cobrar os não cobrados?""")
                    if response__ == 1:
                        global re_cob
                        re_cob = Toplevel()
                        re_cob.title("Lista recobrados")
                        re_cob.geometry("700x300")
                        if saved_color == "system":
                            icon_primp = ("icons/redo_white.ico")
                        elif saved_color == "light":
                            icon_primp = ("icons/recobrar_all.ico")
                        elif saved_color == "dark":
                            icon_primp = ("icons/redo_white.ico")
                        re_cob.wm_iconbitmap(icon_primp)

                        tree_framere = Frame(re_cob)
                        tree_framere.pack(ipady=180, ipadx=450)
                        tree_framere.configure(bg='#bfbfbf')
                        
                        tree_scrollre = Scrollbar(tree_framere)
                        tree_scrollre.pack(side=RIGHT, fill=Y)

                        global my_treere
                        my_treere = ttk.Treeview(tree_framere, selectmode="extended", height=10)
                        my_treere.pack()
                        
                        tree_scrollre.config(command=my_treere.yview)
                        my_treere['columns'] = ("rowid", "nome", "obs")

                        # Format columns
                        my_treere.column("#0", width=0, stretch=NO)
                        my_treere.column("rowid", width=0, stretch=NO)
                        my_treere.column("nome", anchor=W, width=325)
                        my_treere.column("obs", anchor=E, width=325)

                        # Create Headings
                        my_treere.heading("#0", text="", anchor=W)
                        my_treere.heading("rowid", text="", anchor=W)
                        my_treere.heading("nome", text="nome", anchor=W)
                        my_treere.heading("obs", text="obs", anchor=W)

                        for i, res in enumerate(acords_notcob):
                            my_treere.insert("",'end',iid=res,
                            values=(i,res["nome"], res["obs"]))
                        
                        cobsel_btnre = Button(tree_framere, text="Cobrar selecionados", command=lambda:re_cobrar_posi(), anchor= CENTER)
                        cobsel_btnre.pack(pady=10)
                    
                    elif response__ == 0:
                        pass

                elif len(acords_notcob) == 0:
                    messagebox.showinfo("Pronto!", f"""Todos os acordos selecionados foram cobrados posição!
                foram cobrados {len(acordos_selec)}
                """)


#Helper functions for secundary pages in 'cob' functions

def re_cobrar():
        dia_atual = datetime.datetime.now().strftime("%d/%m/20%y")
        x_re = my_treere.selection()
        response__ = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?
caso sim, tenha o celular em mãos""")
        if response__ == 1:
                navegador_re = webdriver.Chrome()
                navegador_re.get("https://web.whatsapp.com/")

                while len(navegador_re.find_elements(By.ID, 'side')) < 1: 
                        time.sleep(1)
                for record_re in x_re:
                    nome_ = (my_treere.item(record_re, 'values')[1])
                    obs_ = (my_treere.item(record_re, 'values')[2])
                    numero = comp(nome_)
                    if numero == None:
                        messagebox.showwarning("Sem numero", f"O caso {nome_} esta sem numero de whatsapp, OBS: {obs_}")
                        pass
                    else:
                        cobrar(nome_, dia_atual, numero, navegador_re)

        elif response__ == 0:
                pass

def re_cobrar_selec(response): 
        dia_atual = datetime.datetime.now().strftime("%d/%m/20%y")
        x_re = my_treere.selection()
        response__ = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?
caso sim, tenha o celular em mãos""")
        if response__ == 1:
                navegador_re = webdriver.Chrome()
                navegador_re.get("https://web.whatsapp.com/")

                while len(navegador_re.find_elements(By.ID, 'side')) < 1: 
                        time.sleep(1)
                for record_re in x_re:
                    nome_ = (my_treere.item(record_re, 'values')[1])
                    obs_ = (my_treere.item(record_re, 'values')[2])
                    numero = comp(nome_)
                    if numero == None:
                        messagebox.showwarning("Sem numero", f"O caso {nome_} esta sem numero de whatsapp, OBS: {obs_}")
                        pass
                    else:
                        cobrar_selected(nome_, dia_atual, numero, navegador_re, response)

        elif response__ == 0:
                pass

def re_cobrar_posi():
        dia_atual = datetime.datetime.now().strftime("%d/%m/20%y")
        x_re = my_treere.selection()
        response__ = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?
caso sim, tenha o celular em mãos""")
        if response__ == 1:
                navegador_re = webdriver.Chrome()
                navegador_re.get("https://web.whatsapp.com/")

                while len(navegador_re.find_elements(By.ID, 'side')) < 1: 
                        time.sleep(1)
                for record_re in x_re:
                    nome_ = (my_treere.item(record_re, 'values')[1])
                    obs_ = (my_treere.item(record_re, 'values')[2])
                    numero = comp(nome_)
                    if numero == None:
                        messagebox.showwarning("Sem numero", f"O caso {nome_} esta sem numero de whatsapp, OBS: {obs_}")
                        pass
                    else:
                        cobrar_posiçao(nome_, dia_atual, numero, navegador_re)

        elif response__ == 0:
                pass 


#Sub level of Main month page

def open_list(mes):#PAGE
        """Open page with subtable of main 'mes' page, with all broken deals """
        global unmade
        unmade = custk.CTkToplevel()
        if saved_color == "system":
            icon_primp = ("icons/block_colored.ico")
        elif saved_color == "light":
            icon_primp = ("icons/unmade_deals.ico")
        elif saved_color == "dark":
            icon_primp = ("icons/block_colored.ico")
        unmade.wm_iconbitmap(icon_primp)
        unmade.state('zoomed')
        unmade.geometry('1920x1090')
        unmade.title(f"Agenda de desfeitos - mes {mes}")

        global my_tree_unmade
        tree_frame_unmade = custk.CTkFrame(unmade)
        tree_frame_unmade.pack()

        #Scrollbar
        tree_scroll_un = custk.CTkScrollbar(tree_frame_unmade)
        tree_scroll_un.pack(side=RIGHT, fill=Y)

        my_tree_unmade = ttk.Treeview(tree_frame_unmade, yscrollcommand=tree_scroll_un.set, selectmode="extended", height=40) #25
        my_tree_unmade.pack()
        my_tree_unmade['columns'] = ("rowid", "nome", "data", "valor", "obs")

        # Format columns
        my_tree_unmade.column("#0", width=0, stretch=NO)
        my_tree_unmade.column("rowid", width=0, stretch=NO)
        my_tree_unmade.column("nome", anchor=W, width=400)
        my_tree_unmade.column("data", anchor=W, width=85)
        my_tree_unmade.column("valor", anchor=CENTER, width=100)
        my_tree_unmade.column("obs", anchor=E, width=1000)

        # Create Headings
        my_tree_unmade.heading("#0", text="", anchor=W)
        my_tree_unmade.heading("rowid", text="", anchor=W)
        my_tree_unmade.heading("nome", text="nome", anchor=W)
        my_tree_unmade.heading("data", text="data", anchor=W)
        my_tree_unmade.heading("valor", text="valor", anchor=CENTER)
        my_tree_unmade.heading("obs", text="obs", anchor=CENTER)

        global rowid_entry_un, n_entry_un, obs_entry_un
        data_frame_un = custk.CTkFrame(unmade)
        data_frame_un.pack(pady=10)

        rowid_entry_un = custk.CTkEntry(data_frame_un)

        n_label_un = custk.CTkLabel(data_frame_un, text="Nome")
        n_label_un.grid(row=0, column=0)
        n_entry_un = custk.CTkEntry(data_frame_un)
        n_entry_un.grid(row=0, column=1, ipadx=150)

        obs_label_un = custk.CTkLabel(data_frame_un, text="OBS")
        obs_label_un.grid(row=0, column=2)
        obs_entry_un = custk.CTkEntry(data_frame_un)
        obs_entry_un.grid(row=0, column=3, ipadx=200)

        update_btn = custk.CTkButton(data_frame_un, text="Aplicar mudança", command=lambda: update_table_un(mes),anchor= CENTER)
        update_btn.grid(row=0, column=4, padx=10)

        del_un_btn = custk.CTkButton(data_frame_un, text="Delete", command=lambda: del_no_sort_un(mes),anchor= CENTER)
        del_un_btn.grid(row=0, column=5)

        update_btn = custk.CTkButton(data_frame_un, text="Get Excel", command=lambda: get_excel_un(mes),anchor= CENTER)
        update_btn.grid(row=0, column=6, padx=10)

        my_tree_unmade.bind("<ButtonRelease-1>", select_record_un)
        query_db_unmade(mes)
        pass


def lookup_records(table):#PAGE
        """Small page that opens, used to search for a case in the given table by calling 'search_records' function"""
        global search_entry, search
        search = custk.CTkToplevel(main)
        search.title("Lookup Records")
        search.geometry("400x200")
        if saved_color == "system":
            icon_primp = ("icons/Search_white.ico")
        elif saved_color == "light":
                icon_primp = ("icons/search_db.ico")
        elif saved_color == "dark":
                icon_primp = ("icons/Search_white.ico")
        search.wm_iconbitmap(icon_primp)
            
        search_frame = custk.CTkFrame(search)
        search_frame.pack(padx=10, pady=10, ipadx=20)

        search_entry = custk.CTkEntry(search_frame, font=("Helvetica", 18), placeholder_text='Informe o nome')
        search_entry.pack(pady=10, ipadx=80)

        search_button = custk.CTkButton(search_frame, text="Search Records", command=lambda:search_records(table))
        search_button.pack(padx=20, pady=30)


#Helper functions

def del_no_sort_un(table):
        response = messagebox.askyesno("Voce tem certeza?", " Voce tem certerza que quer desfazer acordo desfeito da lista?")
        if response == 1:
            table_un = table + "_unmade"
            x = my_tree_unmade.selection()[0]
            my_tree_unmade.delete(x)
            conn_db(f"DELETE from {table_un} WHERE oid=" + rowid_entry_un.get()) 
            clear_entries_un()
            messagebox.showinfo("Deleted!", "O caso foi deletado!")
        else:
            pass
   
def select_record_un(e):
        """Gets information from clicked Treeview element and presents it to Entries"""
        clear_entries_un()
        selected_ = my_tree_unmade.focus()
        values_ = my_tree_unmade.item(selected_, 'values')

        rowid_entry_un.insert(0, values_[0]) 
        n_entry_un.insert(0, values_[1])
        obs_entry_un.insert(0, values_[4])

def clear_entries_un():
    n_entry_un.delete(0, END)
    obs_entry_un.delete(0, END)
    pass

def get_excel_un(table):
    """Gives a Excel with all the information from given secondary table of unmade deals, input to the asked directory  """
    directory_un = filedialog.askdirectory()
    table_un = table + "_unmade"
    columns = ['Nome', 'Data', 'Valor', 'Obs']
    list_un = []

    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute(f"SELECT nome, STRFTIME('%d/%m/%Y', data) as formated_data, valor, obs FROM {table_un} ORDER BY data DESC")
    records = c.fetchall()
    for record in records:
        dict_bruh = {'nome': [], 
                    'data': [],
                    'valor': [],
                    'obs': []}
        
        dict_bruh['nome'].append(record[0])
        dict_bruh['data'].append(record[1])
        dict_bruh['valor'].append(record[2])
        dict_bruh['obs'].append(record[3])
        list_un.append(dict_bruh)
    conn.commit()
    conn.close()

    nomes_un = []
    data_un = []
    valor_un = []
    obs_un = []
    for putt in list_un:
        nomes_un.append(putt['nome'][0])
        data_un.append(putt['data'][0])
        valor_un.append(putt['valor'][0])
        obs_un.append(putt['obs'][0])

    dolf_un = pd.DataFrame(list(zip(nomes_un,data_un,valor_un,obs_un)), columns=columns)
    exit_file = str(directory_un + f"/analise_{table_un}.xlsx")
    dolf_un.to_excel(exit_file, index=False, engine='openpyxl')
    messagebox.showinfo("Salvo!", "Arquivo salvo no local selecionado")

def clear_all_un():
   for item in my_tree_unmade.get_children():
      my_tree_unmade.delete(item)

def update_table_un(table):
        table_un = table + "_unmade"
        selected = my_tree.focus()
        my_tree.item(selected, text="", values=(rowid_entry_un.get(), n_entry_un.get(), obs_entry_un.get()))

        conn = sqlite3.connect(_Db_)
        c = conn.cursor()

        c.execute(f"""UPDATE {table_un} SET
            nome = :nome,
            obs = :obs
            WHERE oid = :oid""",
            {
                'nome': n_entry_un.get(),
                'obs': obs_entry_un.get(),
                'oid': rowid_entry_un.get(),})

        conn.commit()
        conn.close()
        clear_entries_un()
        clear_all_un()
        query_db_unmade(table)


#Sub levels of Year Agenda page 2x

def add_month():#PAGE
    """Opens a page, that's a hub for all the logistics to add a new month, by giving an excel file, or  with logistic page you can create one"""
    global inf, tree__
    inf = custk.CTkToplevel()
    inf.title("Adicionar arquivo")
    inf.geometry("650x400")
    if saved_color == "system":
            icon_primp = ("icons/add_white.ico")
    elif saved_color == "light":
            icon_primp = ("icons/add_month.ico")
    elif saved_color == "dark":
            icon_primp = ("icons/add_white.ico")
    inf.wm_iconbitmap(icon_primp)
    inf.minsize(650, 380)
    inf.maxsize(1200, 350)

    open_btn = custk.CTkButton(inf, text="Selecione arquivo a adicionar", command=lambda:select_file(tree__), anchor= S)
    open_btn.pack(pady=5, ipadx=50)
    
    frame = custk.CTkFrame(inf)
    frame.pack(padx=10, ipadx=50, pady=10)
    tree__ = ttk.Treeview(frame)
    tree__.pack(pady=5)

    frame_obs = custk.CTkFrame(inf)
    frame_obs.pack(ipadx=25)

    var = tkinter.StringVar(inf)
    drop = custk.CTkOptionMenu(frame_obs, values = options_M, variable= var, command=callback_)
    drop.pack(pady=5)

    var.set('Select email')
    comit_month = custk.CTkButton(frame_obs, text="Add month", command=lambda:adding_month(selec))
    comit_month.pack()

    logi_btn = custk.CTkButton(inf, text="Logistica de arquivos", command=logist_page, anchor=S, fg_color='darkgreen')
    logi_btn.pack(pady=5, ipadx=50)

    global label
    label = custk.CTkLabel(frame_obs, text='')
   

def logist_page():#PAGE
    """Is the hub for the logistics for the comparing of the 2 files asked, and the creation on a new excel"""
    global logit, tree_log1, tree_log2
    logit = custk.CTkToplevel()
    logit.title("Logistica dos arquivos")
    logit.state('zoomed')
    logit.geometry('1920x1090')

    frame_lo = custk.CTkFrame(logit)
    frame_lo.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    tree_log1 = ttk.Treeview(frame_lo, height=40)
    tree_log1.grid(row=0, column=0, padx=10)
    tree_log1["column"] = ("X")
    tree_log1.column("X", width = 725, stretch=NO)

    tree_log2 = ttk.Treeview(frame_lo, height=40)
    tree_log2.grid(row=0, column=1, padx=10)
    tree_log2["column"] = ("X")
    tree_log2.column("X", width = 725, stretch=NO)

    orq_btn1 = custk.CTkButton(logit, text="Selecione arquivo - Analise 'Mes' ", command=lambda:select_file(tree_log1), anchor= S)
    orq_btn1.grid(row=0, column=0, pady=5, padx=5)

    orq_btn2 = custk.CTkButton(logit, text="Selecione arquivo - Docs. por Func.", command=lambda:select_file(tree_log2), anchor= S)
    orq_btn2.grid(row=0, column=1, pady=5, padx=5)

    org_btn = custk.CTkButton(logit, text="Fazer analise", command=lambda:analise(tree_log1_filename, tree_log2_filename), anchor= S, fg_color='darkgreen')
    org_btn.grid(row=2, column=0, columnspan=2, pady=5, padx=5, ipadx=35)


#Helper functions

def analise(file_a, file_b):
    """Given both files asked in 'logisti_page' this functions contains all the logit to compare both files and spit out a new one using various filters to be added later to the database in the 'add_month' page. The two files, being one from my Access 2010 runtime sistem, and the other from the excel file produced by the 'get_excel' function on the main month page."""
    analise = pd.read_excel(file_a)
    dev_func = pd.read_excel(file_b)
    dev_average = month_average(file_b)

    analise_list = []
    func_list = []

    final_list = []
    already_add = []
    already_add_pg2 = []

    for index, row in analise.iterrows():
        anal_dict = {
            f'nome{index}': row['Nome'],
            f'data{index}': row['Data'],
            f'prazo{index}':row['Prazo'],
            f'valor{index}':row['Valor'],
            f'pago{index}':row['Pago'],
            f'obs{index}':row['Obs'],
            }
        analise_list.append(anal_dict)

    for index_, row_ in dev_func.iterrows():
        func_dict = {
            f'nome{index_}': row_['CliNome'],
            f'data{index_}': row_['Vencprev'],
            f'valor{index_}': row_['Valprev']
            }
        func_list.append(func_dict)

    for i, anal in enumerate(analise_list):
            ts = str(anal[f'obs{i}'])
            cob = cob_know(ts)

            data_ = date_manip(anal[f'data{i}'])
            date_b = datetime.datetime.strptime(anal[f'data{i}'], '%d/%m/%Y').date()
            num_month = date_b.month
 
            if int(anal[f'pago{i}']) == 2:
                        already_add_pg2.append(anal[f'nome{i}'])

                        a = {'Nome': anal[f'nome{i}'], 'Data': data_, 'prazo': anal[f'prazo{i}'], 'valor': anal[f'valor{i}'], 'pago':2, 'cob': cob[1], 'obs': anal[f'obs{i}']}
                        final_list.append(a)

            if int(anal[f'pago{i}']) == 0 and num_month < dev_average and anal[f'nome{i}'] not in already_add_pg2:
                        already_add_pg2.append(anal[f'nome{i}'])

                        b = {'Nome': anal[f'nome{i}'], 'Data': data_, 'prazo': anal[f'prazo{i}'], 'valor': anal[f'valor{i}'], 'pago': 2, 'cob': cob[1], 'obs': anal[f'obs{i}']}
                        final_list.append(b)

            if int(anal[f'pago{i}']) == 0 and num_month > dev_average and anal[f'nome{i}'] not in already_add:
                        already_add.append(anal[f'nome{i}'])

                        c = {'Nome': anal[f'nome{i}'], 'Data': data_, 'prazo': anal[f'prazo{i}'], 'valor': anal[f'valor{i}'], 'pago': 0, 'cob': cob[1], 'obs': anal[f'obs{i}']}
                        final_list.append(c)

    for i, anal in enumerate(analise_list):       
            for x, func in enumerate(func_list):
                ts = str(anal[f'obs{i}'])
                cob = cob_know(ts)
                data_ = date_manip(func[f'data{x}'])

                if func[f'nome{x}'] == anal[f'nome{i}'] and anal[f'nome{i}'] in already_add_pg2 and func[f'nome{x}'] and anal[f'nome{i}'] not in already_add:
                        already_add.append(func[f'nome{x}'])

                        d = {'Nome': func[f'nome{x}'], 'Data': data_, 'prazo': 'None', 'valor': func[f'valor{x}'], 'pago': 0, 'cob': 0, 'obs': cob[0] + 'Mes passado atrasado '}
                        final_list.append(d)

    for i, anal in enumerate(analise_list):       
            for x, func in enumerate(func_list):
                ts = str(anal[f'obs{i}'])
                cob = cob_know(ts)
                data_ = date_manip(func[f'data{x}'])

                if func[f'nome{x}'] == anal[f'nome{i}'] and int(anal[f'pago{i}']) != 2 and int(anal[f'pago{i}']) != 1 and func[f'nome{x}'] not in already_add:
                        already_add.append(func[f'nome{x}'])

                        e = {'Nome': func[f'nome{x}'], 'Data': data_, 'prazo': 'None', 'valor': func[f'valor{x}'], 'pago': 0, 'cob': cob[1], 'obs': cob[0]}
                        final_list.append(e)

                if func[f'nome{x}'] == anal[f'nome{i}'] and anal[f'nome{i}'] not in already_add_pg2 and func[f'nome{x}'] not in already_add:
                        already_add.append(func[f'nome{x}'])

                        f = {'Nome': func[f'nome{x}'], 'Data': data_, 'prazo': 'None', 'valor': func[f'valor{x}'], 'pago': 0, 'cob': cob[1], 'obs': cob[0]}
                        final_list.append(f)


    for x, func in enumerate(func_list):
         if func[f'nome{x}'] not in already_add and func[f'nome{x}'] not in already_add_pg2:
                        data_ = date_manip(func[f'data{x}'])
                        g = {'Nome': func[f'nome{x}'], 'Data': data_, 'prazo': 'None', 'valor': func[f'valor{x}'], 'pago': 0, 'cob': 1, 'obs': cob[0]}
                        final_list.append(g)

    nomes = list()
    data= list()
    prazo= list()
    valor= list()
    pago= list() 
    obs= list() 
    cob = list() 

    for y, final in enumerate(final_list):
            nomes.append(final['Nome'])
            data.append(final['Data'])
            prazo.append(final['prazo'])
            valor.append(final['valor'])
            pago.append(final['pago'])
            obs.append(final['obs'])
            cob.append(final['cob'])

    columns = ['Nome', 'Data', 'Prazo', 'Valor', 'Pago', 'Obs', 'cob']
    directory_logic = filedialog.askdirectory()
    anal_final= pd.DataFrame(list(zip(nomes,data,prazo,valor,pago,obs, cob)), columns=columns)

    exit_file__ = str(directory_logic + f"/add_sys.xlsx")
    anal_final.to_excel(exit_file__, index=False)
    messagebox.showinfo("Salvo!", "Arquivo salvo no local selecionado")

def cob_know(obs):
    """Returns a list of STR and Int, given a 'obs' STR, that the 'analise' function uses to know if the 'cob' Var should be 0 or 1"""
    cluan = obs.find("#CELL LUAN")
    cbrown = obs.find("#CELL BROWN")
    cmarcos = obs.find("#CELL MARCOS")
    cemail = obs.find("#EMAIL")

    if cluan > -1:
        return ['#CELL LUAN ', 0]
    if cbrown > -1:
        return ['#CELL BROWN ', 0]
    if cmarcos > -1:
        return ['#CELL BROWN ', 0]
    if cemail > -1:
        return ['#EMAIL ', 0]
    else:
        return ['', 1]

def month_average(filename):
        """Given the whole file, returns the avarege month from all the lines in the file, used in login in 'analise' func"""
        dev_func = pd.read_excel(filename)
        func_list = []
        month_list = []

        for index_, row_ in dev_func.iterrows():
            func_dict = {
                f'nome{index_}': row_['CliNome'],
                f'data{index_}': row_['Vencprev'],
                f'valor{index_}': row_['Valprev']
                }
            func_list.append(func_dict)

        for x, func in enumerate(func_list):
            date = func[f'data{x}'].to_pydatetime(func[f'data{x}'])
            monthcheck = int(date.month)
            month_list.append(monthcheck)

        return(max(set(month_list), key=month_list.count))          

def date_manip(date):
    try:
        date = date.to_pydatetime(date)
        mess_data = date.strftime("%d/%m/%y")
        return mess_data 

    except AttributeError:
        mess_data = datetime.datetime.strptime(date, '%d/%m/%Y').date()
        muss_data = mess_data.strftime("%d/%m/%y")
        return muss_data

def select_file(tree_type):
    """Mainly returns the file name, but also adds information to different treeviews, by the 'tree_type' VAR"""
    if str(tree_type) == '.!ctktoplevel2.!ctkframe.!treeview':
        global filename
    filename = filedialog.askopenfilename(title="Open a File", filetype=(("All Files", "*.*"), ("xlrd files", ".*xlrd"), ("xlxs files", ".*xlsx")))
    if filename:
            try:
                filename = r"{}".format(filename)
                global df
                df = pd.read_excel(filename, dtype=str)
            except ValueError:
                label.pack()
                label.config(text="File could not be opened", pady=20, ipady=10)
            except FileNotFoundError:
                label.pack()
                label.config(text="File Not Found",pady=20, ipady=10)
    clear_treeview(tree_type)

    if str(tree_type) == '.!ctktoplevel3.!ctkframe.!treeview'.casefold():
        global tree_log1_filename
        tree_log1_filename = filename
        tree_log1["column"] = list(df.columns)
        tree_log1["show"] = "headings"

        for col in tree_type["column"]:
            tree_log1.column(col, width = 1)
            tree_log1.heading(col, text=col)

        df_rows = (df.to_numpy().tolist())
        for row in df_rows:
            tree_log1.insert("", "end", values=row)
    
    if str(tree_type) == '.!ctktoplevel3.!ctkframe.!treeview2'.casefold():
        global tree_log2_filename
        tree_log2_filename = filename
        tree_log2["column"] = list(df.columns)
        tree_log2["show"] = "headings"

        for col in tree_type["column"]:
            tree_log2.column(col, width = 1)
            tree_log2.heading(col, text=col)

        df_rows = (df.to_numpy().tolist())
        for row in df_rows:
            tree_log2.insert("", "end", values=row)

    if str(tree_type) == '.!ctktoplevel2.!ctkframe.!treeview':
        tree__["column"] = list(df.columns)
        tree__["show"] = "headings"

        for col in tree_type["column"]:
            tree__.heading(col, text=col)

        df_rows = (df.to_numpy().tolist())
        for row in df_rows:
            tree__.insert("", "end", values=row)
    else:
        pass

def clear_treeview(tree_type):
    tree_type.delete(*tree_type.get_children())

def callback_(selection):
    global selec
    selec = selection

def adding_month(selection):
    """Contains all the logic for taking a Excel file, and adding the information to the selected month by the selection VAR."""
    inf.destroy()
    conn = sqlite3.connect(_Db_)
    create_table(selection)
    c = conn.cursor()
    c.execute(f'SELECT count(*) FROM {selection}')
    rest = c.fetchall()
    result = ((rest[0])[0])
    if result == 0:
        messagebox.showinfo("Adding data", "Adding data from selected excel file")
        l = df.values.tolist()
        l_len = len(df.columns)
        n_rows = int(len(l))
        cunt = conn.cursor()
        if l_len == 3:
            df['prazo']=['null' for i in range(n_rows)]
            df['cob']=[1 for i in range(n_rows)]
            df['pago']=[0 for i in range(n_rows)]
            df['obs']=['null' for i in range(n_rows)]
            l = df.values.tolist()
            for _ in l:
                cunt.execute(f"INSERT INTO {selection} VALUES (:nome, :data, :prazo, :valor, :cob, :pago, :obs)", 
                        {
                        'nome': _[0],
                        'data': _[1],
                        'prazo': _[3],
                        'valor': _[2],
                        'cob':_[4],
                        'pago': _[5],
                        'obs': _[6]
                        })
                conn.commit()
        elif l_len == 6 or l_len == 7:
            l = df.values.tolist()
            for _ in l:
                cunt.execute(f"INSERT INTO {selection} VALUES (:nome, :data, :prazo, :valor, :cob, :pago, :obs)", 
                        {
                        'nome': _[0],
                        'data': _[1],
                        'prazo': _[2],
                        'valor': _[3],
                        'cob':_[6],
                        'pago': _[4],
                        'obs': _[5]
                        })
                        
                conn.commit()
    elif result >= 1:
        response = messagebox.askyesno("Table has data", "This table already has data inside, would you like to replace current data?")
        if response == 1:
            drop_table(selection)
            create_table(selection)
            l = df.values.tolist()
            l_len = len(df.columns)
            n_rows = int(len(l))
            cunt = conn.cursor()
            if l_len == 3:
                df['prazo']=['null' for i in range(n_rows)]
                df['cob']=[1 for i in range(n_rows)]
                df['pago']=[0 for i in range(n_rows)]
                df['obs']=['null' for i in range(n_rows)]
                l = df.values.tolist()
                for _ in l:
                    cunt.execute(f"INSERT INTO {selection} VALUES (:nome, :data, :prazo, :valor, :cob, :pago, :obs)", 
                        {
                        'nome': _[0],
                        'data': _[1],
                        'prazo': _[3],
                        'valor': _[2],
                        'cob':_[4],
                        'pago': _[5],
                        'obs': _[6]
                        })
                    conn.commit()
            elif l_len == 6 or l_len == 7:
                l = df.values.tolist()
                for _ in l:
                    cunt.execute(f"INSERT INTO {selection} VALUES (:nome, :data, :prazo, :valor, :cob, :pago, :obs)", 
                        {
                        'nome': _[0],
                        'data': _[1],
                        'prazo': _[2],
                        'valor': _[3],
                        'cob':_[6],
                        'pago': _[4],
                        'obs': _[5]
                        })
                        
                conn.commit()
        if response == 0:
                pass
    conn.commit()
    conn.close()


#Helper Functions focused on DATABASE connection

def conn_db(command):
    """For simple sqlite queries, use this function to avoid repetition, but for Insertions to the database, or more complex queries it does not sufice """
    conn = sqlite3.connect(_Db_)
    c = conn.cursor()
    c.execute(f"{command}")
    
    conn.commit()
    conn.close()

def query_database(table):
    """Opens the database given chosen month, and if it exists, appends data to treeview on the main page. It also contains added filtering by taking all the dates that are weekends, and adding the days nescessary so its a valid week day"""

    my_tree.delete(*my_tree.get_children())
    conn = sqlite3.connect(_Db_)
    c = conn.cursor()

    parser = ConfigParser()
    parser.read("config_files/agenda_ops.ini")
    saved_show = parser.get('colors', 'cleb')

    if saved_show == 'Y':
            c.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, valor, cob, pago, obs FROM {table} ORDER BY pago DESC, data")
    elif saved_show == 'N':
            c.execute(f"""SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, valor, cob, pago, obs FROM {table} WHERE pago <> 1 ORDER BY pago DESC, data""")
    records = c.fetchall()
    for record in records:
                
                month = str(record[2][3] + record[2][4])
                year = str(record[2][6] + record[2][7] + record[2][8] + record[2][9])
                current_data = datetime.datetime.strptime(record[2], "%d/%m/%Y")
                weekcheck = datetime.datetime.strptime(record[2], "%d/%m/%Y").strftime("%A")

                #check weekends and end of month dates
                if weekcheck == "Saturday" and str(record[2]) == f'30/{month}/{year}' or str(record[2]) == f'31/{month}/{year}' or str(record[2]) == f'28/02/{year}':
                    tree_data_ = current_data - datetime.timedelta(days=1)
                    tree_data = tree_data_.strftime("%d/%m/%Y")
                    c.execute(f"""UPDATE {table} SET
                            data = :data
                            WHERE oid = :oid""",
                            {
                                'data': tree_data_,
                                'oid': record[0]})

                elif weekcheck == "Sunday" and str(record[2]) == f'30/{month}/{year}' or str(record[2]) == f'31/{month}/{year}' or str(record[2]) == f'28/02/{year}':
                    tree_data_ = current_data - datetime.timedelta(days=2)
                    tree_data = tree_data_.strftime("%d/%m/%Y")
                    c.execute(f"""UPDATE {table} SET
                            data = :data
                            WHERE oid = :oid""",
                            {
                                'data': tree_data_,
                                'oid': record[0]})
                    
                #check weekends
                elif weekcheck == "Saturday":
                    tree_data_ = current_data + datetime.timedelta(days=2)
                    tree_data = tree_data_.strftime("%d/%m/%Y")
                    c.execute(f"""UPDATE {table} SET
                            data = :data
                            WHERE oid = :oid""",
                            {
                                'data': tree_data_,
                                'oid': record[0]})

                elif weekcheck == "Sunday":
                    tree_data_ = current_data + datetime.timedelta(days=1)
                    tree_data = tree_data_.strftime("%d/%m/%Y")
                    c.execute(f"""UPDATE {table} SET
                            data = :data
                            WHERE oid = :oid""",
                            {
                                'data': tree_data_,
                                'oid': record[0]})

                else:
                    tree_data = record[2]

                my_tog='puss' if record[6] == 2 else 'fail'
                my_tag='pass' if record[6] == 1 else 'fail' 
                looo = record[4]
                currency_string = "R${:,.2f}".format(looo)

                my_tree.insert(parent='', index='end', text='', values=(record[0], record[1], tree_data, record[3], currency_string, record[5], record[6], record[7]), tags=[my_tag, my_tog])
                my_tree.tag_configure('pass', background='lightgreen')
                my_tree.tag_configure('puss', background='tomato')
                    
    conn.commit()
    conn.close()

def query_db_unmade(table):
        """ opens unmade deal table for selectes month and appends data do Treeview"""
        table = table + "_unmade"
        conn = sqlite3.connect(_Db_)
        c_unmade = conn.cursor()
        c_unmade.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, valor, obs FROM {table} ORDER BY data")
        records = c_unmade.fetchall()
        for record in records:
                currency_string_un = "R${:,.2f}".format(record[3])
                my_tree_unmade.insert(parent='', index='end', text='', values=(record[0], record[1], record[2], currency_string_un, record[4]))
        conn.commit()
        conn.close()

def create_table(option):
        """Creates the table, and unmade deals sub table"""
        cancel_acd = str(option + "_unmade")
        conn_db(f"""CREATE TABLE if not exists {option}(
        nome text,
        data integer,
        prazo text,
        valor real,
        cob integer,
        pago integer,
        obs text)""")

        conn_db(f"""CREATE TABLE if not exists {cancel_acd}(
        nome text,
        data integer,
        valor real,
        obs text)""")

def drop_table(table):
    response = messagebox.askyesno("Are you sure?", " Are you sure you would like to delete the current table?")
    if response == 1:
        conn_db(f'DROP TABLE {table}')
        conn_db(f'DROP TABLE {str(table + "_unmade")}')
        main.destroy()
    if response == 0:
            pass

def comp(nome):
    """Used to compare given name with Mluz db (devedor.csv), and return the number for given person."""
    with open("config_files/Devedor.csv", "r", encoding="Latin-1") as file:  
            csv_reader = csv.reader(file, delimiter=';')  
            line_count = 0 
            for devedor in csv_reader:
                if line_count == 0:  
                    line_count += 1   
                else:
                    global forms
                    global obs_dev
                    nome_dev = devedor[1]
                    cobrador = devedor[24]
                    codigo = devedor[25]
                    obs_dev = devedor[29]
                    if cobrador == "6" or cobrador == "7":
                        if codigo.casefold() == "C".casefold():
                            if nome_dev == nome:
                                global formando
                                formando = form(obs_dev)
                                forms = a_form(formando)
                                loko = num_acd(obs_dev, forms)
                                return loko

def clear_all():
   for item in my_tree.get_children():
      my_tree.delete(item)

def search_records(table):
        """Given a name, by the 'search_entry.get()' Var, gets the closest str in the Table for selected month, and inserts into main page Treeview"""
        lookup_record = search_entry.get()
        search.destroy()
        for record in my_tree.get_children():
            my_tree.delete(record)
                    
        conn = sqlite3.connect(_Db_)
        c = conn.cursor()
        c.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, valor, cob, pago, obs FROM {table}")
        records_search = c.fetchall()
        comp__ = []
        for record in records_search:
                looo = record[4]
                currency_string = "R${:,.2f}".format(looo)
                comp = fuzz.ratio(lookup_record.casefold(), record[1].casefold())
                comp_ = {'rowid': record[0], 'nome': record[1], 'data': record[2], 'prazo': record[3], 'valor': record[4], 'cob': record[5], 'pag': record[6], 'obs': record[7], 'comp': comp}
                comp__.append(comp_)

        newlist = sorted(comp__, key=itemgetter('comp'), reverse=True)
        for l in newlist:
            my_tree.insert(parent='', index='end', text='', values=(l['rowid'], l['nome'], l['data'], l['prazo'], l['valor'], l['cob'], l['pag'], l['obs']))


#ROOT
if __name__ == "__main__":
    root = custk.CTk()
    root.title("Agenda 1.4")
    root.minsize(430, 350)
    root.maxsize(430, 350)

    if saved_color == "system":
            icon_primp = ("icons/agenda_white.ico")
    elif saved_color == "light":
            icon_primp = ("icons/home_page.ico")
    elif saved_color == "dark":
            icon_primp = ("icons/agenda_white.ico")
    root.wm_iconbitmap(icon_primp)

    #Style for treeview
    style = ttk.Style()
    style.theme_use("classic")
    style.configure('Treeview', background='silver', foreground='black', fieldbackground='silver')
    style.map('Treeview', background=[('selected', '#009EFF')])

    main_title = custk.CTkLabel(root, text="Agenda 2023", anchor=CENTER, padx=3, pady=2, font=("Times New Roman", 50))
    main_title.grid(column=0, row=0, columnspan = 3, ipadx=100, ipady=30)

    credit = custk.CTkLabel(root, text="Feito por Superjoa10 (click link)", padx=10, pady=50, anchor=W, font=("Times New Roman", 10), cursor="hand2", text_color='blue')
    credit.grid(column=0, row=3)
    credit.bind("<ButtonPress-1>", lambda e:callback("https://github.com/Superjoa10"))

    open_btn = custk.CTkButton(root, text="Abrir agenda", command=year_agenda, anchor= CENTER)
    open_btn.grid(column=0, row=1, columnspan=3, ipadx=10, pady=30)

    open_btn = custk.CTkButton(root, text="Opções", command=option_page, anchor=CENTER)
    open_btn.grid(column=0, row=2, columnspan=3, ipadx=10, pady=10)
    

    root.mainloop()
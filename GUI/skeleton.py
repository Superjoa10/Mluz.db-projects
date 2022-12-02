import sqlite3
import sys
import tkinter
import traceback
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib
from logging import PlaceHolder
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from func import form, a_form, num_acd, who_acd, cobrar, cob_prazo, cobrar_selected, cobrar_posiçao, real_logic 

import pandas as pd

#make function for final de semana skip

#----Defining tables, treviews and buttons-----------------------------------------------------
#****** Main page: ******
root = Tk()
root.title("Agenda BETA 1.0")
root.geometry("430x400")
root.minsize(430, 400)
root.maxsize(430, 400)

main_title = Label(root, text="Agenda 2022", anchor=CENTER, padx=3, pady=2, font=("Times New Roman", 25))
main_title.grid(column=0, row=0, columnspan = 3, ipadx=100, ipady=50)

credit = Label(root, text="Made by Superjoa10 (Click to access my github)", padx=3, pady=2, anchor=CENTER, font=("Times New Roman", 7),fg="blue", cursor="hand2")
credit.grid(column=0, row=3)
credit.bind("<Button-1>", lambda e: callback("https://github.com/Superjoa10"))

#******page for select agenda ******:2
def year_agenda(): #this is the page
    global year
    #Show old and new months/ see how to add list of tables from db
    year = Toplevel()
    year.title("Selecione mes")
    year.geometry("175x325")
    year.minsize(175, 325)
    year.maxsize(200, 330)

    #buttons:
    add_btn = Button(year, text="Adicionar novo mes", command=add_month, anchor=CENTER)
    add_btn.grid(column = 0, row = 0, padx=5, pady=5, ipadx= 5, sticky=NE, columnspan = 2)
    open_btn = Button(year, text="01/22", command=lambda:open_selected('Januery'))
    open_btn.grid(column = 0, row = 1, pady=5, sticky=N)
    open_btn = Button(year, text="02/22", command=lambda:open_selected('Fevereiro'))
    open_btn.grid(column = 1, row = 1, pady=5, sticky=N)
    open_btn = Button(year, text="03/22", command=lambda:open_selected('Março'))
    open_btn.grid(column = 0, row = 2, pady=5, sticky=N)
    open_btn = Button(year, text="04/22", command=lambda:open_selected('Abril'))
    open_btn.grid(column = 1, row = 2, pady=5, sticky=N)
    open_btn = Button(year, text="05/22", command=lambda:open_selected('Maio'))
    open_btn.grid(column = 0, row = 3, pady=5, sticky=N)
    open_btn = Button(year, text="06/22", command=lambda:open_selected('Junho'))
    open_btn.grid(column = 1, row = 3, pady=5, sticky=N)
    open_btn = Button(year, text="07/22", command=lambda:open_selected('Julho'))
    open_btn.grid(column = 0, row = 4, pady=5, sticky=N)
    open_btn = Button(year, text="08/22", command=lambda:open_selected('Agosto'))
    open_btn.grid(column = 1, row = 4, pady=5, sticky=N)
    open_btn = Button(year, text="09/22", command=lambda:open_selected('Setembro'))
    open_btn.grid(column = 0, row = 5, pady=5, sticky=N)
    open_btn = Button(year, text="10/22", command=lambda:open_selected('Outubro'))
    open_btn.grid(column = 1, row = 5, pady=5, sticky=N)
    open_btn = Button(year, text="11/22", command=lambda:open_selected('Novembro'))
    open_btn.grid(column = 0, row = 6, pady=5, sticky=N)
    open_btn = Button(year, text="12/22", command=lambda:open_selected('Dezembro'))
    open_btn.grid(column = 1, row = 6, pady=5, sticky=N)

#main page button to open page
open_btn = Button(root, text="Abrir agenda", command=year_agenda, padx=3, pady=2, anchor= CENTER)
open_btn.grid(column=0, row=1, columnspan=3, ipadx=10, pady=30)

open_btn = Button(root, text="Informações", command=PlaceHolder, anchor=CENTER)
open_btn.grid(column=2, row=3, sticky=E, pady=70, padx=50)

#***********Main agenda page definition************
def return_entry():
    lonst = []
    n = n_entry.get()

    clumber = ''.join([x for x in dt_entry.get() if x.isdigit()])
    clomber = str(datetime.datetime.strptime(clumber, '%d%m%Y'))
    dt = clomber

    pz = pz_entry.get()
    val = float(val_entry.get())
    cob = cbr.get()
    pago = pg.get()
    obs = obs_entry.get()
    lonst.append(n)
    lonst.append(dt)
    lonst.append(pz)
    lonst.append(val)
    lonst.append(cob)
    lonst.append(pago)
    lonst.append(obs)
    return lonst

def add_acordo(table):
        clomber = return_entry()
        clear_entries()

        conn = sqlite3.connect('agenda.db')
        l = conn.cursor()
        l.execute(f"INSERT INTO {table} VALUES (:nome, :data, :prazo, :valor, :cob, :pago, :obs)",
            {
                'nome': clomber[0],
                'data': clomber[1],
                'prazo': clomber[2],
                'valor': clomber[3],
                'cob': clomber[4],
                'pago': clomber[5],
                'obs': clomber[6],})
        conn.commit()
        conn.close()

        clear_entries()
        my_tree.delete(*my_tree.get_children())
        query_database(table)
        pass

def open_selected(mes):#This is page
    try:
        global main
        main = Toplevel()
        main.attributes('-fullscreen', False)
        main.title(f"Agenda do mes {mes}")
        year.destroy()

        global my_tree
        tree_frame = Frame(main)
        tree_frame.pack(ipady=180, ipadx=450)
        tree_frame.configure(bg='#bfbfbf')
        # Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=38) #25
        my_tree.pack()
        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define columns
        my_tree['columns'] = ("rowid", "nome", "data", "prazo", "valor","cob", "pago", "obs")

        # Format columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("rowid", width=0, stretch=NO)
        my_tree.column("nome", anchor=W, width=300)
        my_tree.column("data", anchor=W, width=85)
        my_tree.column("prazo", anchor=CENTER, width=85)
        my_tree.column("valor", anchor=CENTER, width=100)
        my_tree.column("cob", anchor=CENTER, width=50)
        my_tree.column("pago", anchor=CENTER, width=50)
        my_tree.column("obs", anchor=E, width=840)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("rowid", text="", anchor=W)
        my_tree.heading("nome", text="nome", anchor=W)
        my_tree.heading("data", text="data", anchor=W)
        my_tree.heading("prazo", text="prazo", anchor=CENTER)
        my_tree.heading("valor", text="valor", anchor=CENTER)
        my_tree.heading("cob", text="cob", anchor=CENTER)
        my_tree.heading("pago", text="pago", anchor=CENTER)
        my_tree.heading("obs", text="obs", anchor=W)
        query_database(mes)
        
        #Frame for editing info.
        data_frame = LabelFrame(main, text="Informações")
        data_frame.place(x=25,y=800,height=150,width=1800)

        global rowid_entry, n_entry, val_entry, dt_entry, pz_entry, pg, cbr, obs_entry
        rowid_entry = Entry(data_frame)

        n_label = Label(data_frame, text="Nome")
        n_label.grid(row=0, column=0)
        n_entry = Entry(data_frame)
        n_entry.grid(row=0, column=1, ipadx=100)

        dt_label = Label(data_frame, text="Data")
        dt_label.grid(row=0, column=2)
        dt_entry = Entry(data_frame)
        dt_entry.grid(row=0, column=3)

        pz_label = Label(data_frame, text="Prazo")
        pz_label.grid(row=1, column=2)
        pz_entry = Entry(data_frame)
        pz_entry.grid(row=1, column=3)

        val_label = Label(data_frame, text="Valor")
        val_label.grid(row=1, column=0, pady=2)
        val_entry = Entry(data_frame)
        val_entry.grid(row=1, column=1, pady=2, ipadx=100)

        cbr_label = Label(data_frame, text="Cob auto.")
        cbr_label.grid(row=0, column=4)
        cbr = Entry(data_frame)
        cbr.grid(row=0, column= 5)

        pg_label = Label(data_frame, text="Pago")
        pg_label.grid(row=1, column=4)
        pg = Entry(data_frame)
        pg.grid(row=1, column= 5, ipadx=0.0001, ipady=0.0001)

        obs_label = Label(data_frame, text="OBS")
        obs_label.grid(row=0, column=6)
        obs_entry = Entry(data_frame)
        obs_entry.grid(row=0, column=7, columnspan=5, ipadx=300)

        cob_btn = Button(data_frame, text="Cobrar do dia", command=lambda: cob_dia(mes), anchor= CENTER)
        cob_btn.grid(row=1, column=7)

        cobsel_btn = Button(data_frame, text="Cobrar selecionados", command=lambda: cob_selected(mes), anchor= CENTER)
        cobsel_btn.grid(row=1, column=8)

        acd_list_btn = Button(data_frame, text="Posição selecionado", command=lambda:cob_posicao(mes),anchor= CENTER)
        acd_list_btn.grid(row=1, column=9, pady=5) 

        clear_btn = Button(data_frame, text="Limpar campos", command=lambda:clear_entries(), anchor= CENTER)
        clear_btn.grid(row=1, column=10, pady=5)

        update_btn = Button(data_frame, text="Aplicar mudança", command=lambda: update_record(mes),anchor= CENTER)
        update_btn.grid(row=1, column=11, pady=5)

        add_acd_btn = Button(data_frame, text="Adicionar acordo", command=lambda:add_acordo(mes),anchor= CENTER)
        add_acd_btn.grid(row=2, column=1, padx=1, pady=5) 

        canc_btn = Button(data_frame, text="Cancelar acordo", command=lambda: del_and_sort(mes),anchor= CENTER)
        canc_btn.grid(row=2, column=3)

        delNO_btn = Button(data_frame, text="Deletar acd. sem organizar", command=lambda:del_no_sort(mes),anchor= CENTER)
        delNO_btn.grid(row=2, column=5, pady=5) 

        del_btn = Button(data_frame, text="Deletar agenda", command=lambda:drop_table(mes),anchor= CENTER)
        del_btn.grid(row=2, column=7, pady=5) 

        acd_list_btn = Button(data_frame, text="Pegar Excel - Lista de acordos", command=lambda:get_excel(mes),anchor= CENTER)
        acd_list_btn.grid(row=2, column=9, pady=5)

        acd_list_btn = Button(data_frame, text="Lista acordos desfeitos", command=lambda:open_list(mes),anchor= CENTER)
        acd_list_btn.grid(row=2, column=11, pady=5)
        
        my_tree.bind("<ButtonRelease-1>", select_record)

    except sqlite3.Error as er:
        main.destroy()
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        messagebox.showerror("Table not diffined", "A agenda desse mes não foi definida, caso queira a defina adicionando um mes")
    
def select_record(e):
        clear_entries()
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        valor_shit = real_logic(values[4])

        try:
            cleber = values[4].replace('R$', '')
        except:
            valor_shit == False

        rowid_entry.insert(0, values[0]) 
        n_entry.insert(0, values[1])
        dt_entry.insert(0, values[2])
        pz_entry.insert(0, values[3])
        val_entry.insert(0, cleber)
        cbr.insert(0, values[5])
        pg.insert(0, values[6])
        obs_entry.insert(0, values[7])

def clear_entries():
        rowid_entry.delete(0, END)
        n_entry.delete(0, END)
        dt_entry.delete(0, END)
        pz_entry.delete(0, END)
        val_entry.delete(0, END)
        cbr.delete(0, END)
        pg.delete(0, END)
        obs_entry.delete(0, END)        

#FUNCTIONS FOR BUTTONS :

def clear_all():
   for item in my_tree.get_children():
      my_tree.delete(item)

def cob_dia(table):
        messagebox.showwarning("Checar Whatsapp", "Essa versão da agenda usa o Selenium para mandar mensagem, antes de continuar abra o whatsapp e verifique se não a nenhuma atualização")
        navegador = webdriver.Chrome()
        navegador.get("https://web.whatsapp.com/")

        while len(navegador.find_elements(By.ID, 'side')) < 1: 
            time.sleep(1)

        acordo_hj = []
        acordo_cobdesl = []
        dia_atual = datetime.datetime.now().strftime("%d/%m/20%y")
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        c.execute(f"SELECT nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, pago , cob, obs FROM {table} ORDER BY pago ASC")
        records = c.fetchall()
        for record in records:
            nome = record[0]
            data = record[1]
            prazo = record[2]
            pago = record[3]
            cobrar_ = record[4]
            obs = record[5]

            if dia_atual == data:
                if pago == 0 or pago ==2:
                    if cobrar_ == 1:
                        numero = comp(nome) 
                        if numero == None:
                                        messagebox.showwarning("Sem numero", f"O caso {nome} esta sem numero de whatsapp, OBS: {obs}")
                                        dicto = {'nome': nome, 'obs': obs}
                                        acordo_cobdesl.append(dicto)
                        else:
                            acordo_hj.append(nome)
                            if forms == True:
                                if who_acd(obs_dev) == True:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}, porem possui formando")
                                        cobrar(nome, dia_atual, numero, navegador)  
                                        print(f"{nome} cobrado(a)")  
                                elif who_acd(obs_dev) == False:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o formando: {formando} {numero}")
                                        cobrar(formando, dia_atual, numero, navegador)  
                                        print(f"{nome} cobrado(a)") 
                            else:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}")
                                        cobrar(nome, dia_atual, numero, navegador)  
                                        print(f"{nome} cobrado(a)")  
                    elif cobrar_ == 0:
                                        messagebox.showwarning("Cobrança automatica desligada!", f"O caso {nome} esta com cobrança automatica desligada, OBS: {obs}")
                                        dicto = {'nome': nome, 'obs': obs}
                                        acordo_cobdesl.append(dicto)
                                        pass
                elif pago == 1:
                    pass

            if dia_atual == prazo:
                if pago == 0 or pago ==2:
                    if cobrar_ == 1:
                        numero = comp(nome) 
                        if numero == None:
                                        messagebox.showwarning("Sem numero", f"O caso {nome} esta sem numero de whatsapp, OBS: {obs}")
                                        dicto = {'nome': nome, 'obs': obs}
                                        acordo_cobdesl.append(dicto)
                        else:
                            acordo_hj.append(nome)
                            if forms == True:
                                if who_acd(obs_dev) == True:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}, porem possui formando")
                                        cob_prazo(nome, dia_atual, numero, navegador)  
                                        print(f"{nome} cobrado(a)")  
                                elif who_acd(obs_dev) == False:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o formando: {formando} {numero}")
                                        cob_prazo(formando, dia_atual, numero, navegador)  
                                        print(f"{nome} cobrado(a)") 
                            else:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}")
                                        cob_prazo(nome, dia_atual, numero, navegador)  
                                        print(f"{nome} cobrado(a)")
                    elif cobrar_ == 0:
                                        messagebox.showwarning("Cobrança automatica desligada!", f"O caso {nome} , com acordo dia {data} e prazo para hoje, esta com cobrança automatica desligada, OBS: {obs}")
                                        dicto = {'nome': nome, 'obs': obs}
                                        acordo_cobdesl.append(dicto)
                                        pass
                elif pago == 1:
                    pass
        if len(acordo_cobdesl) >= 1:
            response = messagebox.askyesno("Pronto!", f"""Todos os casos para o dia {dia_atual} foram cobrados!
    foram cobrados {len(acordo_hj)}, gostaria de tentar cobrar novamente?
    casos com cobrança automatica desligada:
    {acordo_cobdesl}""")
        elif len(acordo_cobdesl) == 0:
               messagebox.showinfo("Pronto!", f"""Todos os casos para o dia {dia_atual} foram cobrados]
               foram cobrados{len(acordo_hj)}
               """) 
        if response == 1:
            #create page with list of this cases, and way to select which ones
            pass
        if response == 0:
            pass

def cob_selected(table):
	response = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?
caso sim, tenha o celular em mãos""")
	if response == 1:
            response = messagebox.askyesno("Escolha tipo de mensagem", "Sim para acordo, não para prazo")

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
            conn = sqlite3.connect('agenda.db')
            cunt = conn.cursor()
            nome_list = []
            for rowid in ids_a_cobrar:
                cunt.execute(f'SELECT rowid, nome FROM {table} WHERE rowid = {rowid}')
                nomes = cunt.fetchall()
                nome_list.append(nomes)
            for olo in nome_list:
                nome_ = olo[0]
                numero = comp(nome_[1]) 
                if numero == None:
                            messagebox.showwarning("Sem numero", f"O caso {nome_[1]} esta sem numero de whatsapp")
                            acords_bruhh.append(nome_[1])
                else:
                    acordos_selec.append(nome_[1])
                    if forms == True:
                        if who_acd(obs_dev) == True:
                            print("----------------------------------------------------------------------------------")
                            print(f"Cobrando acordo do {nome_[1]}, acordo sendo com o devedor {numero}, porem possui formando")
                            cobrar_selected(nome_[1], numero, navegador, response)  
                            print(f"{nome_[1]} cobrado(a)")  
                        elif who_acd(obs_dev) == False:
                            print("----------------------------------------------------------------------------------")
                            print(f"Cobrando acordo do {nome_[1]}, acordo sendo com o formando: {formando} {numero}")
                            cobrar_selected(formando, numero, navegador, response)  
                            print(f"{nome_[1]} cobrado(a)") 
                    else:
                            print("----------------------------------------------------------------------------------")
                            print(f"Cobrando acordo do {nome_[1]}, acordo sendo com o devedor {numero}")
                            cobrar_selected(nome_[1], numero, navegador, response)  
                            print(f"{nome_[1]} cobrado(a)") 

            messagebox.showwarning("Pronto!", f"""Todos os casos selecionadod foram cobrados!
foram cobrados {len(acordos_selec)}
casos que não foi possivel cobrar:
{acords_bruhh}""")

def cob_posicao(table):
	response = messagebox.askyesno("Cobrar selecionado", """Voce tem certeza que gostaria de cobrar os casos selecionados?
caso sim, tenha o celular em mãos""")
	if response == 1:
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
            conn = sqlite3.connect('agenda.db')
            cunt = conn.cursor()
            nome_list = []
            for rowid in ids_a_cobrar:
                cunt.execute(f'SELECT rowid, nome FROM {table} WHERE rowid = {rowid}')
                nomes = cunt.fetchall()
                nome_list.append(nomes)
            for olo in nome_list:
                nome_ = olo[0]
                numero = comp(nome_[1]) 
                if numero == None:
                            messagebox.showwarning("Sem numero", f"O caso {nome_[1]} esta sem numero de whatsapp")
                            acords_bruhh.append(nome_[1])
                else:
                    acordos_selec.append(nome_[1])
                    if forms == True:
                        if who_acd(obs_dev) == True:
                            print("----------------------------------------------------------------------------------")
                            print(f"Pedindo posição do acordo do {nome_[1]}, acordo sendo com o devedor {numero}, porem possui formando")
                            cobrar_posiçao(nome_[1], numero, navegador)  
                            print(f"{nome_[1]} cobrado(a)")  
                        elif who_acd(obs_dev) == False:
                            print("----------------------------------------------------------------------------------")
                            print(f"Pedindo posição do acordo {nome_[1]}, acordo sendo com o formando: {formando} {numero}")
                            cobrar_posiçao(formando, numero, navegador)  
                            print(f"{nome_[1]} cobrado(a)") 
                    else:
                            print("----------------------------------------------------------------------------------")
                            print(f"Pedindo posição do acordo {nome_[1]}, acordo sendo com o devedor {numero}")
                            cobrar_posiçao(nome_[1], numero, navegador)  
                            print(f"{nome_[1]} cobrado(a)") 

            messagebox.showwarning("Pronto!", f"""Todos os casos selecionados pedidos posição!
foram cobrados {len(acordos_selec)}
casos que não foi possivel cobrar:
{acords_bruhh}""")

def del_and_sort(table):
            response = messagebox.askyesno("Voce tem certeza?", " Voce tem certerza que quer desfazer acordo e adicionar a lista de desfeitos?")
            if response == 1:
                        acd_dele = str(table + "_unmade")
                        x = my_tree.selection()[0]
                        my_tree.delete(x)

                        conn = sqlite3.connect('agenda.db')
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

                        clear_entries()
                        messagebox.showinfo("Deleted!", "Caso foi deletado e adicionado a lista de desfeitos do mes!")
            else:
                        pass
            
def del_no_sort(table):
        response = messagebox.askyesno("Voce tem certeza?", " Voce tem certerza que quer desfazer acordo sem organizar?")
        if response == 1:
            x = my_tree.selection()[0]
            my_tree.delete(x)
            conn_db(f"DELETE from {table} WHERE oid=" + rowid_entry.get()) 
            clear_entries()
            messagebox.showinfo("Deleted!", "O caso foi deletado sem organizar!")
        else:
            pass
   
def update_record(table):
        selected = my_tree.focus()
        clumber = ''.join([x for x in dt_entry.get() if x.isdigit()])
        clomber = str(datetime.datetime.strptime(clumber, '%d%m%Y'))

        #error handlings for Entry widgets
        try:
            valor_float = val_entry.get()
            valor_float = float(valor_float)
        except ValueError:
            messagebox.showinfo("Invalido", "Valor precisa ser um numero")
            raise TypeError("Only integers are allowed")
        try:
            int(cbr.get())
            int(pg.get())
        except ValueError:
            messagebox.showinfo("Invalido", "Valor precisa ser um numero")
            raise TypeError("Only integers are allowed")

        my_tree.item(selected, text="", values=(rowid_entry.get(), n_entry.get(), clomber, pz_entry.get(), valor_float, cbr.get(), pg.get(), obs_entry.get()))
        
        conn = sqlite3.connect('agenda.db')
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
                'cob': cbr.get(),
                'pago':pg.get(),
                'obs': obs_entry.get(),
                'oid': rowid_entry.get(),})

        conn.commit()
        conn.close()
        clear_entries()
        clear_all()
        query_database(table)

def comp(nome):#queries Mluz db.
    with open("Devedor.csv", "r", encoding="Latin-1") as file:  
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
                    if cobrador == "6":
                        if codigo == "C":
                            if nome_dev == nome:
                                global formando
                                formando = form(obs_dev)
                                forms = a_form(formando)
                                loko = num_acd(obs_dev, forms)
                                return loko

def get_excel(table):
    directory = filedialog.askdirectory()
    pg_lol = []
    normal_lol = []
    columns = ['Nome', 'Data', 'Prazo', 'Valor', 'Pago', 'Obs']

    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, valor, cob, pago, obs FROM {table} ORDER BY pago DESC, data")
    records = c.fetchall()
    for record in records:
                important_shit = {'nome': [], 
                    'data': [],
                    'prazo': [],
                    'valor': [],
                    'pago': [],
                    'obs': [],
                    'style':[]}
                    
                pg_shit = {'nome': [],
                    'data': [],
                    'prazo': [],
                    'valor': [],
                    'pago': [],
                    'obs': [],
                    'style':[]}
                    
                if record[6] == 1:
                    #acordo pago 
                        pg_shit['nome'].append(record[1])
                        pg_shit['data'].append(record[2])
                        pg_shit['prazo'].append(record[3])
                        pg_shit['valor'].append(record[4])
                        pg_shit['pago'].append(1)
                        pg_shit['obs'].append(record[7])
                        pg_shit['style'].append(1)
                        pg_lol.append(pg_shit)
                else:
                        important_shit['nome'].append(record[1])
                        important_shit['data'].append(record[2])
                        important_shit['prazo'].append(record[3])
                        important_shit['valor'].append(record[4])
                        important_shit['pago'].append(record[6])
                        important_shit['obs'].append(record[7])
                        important_shit['style'].append(2)
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

#Unmade deals page and function especifics.
def open_list(mes): #unmade acds page
        unmade = Toplevel()
        screen_width = unmade.winfo_screenwidth()
        screen_height = unmade.winfo_screenheight()

        global my_tree_unmade
        tree_frame_unmade = Frame(unmade)
        tree_frame_unmade.pack(ipady=180, ipadx=350)

        #Scrollbar
        tree_scroll_un = Scrollbar(tree_frame_unmade)
        tree_scroll_un.pack(side=RIGHT, fill=Y)

        my_tree_unmade = ttk.Treeview(tree_frame_unmade, yscrollcommand=tree_scroll_un.set, selectmode="extended", height=40) #25
        my_tree_unmade.pack()
        tree_scroll_un.config(command=my_tree.yview)
        my_tree_unmade['columns'] = ("rowid", "nome", "data", "valor", "obs")

        # Format columns
        my_tree_unmade.column("#0", width=0, stretch=NO)
        my_tree_unmade.column("rowid", width=0, stretch=NO)
        my_tree_unmade.column("nome", anchor=W, width=300)
        my_tree_unmade.column("data", anchor=W, width=85)
        my_tree_unmade.column("valor", anchor=CENTER, width=100)
        my_tree_unmade.column("obs", anchor=E, width=840)

        # Create Headings
        my_tree_unmade.heading("#0", text="", anchor=W)
        my_tree_unmade.heading("rowid", text="", anchor=W)
        my_tree_unmade.heading("nome", text="nome", anchor=W)
        my_tree_unmade.heading("data", text="data", anchor=W)
        my_tree_unmade.heading("valor", text="valor", anchor=CENTER)
        my_tree_unmade.heading("obs", text="obs", anchor=CENTER)

        global rowid_entry_un, n_entry_un, obs_entry_un
        data_frame_un = LabelFrame(unmade, text="Record")
        data_frame_un.place(x=100,y=850,height=60,width=1650)

        rowid_entry_un = Entry(data_frame_un)

        n_label_un = Label(data_frame_un, text="Nome")
        n_label_un.grid(row=0, column=0)
        n_entry_un = Entry(data_frame_un)
        n_entry_un.grid(row=0, column=1, ipadx=100, padx=5)

        obs_label_un = Label(data_frame_un, text="OBS")
        obs_label_un.grid(row=0, column=2)
        obs_entry_un = Entry(data_frame_un)
        obs_entry_un.grid(row=0, column=3, ipadx=350, padx=5)

        update_btn = Button(data_frame_un, text="Aplicar mudança", command=lambda: update_table_un(mes),anchor= CENTER)
        update_btn.grid(row=0, column=4, padx=10)

        del_un_btn = Button(data_frame_un, text="Delete", command=lambda: del_no_sort_un(mes),anchor= CENTER)
        del_un_btn.grid(row=0, column=5)

        update_btn = Button(data_frame_un, text="Get Excel", command=lambda: get_excel_un(mes),anchor= CENTER)
        update_btn.grid(row=0, column=6, padx=10)

        my_tree_unmade.bind("<ButtonRelease-1>", select_record_un)
        query_db_unmade(mes)
        pass

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

        conn = sqlite3.connect('agenda.db')
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

# *****add month page *****:

def add_month(): #this is the page
    global inf
    inf = Toplevel()
    inf.title("Adicionar arquivo")
    inf.geometry("650x400")
    inf.minsize(650, 400)
    inf.maxsize(1200, 800)

    open_btn = Button(inf, text="Selecione arquivo a adicionar", command=select_file, padx=3, pady=2, anchor= S)
    open_btn.pack()
    frame = Frame(inf, highlightbackground="black", highlightthickness=2.)
    frame.pack()

    global tree
    tree = ttk.Treeview(frame)

    global options_M
    options_M = [
    "Januery", 
    "Fevereiro", 
    "Março", 
    "Abril", 
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"]
    var = tkinter.StringVar(inf)
    drop = OptionMenu(inf, var, *options_M, command=callback)
    drop.pack()

    var.set('Select email')
    comit_month = Button(inf, text="Add month", command=lambda:adding_month(selec, filename), padx=3, pady=2)
    comit_month.pack(pady=5)

    global label
    label = Label(inf, text='')
    label.pack(pady=0, padx=0)
   
def select_file():
    global filename
    filename = filedialog.askopenfilename(title="Open a File", filetype=(("All Files", "*.*"), ("xlrd files", ".*xlrd"), ("xlxs files", ".*xlsx")))
    if filename:
            try:
                filename = r"{}".format(filename)
                global df
                df = pd.read_excel(filename, dtype=str)
            except ValueError:
                label.config(text="File could not be opened", pady=20, ipady=10)
            except FileNotFoundError:
                label.config(text="File Not Found",pady=20, ipady=10)
    clear_treeview()

    tree["column"] = list(df.columns)
    tree["show"] = "headings"

    for col in tree["column"]:
        tree.heading(col, text=col)

    df_rows = (df.to_numpy().tolist())
    for row in df_rows:
        tree.insert("", "end", values=row)
    tree.pack()

def clear_treeview():
    tree.delete(*tree.get_children())

def callback(selection):
    global selec
    selec = selection 

def adding_month(selection, filename):
    inf.destroy()
    conn = sqlite3.connect('agenda.db')
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

#--------Functions for database-----------------------------------------------------------------------------------------------------------------
def conn_db(command):
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute(f"{command}")
    
    conn.commit()
    conn.close()

def query_database(table):
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        c.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, prazo, valor, cob, pago, obs FROM {table} ORDER BY pago DESC, data")
        records = c.fetchall()
        for record in records:
                current_data = datetime.datetime.strptime(record[2], "%d/%m/%Y")
                weekcheck = datetime.datetime.strptime(record[2], "%d/%m/%Y").strftime("%A")
                if weekcheck == "Saturday":
                      tree_data_ = current_data + datetime.timedelta(days=2)
                      tree_data = tree_data_.strftime("%d/%m/%Y")
                elif weekcheck == "Sunday":
                      tree_data_ = current_data + datetime.timedelta(days=1)
                      tree_data = tree_data_.strftime("%d/%m/%Y")
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
        table = table + "_unmade"
        conn = sqlite3.connect('agenda.db')
        c_unmade = conn.cursor()
        c_unmade.execute(f"SELECT rowid, nome, STRFTIME('%d/%m/%Y', data) as formated_data, valor, obs FROM {table} ORDER BY data")
        records = c_unmade.fetchall()
        for record in records:
                currency_string_un = "R${:,.2f}".format(record[3])
                my_tree_unmade.insert(parent='', index='end', text='', values=(record[0], record[1], record[2], currency_string_un, record[4]))
        conn.commit()
        conn.close()

def create_table(option):
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

def add_info(list, table, row):
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    for record in list:
        c.execute(f"INSERT INTO {table} VALUES (:{row})", 
            {
            row : record,
            })
    query_database(table)
    conn.commit()
    conn.close()
#---------------------------------------------------------------------------------------------------------------------------------------------
mainloop()

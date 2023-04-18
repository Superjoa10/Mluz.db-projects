import pyautogui as gui, datetime, time, csv
import re
from command_line_scripts.gett_gender import get_gender, num_acd, form, a_form, get_time, who_acd
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
#acertar **acordos.csv** antes de rodar

def cobrar(nome, dia_atual, numero_, navegador):
    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)
    Horario = get_time()
    numero = "55" + numero_
    mensagem = (f"{Horario} {pronome[0]}, conforme acordo nesse dia {dia_atual}, aguardo pagamento")  

    texto = urllib.parse.quote(mensagem)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)
    navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
    time.sleep(5) 

def cob_prazo(nome, dia_atual, numero_, navegador):
    nom = nome.split(" ")
    primeir_nome = nom[0].capitalize()
    pronom = get_gender(primeir_nome)
    Horari = get_time()
    numero = "55" + numero_
    mensage = (f"{Horari} {pronom[0]}, conforme prazo nesse dia {dia_atual}, aguardo pagamento")   
 
    text = urllib.parse.quote(mensage)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={text}"
    navegador.get(link)
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)
    navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
    time.sleep(5) 

def comp(nome):
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
   
def main(navegador):
        with open("acordos.csv", "r", encoding="Latin-1") as file:  
            csv_reader = csv.reader(file, delimiter=';')  
            line_count = 0 
            acordos_cob = []
            acords_n_cob = []
            for lol in csv_reader:
                if line_count == 0:  
                    line_count += 1   
                else:
                    global nome
                    nome = lol[0]
                    data_acd = lol[1]
                    prazo = lol[2] 
                    cobr = lol[3]
                    obs = lol[4]
                    dia_atual = datetime.datetime.now().strftime("%d/%m/20%y")  
                    if dia_atual == data_acd:
                        if cobr == "sim":
                            numero = comp(nome)  
                            if numero == None:
                                        if obs == "0":
                                            obs == None 
                                        print("----------------------------------------------------------------------------------")
                                        print(f"no num on case {nome}")
                                        gui.alert(text=f'''O caso {nome} não possui numero!
                                        Obs: {obs}''', title='Aviso', button='Pass')
                                        acords_n_cob.append(nome)
                                
                            else:
                                if forms == True:
                                    if who_acd(obs_dev) == True:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}, porem possui formando")
                                        cobrar(nome, dia_atual, numero, navegador)
                                        acordos_cob.append(nome)
                                        print(f"{nome} cobrado(a)")  
                                    elif who_acd(obs_dev) == False:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o formando: {formando} {numero}")
                                        cobrar(formando, dia_atual, numero, navegador)
                                        acordos_cob.append(formando)  
                                        print(f"{nome} cobrado(a)") 
                                else:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}")
                                        cobrar(nome, dia_atual, numero, navegador)
                                        acordos_cob.append(nome)  
                                        print(f"{nome} cobrado(a)")  
                        elif cobr == "nao":
                                        if obs == "0":
                                            obs == None
                                        print("----------------------------------------------------------------------------------")  
                                        gui.alert(text=f'''O caso {nome} esta com cobrança automatica desligada!
                                        Obs: {obs}''', title='Aviso', button='OK')
                                        acords_n_cob.append(nome)

                    if dia_atual == prazo: 
                        if cobr == "sim":
                            numero = comp(nome) 
                            if numero == None:
                                        print("----------------------------------------------------------------------------------")
                                        gui.alert(text=f'''O caso {nome} não possui numero!
                                        Obs: {obs}''', title='Aviso', button='Pass')
                                        print(f"No num in case {nome}")
                                        acords_n_cob.append(nome)
                            else:
                                numero = comp(nome)  
                                if forms == True:
                                    if who_acd(obs_dev) == True:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}, porem possui formando")
                                        cob_prazo(nome, dia_atual, numero, navegador)
                                        acordos_cob.append(nome)   
                                        print(f"{nome} cobrado(a)")  
                                    elif who_acd(obs_dev) == False:
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o formando: {formando} {numero}")
                                        cob_prazo(formando, dia_atual, numero, navegador)
                                        acordos_cob.append(formando)   
                                        print(f"{nome} cobrado(a)") 
                                else:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}")
                                        cob_prazo(nome, dia_atual, numero, navegador)
                                        acordos_cob.append(nome) 
                                        print(f"{nome} cobrado(a)")

                        elif cobr == "nao":
                                        if obs == "0":
                                            obs == None
                                        print("----------------------------------------------------------------------------------")  
                                        gui.alert(text=f'''O caso {nome} esta com cobrança automatica desligada!
                                        Obs: {obs}''', title='Aviso', button='OK')
                                        acords_n_cob.append(nome)

                    line_count += 1  
            print(f'''hoje é dia {dia_atual}. 
Acordos ativos: {line_count - 1}. 
acordos cobrados hoje: {len(acordos_cob)}
lista acordos cob. automatica desligada: {acords_n_cob}''')
            gui.alert(text=f'''Todos acordos possiveis cobrados do dia {dia_atual}''', title='Done', button='OK')

if __name__ == "__main__":
    navegador = webdriver.Chrome()
    navegador.get("https://web.whatsapp.com/")

    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)
    main(navegador)

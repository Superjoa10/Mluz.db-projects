import re
import time
import csv
import sys
import os
import pyautogui as gui
import gender_guesser.detector as gender
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


import time
import urllib
import datetime

#Automation functions -----------
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
        time.sleep(2)
    time.sleep(3)
    try:
        send = navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]')
        send.click()
    except NoSuchElementException:
        return False
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
            time.sleep(2)
    time.sleep(3)
    try:
        send = navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]')
        send.click()
    except NoSuchElementException:
        return False
    time.sleep(5) 
    
def cobrar_selected(nome, numero_, navegador, response):
    nom = nome.split(" ")
    primeir_nome = nom[0].capitalize()
    pronom = get_gender(primeir_nome)
    Horari = get_time()
    numero = "55" + numero_
    if response == 1:
        mensage = (f"{Horari} {pronom[0]}, conforme acordo, aguardo pagamento")
    elif response == 2:
        mensage = (f"{Horari} {pronom[0]}, conforme prazo, aguardo pagamento")
    text = urllib.parse.quote(mensage)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={text}"
    navegador.get(link)
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
            time.sleep(2)
    time.sleep(3)
    try:
        send = navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]')
        send.click()
    except NoSuchElementException:
        return False
    time.sleep(5)

def cobrar_posiçao(nome, numero_, navegador):
    nom = nome.split(" ")
    primeir_nome = nom[0].capitalize()
    pronom = get_gender(primeir_nome)
    Horari = get_time()
    numero = "55" + numero_
    mensage = (f"{Horari} {pronom[0]}, alguma posição?")   
 
    text = urllib.parse.quote(mensage)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={text}"
    navegador.get(link)
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
            time.sleep(2)
    time.sleep(3)
    try:
        send = navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]')
        send.click()
    except NoSuchElementException:
        return False
    time.sleep(5) 

#Basic info funcions -----
def get_gender(prompt):
    L = gender.Detector()
    result = (L.get_gender(prompt))
    if result  == "male":
        return["senhor", "do", "o"]
    elif result == "mostly male":
        return["senhor", "do", "o"]
    elif result == "female":
        return["senhora", "da", "a"]
    elif result == "mostly female":
        return["senhora", "da", "a"]
    elif result == "andy":
        while True:
            real_result = gui.prompt(f"""Erro ao detectar pronome! especifique o mesmo. Nome {prompt}:
            Como gostaria de ser referido? Senhor ou senhora? """)
            if real_result == "senhor":
                return ["senhor", "do", "o"]
            elif real_result == "senhora":
                return ["senhora", "da", "a"]
            else:
                print("Please Write a valid command!")
    else:
        while True:
            real_result = gui.prompt(f"""Erro ao detectar pronome! especifique o mesmo. Nome {prompt}:
            Como gostaria de ser referido? Senhor ou senhora? """)
            if real_result == "senhor":
                return ["senhor", "do", "o"]
            elif real_result == "senhora":
                return ["senhora", "da", "a"]

def get_time():
    currentTime  = int(time.strftime('%H')) 
    if currentTime < 12 :
        return('Bom dia')
    if currentTime >= 12 :
        return('Boa tarde')
    if currentTime > 6 :
        return('Boa noite')

def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Regex func -------------
def form(obs):
    form = re.compile(r"(Formando:|formando:|FORMANDO:|Formando|formando|FORMANDO|Formanda:|formanda:|FORMANDA:|Formanda|formanda|FORMANDA) (o mesmo|O MESMO|O Mesmo|o Mesmo|O mesmo|[aA-zZ*\_\-\s]+\n)")
    matches = form.findall(obs)
    #match is a list of ["formando" , "O mesmo"]
    for match in matches:
        return match[1]

def a_form(formando):
    if formando == "o mesmo":
        return False
    elif formando == "O MESMO":
        return False
    elif formando == "O Mesmo":
        return False
    elif formando == "o Mesmo":
        return False
    elif formando == "O mesmo":
        return False
    elif formando == None:
        return False
    else: 
        return True

def num_acd(obs,forms):
    if forms == True:
        n_form = re.compile(r'(N_form:|n_Form:|N_Form:|n_form:|N_FORM:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
        n_dev = re.compile(r'(N_dev:|n_Dev:|N_Dev:|n_dev:|N_DEV:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
        whom_acd = who_acd(obs)
        #true is devedor
        if whom_acd == True:
            matches_dev = n_dev.findall(obs)
            for match_dev in matches_dev:
                global num_dev
                num_dev = match_dev[1]
                return num_dev
            
        if whom_acd == False:
            matches_form = n_form.findall(obs)
            for match_form in matches_form:
                global num_forms
                num_forms = match_form[1]
                return num_forms

    elif forms == False:
        n_unico = re.compile(r"(N:|n:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})")
        matches_Dev = n_unico.findall(obs)
        for match in matches_Dev:
            global num
            num = match[1]
            return num

def who_acd(obs_dev):
        acd_dev = re.compile(r"(acd_dev|Acd_Dev|acd_Dev|Acd_dev)\n")
        acd_form = re.compile(r"(acd_form|Acd_Form|acd_Form|Acd_form)\n")
        matches_acd = bool(acd_dev.search(obs_dev))
        matches_acd_form = bool(acd_form.search(obs_dev))
        if matches_acd == True:
            return True
        elif matches_acd_form == True:
            return False
        else:
            return "WOW whats fucking up now"

def real_logic(shit):
    shit = bool(re.search("R$", shit))
    if shit == True:
        return True
    elif shit == False:
        return False

#tests get_gender, and selenium whatsapp message
if __name__ == "__main__":
    navegador = webdriver.Chrome()
    navegador.get("https://web.whatsapp.com/")

    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)

    dia_atual = datetime.datetime.now().strftime("%d/%m/20%y") 
    teste = ["João", "5511954599589"]
    pronome = get_gender(teste[0])
    Horario = get_time()
    numero = teste[1]
    mensagem = (f"{Horario} {pronome[0]}, nesse dia {dia_atual}, {pronome[2]} {pronome[0]} esta testando as funções de mensagem automatica seu otario")  
    texto = urllib.parse.quote(mensagem)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)
    try:
        navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
    except NoSuchElementException:
        print("Bru u some sort of gay")
    time.sleep(5) 
    
import re
import time
import pyautogui as gui
import gender_guesser.detector as gender
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import urllib
import datetime
import smtplib
import ssl
from email.message import EmailMessage

#Automation functions --------------------------
def cobrar_dev(nome, numero_, navegador, setor):
    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)
    Horario = get_time()
    numero = "55" + numero_

    #mensage defenition:
    if setor.casefold() == "D".casefold():
        mensagem = (f"{Horario} {pronome[0]}, é o Vitor referente a seu debito com a Millenium formaturas. Estamos com condições especiais de fim de ano para quitação do seu Debito. *Protesto não caduca!*, caso queira limpar seu nome e pagar *SEM JUROS* me retorne para que eu passe as condições.")

    if setor.casefold() == "B".casefold():
        #how to know if doc is cheque or not
        mensagem = (f"{Horario} {pronome[0]}, é o Vitor referente a seu debito com a Millenium formaturas. Estamos com condições especiais de fim de ano para quitação do seu Debito. Caso queira limpar seu nome e pagar *SEM JUROS* me retorne para que eu passe as condições.")
        
    else:
        mensagem = (f"{Horario} {pronome[0]}, é o Vitor referente a seu debito com a Millenium formaturas. Estamos com condições especiais de fim de ano para quitação do seu Debito. Caso queira limpar seu nome e pagar *SEM JUROS* me retorne para que eu passe as condições.")

    texto = urllib.parse.quote(mensagem)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)
    try:
        navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]').click
    except NoSuchElementException:
        pass
    time.sleep(5)

def cobrar_form(nome, dev, numero_, navegador, setor):
    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)
    nime_dev = dev.split(" ")
    primeiro_nome_dev = nime_dev[0].capitalize()
    pronome_dev = get_gender(primeiro_nome_dev)
    Horario = get_time()
    numero = "55" + numero_

    #mensage defenition:
    if setor == "D".casefold():
        mensagem = (f"{Horario} {pronome[0]}, é o Vitor referente a seu debito com a Millenium formaturas no nome {pronome_dev[1]} {dev}. Estamos com condições especiais de fim de ano para quitação do seu Debito. *Protesto não caduca!*, caso queira limpar o nome {pronome_dev[1]} {nime_dev} e pagar *SEM JUROS* me retorne para que eu passe as condições.")
    if setor == "B".casefold():
        #how to know if doc is cheque or not
        mensagem = (f"{Horario} {pronome[0]}, é o Vitor referente a seu debito com a Millenium formaturas no nome {pronome_dev[1]} {dev}. Estamos com condições especiais de fim de ano para quitação do seu Debito. Caso queira limpar o nome {pronome_dev[1]} {nime_dev}, e pagar *SEM JUROS* me retorne para que eu passe as condições.")
    else:
        mensagem = (f"{Horario} {pronome[0]}, é o Vitor referente a seu debito com a Millenium formaturas no nome {pronome_dev[1]} {dev}. Estamos com condições especiais de fim de ano para quitação do seu Debito. Caso queira limpar o nome {pronome_dev[1]} {nime_dev} e pagar *SEM JUROS* me retorne para que eu passe as condições.")

    texto = urllib.parse.quote(mensagem)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)
    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)
    try:
        navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]').click
    except NoSuchElementException:
        pass
    time.sleep(5)

def send_email_dev(nome, setor, email_receiver):
    Horario = get_time()
    password = 'saajuaejqxvusgiy'
    email_sender = 'contato.mluzassessoria@gmail.com'
    subject = 'Debito'

    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)

    if setor.casefold() == "D".casefold():
        body = F"""#PLACE CABEÇALHO
    {Horario} {pronome[0]} {primeiro_nome}, meu nome é Vitor falo em nome de Millenium formaturas, referente a seu album de formatura em aberto.
    Seu nome esta negativado no SPC, protestado em cartório e devido a dificuldade de negociação ah Millenium tem interesse em seguir com ação monitória de cobrança contra {pronome[2]} {pronome[0]}. Estamos com condições especiais *SEM JUROS* para quitação.
    Venho por meio desse contato perguntar seu interesse em negociar para limpar o seu nome no SPC, retirar protesto do cartório e evitar futura ação. Caso haja me retorne no numero de Whatsapp +55(11)94875-1769, ou no fixo **COLOCAR TELL FISICO ou retorne o contato nesse Email.

    Att. Vitor
    """
        
    if setor.casefold() == "B".casefold():
        body = F"""#PLACE CABEÇALHO
    {Horario} {pronome[0]} {primeiro_nome}, meu nome é Vitor falo em nome de Millenium formaturas, referente a seu album de formatura em aberto.
    Seu nome esta negativado no SPC e devido a dificuldade de negociação ah Millenium tem interesse em seguir com ação monitória de cobrança contra {pronome[2]} {pronome[0]}. Estamos com condições especiais *SEM JUROS* para quitação.
    Venho por meio desse contato perguntar seu interesse em negociar para limpar o seu nome e evitar futura ação. Caso haja me retorne no numero de Whatsapp +55(11)94875-1769, ou no fixo **COLOCAR TELL FISICO ou retorne o contato nesse Email.

    Att. Vitor
    """
        
    else:
        body = F"""#PLACE CABEÇALHO
    {Horario} {pronome[0]} {primeiro_nome}, meu nome é Vitor falo em nome de Millenium formaturas, referente a seu album de formatura em aberto.
    Seu nome esta negativado no SPC e devido a dificuldade de negociação ah Millenium tem interesse em seguir com ação monitória de cobrança contra {pronome[2]} {pronome[0]}. Estamos com condições especiais *SEM JUROS* para quitação.
    Venho por meio desse contato perguntar seu interesse em negociar para limpar o seu nome e evitar futura ação. Caso haja me retorne no numero de Whatsapp +55(11)94875-1769, ou no fixo **COLOCAR TELL FISICO ou retorne o contato nesse Email.

    Att. Vitor
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            time.sleep(5)

def send_email_form(nome, dev, setor, email_receiver):
    Horario = get_time()
    password = 'saajuaejqxvusgiy'
    email_sender = 'contato.mluzassessoria@gmail.com'
    subject = 'Debito'

    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)

    nime_dev = dev.split(" ")
    primeiro_nome_dev = nime_dev[0].capitalize()
    pronome_dev = get_gender(primeiro_nome_dev)

    if setor.casefold() == "D".casefold():
        body = F"""#PLACE CABEÇALHO
    {Horario} {pronome[0]} {primeiro_nome}, meu nome é Vitor falo em nome de Millenium formaturas, referente a seu album de formatura no nome {pronome_dev[1]} {pronome_dev[0]} {primeiro_nome_dev}. Nome {pronome_dev[1]} mesm{pronome_dev[2]}, esta negativado no Spc, protestado em cartório e devido a dificuldade de negociação ah Millenium tem interesse em seguir com ação monitória de cobrança contra {pronome_dev[2]} {primeiro_nome_dev}. Estamos com condições especiais *SEM JUROS* para quitação.
    Venho por meio desse contato perguntar seu interesse em negociar para limpar o nome {pronome_dev[1]} mesm{pronome_dev[2]}, retirar do protesto e evitar futura ação. Caso haja me retorne no numero de Whatsapp +55(11)94875-1769, ou no fixo **COLOCAR TELL FISICO ou retorne o contato nesse Email.

    Att. Vitor
    """
        
    if setor.casefold() == "B".casefold():
        body = F"""#PLACE CABEÇALHO
    {Horario} {pronome[0]} {primeiro_nome}, meu nome é Vitor falo em nome de Millenium formaturas, referente a seu album de formatura no nome {pronome_dev[1]} {pronome_dev[0]} {primeiro_nome_dev}. Nome {pronome_dev[1]} mesm{pronome_dev[2]}, esta negativado no SPC e devido a dificuldade de negociação ah Millenium tem interesse em seguir com ação monitória de cobrança contra {pronome_dev[2]} {primeiro_nome_dev}. Estamos com condições especiais *SEM JUROS* para quitação.
    Venho por meio desse contato perguntar seu interesse em negociar para limpar o nome {pronome_dev[1]} mesm{pronome_dev[2]} e evitar futura ação. Caso haja me retorne no numero de Whatsapp +55(11)94875-1769, ou no fixo **COLOCAR TELL FISICO ou retorne o contato nesse Email.

    Att. Vitor
    """
        
    else:
        body = F"""#PLACE CABEÇALHO
    {Horario} {pronome[0]} {primeiro_nome}, meu nome é Vitor falo em nome de Millenium formaturas, referente a seu album de formatura no nome {pronome_dev[1]} {pronome_dev[0]} {primeiro_nome_dev}. Nome {pronome_dev[1]} mesm{pronome_dev[2]}, esta negativado no SPC e devido a dificuldade de negociação ah Millenium tem interesse em seguir com ação monitória de cobrança contra {pronome_dev[2]} {primeiro_nome_dev}. Estamos com condições especiais *SEM JUROS* para quitação.
    Venho por meio desse contato perguntar seu interesse em negociar para limpar o nome {pronome_dev[1]} mesm{pronome_dev[2]} e evitar futura ação. Caso haja me retorne no numero de Whatsapp +55(11)94875-1769, ou no fixo **COLOCAR TELL FISICO ou retorne o contato nesse Email.

    Att. Vitor
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            time.sleep(5)
    
def get_contact(obs, forms):
        if forms == True:
            n_dev = re.compile(r'(N_dev:|n_Dev:|N_Dev:|n_dev:|N_DEV:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
            email_dev = re.compile(r'(Email_dev:|email_Dev:|EMAIL_Dev:|email_dev:|EMAIL_DEV:) (\S+@\S+\.\S+)')
            n_form = re.compile(r'(N_form:|n_Form:|N_Form:|n_form:|N_FORM:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
            email_form = re.compile(r'(Email_form:|email_Form:|EMAIL_Form:|email_form:|EMAIL_FORM:) (\S+@\S+\.\S+)')
            
            matches_dev_ = bool(n_dev.search(obs))
            if matches_dev_ == True:
                matches_dev = n_dev.findall(obs)
                for match_dev in matches_dev:
                    num_dev = match_dev[1]
            else:
                num_dev = None

            matches_dev_email = bool(email_dev.search(obs))
            if matches_dev_email == True:
                matches_dev_email = email_dev.findall(obs)
                for match_dev_email in matches_dev_email:
                    email_dev_ = match_dev_email[1]
            else:
                email_dev_ = None

            matches_form_ = bool(n_form.search(obs))
            if matches_form_ == True:
                    global matches_form
                    matches_form = n_form.findall(obs)
                    for match_form in matches_form:
                        num_form = match_form[1]
            else:
                    num_form = None

            matches_form_email = bool(email_form.search(obs))
            if matches_form_email == True:
                matches_form_email_ = email_form.findall(obs)
                for match_form_email in matches_form_email_:
                    email_form_ = match_form_email[1]
            else:
                email_form_ = None

            return [num_dev, num_form, email_dev_, email_form_]

        elif forms == False:
            n_unico = re.compile(r"(N:|n:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})")
            email_unico = re.compile(r'(Email:|email:|EMAIL:) (\S+@\S+\.\S+)')

            matches = bool(n_unico.search(obs))
            if matches == True:
                matches_Dev = n_unico.findall(obs)
                for match in matches_Dev:
                    num = match[1]
            else:
                num = None

            matches_email = bool(email_unico.search(obs))
            if matches_email == True:
                matches__email = email_unico.findall(obs)
                for match_dev_email in matches__email:
                    email__ = match_dev_email[1]
            else:
                email__ = None
            return [num, email__]

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

def num_acd(obs,forms):
    if forms == True:
        n_form = re.compile(r'(N_form:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
        n_dev = re.compile(r'(N_dev:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
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
        #global numbers_geral
        #numbers_geral = [num_dev, num_forms]
        #can be called
    elif forms == False:
        n_unico = re.compile(r"(N:|n:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})")
        matches_Dev = n_unico.findall(obs)
        for match in matches_Dev:
            global num
            num = match[1]
            return num

def dev_num(obs,forms):
    global num_forms
    global num_dev
    if forms == True:
        n_form = re.compile(r'(N_form:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
        n_dev = re.compile(r'(N_dev:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})')
        matches_dev = n_dev.findall(obs)
        for match_dev in matches_dev:
            if not match:
                print (" Sem num devedor!!")
                num_dev = None
                continue
            print(f"numero dev {match_dev[1]}")
            num_dev = match_dev[1]  
        matches_form = n_form.findall(obs)
        for match_form in matches_form:
            if not match:
                print (" Sem num formando")
                num_forms = None
                continue
            print(f"n formando {match_form[1]}")
            num_forms = match_form[1]
        numbers_geral = [num_dev, num_forms]
        return numbers_geral
        #can be called
    elif forms == False:
        n_unico = re.compile(r"(N:|n:) ((?:\+?\d{2,3}[ ]{0,4})?(?:(?:\(0?\d{2}\)|0?\d{2})[ ]{0,4})?(?:9[ .-]?)?\d{4}[ .-]?\d{4})")
        matches_Dev = n_unico.findall(obs)
        for match in matches_Dev:
            if not match:
                print("U GAY AS FUCK")
                break
            print(f"dev unico :{match}")
            global num
            num = match_form[1]
            return num


#Basic info funcions ---------------------------
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
        real_result = gui.prompt(f"""Erro ao detectar pronome! especifique o mesmo. Nome {prompt}:
        Como gostaria de ser referido? Senhor ou senhora? """)
        if real_result == "senhor":
            return ["senhor", "do", "o"]
        elif real_result == "senhora":
            return ["senhora", "da", "a"]
    else:
        gui.alert(text='Erro ao detectar pronome! Retorne ao console e especifique o mesmo.', title='Erro!!', button='OK')
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

#Regex func ------------------------------------
def form(obs):
    form = re.compile(r"(Formando:|formando:|FORMANDO:|Formando|formando|FORMANDO) (o mesmo|O MESMO|O Mesmo|o Mesmo|O mesmo|[aA-zZ*\_\-\s]+\n)")
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

#tests get_gender, and selenium whatsapp message
if __name__ == "__main__":
    navegador = webdriver.Chrome()
    navegador.get("https://web.whatsapp.com/")

    while len(navegador.find_elements(By.ID, 'side')) < 1: 
        time.sleep(1)

    dia_atual = datetime.datetime.now().strftime("%d/%m/20%y") 
    teste = ["João", "954599589"]
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
        navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]').click
    except NoSuchElementException:
        pass
    time.sleep(5)    

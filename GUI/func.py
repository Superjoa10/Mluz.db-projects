import re
import time
import pyautogui as gui
import gender_guesser.detector as gender

#GUI functions -----------
def cobrar(nome, dia_atual, numero):
    print(f"Lolllllllll {nome} is loko on the {numero}")
    """
    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)
    Horario = get_time()
    mensagem = (f"{Horario} {pronome[0]}, conforme acordo nesse dia {dia_atual}, aguardo pagamento")   
    time.sleep(5) 

    gui.leftClick(x=141, y=141)
    gui.press('backspace', presses = 15)
    gui.press('delete', presses = 15)
    gui.leftClick(x=141, y=141)
    gui.PAUSE = 2
    gui.write(numero)
    gui.press('enter')
    gui.leftClick(x=755, y=980)
    gui.PAUSE = 2
    gui.write(mensagem)
    gui.press('enter')
    """

def cob_prazo(nome, dia_atual, numero):
    print(f"Lolllllllll {nome} is loko on the {numero}")
    '''
    nom = nome.split(" ")
    primeir_nome = nom[0].capitalize()
    pronom = get_gender(primeir_nome)
    Horari = get_time()
    mensage = (f"{Horari} {pronom[0]}, conforme prazo nesse dia {dia_atual}, aguardo pagamento")   
    time.sleep(5) 

    gui.leftClick(x=141, y=141)
    gui.press('backspace', presses = 15)
    gui.press('delete', presses = 15)
    gui.leftClick(x=141, y=141)
    gui.PAUSE = 2
    gui.write(numero)
    gui.press('enter')
    gui.leftClick(x=755, y=980)
    gui.PAUSE = 2
    gui.write(mensage)
    gui.press('enter')
    '''

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
    if currentTime > 12 :
        return('Boa tarde')
    if currentTime > 6 :
        return('Boa noite')

#Regex func -------------
def form(obs):
    form = re.compile(r"(Formando:|formando:|FORMANDO:) (o mesmo|O MESMO|O Mesmo|o Mesmo|O mesmo|[aA-zZ*\_\-\s]+\n)")
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

if __name__ == "__main__":
    pass
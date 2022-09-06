import gender_guesser.detector as gender, pyautogui as gui, re, time

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

def who_acd(obs):
        acd_dev = re.compile(r"(acd_dev|Acd_Dev|acd_Dev|Acd_dev)")
        acd_form = re.compile(r"(acd_form|Acd_Form|acd_Form|Acd_form)")
        matches_acd = acd_dev.findall(obs)
        for match_acd in matches_acd:
                    if  not match_acd:
                        matches_acd_form = acd_form.findall(obs)
                        for match_acd_forms in matches_acd_form:
                            if not match_acd_forms:
                                Raise: TypeError("Lol sem def de acordo")
                            return False
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
                if not match:
                    print (" Sem num devedor!!")
                    break
                print(f"numero dev {match_dev[1]}")
                global num_dev
                num_dev = match_dev[1]
                return num_dev
            
        if whom_acd == False:
            matches_form = n_form.findall(obs)
            for match_form in matches_form:
                if not match:
                    print (" Sem num formando")
                    break
                print(f"n formando {match_form[1]}")
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
            if not match:
                print("U GAY AS FUCK")
                break
            print(f"dev unico :{match}")
            global num
            num = match_form[1]
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

def get_time():
    currentTime  = int(time.strftime('%H')) 
    if currentTime < 12 :
        return('Bom dia')
    if currentTime > 12 :
        return('Boa tarde')
    if currentTime > 6 :
        return('Boa noite')

def main():
    pass
if __name__ == "__main__":
    main()

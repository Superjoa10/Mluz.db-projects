import pyautogui as gui, datetime, time, csv
from gett_gender import get_gender, num_acd, form, a_form, get_time, who_acd
#acertar **acordos.csv** antes de rodar
def cobrar(nome, dia_atual, numero):
    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)
    Horario = get_time()
    mensagem = (f"{Horario} {pronome[0]}, conforme acordo nesse dia {dia_atual}, aguardo pagamento")   
    time.sleep(5) 

    gui.leftClick(x=141, y=185)
    gui.press('delete', presses = 30)
    gui.press('backspace', presses = 30)
    gui.leftClick(x=141, y=185)
    gui.PAUSE = 2
    gui.write(numero)
    gui.press('enter')
    gui.leftClick(x=600, y=690)
    gui.press('delete', presses = 200)
    gui.press('backspace', presses = 200)
    gui.PAUSE = 4
    gui.write(mensagem)
    gui.PAUSE = 4
    gui.leftClick(x=600, y=690)
    gui.press('enter')

def cob_prazo(nome, dia_atual, numero):
    nom = nome.split(" ")
    primeir_nome = nom[0].capitalize()
    pronom = get_gender(primeir_nome)
    Horari = get_time()
    mensage = (f"{Horari} {pronom[0]}, conforme prazo nesse dia {dia_atual}, aguardo pagamento")   
    time.sleep(5) 

    gui.leftClick(x=141, y=185)
    gui.press('delete', presses = 30)
    gui.press('backspace', presses = 30)
    gui.leftClick(x=141, y=185)
    gui.PAUSE = 2
    gui.write(numero)
    gui.press('enter')
    gui.leftClick(x=600, y=690)
    gui.press('delete', presses = 200)
    gui.press('backspace', presses = 200)
    gui.PAUSE = 4
    gui.write(mensage)
    gui.PAUSE = 4
    gui.leftClick(x=600, y=690)
    gui.press('enter')

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
   
def main():
        with open("Acordos_9.csv", "r", encoding="Latin-1") as file:  
            csv_reader = csv.reader(file, delimiter=';')  
            line_count = 0  
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
                            # true is acd dev
                            if numero == None:
                                if obs == "0":
                                   obs == None 
                                print("----------------------------------------------------------------------------------")
                                print(f"no num on case {nome}")
                                gui.alert(text=f'''O caso {nome} não possui numero!
                                Obs: {obs}''', title='Aviso', button='Pass')
                                pass
                            else:
                                if forms == True:
                                    if who_acd(obs_dev) == True:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}, porem possui formando")
                                        cobrar(nome, dia_atual, numero)  
                                        print(f"{nome} cobrado(a)")  
                                    elif who_acd(obs_dev) == False:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o formando: {formando} {numero}")
                                        cobrar(formando, dia_atual, numero)  
                                        print(f"{nome} cobrado(a)") 
                                else:
                                    print("----------------------------------------------------------------------------------")
                                    print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}")
                                    cobrar(nome, dia_atual, numero)  
                                    print(f"{nome} cobrado(a)")  
                        elif cobr == "nao":
                            if obs == "0":
                                obs == None
                            print("----------------------------------------------------------------------------------")  
                            print(f"O caso {nome} esta com cobrança automatica desligada!")
                            gui.alert(text=f'''O caso {nome} esta com cobrança automatica desligada!
                            Obs: {obs}''', title='Aviso', button='OK')

                    if dia_atual == prazo: 
                        if cobr == "sim":
                            if numero == None:
                                print("----------------------------------------------------------------------------------")
                                gui.alert(text=f'''O caso {nome} não possui numero!
                                Obs: {obs}''', title='Aviso', button='Pass')
                                print(f"No num in case {nome}")
                                pass
                            else:
                                numero = comp(nome)  
                                if forms == True:
                                    if who_acd(obs_dev) == True:
                                        print("----------------------------------------------------------------------------------")
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}, porem possui formando")
                                        cob_prazo(nome, dia_atual, numero)  
                                        print(f"{nome} cobrado(a)")  
                                    elif who_acd(obs_dev) == False:
                                        print(f"Cobrando acordo do {nome}, acordo sendo com o formando: {formando} {numero}")
                                        cob_prazo(formando, dia_atual, numero)  
                                        print(f"{nome} cobrado(a)") 
                                else:
                                    print("----------------------------------------------------------------------------------")
                                    print(f"Cobrando acordo do {nome}, acordo sendo com o devedor {numero}")
                                    cob_prazo(nome, dia_atual, numero)  
                                    print(f"{nome} cobrado(a)")  
                    line_count += 1  
            print(f'hoje é dia {dia_atual}. Acordos ativos: {line_count - 1}. ')

if __name__ == "__main__":
    main()

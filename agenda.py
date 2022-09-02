import pyautogui as gui, datetime, time, csv
import gett_gender 
#acertar **acordos.csv** antes de rodar

def cobrar(nome, dia_atual, numero):
    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = gett_gender.get_gender(primeiro_nome)
    Horario = "Bom dia"
    mensagem = (f"{Horario} {pronome[0]}, conforme acordo nesse dia {dia_atual}, aguardo pagamento")   
    time.sleep(5) 
    print(Horario)

    gui.leftClick(x=141, y=141)
    gui.press('backspace', presses = 15)
    gui.press('delete', presses = 15)
    gui.PAUSE = 2
    gui.write(numero)
    gui.press('enter')
    gui.leftClick(x=755, y=980)
    gui.PAUSE = 2
    gui.write(mensagem)
    gui.press('enter')

def cob_prazo(nome, dia_atual, numero):
    nom = nome.split(" ")
    primeir_nome = nom[0].capitalize()
    pronom = gett_gender.get_gender(primeir_nome)
    Horari = "Bom dia"
    mensage = (f"{Horari} {pronom[0]}, conforme prazo nesse dia {dia_atual}, aguardo pagamento")   
    time.sleep(5) 

    gui.leftClick(x=141, y=141)
    gui.press('backspace', presses = 15)
    gui.press('delete', presses = 15)
    gui.PAUSE = 2
    gui.write(numero)
    gui.press('enter')
    gui.leftClick(x=755, y=980)
    gui.PAUSE = 2
    gui.write(mensage)
    gui.press('enter')

def get_horario():
    current_time = (datetime.datetime.now())
    timer = current_time.strftime("%H, %M, %S")
    lol = timer.split(", ")
    hour = lol[0]

    if hour == ["06","07","08","09","10","11"]:
        return "Bom dia"
    elif hour == ["12","13","14","15","16","17","18"]:
        return "Boa tarde"

def comp():
    with open("C:/Users/João/Desktop/Access/Devedor.csv", "r", encoding="Latin-1") as file:  
            csv_reader = csv.reader(file, delimiter=';')  
            line_count = 0 
            for devedor in csv_reader:
                if line_count == 0:  
                    line_count += 1   
                else:
                    nome_dev = devedor[1]
                    cobrador = devedor[24]
                    obs_dev = devedor[29]
                    if cobrador == "6":
                        if nome_dev == nome:
                            pass
                        #search insede obs for my number and formando acordo identifications

def main():
        with open("C:/Users/João/Desktop/automation_acd/acordos.csv", "r", encoding="Latin-1") as file:  
            csv_reader = csv.reader(file, delimiter=';')  
            line_count = 0  
            for lol in csv_reader:
                if line_count == 0:  
                    line_count += 1   
                else:
                    global formando 
                    global obs
                    formando = lol[1]  
                    cobrarr = lol[5]
                    obs = lol[6] 
                    data_acd = lol[2]
                    prazo = lol[3]  
                    numero = lol[4] 
                    dia_atual = datetime.datetime.now().strftime("%d/%m/%y")  
                    global nome
                    nome = lol[0]
                    #if formando == "null":
                    #    nome = lol[0]  
                    #else:
                    #    nome = lol[1] 

                    if dia_atual == data_acd: 
                        if cobrarr == "sim":
                            print(f"Cobrando caso {lol[0]}, Formando: {lol[1]}")
                            cobrar(nome, dia_atual, numero)  
                            print(f"{nome} cobrado(a)")  
                        elif cobrarr == "nao":  
                            gui.alert(text=f'''O caso {nome} esta com cobrança automatica desligada!
                            Obs: {obs}''', title='Aviso', button='OK')

                    if dia_atual == prazo:
                        if cobrarr == "sim":
                            print(f"Cobrando prazo para dia {lol[3]}, nome {lol[0]}, Formando: {lol[1]}")
                            cob_prazo(nome, dia_atual, numero) 
                        elif cobrarr == "nao":  
                            gui.alert(text=f'''O caso com prazo {nome} esta com cobrança automatica desligada!
                            Obs: {obs}''', title='Aviso', button='OK') 

                    line_count += 1  
            print(f'hoje é dia {dia_atual}. Acordos ativos: {line_count - 1}. ')

if __name__ == "__main__":
    main()

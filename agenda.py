import pyautogui as gui, datetime, time, csv
import re
from gett_gender import get_gender, dev_num, form, a_form, get_time, who_acd
#acertar **acordos.csv** antes de rodar
#acertar funçao GUI para adicionar "prazo" na agenda? "gostaria de adicionar prazo?" se ja possui prazo colocado mostrar junto
#caso cancelar segue como normal, caso adicionar, colocar um imput de data e adicionar, colocar detecção de erro de tipo de data
#move to an vertual env.

def cobrar(nome, dia_atual, numero):
    nime = nome.split(" ")
    primeiro_nome = nime[0].capitalize()
    pronome = get_gender(primeiro_nome)
    Horario = get_time()
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
    pronom = get_gender(primeir_nome)
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

def comp():
    with open("C:/Users/João/Desktop/Access/Devedor.csv", "r", encoding="Latin-1") as file:  
            csv_reader = csv.reader(file, delimiter=';')  
            line_count = 0 
            for devedor in csv_reader:
                if line_count == 0:  
                    line_count += 1   
                else:
                    global forms
                    nome_dev = devedor[1]
                    cobrador = devedor[24]
                    obs_dev = devedor[29]
                    if cobrador == "6":
                            formando = form(obs_dev)
                            print(formando)
                            forms = a_form(formando)
                            loko = dev_num(obs_dev, forms)
                            print(loko[0])
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
                    comp()
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

import pandas as pd
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import threading
import pygetwindow as gw
from Python_testes import cameraID, checkMAC, input_diag, gui   
import time
import subprocess
import os


stop = False


janela_estacao = "Estação"
janela_matricula = "Matricula"
janela_serial = "Serial"
search_input_window = True


def save_dados(linha, info, dados):
    csv_file = 'infos.csv'

    # Verifica se o arquivo CSV existe
    if not os.path.exists(csv_file):
        # Se o arquivo não existir, cria um DataFrame vazio
        df = pd.DataFrame(columns=['INFO', 'VALUE'])  # Colunas 'INFO' e 'VALUE'
    else:
        # Se o arquivo existir, carrega os dados em um DataFrame
        df = pd.read_csv(csv_file)

    # Verifica se a linha existe no DataFrame
    if linha >= len(df):
        # Se a linha não existir, adiciona uma nova linha com os valores padrão
        df.loc[linha] = [''] * df.shape[1]  # Preenche a nova linha com valores vazios

    # Atualiza o valor da linha e da coluna especificadas no DataFrame
    df.iloc[linha, 0] = f'{info}:{dados}'

    # Salva o DataFrame atualizado de volta no arquivo CSV, excluindo o índice
    df.to_csv(csv_file, index=False)


def end_fbt():
    cmd = 'taskkill /IM python.exe /F'
    subprocess.run(cmd, shell=True)


def top_input_window():
    global search_input_window
    print("Thread iniciada.")
    while search_input_window:
        janelas_do_processo = gw.getWindowsWithTitle(janela_matricula)
        time.sleep(0.1)
        if janelas_do_processo:
            print('input matricula encontrada')
            try:
                for janela in janelas_do_processo:
                    janela.activate()
                    break
            except:
                print('janela nao encontrada')
        janelas_do_processo2 = gw.getWindowsWithTitle(janela_estacao)
        time.sleep(0.1)
        if janelas_do_processo2:
            print('input estacao encontrada')
            try:
                for janela in janelas_do_processo2:
                    janela.activate()
                    break
            except:
                print('janela nao encontrada')
        janelas_do_processo3 = gw.getWindowsWithTitle(janela_serial)
        time.sleep(0.1)
        if janelas_do_processo3:
            print(f'encontrada {janelas_do_processo3}')
            try:
                for janela in janelas_do_processo3:
                    janela.activate()
                    break
            except:
                print('janela serial nao encontrada')
    print("Thread encerrada.")


def is_numeric(input_str):
    return input_str.isdigit()




# Iniciar o cronômetro em uma thread separada

def input_labels(trv):
    
    # Exibir a caixa de diálogo para inserir a matrícula
    while True:
        with open ('C:\\Users\\mayco\\Desktop\\FBT_GUI\\Opid.txt', 'r') as opid:
            ultimo_opid= opid.read().strip()
        global search_input_window  # Mova a declaração global para o início da função
        search_input_window = True
        size = 6
        matricula = input_diag.show_custom_dialog("Matricula", "Matrícula do Operador:", gui.my_w, size)
        if matricula is not None:
            # Verifica se a matrícula tem exatamente 6 caracteres
            if len(matricula) == 6 and is_numeric(matricula):
                # Salva a matrícula no arquivo Opid.txt
                with open('C:\\Users\\mayco\\Desktop\\FBT_GUI\\Opid.txt', 'w') as file:
                    file.write(matricula)
                    save_dados(0,'OPID',matricula)
                result = "PASS"

                for child in trv.get_children():
                    values = trv.item(child)['values']
                    if values[1] == 'INPUT_OPID':
                        if result == 'PASS':
                            gui.reload_infos_csv()
                            trv.tag_configure('green', background='green', font=('Arial', 12, 'bold'))
                            trv.item(child, values=(values[0], values[1], result), tags=('green',))
                        else:
                            trv.tag_configure('orangered', background='orangered', font=('Arial', 12, 'bold'))
                            trv.item(child, values=(values[0], values[1], result), tags=('orangered',))
                            
                break
            else:
                # Se a matrícula não tiver 6 caracteres, exibe uma mensagem de erro
                tk.messagebox.showerror("Erro", "A matrícula deve conter exatamente 6 caracteres\nE Conter Apenas Numeros.")
        else:
            end_fbt()
 
    while True:
        size = 6
        print(matricula,ultimo_opid)
        if matricula == ultimo_opid:
            for child in gui.trv.get_children():
                with open ('C:\\Users\\mayco\\Desktop\\FBT_GUI\\estacao.txt', 'r') as station:
                    station= station.read().strip()
                save_dados(1, 'STATION',station)
                gui.reload_infos_csv()
                values = gui.trv.item(child)['values']
                if values[1] == 'INPUT_MACHINEID':
                    if result == 'PASS':
                        gui.trv.tag_configure('green', background='green', font=('Arial', 12, 'bold'))
                        gui.trv.item(child, values=(values[0], values[1], result), tags=('green',))
            break
        estacao = input_diag.show_custom_dialog("Estação", "Digitalize o ID da Estação:", gui.my_w, size)
        # estacao = simpledialog.askstring("Estação", "Digitalize o ID da Estação (6 dígitos):", parent=my_w)
        if estacao is not None:
            # Verifica se a matrícula tem exatamente 6 caracteres
            if len(estacao) == 6:
                # Salva a matrícula no arquivo Opid.txt
                with open('C:\\Users\\mayco\\Desktop\\FBT_GUI\\estacao.txt', 'w') as file:
                    file.write(estacao)
                result = "PASS"
                save_dados(1,'STATION',estacao)
                for child in gui.trv.get_children():
                    values = gui.trv.item(child)['values']
                    if values[1] == 'INPUT_MACHINEID':
                        if result == 'PASS':
                            gui.reload_infos_csv()
                            gui.trv.tag_configure('green', background='green', font=('Arial', 12, 'bold'))
                            gui.trv.item(child, values=(values[0], values[1], result), tags=('green',))
                        else:
                            gui.trv.tag_configure('orangered', background='orangered', font=('Arial', 12, 'bold'))
                            gui.trv.item(child, values=(values[0], values[1], result), tags=('orangered'))
                break
            else:
                # Se a matrícula não tiver 6 caracteres, exibe uma mensagem de erro
                tk.messagebox.showerror( "Erro", "O ID da Estação deve conter exatamente 6 caracteres.")
        else:
            end_fbt()

    while True:
        size = 18
        serial = input_diag.show_custom_dialog("Serial", "Digitalize o Serial da Placa", gui.my_w, size)
        # serial = simpledialog.askstring("Serial", "Digitalize o Serial da Placa (18 dígitos):", parent=my_w)
        if serial is not None:
            # Verifica se a matrícula tem exatamente 6 caracteres
            if len(serial) == 18:
                # Salva a matrícula no arquivo Opid.txt
                with open('C:\\Users\\mayco\\Desktop\\FBT_GUI\\serial.txt', 'w') as file:
                    file.write(serial)
                result = "PASS"
                save_dados(2,'SERIAL',serial)
                for child in trv.get_children():
                    values = trv.item(child)['values']
                    if values[1] == 'INPUT_MAIN_SERIAL':
                        gui.reload_infos_csv()
                        if result == 'PASS':
                            trv.tag_configure('green', background='green', font=('Arial', 12, 'bold'))
                            trv.item(child, values=(values[0], values[1], result), tags=('green',))
                        else:
                            trv.tag_configure('orangered', background='orangered', font=('Arial', 12, 'bold'))
                            trv.item(child, values=(values[0], values[1], result), tags=('orangered',))
                break
            else:
                # Se a matrícula não tiver 6 caracteres, exibe uma mensagem de erro
                tk.messagebox.showerror( "Erro", "O Serial da placa deve conter 18 caracteres.")
        else:
            end_fbt()

 

gui.my_w.protocol("WM_DELETE_WINDOW", end_fbt)

def stop_threads():
    global stop
    stop = True  # Define stop como True para interromper os threads

    # Cancela todos os threads ativos
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.cancel()

    # Cancela o after existente
    gui.my_w.after_cancel(checkpass_id)


def checkpass():
    global checkpass_id, stop

    if stop == True:
        gui.my_w.after_cancel(checkpass_id)
        gui.my_w.after_cancel(gui.loop_time)
        print('falha')
        ask_fail = messagebox.askquestion("Fail", "REINICIAR TESTE?")
        print(ask_fail)
        if ask_fail == 'yes':
            gui.reload_csv()
            start_gui()     # Reinicia o teste
        else:
            stop = False
            print('ok')
            # end_fbt()

    checkpass_id = gui.my_w.after(300, checkpass)  # Reinicia o after (loop de 1 segundo)

def on_closing():
    if messagebox.askokcancel("Fechar", "Deseja fechar o programa?"):exit()

def CameraID():
    global stop
    result = cameraID.camera_teste(gui.trv)
    if result == 'PASS':
        print('CONTINUE THREADING')
        stop = False
    else:
        print('STOP THREADING')
        stop = True
def CheckMac():
    checkMAC.check_mac_teste(gui.trv)

def sequencia0():
    threading.Thread(target=top_input_window).start()
    input_labels(gui.trv)
    print('ended')


def sequencia1():
    threading.Thread(target=CameraID).start()
     

def sequencia2():
    threading.Thread(target=CheckMac).start()

def start_gui():
    global stop, segundos
    segundos = time.time()
    stop = False
    gui.reload_infos_csv()
    gui.update_timer(segundos)
    checkpass()
    sequencia0()
    sequencia1()
    sequencia2()

start_gui()
gui.my_w.mainloop()

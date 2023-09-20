import pandas as pd
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import gspread
import time

gc = gspread.service_account(filename='creds.json')
sheet = gc.open('spreadsheetdata').sheet1

class message():

    def getDataFromFile():

        path = r"C://Users//jc160//OneDrive//Área de Trabalho//projeto de Programa, Contra evasão escolar//spreadsheetdata - Página1.csv"
        contatos = pd.read_csv(path)
        print(contatos)

        data_dict = {}

        for i, aluno in enumerate(contatos['Aluno']):
            responsavel = str(contatos.loc[i, 'Responsável'])
            numero = contatos.loc[i, 'Número']
            enviada = contatos.loc[i,'Enviada']

            if enviada == False:
                mensagem = str((f'Olá, {responsavel}, a Escola EREM Manoel Bacelar gostaria de saber os possíveis motivos da evasão do(a) aluno(a): {aluno}. Por favor, nos informe o quanto antes, agradecimentos, a direção.'))

                data = {'aluno':aluno,
                        'reponsavel':responsavel,
                        'numero': numero,
                        'mensagem': mensagem,
                        'enviada': enviada}
                
                data_dict.setdefault(aluno,data)
            else:
                print(f'Mensagem já enviada para {aluno}')
                pass

        return data_dict
    
    def createLink(data,aluno):

        phoneNumber = data[aluno]['numero']
        message = quote(data[aluno]['mensagem'])

        link = f"https://web.whatsapp.com/send/?phone={phoneNumber}&text={message}"
        
        print(link)
        return link

    def send(link,sheetRow):
        navegador.get(link)
        
        while len(navegador.find_elements(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span')) < 1:
            time.sleep(1)

        pyautogui.press('enter')
        sheet.update(f'D{sheetRow}',True)
        time.sleep(3)

data_dict = message.getDataFromFile()
navegador = webdriver.Chrome()

for row,aluno in enumerate(data_dict.keys(),start=2):
    message.send(message.createLink(data_dict,aluno),row)
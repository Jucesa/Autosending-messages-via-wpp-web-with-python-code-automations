import pandas as pd
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import gspread
import time

#conecting to spreadsheet in google sheets
gc = gspread.service_account(filename='key.json')
sheet = gc.open('spreadsheetdata').sheet1

class message():

    def getDataFromFile():
        #declaring a dict object to store the data from the sheet
        data_dict = {}

        #receiving the data from the sheet
        dataUpdate = sheet.get_all_values()
        contatos = pd.DataFrame(dataUpdate[1:],columns=dataUpdate[0])
        print(contatos)

        # organizing the data for each student
        for i, aluno in enumerate(contatos['Aluno']):
            responsavel = str(contatos.loc[i, 'Responsável'])
            numero = str(contatos.loc[i, 'Número'])
            enviada = contatos.loc[i,'Enviada']
            mensagem = f'Olá, {responsavel}, a Escola EREM Manoel Bacelar gostaria de saber os possíveis motivos da evasão do(a) aluno(a): {aluno}. Por favor, nos informe o quanto antes, agradecimentos, a direção.'

            if enviada == 'SIM':
                enviada = True
            else:
                enviada = False

            data = {'aluno':aluno,
                        'responsavel':responsavel,
                        'numero': numero,
                        'mensagem': mensagem,
                        'enviada': enviada}
            print(enviada)
            print(type(enviada))
            data_dict.setdefault(aluno,data)

        return data_dict
    
    def createLink(data,aluno):
        # Creating a custom link for each message
        phoneNumber = data[aluno]['numero']
        message = quote(data[aluno]['mensagem'])

        link = f"https://web.whatsapp.com/send/?phone={phoneNumber}&text={message}"
        print(link)

        return link
            
    def send(link,sheetRow):

        navegador.get(link)
         # Verify if the element of the send button is availabe on the screen before sending the message 
        while len(navegador.find_elements(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span')) < 1:
            time.sleep(1)

        pyautogui.press('enter')

        time.sleep(1)
        # Verify if the message was sent by looking for the clock element
        while len(navegador.find_elements(By.XPATH,'//*[@id="main"]/div[2]/div/div[2]/div[3]/div[19]/div/div/div/div[1]/div[1]/div/div[2]/div/div/span/svg')) >= 1:
            time.sleep(1)
        else:
            sucesso = True
        
        if sucesso:
            sheet.update(f'D{sheetRow}','SIM')

data_dict = message.getDataFromFile()
navegador = webdriver.Chrome()

for row,aluno in enumerate(data_dict.keys(),start=2):

    # Verifying if a message was already sent
    if  data_dict[aluno]['enviada']:
        print(f'Mensagem já enviada para {data_dict[aluno]["responsavel"]}')
    else:
        message.send(message.createLink(data_dict,aluno),row)
        print(f'Enviando mensagem para {data_dict[aluno]["responsavel"]}')

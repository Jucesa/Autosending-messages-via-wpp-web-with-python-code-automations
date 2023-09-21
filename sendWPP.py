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
        #getting the path where the csv file is located
        path = r"C://Users//jc160//OneDrive//Área de Trabalho//projeto de Programa, Contra evasão escolar//spreadsheetdata - Página1.csv"

        #updating the data from the csv file
        dataUpdate = sheet.get_all_values()
        df = pd.DataFrame(dataUpdate[1:],columns=dataUpdate[0])

        df.to_csv(path,index=False)
        print(f'CSV file updated at: {path}')

        #reading the data provided
        contatos = pd.read_csv(path)
        print(contatos) 

        #declaring a dict object to store the data from the csv file
        data_dict = {}

        # organizing the data for each student
        for i, aluno in enumerate(contatos['Aluno']):
            responsavel = str(contatos.loc[i, 'Responsável'])
            numero = contatos.loc[i, 'Número']
            enviada = contatos.loc[i,'Enviada']

            mensagem = str((f'Olá, {responsavel}, a Escola EREM Manoel Bacelar gostaria de saber os possíveis motivos da evasão do(a) aluno(a): {aluno}. Por favor, nos informe o quanto antes, agradecimentos, a direção.'))

            data = {'aluno':aluno,
                        'responsavel':responsavel,
                        'numero': numero,
                        'mensagem': mensagem,
                        'enviada': enviada}
                
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
        
        while len(navegador.find_elements(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span')) < 1:
            time.sleep(1)

        pyautogui.press('enter')

        sheet.update(f'D{sheetRow}',True)

        time.sleep(3)

data_dict = message.getDataFromFile()
navegador = webdriver.Chrome()

for row,aluno in enumerate(data_dict.keys(),start=2):

    # Verifying if a message was already sent
    if data_dict[aluno]['enviada'] == False:

        message.send(message.createLink(data_dict,aluno),row)
        print(f'Enviando mensagem para {data_dict[aluno]["responsavel"]}')

    else:

        print(f'Mensagem já enviada para {data_dict[aluno]["responsavel"]}')

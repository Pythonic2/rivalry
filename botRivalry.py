from selenium.webdriver import Keys
from pages.page_itens import Itens_Pagina
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import pyautogui
import openpyxl
from time import sleep
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class BotChrome:

    def __init__(self):
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
       
        self.chrome_options.add_argument(r'--user-data-dir=C:\Users\igorsilv\OneDrive - Capgemini\Desktop\rivalry\DadosNavegador')
        #drive
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 120)
        

    def get_element_by_xpath(self, xpath, ec=None):
        ec = ec if ec else EC.presence_of_element_located
        return self.wait.until(ec((By.XPATH, xpath)))

    def apostar(self,url_aposta,acima_abaixo,iten, tipo_aposta):
        self.driver.get(url_aposta)
        sleep(5)
        self.lista_rivalry = [i.text for i in self.driver.find_elements(By.XPATH, '//h2')]
        self.nova_lista_rivalry = []

        menu_itens = self.driver.find_elements(By.XPATH,"//a[contains(@class,'text-white hover:text-football-tint')]")
        menu_itens[0].click()

        aposta_escanteios_acima = f"//div[@class='match-market-block Regulation Time Total Corners Over/Under-market-group']/div/h2[contains(text(),'{tipo_aposta}')]/../..//div[contains(text(),'{acima_abaixo} de')]//span[contains(text(),'{iten}')]"
        self.get_element_by_xpath(aposta_escanteios_acima).click()
        sleep(3)
        pyautogui.click(x=1802, y=959)


    def telegram(self):
        self.driver.get(Itens_Pagina.URL)
        self.get_element_by_xpath(Itens_Pagina.LISTA_MSG)
        mensagens_aposta2 = self.driver.find_elements(By.XPATH, Itens_Pagina.LISTA_MSG)

        mensagens_aposta = self.driver.find_elements(By.XPATH,Itens_Pagina.LISTA_MSG)[-1].text

        quantidade_do_tipo = mensagens_aposta.split()

        tabele_menosdetalhes = mensagens_aposta2[-1].text.splitlines()

        lista_consulta_tipo_aposta = [word.strip() for word in tabele_menosdetalhes if word.strip() != ""]

        ignorarcasLista = [i.capitalize()  for i in lista_consulta_tipo_aposta]

        self.ignorarcasLista_compara_com_lista_rivalry = ignorarcasLista[3]

        ######## DADOS PARA O EXCEL #########
        self.tipo_aposta = self.ignorarcasLista_compara_com_lista_rivalry
        self.url = lista_consulta_tipo_aposta[7]
        self.acima_abaixo = quantidade_do_tipo[5]
        self.iten = quantidade_do_tipo[7]

    def escrever_excel(self):
        book = openpyxl.load_workbook('dadosApostas.xlsx')
        tabela = book.active
        tabela.append([self.tipo_aposta, self.url, self.acima_abaixo, self.iten])
        tabela.column_dimensions['A'].width = 80
        tabela.column_dimensions['B'].width = 25
        tabela.column_dimensions['C'].width = 25
        tabela.column_dimensions['D'].width = 25
        book.save('dadosApostas.xlsx')

    def ler_excel_dadosProdutos(self):
        df = pd.read_excel('dadosApostas.xlsx')
        tab = pd.DataFrame(df)
        self.url_excel, = tab['url'][-1:]

        if self.url_excel != self.url:
            self.escrever_excel()
            self.apostar(self.url,self.acima_abaixo,self.iten,self.tipo_aposta)


    def fechar(self):
        self.driver.close()

        # for i in self.lista_rivalry:
        #     self.nova_lista_rivalry.append(i.capitalize())
        #
        # if self.nova_lista_rivalry.__contains__(self.ignorarcasLista_compara_com_lista_rivalry):
        #     ...
        #     # self.apostar(self.url, self.acima_abaixo, self.iten, self.tipo_aposta)
        # else:
        #     print('asposta n encontrada')


        # verificar se o link os itens da aposta sao iguais a do excel para poder apostar ou n












    
    
    
    #     dica = itens[-1].text
    #     itens_dica_detalhada = dica.splitlines()
    #     print(itens_dica_detalhada)
    
    #     dados_mais = dica.split()
    #     print(dados_mais)
    
    
    #     if itens_dica_detalhada.__contains__('Tempo regulamenter Total de escanteios acima/abaixo') and dados_mais.__contains__('Acima'):
    #         for i in dados_mais:
    #             if i.__contains__('edited'):
    #                 print(i)
    #                 break
    #             elif i.__contains__('https'):
    #                 self.driver.get(i)
    #                 sleep(5)
    #                 menu_itens = self.driver.find_elements(By.XPATH,"//a[contains(@class,'text-white hover:text-football-tint')]")
    #                 menu_itens[0].click()
    
    
    #                 aposta_escanteios_acima = f"//div[@class='match-market-block Regulation Time Total Corners Over/Under-market-group']/div/h2[contains(text(),'Tempo regulamenter Total de escanteios acima/abaixo')]/../..//div[contains(text(),'Acima de')]//span[contains(text(),'{dados_mais[7]}')]"
    #                 self.get_element_by_xpath(aposta_escanteios_acima).click()
    #                 sleep(3)
    #                 pyautogui.click(x=1802, y=959)
    
    #                 sleep(10)
    
    #     elif itens_dica_detalhada.__contains__('Tempo regulamenter Total de escanteios acima/abaixo') and dados_mais.__contains__('Abaixo'):
    #         for i in dados_mais:
    #             if i.__contains__('edited'):
    #                 print(i)
    #                 break
    #             elif i.__contains__('https'):
    #                 self.driver.get(i)
    #                 aposta_escanteios_acima = f"//div[@class='match-market-block Regulation Time Total Corners Over/Under-market-group']/div/h2[contains(text(),'Tempo regulamenter Total de escanteios acima/abaixo')]/../..//div[contains(text(),'Abaixo de')]//span[contains(text(),'{dados_mais[7]}')]"
    #                 self.get_element_by_xpath(aposta_escanteios_acima).click()
    #                 self.driver.find_element("//span[contains(text(),'Fazer Apostas')]").click()





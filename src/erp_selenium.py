import os
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from src.functions import formatar_cpf
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

#Carregando as variaveis de ambiente
load_dotenv()

user = os.getenv("ERP_USERNAME")
password = os.getenv("ERP_PASSWORD")


#definindo as opções do navegador(Chrome)
chrome_options = Options()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless")

def buscar_cliente():
    while True:
        cpf_cliente = input("Digite o cpf a ser pesquisado: ")
        if cpf_cliente == "0":
            print("Programa encerrando")
            break
        
        try:
            cpf_cliente = formatar_cpf(cpf_cliente)
        except ValueError as ve:
            print(f"Erro: {ve}. Digite um CPF válido com 11 dígitos.")
            continue
            
        #instanciando o driver 
        driver = webdriver.Chrome(options=chrome_options)

        #acessando o site do Olist
        driver.get("https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth?client_id=tiny-webapp&redirect_uri=https://erp.tiny.com.br/login&scope=openid&response_type=code")
        driver.maximize_window()

        #Fazedo o login com o email 1°
        box_login = driver.find_element(by=By.ID, value="username")
        time.sleep(1)
        box_login.send_keys(user)

        submit_login = driver.find_element(by=By.CSS_SELECTOR, value=".sc-dAlyuH")
        time.sleep(1)
        submit_login.click()

        #Colocando o campo senha e clickando no botão.
        time.sleep(1)
        box_password = driver.find_element(by=By.ID, value="password")
        box_password.send_keys(password)
        time.sleep(1)
        submit_password = driver.find_element(by=By.CSS_SELECTOR, value=".sc-dAlyuH")
        time.sleep(1)
        submit_password.click()

        time.sleep(5)
        #Esperando a tela de usuario logado aparecer, se não apaarecer continua normalmente
        try:
            popup_button = driver.find_element(by=By.CSS_SELECTOR, value="button.btn:nth-child(1)")
            popup_button.click()
            time.sleep(5)
        except NoSuchElementException:
                time.sleep(5)
            
        #clickando no menu
        menu = driver.find_element(by=By.CSS_SELECTOR, value=".btn-sidebar-menu > .icon-menu-bars")
        menu.click()
        time.sleep(3)

        #Selecionando o campo cadastros
        cadastro = driver.find_element(by=By.CSS_SELECTOR, value="li:nth-child(2) .menu-description")
        cadastro.click()
        time.sleep(4)
        cadastro_clientes = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div[2]/nav[2]/ul/li[1]/a/span")
        cadastro_clientes.click()
        time.sleep(3)


        #Procurando o cliente
        search_box = driver.find_element(by=By.CSS_SELECTOR, value=".form-control:nth-child(1)")
        search_box.clear()
        search_box.send_keys(cpf_cliente)
        search_box.send_keys(Keys.ENTER)
        time.sleep(4)

        #Definindo onde o cursor vai clcikar na tela.
        try:
            cursor_locate = driver.find_element(by=By.XPATH, value="/html/body/div[6]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]")
            #instanciando o actions chains para fazer a ação.
            actions = ActionChains(driver)
            actions.move_to_element(cursor_locate).click().perform()
            time.sleep(5)

            #Coletando o cabelo do cliente
            nome_cliente = driver.find_element(by=By.XPATH, value="/html/body/div[6]/div/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/p")
            nome_cliente_txt = nome_cliente.text
            #Coletando as tags do cliente
            tags = driver.find_elements(By.CSS_SELECTOR, value="span.badge")
            texto_tags = []

            for tag in tags:
                texto = tag.text.strip()
                if texto:
                    texto_tags.append(texto)
            time.sleep(1.5)

            #Coletando as ultimas venda do cliente
            more_options = driver.find_element(by=By.CSS_SELECTOR, value="#root-contatos > div > div > div.top-bar > div > div > div.dropdown.dropdown-in.featured-actions-menu > button")
            more_options.click()
            time.sleep(1)
            ultimas_vendas = driver.find_element(by=By.XPATH, value="//*[text()=' Consultar últimas vendas']")  
              
            ultimas_vendas.click()
            time.sleep(2)   
            
            try: 
                vendas = driver.find_element(by=By.CSS_SELECTOR, value="#bs-modal > div > div > div > div.modal-body > div:nth-child(1) > ul > li:nth-child(2) > a")
                vendas.click()
                
                id_venda = driver.find_element(by=By.CSS_SELECTOR, value="#bs-modal > div > div > div > div.modal-body > div.table-responsive > table > tbody > tr > td:nth-child(1) > a")
                num_venda = id_venda.text
                id_venda.click()
                time.sleep(4)

                # nome_cliente = driver.find_element(by=By.CSS_SELECTOR, value="#vendaForm > div:nth-child(17) > div:nth-child(2) > div > div.input-group.viewing-input-group > p")
                # nome_cliente_txt = nome_cliente.text

                item = driver.find_element(by=By.CSS_SELECTOR, value="#detailItem0 > td.coluna-destaque.edit-col.hand-cursor.readonly > p.form-control-static.viewing-input")
                item_txt = item.text

                valor = driver.find_element(by=By.CSS_SELECTOR, value="#detailItem0 > td:nth-child(9) > p.form-control-static.viewing-input")
                valor_txt = valor.text

                quantidade = driver.find_element(by=By.CSS_SELECTOR, value="#detailItem0 > td:nth-child(4) > p.form-control-static.viewing-input")
                quantidade_txt = quantidade.text

                quantidade_txt = quantidade_txt.replace(",",".")
                quantidade_txt = float(quantidade_txt)
                quantidade_txt_int = int(quantidade_txt)

                data_ultima_compra = driver.find_element(by=By.CSS_SELECTOR, value="#vendaForm > div:nth-child(21) > div > div > div:nth-child(1) > div > p")
                data_ultima_compra_txt = data_ultima_compra.text


                driver.quit() 

                
                print(f"Dados do Cliente: {nome_cliente_txt}, {num_venda}, {item_txt}, {valor_txt}, {quantidade_txt_int}, {data_ultima_compra_txt}")  
                print(f"Tags: {texto}")  
            except NoSuchElementException:
                print(f"Nome do Ciente: {nome_cliente_txt}, Tags: {texto_tags}")
                print("Não foi encontrado nenhuma venda para esse cliente")
                driver.quit()
        except NoSuchElementException:
            print("Cliente não encontrado")
            driver.quit()

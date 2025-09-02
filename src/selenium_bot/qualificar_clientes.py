import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.api.tiny_api import obter_tipo_contato_por_cpf
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

kommo_user = os.getenv("KOMMO_USERNAME")
kommo_password = os.getenv("KOMMO_PASSWORD")
url_kommo = os.getenv("KOMMO_URL")
print(url_kommo)
url_olist = ""

chrome_options = Options()
chrome_options.add_argument("--icognito")
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")

def qualificar_clientes():
    
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url_kommo)
    driver.maximize_window()
    
    #================================= Login ===============================================
    time.sleep(5)
    
    login_username_kommo = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div[1]/span/input")))
    login_username_kommo.send_keys(kommo_user)
    
    time.sleep(1)

    login_password_kommo = driver.find_element(by=By.ID, value="password")
    login_password_kommo.send_keys(kommo_password)
    
    login_button_kommo = driver.find_element(by=By.CSS_SELECTOR, value="#auth_submit")
    login_button_kommo.click()
    #================================== Lidando com os poup ups ================================================
    try:
        time.sleep(5)
        popup_kommo = driver.find_element(by=By.CSS_SELECTOR, value="body > div.modal.modal-list > div.modal-scroller.custom-scroll > div > div > button")
        popup_kommo.click()
    except TimeoutException:
        print("Nenhum poupup encontrado")
        
    #================================== Leads ==================================================================
    btn_leads = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[6]/div/div/div[2]/a")
    btn_leads.click()
    time.sleep(1)
    
    element = driver.find_element("tag name", "body")
    ActionChains(driver).move_to_element(element).perform()
    
    time.sleep(1)
    btn_leads_dropdown = driver.find_element(by=By.CSS_SELECTOR, value="div.list-top-nav__icon-button_dark:nth-child(2)")
    btn_leads_dropdown.click()
    time.sleep(1)
    
    btn_select_base_leads = driver.find_element(by=By.CSS_SELECTOR, value="li.aside__list-item:nth-child(2) > a:nth-child(1)")
    btn_select_base_leads.click()
    time.sleep(4)
    
    btn_list_mode = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[1]/div[2]/a[2]")
    btn_list_mode.click()
    time.sleep(2)
    #================================== Fazendo um Filtro somente para meu usuário =============+================    
    filter_box = driver.find_element(by=By.ID, value="search_input")
    filter_box.click()
    time.sleep(1)
    
    # select_filters_1 = driver.find_element(by=By.CSS_SELECTOR, value="li.tags-lib__item:nth-child(6) > div:nth-child(1)")
    # select_filters_1.click()
    # time.sleep(1)
    
    # select_filters_2 = driver.find_element(by=By.CSS_SELECTOR, value="div.filter-search__filter__group__wrapper:nth-child(11) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1) > div:nth-child(1)")
    # driver.execute_script("arguments[0].scrollIntoView(true);", select_filters_2)
    # select_filters_2.click()
    # time.sleep(1)
    
    # resp_atend = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[2]/form/div[1]/div[1]/div/div[11]/div/div/div/div[1]/div/div[3]/label")
    # resp_atend.click()
    # time.sleep(1)
    
    # apply_filters = driver.find_element(by=By.ID, value="filter_apply")
    # apply_filters.click()
    # time.sleep(3)
    
    filtro_qualificar = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[1]/ul/li[7]/div/span[2]")
    filtro_qualificar.click()
    time.sleep(2)
    #====================== Contadores de estatisticas ====================================    
    total_leads = 0
    contador_profissional = 0
    contador_final = 0
    
    while True:
        try:
            time.sleep(7)
            first_lead = driver.find_element(By.XPATH, "(//a[@class='js-navigate-link list-row__template-name__table-wrapper__name-link'])[1]")
            first_lead.click()
            time.sleep(4)
            
            cpf_lead_txt = None
            cnpj_lead_txt = None
            
            try:
                cpf_lead = driver.find_element(by=By.XPATH, value="//input[@class='control--suggest--input js-control--suggest--input-ajax linked-form__cf js-legal-entity-vat legal-entity__item-mini-input js-control-allow-numeric control-price_autosized']")
                cpf_lead_txt = cpf_lead.get_attribute("value")
                print(f"O CPF é: {cpf_lead_txt}")
                search_client = cpf_lead_txt
            except NoSuchElementException:
                print("Não foi encontrado cpf para este cliente")
             
           
            if not cpf_lead_txt:
                try:
                    cnpj_lead = driver.find_element(By.XPATH, value="/html/body/div[7]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[1]/ul/li/form/div[2]/div[4]/div[1]/div[2]/div/div[3]/div/input")
                    cnpj_lead_txt = cnpj_lead.get_attribute("value")
                    print(f"O CNPJ é: {cnpj_lead_txt}")
                    search_client = cnpj_lead_txt
                except NoSuchElementException:
                    print("Não foi encontrado CNPJ para este cliente")
            
            if not cpf_lead_txt and not cnpj_lead_txt:
                print("Nenhum CPF ou CNPJ encontrado → definindo ele como cliente final")
                qualify_lead = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[2]/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div/div/div[1]/div/div/div/div[2]")
                qualify_lead.click()
                time.sleep(3)
                
                send_to_hopper_Home_care = driver.find_element(by=By.CSS_SELECTOR, value="div.pipeline-select:nth-child(5) > ul:nth-child(2) > li:nth-child(2)")
                send_to_hopper_Home_care.click()
                time.sleep(3)
                
                save_changes = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[2]/div[1]/div[2]/button[1]/span/span")    
                save_changes.click()
                time.sleep(3)
                
                back_to_qualify = driver.find_element(by=By.CSS_SELECTOR, value=".js-back-button")
                back_to_qualify.click()
                time.sleep(4)
                
                
                total_leads += 1
                contador_final += 1
            else:
                # Se encontrou CPF ou CNPJ, seguir fluxo normal
                print("Cliente possui CPF ou CNPJ → seguindo fluxo normal")
            
                #========================================== Definindo se e cliente final ou profissional ====================================
                #O código faz acesso a api do Olist v2(Não e a mais recente, possui a v3) para 
                #pegar a tag do cliente e verificar se ele e um cliente profissional ou Final
                #para assim da segmento ao fluxo do robô.
            
                tipo_contato = obter_tipo_contato_por_cpf(search_client)
                print(f"Tipo de contato do cliente: {tipo_contato}")
                
                #=============================================================================================================================
                
                #============================================ Definindo o fluxo do lead =================================================
                qualify_lead = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[2]/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div/div/div[1]/div/div/div/div[2]")
                qualify_lead.click()
                time.sleep(3)
                
                if tipo_contato == "Cliente profissional":
                    send_to_hopper_profissional = driver.find_element(by=By.CSS_SELECTOR, value="div.pipeline-select:nth-child(5) > ul:nth-child(2) > li:nth-child(6) > label:nth-child(2)")
                    send_to_hopper_profissional.click()
                    time.sleep(4)
                    
                    total_leads += 1
                    contador_profissional += 1
                    
                elif tipo_contato == "Cliente Home Care":
                    send_to_hopper_Home_care = driver.find_element(by=By.CSS_SELECTOR, value="div.pipeline-select:nth-child(5) > ul:nth-child(2) > li:nth-child(2)")
                    send_to_hopper_Home_care.click()
                    time.sleep(4)
                    
                    total_leads += 1
                    contador_final += 1
                else:
                    print("Não foi identificado se ele e profissional ou Final → Definindo ele como cliente final. ")
                    send_to_hopper_Home_care = driver.find_element(by=By.CSS_SELECTOR, value="div.pipeline-select:nth-child(5) > ul:nth-child(2) > li:nth-child(2)")
                    send_to_hopper_Home_care.click()                                                        
                    time.sleep(4)
                    
                    total_leads += 1
                    contador_final += 1
                    
                    
                save_changes = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[2]/div[1]/div[2]/button[1]/span/span")    
                save_changes.click()
                time.sleep(4)
                
                back_to_qualify = driver.find_element(by=By.CSS_SELECTOR, value=".js-back-button")
                back_to_qualify.click()
            
            
            
        except NoSuchElementException:
            print("Não há mais leads disponíveis ou a lista de leads está vazia.")
            break
        
        
    print("===== RESULTADO FINAL =====")
    print(f"Total de leads processados: {total_leads}")
    print(f"Clientes Profissionais: {contador_profissional}")
    print(f"Clientes Finais (Home Care): {contador_final}")
    
    driver.quit()
    


qualificar_clientes()
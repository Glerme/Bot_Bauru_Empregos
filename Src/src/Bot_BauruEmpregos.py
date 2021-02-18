import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
import PySimpleGUI as sg  

# Layout
sg.theme('Dark Blue 3')
layout = [  [sg.Text('Digite a vaga procurada: '),sg.Input(key='digitar',size=(40,30))], 
            [sg.OK('Começar',size=(20,2)), sg.Exit('Cancelar',key='cancel',size=(20,2))]
        ] 

# criar janela
janela = sg.Window('Procura Vagas', layout)
eventos, valores = janela.read()

# ler os eventos
while True:
    if eventos == sg.WINDOW_CLOSED or eventos == 'cancel':
        break

    if eventos == 'Começar':
        vagas = []
        vagas.append(valores['digitar'].capitalize())

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.maximize_window()
        driver.get("https://www.bauruempregos.com.br/home/vagas")

        def pegarVaga(vaga):
            ac = webdriver.ActionChains(driver)
            time.sleep(2)
            ac.key_down(Keys.CONTROL).move_to_element(vaga).click()
            ac.perform()
            time.sleep(2)
            url = driver.current_url
            if url == 'https://www.bauruempregos.com.br/home/vagas#google_vignette':
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                driver.back()
                time.sleep(3)
                elementos = driver.find_elements_by_partial_link_text(i)          
                for elemento in elementos:
                    pegarVaga(elemento)
             
        for i in vagas:
            time.sleep(3)
            elementos = driver.find_elements_by_partial_link_text(i)          
            for elemento in elementos:
                pegarVaga(elemento)
                

    janela.close()
    break


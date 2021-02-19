import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
import PySimpleGUI as sg  

# Layout
sg.theme('Dark Blue 3')
layout = [  [sg.Text('Digite a vaga procurada: '),sg.Input(key='digitar',size=(40,30))],
            [sg.Radio('Chrome',"SELECTED", default=True,key='chrome'),sg.Radio('Firefox',"SELECTED", default=False,key='firefox'),sg.Radio('Edge',"SELECTED", default=False,key='edge')],
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
        def iniciar(driver):
            vagas = []
            vagas.append(valores['digitar'].capitalize())
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

        def valor(valores):
            if valores['chrome'] == True:
                driver = webdriver.Chrome(ChromeDriverManager().install())
                iniciar(driver)
            elif valores['firefox'] == True:
                driver = webdriver.Firefox()
                iniciar(driver)
            elif valores['edge'] == True:
                driver = webdriver.Edge(EdgeChromiumDriverManager().install())
                iniciar(driver)
            else:
                sg.popup_auto_close("Você não selecionou nenhum navegador!",title='Erro')

                
        valor(valores)

    janela.close()
    break


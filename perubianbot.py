from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import warnings
import requests
from colorama import Fore, Style
from consolemenu import *
from consolemenu.items import *
import signal
import sys
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import time
import os
import argparse
from unidecode import unidecode
import re
from os import system

version = '2.3 BETA'
global debug

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', help="Habilitar el modo debug")
parser.add_argument('--headless', action='store_true', help="Ejecutar en modo headless")
parser.add_argument('--start', nargs=4, metavar=('nombre', 'apellido', 'telefono', 'email'),
                    help="Iniciar el programa con datos: nombre apellido telefono email")
# Leer los argumentos
args = parser.parse_args()
debug = int(args.debug)
headless = int(args.headless)

if os.name == 'nt':
    system("title " 'PerubianBot v'+version)
else:
    system("echo -e '\033]2;PerubianBot v"+version+"\007'")

global perubian
perubian = Fore.MAGENTA + Style.BRIGHT + r"""
  _____                _     _               ___    ____  
 |  __ \              | |   (_)             |__ \  |___ \ 
 | |__) |__ _ __ _   _| |__  _  __ _ _ __      ) |   __) |
 |  ___/ _ \ '__| | | | '_ \| |/ _` | '_ \    / /   |__ < 
 | |  |  __/ |  | |_| | |_) | | (_| | | | |  / /_ _ ___) |
 |_|   \___|_|   \__,_|_.__/|_|\__,_|_| |_| |____(_)____/ 
""" + Style.RESET_ALL

def check_version():
    try:
        current_version_num = version.split(" ")[0]

        gist_url = "https://gist.githubusercontent.com/Oihalitz/06b39df2b15439c8aa0c6419e5565341/raw/versionperubian.json"

        response = requests.get(gist_url)
        response.raise_for_status()
        latest_version = response.json().get("latest_version")

        if not latest_version:
            return "No se pudo obtener la versión más reciente."

        if current_version_num < latest_version:
            return f"¡Nueva versión disponible! (Actual: {version}, Nueva: {latest_version})"
        else:
            return ""
    except requests.exceptions.RequestException as e:
        return f"Error al comprobar la versión: {e}"

menu = ConsoleMenu(Fore.YELLOW + perubian + check_version(), "Seleccione un modo" + Style.RESET_ALL)


def setup_browser():
    global binary, profile, PATH_TO_DEV_NULL
    global browser

    if os.name == 'nt':  # Windows
        firefox_binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        PATH_TO_DEV_NULL = 'nul'
    elif os.uname().sysname == 'Darwin':  # macOS
        firefox_binary = '/Applications/Firefox.app/Contents/MacOS/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    else:
        firefox_binary = '/usr/bin/firefox'
        PATH_TO_DEV_NULL = '/dev/null'

    # Comprobar si Firefox está instalado
    if os.path.exists(firefox_binary):
        PATH_TO_DEV_NULL = 'nul' if os.name == 'nt' else '/dev/null'
        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.autoplay.default", 0)
        profile.accept_untrusted_certs = True
        profile.set_preference("media.volume_scale", "0.0")
        profile.set_preference("dom.webnotifications.enabled", False)

        if getattr(sys, 'frozen', False):
            geckodriver_path = os.path.join(sys._MEIPASS, 'geckodriver')
        else:
            geckodriver_path = './geckodriver'
        
        if headless:
            options = webdriver.FirefoxOptions()
            options.headless = True
            browser = webdriver.Firefox(firefox_binary=firefox_binary, executable_path=geckodriver_path, firefox_profile=profile, service_log_path=PATH_TO_DEV_NULL, options=options)
        else:
            browser = webdriver.Firefox(firefox_binary=firefox_binary, executable_path=geckodriver_path, firefox_profile=profile, service_log_path=PATH_TO_DEV_NULL)
    
    # Configurar para Chrome si Firefox no está disponible
    else: 
        print("Firefox no está instalado, usando Chrome...")
        chrome_service = ChromeService(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--silent')
        browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

#Limpiar Consola
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

#Formulario Datos
def pregunta_estilizada(prompt, datos_previos='', email='', validacion=None):
    clear_console()
    print(perubian)
    # Imprimir los datos previos antes de hacer la nueva pregunta
    if datos_previos:
        print(datos_previos)
    print(Fore.YELLOW + Style.BRIGHT + prompt)
    
    while True:
        try:
            respuesta = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL)
            # Si se proporciona una función de validación y la respuesta es válida, romper el bucle
            if not validacion or validacion(respuesta):
                break
            else:
                print(Fore.RED + "Entrada inválida, por favor intente de nuevo." + Style.RESET_ALL)
        except EOFError:
            clear_console()
            exit(0)
    
    # Agregar el correo electrónico a datos_previos si se proporciona
    if email:
        datos_previos += Fore.WHITE + Style.BRIGHT + f"Correo: {email}\n" + Style.RESET_ALL
    
    return respuesta

def validacion_no_vacia(input_str):
    return input_str.strip() != ''

#Formulario
def formulario():
    global email 
    prefijos = ('6', '7', '9')
    if debug == 1:
        print(perubian)
        print('DEBUG MODE ON')
        global number, name, surname, email
        number, name, surname, email = '666666666', 'NombrePrueba', 'ApellidoPrueba', 'CorreoPrueba@gmail.com'
    else:
        def normalizar_cadena(cadena):
            # Quitar tildes y caracteres especiales
            cadena = unidecode(cadena)
            # Eliminar cualquier carácter que no sea alfanumérico
            cadena = re.sub(r'[^a-zA-Z0-9]', '', cadena)
            return cadena

        datos_persona = ''
        number = pregunta_estilizada('Nº de Teléfono: ')
        while len(number) != 9 or not number.isdigit() or number[0] not in prefijos:
            number = pregunta_estilizada('Número incorrecto. Ingrese Nº de Teléfono nuevamente: ')
        datos_persona += Fore.WHITE + Style.BRIGHT + f"Nº de Teléfono: {number}\n" + Style.RESET_ALL

        name = pregunta_estilizada('Nombre de la persona: ', datos_previos=datos_persona, validacion=validacion_no_vacia)
        surname = pregunta_estilizada('Apellido: ', datos_previos=datos_persona, validacion=validacion_no_vacia)
        nombre_completo = Fore.WHITE + Style.BRIGHT + f"Nombre: {name} {surname}\n" + Style.RESET_ALL
        datos_persona += nombre_completo

        # Normalizar el nombre y apellido
        name = normalizar_cadena(name.lower())
        surname = normalizar_cadena(surname.lower())

        email = pregunta_estilizada('Si no indicas email se va a introducir: ' + name + surname + '@gmail.com' + '\nCorreo: ', datos_persona)
        if not email:
            email = f'{name}.{surname}@gmail.com'
        datos_persona += Fore.WHITE + Style.BRIGHT + f"Correo: {email}\n" + Style.RESET_ALL

    # Después de recopilar toda la información, puedes mostrar datos_persona
    clear_console()
    print(perubian)
    if debug == 0:
        print(datos_persona)
    else:
        print('DEBUG MODE ON')

interrupted = False

def handle_interrupt(browser):
    global interrupted
    interrupted = True
    browser.quit()
    print("Navegador cerrado. Volviendo al menú principal...")

def main():
    #Limite hora
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start = '10:40:00'
    end = '22:00:00'

    if args.start or debug:
        repeat = 0
    else:
        repeat = input('Modo repetición [S/N]: ').lower()
        if repeat in ('y', 'yes', 's', 'si'):
            repeat = 1
        
    global interrupted
    while not interrupted:
        setup_browser()

        #SECURITAS DIRECT
        try:
            browser.get('https://www.securitasdirect.es/')
            time.sleep(5) #Cookies
            try:
                browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('//*[@id="edit-telefono1"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="edit-submit"]').click()
            time.sleep(1)
            if(browser.current_url == 'https://www.securitasdirect.es/error-envio'):
                print('Securitas Direct: Skipeado (Limite Excedido)')
            else:
                print('Securitas Direct: OK')
        except Exception as e:
            print('Securitas Direct: Skipeado (ERROR)')

        #euroinnova
        try:
            browser.get('https://www.euroinnova.com/')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="accept-cookies"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/button').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="mail"]').send_keys(email)
            browser.find_element_by_xpath('//*[@id="tel"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[7]/div/div/div[3]/form/div[3]/div[2]/div/select/option[10]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="privacidad"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="btn_enviar"]').click()
            time.sleep(3)
            print('Euroinnova: OK')
        except:
            print('Euroinnova: Skipeado (ERROR)')

        #GENESIS
        try:
            if current_time > start and current_time < end:
                browser.get('https://www.genesis.es/modal/c2c')
                time.sleep(3)
                try: #Cookies
                    browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/article/div/div/div/div/div/form/section/div/div[2]/div/select/option[2]').click()
                browser.find_element_by_xpath('//*[@id="edit-por-quien-preguntamos-"]').send_keys(name)
                browser.find_element_by_xpath('//*[@id="edit-phone"]').send_keys(number)
                browser.find_element_by_xpath('//*[@id="edit-phone-confirmation"]').send_keys(number)

                browser.find_element_by_xpath('//*[@id="edit-actions-submit"]').click()
                time.sleep(3)
                print('Genesis: OK')
            else:
                print('Genesis: Skipeado (Fuera de Horario)')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Genesis: Skipeado (ERROR)')

        #RACCTEL+
        try:
            browser.get('https://www.racctelplus.cat/es')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="c2c-submit"]').click()
            time.sleep(3)
            print('Racctel+ OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Racctel+ Skipeado: (ERROR)')

        #JAZZTEL
        try:
            browser.get('https://llamamegratis.es/jazztel/v2/webphone.html?lang=es-ES&isLandingLander=1&typeOrigin=wphFollow&widget=3294&wphUrl#https://www.telefonojazztel.es/')
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="phoneNumber"]').send_keys(number)
            time.sleep(1)
            try: #Horario
                browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[3]/div/div[2]/form/div/div[3]/div/select/option[2]').click()
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('//*[@id="env"]').click()
            time.sleep(3)
            print('Jazztel: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Jazztel: Skipeado (ERROR)')

        #Ford
        try:
            browser.get('https://www.infoford.es/c2c/iframe/flotas/ford-pro-expert/')
            time.sleep(4)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
                time.sleep(2)
            except:
                pass
            field = browser.find_element_by_xpath('//*[@id="telefono"]')
            browser.execute_script("arguments[0].value = arguments[1];", field, number)
            browser.find_element_by_xpath('//*[@id="legales"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="btn-enviar"]').click()
            time.sleep(5)
            print('Ford: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Ford: Skipeado (ERROR)')
    
        #spamovil
        try:
            browser.get('https://spamovil.es/te-llamamos-gratis/')
            time.sleep(1)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[1]/div/div/article/div/div/div/div[2]/div[2]/div/form/p[1]/label/span/input').send_keys(name)
            browser.find_element_by_xpath('/html/body/div[1]/div/div/article/div/div/div/div[2]/div[2]/div/form/p[2]/label/span/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/div/div/article/div/div/div/div[2]/div[2]/div/form/p[3]/label/span/span/span/input').click()
            browser.find_element_by_xpath('/html/body/div[1]/div/div/article/div/div/div/div[2]/div[2]/div/form/p[4]/input').click()
            time.sleep(5)
            print('spamovil: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('spamovil: Skipeado (ERROR)')

        #Vodafone
        try:
            browser.get('https://www.vodafone.es/c/empresas/es/marketing-online/')
            time.sleep(1)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[2]/main/div[1]/div/div[2]/div/div/div/section/div/div/div/div/div/a[1]/span[1]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            checkbox_gdpr = browser.find_element_by_xpath('//*[@id="cmb-gdpr"]')
            browser.execute_script("arguments[0].click();", checkbox_gdpr)
            checkbox_commercial = browser.find_element_by_xpath('//*[@id="cmb-check"]')
            browser.execute_script("arguments[0].click();", checkbox_commercial)
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[13]/div/div/div/span/div/div/div/div[2]/div[1]/div/div/form/input[2]').click()
            time.sleep(4)
            print('Vodafone: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Vodafone: Skipeado (ERROR)')

        #Euskaltel
        try:
            browser.get('https://www.euskaltel.com/?idioma=esp')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="c2c-submit"]').click()
            time.sleep(3)
            print('Euskaltel OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Euskaltel Skipeado: (ERROR)')

        #Pelayo
        try:
            browser.get('https://www.pelayo.com/nosotros_te_llamamos/tellamamos')
            time.sleep(2)
            try: #Cookies
                browser.find_element_by_xpath('/html/body/app-root/app-cookies-block/div[2]/div/div/a[1]').click()
                time.sleep(3)
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="input3"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/app-root/div/app-layout-click-to-call/main/div/div/app-ad-elem/app-panel-window-te-llamamos/form/div[2]/button').click()
            time.sleep(3)
            print('Pelayo OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Pelayo Skipeado: (ERROR)')

        #Movistar
        try:
            browser.get('https://www.movistar.es/estaticos/html/modal/modal-formulario-C2C-empresas-inside-sales-new.html')
            time.sleep(1)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="nameC2CplainModal_IS"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="tlfC2CplainModal_IS"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="cifC2CplainModal_IS"]').send_keys('D09818238')
            browser.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div[1]/div[4]/select/option[33]').click()
            browser.find_element_by_xpath('//*[@id="modal__emp__cta"]').click()
            time.sleep(2)
            print('Movistar OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Movistar Skipeado: (ERROR)')

        #Santalucia
        try:
            browser.get('https://seguro.santalucia.es/?utm_source=bing_santalucia_lbm_paid-search_bing_generica_multiramo_otros_na-site-section_na-ad-size_na-served-type_na-princing&msclkid=dac0ba5685891c9f6da6dd0efc479885')
            time.sleep(6)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="landings_ty_form115200807"]/div[1]/div/div[1]').click()
            time.sleep(2)
            browser.find_element_by_xpath("//*[starts-with(@id, 'phone')]").send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath("//*[starts-with(@id, 'checkProteccion')]").click()
            browser.find_element_by_xpath("//*[starts-with(@id, 'checkInformation')]").click()
            browser.find_element_by_xpath('//*[@id="landings_ty_form115200807"]/input').click()
            time.sleep(2)
            print('SantaLucia OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('SantaLucia Skipeado: (ERROR)')

        #Asisa
        try:
            browser.get('https://asisa.contratarsegurodesalud.com/seguro-salud-pyme')
            time.sleep(5)
            try: #Cookies
                browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[2]/button[4]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id=":R2kla2l6:"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/label/span[1]/input').click()
            browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div[4]/button/p').click()
            time.sleep(2)
            print('Asisa OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Asisa Skipeado: (ERROR)')

        #ITEP
        try:
            browser.get('https://www.itep.es/')
            time.sleep(4)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="cookiesjsr"]/div/div/div[2]/button[3]').click()
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('/html/body/header/div/div[5]/div/p/button').click() # Solicitar Informacion
            time.sleep(1)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-name')]").send_keys(name)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-email')]").send_keys(email)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-phone')]").send_keys(number)
            browser.find_element_by_xpath('//*[@id="edit-cp"]').send_keys("08002")
            browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/form/div[5]/select/option[2]').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/form/div[6]/select/optgroup[1]/option[1]').click()
            browser.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/form/div[7]/label").click()
            browser.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/form/div[8]/label").click()
            time.sleep(1)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-submit-lead-form-header-web-solicita-info-general-2--')]").click()
            time.sleep(3)
            print('ITEP: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('ITEP: Skipeado (ERROR)')

        #MasMovil Alarmas
        try:
            browser.get('https://masmovilalarmas.es/')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/main/div/section[1]/div[2]/div[1]/div[2]/div/div[2]/div[1]/a').click()
            time.sleep(2)
            browser.find_element_by_xpath("//*[starts-with(@id, 'BysidePhoneBySideData_')]").send_keys(number)
            browser.find_element_by_xpath("//*[starts-with(@id, 'BysideCallBtnBySideData_')]").click()
            try:
                browser.find_element_by_xpath("/html/body/div[51]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[1]/input[1]").click()
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            print('MasMovil Alarmas: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('MasMovil Alarmas: Skipeado (ERROR)')

        #Prosegur
        try:
            browser.get('https://www.prosegur.es/')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]/span').click()
                time.sleep(1)
            except:
                pass
            time.sleep(1)
            try:#Deisgn 1
                browser.find_element_by_xpath('//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[2]/div/input').send_keys(number)
                browser.find_element_by_xpath('//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[4]/div/fieldset/label/span').click()
                browser.find_element_by_xpath('//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[5]/div/div/div/button/span').click()
            except:
                pass
            try:#Design 2
                browser.find_element_by_xpath('/html/body/main/div/section/div/div/div[2]/section[2]/div/div/div/div/div[1]/div[2]/form/div[2]/div[2]/div/input').send_keys(number)
                browser.find_element_by_xpath('/html/body/main/div/section/div/div/div[2]/section[2]/div/div/div/div/div[1]/div[2]/form/div[2]/div[4]/div/fieldset/label/span').click()
                browser.find_element_by_xpath('/html/body/main/div/section/div/div/div[2]/section[2]/div/div/div/div/div[1]/div[2]/form/div[2]/div[5]/div/div/div/button/span').click()
            except:
                pass
            time.sleep(3)
            print('Prosegur: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Prosegur: Skipeado (ERROR)')

        #LineaDirecta
        try:
            browser.get('https://www.lineadirecta.com/te-llamamos-gratis.html?idServicio=http0036&from=B009975&indVehiculo=C')
            time.sleep(4)
            try: #Cookies
                browser.find_element_by_xpath('//button[@id="didomi-notice-agree-button"]').click()
            except:
                pass
            browser.find_element_by_xpath('//*[@id="telefono-numerico"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="btn1"]').click() # Buttom 1
            time.sleep(2)
            print('Linea Directa: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Linea Directa: Skipeado (ERROR)')


        #Telecable
        try:
            browser.get('http://marcador-c2c.alisys.net/telecablec2c_v2/c2c.php')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="numero"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/button').click()
            time.sleep(3)
            print('Telecable: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Telecable: Skipeado (ERROR)')

        #Mapfre
        try:
            browser.get('https://www.mapfre.es/boi/inicio.do?origen=autos_portalmapfre&destino=sgc_new&producto=autos')
            time.sleep(2)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('//*[@id="nombre"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="primer_apellido"]').send_keys(surname)
            browser.find_element_by_xpath('//*[@id="codigo_postal"]').send_keys("08002")
            browser.find_element_by_xpath('//*[@id="tlfn"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="marca_robinson"]').click()
            browser.find_element_by_xpath('//*[@id="politicaprivacidad"]').click()
            browser.find_element_by_xpath('/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input').click()
            time.sleep(3)
            print('Mapfre: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Mapfre: Skipeado (ERROR)')

        #Orange
        try:
            if current_time > start and current_time < end:
                browser.get('https://selectra.es/internet-telefono/companias/orange/telefono')
                time.sleep(2)
                try: #Cookies
                    browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div/div[3]/div/button[3]').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/aside/div[1]/div[1]/div/div/div[1]/a[2]').click()
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="callback-modal__phone"]').send_keys(number)
                browser.find_element_by_xpath('//*[@id="callback-modal__submit"]').click()
                time.sleep(3)
                print('Orange: OK')
            else:
                print('Orange: Skipeado (Fuera de Horario)')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Orange: Skipeado (ERROR)')

        #HomeGO
        try:
            browser.get('https://homego.es/alarmas-para-casa-precios-no-cliente')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.execute_script("window.scrollBy(0, 500);")
            time.sleep(3)
            try: #Hora
                browser.find_element_by_xpath("//*[starts-with(@id, 'BysideScheduleBySideData_')]/option[2]").click()
            except:
                pass
            browser.find_element_by_xpath("//*[starts-with(@id, 'BysidePhoneBySideData_')]").send_keys(number)
            browser.find_element_by_xpath("//*[starts-with(@id, 'BysideCallBtnBySideData_')]").click()
            try:
                browser.find_element_by_xpath("/html/body/div[82]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/input[1]").click()
                time.sleep(2)
            except:
                pass
            time.sleep(1)
            print('HomeGO: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('HomeGO: Skipeado (ERROR)')

        #Iberdrola
        try:
            browser.get('https://www.iberdrola.es/')
            time.sleep(4)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="telf-lc-header"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="checks"]/div[1]/label').click()
            browser.find_element_by_xpath('//*[@id="checks"]/div[2]/label').click()
            browser.find_element_by_xpath('//*[@id="btn-click-to-call-luz"]/span').click()
            time.sleep(3)
            print('Iberdrola: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Iberdrola: Skipeado (ERROR)')

        #iSalud
        try:
            browser.get('https://asisa.isalud.com/llama-gratis')
            time.sleep(4)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="email"]').send_keys(email)
            browser.find_element_by_xpath('/html/body/div[1]/section[1]/div[2]/form/div/div[5]/div/a').click()
            browser.find_element_by_xpath('//*[@id="contact_freecall"]').click()
            time.sleep(3)
            print('iSalud: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('iSalud: Skipeado (ERROR)')

        #iSalud2
        try:
            payload = {'name': name, 'surname': surname, 'email': email, 'number': number}
            requests.post('https://vsec.es/llamada.php', data=payload)
        except:
            pass

        #Recordador
        try:
            payload = {'phoneNumber': '34'+number}
            files=[]
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://recordador.com/',
            'Origin': 'https://recordador.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=0',
            'Cookie': 'ci_connect_pabbly_sesion=deehc3mngn2kmr42jkt5aotfcdmab2f1'}
            response = requests.request("POST", 'https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NjUwNTY5MDYzNTA0M2M1MjZmNTUzNTUxMzci_pc', headers=headers, data=payload, files=files)
            if response.status_code == 200:
                print('Recordador: OK')
        except:
            print('Recordador (ERROR)')
    
        #proyectosyseguros
        try:
            browser.get('https://www.proyectosyseguros.com/te-llamamos/')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="Nombre"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="Email"]').send_keys(email)
            browser.find_element_by_xpath('//*[@id="Telefono"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[3]/main/div/div/div/div/div/form/div[3]/div/div[1]/select/option[2]').click()
            browser.find_element_by_xpath('//*[@id="acepto_condiciones"]').click()
            browser.find_element_by_xpath('/html/body/div[3]/main/div/div/div/div/div/form/div[6]/button/span[1]').click()
            time.sleep(3)
            print('Proyectos y Seguros: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Proyectos y Seguros: Skipeado (ERROR)')

        #MoneyGO
        try:
            browser.get('https://ctc.moneygo.es/money-go-ctc-web/ctc/04f25d44-f1ce-4554-ba40-57211f7133ce')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="telefono"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/create-ctc/div[2]/form/div[4]/div/label').click()
            browser.find_element_by_xpath('/html/body/div[1]/create-ctc/div[2]/form/button').click()
            time.sleep(3)
            print('MoneyGO: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('MoneyGO: Skipeado (ERROR)')

        #emagister
        try:
            browser.get('https://www.emagister.com/')
            time.sleep(2)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('/html/body/header/div[2]/div/div[3]/div/nav/div[1]/div/div/section[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="callMe-phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/div/div[2]/form/p/label/span[2]').click()
            browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/div/div[2]/form/button').click()
            time.sleep(3)
            print('emagister: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('emagister: Skipeado (ERROR)')

        #Mundo-R
        try:
            browser.get('https://mundo-r.com/es')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="c2c-submit"]').click()
            time.sleep(3)
            print('Mundo-R OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Mundo-R Skipeado: (ERROR')

        #homeserve
        try:
            browser.get('https://www.homeserve.es/servicios-reparaciones/fontaneros')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="basicCookies"]/div/div[2]/div[3]/div/button').click()
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[2]/select/option[2]').click()
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[5]/input[1]').send_keys(name)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[5]/input[2]').send_keys(surname)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[6]/input[1]').send_keys(number)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[6]/input[2]').send_keys(email)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[7]/input').click()
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[9]/button').click()
            time.sleep(1)
            print('homeserve: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('homeserve: Skipeado (ERROR)')

        #clinicaboccio
        try:
            browser.get('https://www.clinicaboccio.com/pide-cita/')
            time.sleep(3)
            try: #Cokies
                browser.find_element_by_xpath('//*[@id="cmplz-cookiebanner-container"]/div/div[6]/button[1]').click()
            except:
                pass
            browser.find_element_by_xpath('//*[@id="input_5_1"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="input_5_4"]').send_keys(number)
            browser.execute_script("window.scrollBy(0, 600);")
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="input_5_5_1"]').click()
            browser.find_element_by_xpath('//*[@id="gform_submit_button_5"]').click()
            time.sleep(2)
            print('Clinica Boccio: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Clinica Boccio: Skipeado (ERROR)')

        #MásMóvil
        try:
            browser.get('https://www.masmovil.es/empresas/negocios-autonomos')
            time.sleep(2)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath("//*[starts-with(@id, 'BysidePhoneBySideData_')]").send_keys(number)
            try: #Horario
                browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/fieldset/label/select/option[2]').click()
            except:
                pass
            browser.find_element_by_xpath("//*[starts-with(@id, 'BysideCallBtnBySideData_')]").click()
            time.sleep(2)
            try: #Encuesta
                browser.find_element_by_xpath("//*[starts-with(@id, 'BysideEncuestaBySideData_')]").click()
                time.sleep(2)
            except:
                pass
            time.sleep(2)
            print('MasMovil: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('MasMovil: Skipeado (ERROR)')

        #ElPaso2000
        try:
            browser.get('https://www.elpaso2000.com/te-llamamos/')
            time.sleep(1)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[1]/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/label/span').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[3]/button/span').click()
            time.sleep(2)
            print('ElPaso2000: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('ElPaso2000: Skipeado (ERROR)')

        #Alarmak
        try:
            browser.get('https://euskaltelalarmak.com/')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/main/div/section[2]/div[2]/div[1]/div[2]/div[2]/button').click()
            time.sleep(2)
            browser.find_element_by_xpath("//*[starts-with(@id, 'BysidePhoneBySideData_')]").send_keys(number)
            browser.find_element_by_xpath("//*[starts-with(@id, 'submit_btBySideData_')]").click()
            try:
                browser.find_element_by_xpath("//*[starts-with(@id, 'btn-quieroBySideData_')]").click()
                time.sleep(2)
            except:
                pass
            time.sleep(1)
            print('Alarmak: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Alarmak: Skipeado (ERROR)')

        #centrodermatologicoestetico
        try:
            browser.get('https://www.centrodermatologicoestetico.com/te-llamamos/')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="cookie_action_close_header"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[5]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="international_PhoneNumber_countrycode"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[7]').send_keys(email)
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/div/div/div/input').click()
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/button').click()
            time.sleep(2)
            print('centrodermatologicoestetico: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('centrodermatologicoestetico: Skipeado (ERROR)')

        #Mutua Madrileña
        try:
            browser.get('https://www.mutua.es/recursos/html/404.htm')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="consent_prompt_submit"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('//*[@id="nombreformC2C2"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="telefonoformC2C2"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/form/div/div/div/div[4]/div[3]/label').click()
            browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/form/div/div/div/div[5]/div/a').click()
            time.sleep(2)
            print('Mutua: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Mutua: Skipeado (ERROR)')

        #generali
        try:
            browser.get('https://www.generali.es/blog/tuasesorsalud/solicitar-informacion/')
            time.sleep(3)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[1]/div[2]/label').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="cmb-form--name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="cmb-form--phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div[3]/select/option[2]').click()
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div[4]/select/option[2]').click()
            element = browser.find_element_by_xpath("//div[contains(@class, 'container-tooltip-autorization-text')]")
            browser.execute_script("arguments[0].click();", element)
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[3]/button/span').click()
            time.sleep(5)
            print('Generali: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Generali: Skipeado (ERROR)')

        #FiNetwork
        try:
            browser.get('https://finetworkonline.com/')
            time.sleep(2)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="banner"]/div[2]/a[3]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('//*[@id="form-field-name"]').send_keys(number)
            browser.find_element_by_xpath("//*[starts-with(@id, 'form-field-field_')]").click()
            browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[4]/div/form/div/div[4]/button/span/span[2]').click()
            time.sleep(1)
            print('FiNetwork: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('FiNetwork: Skipeado (ERROR)')

        #Nara
        try:
            browser.get('https://www.naradigital.es/te-llamamos')
            time.sleep(2)
            try: #Cookies
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_embCTC_txtNombre"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_embCTC_txtTelefono"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_embCTC_txtEmail"]').send_keys(email)
            browser.find_element_by_xpath('/html/body/form/div[3]/div[1]/div[3]/div/div/div/div[1]/div[2]/div[1]/div[6]/div/label[2]/select/option[2]').click()
            time.sleep(5)
            try:
                browser.find_element_by_xpath('/html/body/form/div[3]/div[1]/div[3]/div/div/div/div[1]/div[2]/div[1]/div[8]/div/label[2]/select/option[2]').click()
                time.sleep(5)
            except:
                pass
            try:
                browser.find_element_by_xpath('/html/body/form/div[3]/div[1]/div[3]/div/div/div/div[1]/div[2]/div[1]/div[7]/div/label[2]/select/option[2]').click()
                time.sleep(5)
            except:
                pass
            time.sleep(5)
            browser.find_element_by_xpath('/html/body/form/div[3]/div[1]/div[3]/div/div/div/div[1]/div[2]/div[1]/div[8]/div/div/label/i').click()
            browser.find_element_by_xpath('//*[@id="btnLlamar"]').click()
            time.sleep(1)
            print('Nara: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Nara: Skipeado (ERROR)')
        

        #regal
        try:
            browser.get('https://te-llamamos.regal.es/user-details')
            time.sleep(3)
            browser.find_element_by_xpath('(//*[@id="primaryPhoneInput"])[1]').send_keys(number)
            browser.find_element_by_xpath('(//*[@id="primaryPhoneInput"])[2]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="continueButton"]').click()
            time.sleep(2)
            print('Regal: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Regal: Skipeado (ERROR)')

        if repeat == 1:
            browser.close()
            print('Repeat ON')
        else:
            if args.start:
                try:
                    browser.close()
                except:
                    pass
                sys.exit()
            else:
                browser.quit()
                break

#Menu
def modo_automatico():
    print('Activando Modo automatico...')
    time.sleep(0.5)
    formulario()
    main()

def modo_porculero():
    print("MODO NO DISPONIBLE")
    time.sleep(2)

def modo_nocturno():
    print("MODO NO DISPONIBLE")
    time.sleep(2)


submenu_selection_menu = SelectionMenu(
    ["En construcción", "En construcción"],
    title="Modo Contrareembolso",
    exit_option_text="Volver al menu princiipal")
submenu_item = SubmenuItem("Modo Contrareembolso", submenu=submenu_selection_menu, menu=menu)

# Crear los ítems del menú
item1 = FunctionItem("Modo Automático", modo_automatico)
item2 = FunctionItem("Modo Porculero", modo_porculero)
item3 = FunctionItem("Modo Nocturno", modo_nocturno)

# Añadir los ítems al menú
menu.append_item(item1)
menu.append_item(item2)
menu.append_item(item3)
menu.append_item(submenu_item)

if args.start:
    global number, name, surname, email
    name, surname, number, email = args.start
    main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda sig, frame: handle_interrupt(browser))
    menu.show()
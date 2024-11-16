from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime
import warnings
import requests
import json
import colorama
from colorama import Fore, Style
from consolemenu import *
from consolemenu.items import *
import signal
import sys
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import time
import os
from os import system

version = 'Beta 2.1'
global debug
debug = 0

system("title " 'PerubianBot '+version)

global perubian
perubian = Fore.MAGENTA + Style.BRIGHT + r"""
  _____                _     _               ___   __ 
 |  __ \              | |   (_)             |__ \ /_ |
 | |__) |__ _ __ _   _| |__  _  __ _ _ __      ) | | |
 |  ___/ _ \ '__| | | | '_ \| |/ _` | '_ \    / /  | |
 | |  |  __/ |  | |_| | |_) | | (_| | | | |  / /_ _| |
 |_|   \___|_|   \__,_|_.__/|_|\__,_|_| |_| |____(_)_|
""" + Style.RESET_ALL

menu = ConsoleMenu(Fore.YELLOW + perubian, "Seleccione un modo"+ Style.RESET_ALL)

#Firefox Configuration
def firefoxsetup():
    global binary, profile, PATH_TO_DEV_NULL
    if os.name == 'nt':  # Windows
        binary = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        PATH_TO_DEV_NULL = 'nul'
    elif os.uname().sysname == 'Darwin':  # macOS
        binary = '/Applications/Firefox.app/Contents/MacOS/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    else:
        binary = '/usr/bin/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.autoplay.default", 0)
    profile.accept_untrusted_certs = True
    profile.set_preference("media.volume_scale", "0.0")

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
        global number, name, surname
        number, name, surname, email = '666666666', 'NombrePrueba', 'ApellidoPrueba', 'CorreoPrueba@gmail.com'
    else:
        datos_persona = ''
        number = pregunta_estilizada('Nº de Teléfono: ')
        while len(number) != 9 or not number.isdigit() or number[0] not in prefijos:
            number = pregunta_estilizada('Número incorrecto. Ingrese Nº de Teléfono nuevamente: ')
        datos_persona += Fore.WHITE + Style.BRIGHT + f"Nº de Teléfono: {number}\n" + Style.RESET_ALL

        name = pregunta_estilizada('Nombre de la persona: ', datos_previos=datos_persona, validacion=validacion_no_vacia)
        surname = pregunta_estilizada('Apellido: ', datos_previos=datos_persona, validacion=validacion_no_vacia)
        nombre_completo = Fore.WHITE + Style.BRIGHT + f"Nombre: {name} {surname}\n" + Style.RESET_ALL
        datos_persona += nombre_completo

        email = pregunta_estilizada('Si no indicas email se va a introducir: ' + name.lower() + surname.lower() + '@gmail.com' + '\nCorreo: ', datos_persona)
        if not email:
            email = f'{name.lower()}.{surname.lower()}@gmail.com'
        datos_persona += Fore.WHITE + Style.BRIGHT + f"Correo: {email}\n" + Style.RESET_ALL

    # Después de recopilar toda la información, puedes mostrar datos_persona
    clear_console()
    print(perubian)
    print(datos_persona)

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

    repeat = input('Modo repetición [S/N]: ').lower()
    if repeat in ('y', 'yes', 's', 'si'):
        repeat = 1
        
    global interrupted
    while not interrupted:
        firefoxsetup()
        global browser
        if getattr(sys, 'frozen', False):
            geckodriver_path = os.path.join(sys._MEIPASS, 'geckodriver')
        else:
            geckodriver_path = 'geckodriver'
        browser = webdriver.Firefox(firefox_binary=binary, executable_path = geckodriver_path, firefox_profile=profile, service_log_path=PATH_TO_DEV_NULL)
        
        #SECURITAS DIRECT
        if interrupted:
            print("galleta")
        try:
            browser.get('https://www.securitasdirect.es/')
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click() #Cookies
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="edit-telefono1"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="edit-submit"]').click()
            time.sleep(1)
            if(browser.current_url == 'https://www.securitasdirect.es/error-envio'):
                print('Securitas Direct: Skipeado (Limite Excedido)')
            else:
                print('Securitas Direct: OK')
        except Exception as e:
            print('Securitas Direct: Skipeado (ERROR)')

        #Vodafone
        if interrupted:
            break    
        try:
            browser.get('https://www.vodafone.es/c/empresas/pymes/es/conectividad/red-infinity/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[2]/main/div[9]/div/div/div/span/div/div/div/form-viewer/div/form/fieldset/div[2]/app-form-element-dispatcher[2]/span/app-select-element/div/div/div/select/option[1]').click()
            browser.find_element_by_xpath('//*[@name="enterprise"]').send_keys(name)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[9]/div/div/div/span/div/div/div/form-viewer/div/form/fieldset/div[3]/app-form-element-dispatcher[3]/span/app-select-element/div/div/div/select/option[2]').click()
            browser.find_element_by_xpath('//*[@name="givenName"]').send_keys(name)
            browser.find_element_by_xpath('//*[@name="familyName"]').send_keys(surname)
            browser.find_element_by_xpath('//*[@name="phoneNumber"]').send_keys(number)
            browser.find_element_by_xpath('//*[@name="emailAddress"]').send_keys(email)
            time.sleep(1)
            browser.find_element_by_xpath("//input[@type='checkbox' and contains(@class, 'fe-viewer__checkbox')]").click()
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[9]/div/div/div/span/div/div/div/form-viewer/div/form/fieldset/div[5]/app-form-element-dispatcher[4]/span/app-button-submit-element/div/div/button').click()
            time.sleep(8)
            print('Vodafone: OK')
        except:
            print('Vodafone: Skipeado (ERROR)')

        #euroinnova
        if interrupted:
            break
        try:
            browser.get('https://www.euroinnova.edu.es/cursos#formulario')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="accept-cookies"]').click() #Cookies
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/button').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="mail"]').send_keys(email)
            browser.find_element_by_xpath('//*[@id="tel"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[9]/div/div/div[3]/form/div[3]/div[2]/div/select/option[10]').click()
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
                try:
                    browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/article/div/div/div/div/div/form/section/div/div[2]/div/select/option[2]').click()
                browser.find_element_by_xpath('//*[@id="edit-por-quien-preguntamos-"]').send_keys(name)
                browser.find_element_by_xpath('//*[@id="edit-phone"]').send_keys(number)
                browser.find_element_by_xpath('//*[@id="edit-phone-confirmation"]').send_keys(number)

                browser.find_element_by_xpath('//*[@id="edit-actions-submit"]').click()
                time.sleep(1)
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
            try:
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cookies
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="c2c-submit"]/span').click()
            time.sleep(3)
            print('Racctel+ OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Racctel+ Skipeado: ERROR')

        #JAZZTEL
        try:
            browser.get('https://llamamegratis.es/jazztel/v2/webphone.html?lang=es-ES&isLandingLander=1&typeOrigin=wphFollow&widget=3294&wphUrl#https://www.telefonojazztel.es/')
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="phoneNumber"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="env"]').click()
            time.sleep(3)
            print('Jazztel: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Jazztel: Skipeado (ERROR)')

        #Euskaltel
        try:
            browser.get('https://www.euskaltel.com/?idioma=esp')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cookies
                time.sleep(1)
            except:
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="c2c-submit"]/span').click()
            time.sleep(3)
            print('Euskaltel OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Euskaltel Skipeado: ERROR')

        #ITEP
        try:
            browser.get('https://www.itep.es/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/button[1]').click() # Cookies
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('//*[@id="block-cabecerasolicitainformacion"]/p/button').click() # Solicitar Informacion
            time.sleep(1)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-name--')]").send_keys(name)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-email--')]").send_keys(email)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-phone--')]").send_keys(number)
            browser.find_element_by_xpath('//*[@id="edit-cp--2"]').send_keys("08002")
            browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/form/div[5]/select/option[2]').click()
            browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/form/div[6]/select/optgroup[1]/option[4]').click()
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-conditions--')]").click()
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-educa-consent--')]").click()
            time.sleep(1)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-submit-lead-form-header-web-solicita-info-general-2--')]").click()
            time.sleep(3)
            print('ITEP: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('ITEP: Skipeado (ERROR)')

        #Prosegur
        try:
            browser.get('https://www.prosegur.es/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]/span').click()
                time.sleep(1)
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[2]/div/input').send_keys(number)
            browser.find_element_by_xpath('//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[4]/div/fieldset/label/span').click()
            browser.find_element_by_xpath('//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[5]/div/div/div/button/span').click()
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
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//button[@id="didomi-notice-agree-button"]').click()
            except:
                pass
            browser.find_element_by_xpath('//*[@id="telefonoC2c"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/div[2]/div/form/div[5]/a').click() # Buttom 1
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
            browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="nombre"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="primer_apellido"]').send_keys(surname)
            browser.find_element_by_xpath('//*[@id="codigo_postal"]').send_keys("08002")
            browser.find_element_by_xpath('//*[@id="tlfn"]').send_keys(number)
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
            browser.get('https://selectra.es/internet-telefono/companias/orange/telefono')
            time.sleep(2)
            try:
                browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/button[1]').click() #Cookies
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/aside/div[1]/div[1]/div/div/div[1]/a[2]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="callback-modal__phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="callback-modal__submit"]').click()
            time.sleep(3)
            print('Orange: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Orange: Skipeado (ERROR)')

        #Selectra
        try:
            browser.get('https://ww.selectra.es/contact-internet')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/label/span[1]').click()
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/input[3]').click()
            time.sleep(3)
            print('Selectra: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Selectra: Skipeado (ERROR)')

        #Iberdrola
        try:
            browser.get('https://www.iberdrola.es/')
            time.sleep(4)
            try:
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cookies
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

        #emagister
        try:
            browser.get('https://www.emagister.com/')
            time.sleep(2)
            try:
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cookies
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('/html/body/header/div[2]/div/div[3]/div/nav/div[1]/div/div/section[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="callMe-phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/p/label/span[2]').click()
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/button').click()
            time.sleep(3)
            print('emagister: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('emagister: Skipeado (ERROR)')

        #homeserve
        try:
            browser.get('https://www.homeserve.es/servicios-reparaciones/fontaneros')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="basicCookies"]/div/div[2]/div[3]/div/button').click() #Cookies
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
            try:
                browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/button[1]').click() #Cokies
            except:
                pass
            browser.find_element_by_xpath('//*[@id="input_5_1"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="input_5_4"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="input_5_5_1"]').click()
            browser.find_element_by_xpath('//*[@id="gform_submit_button_5"]').click()
            time.sleep(2)
            print('Clinica Boccio: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Clinica Boccio: Skipeado (ERROR)')

        #pontgrup
        try:
            browser.get('https://www.pontgrup.com/contacto/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div[2]/button[2]').click() #Cookies
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/nav/div/ul/li[4]/a/span').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="nombre-popup"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="telefono-popup"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/section/div/div/div/div/div/form/div[3]/div[1]/select/option[3]').click()
            browser.find_element_by_xpath('//*[@id="terminos-popup"]').click()
            browser.find_element_by_xpath('//*[@id="btn-submit-popup"]').click()
            time.sleep(2)
            print('PontGrup: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('PontGrup: Skipeado (ERROR)')

        #ElPaso2000
        try:
            browser.get('https://www.elpaso2000.com/te-llamamos/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="elpaso-button-accept"]').click() #Cookies
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[1]/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/label/span').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[3]/button/span').click()
            time.sleep(2)
            print('ElPaso2000: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('ElPaso2000: Skipeado (ERROR)')

        #centrodermatologicoestetico
        try:
            browser.get('https://www.centrodermatologicoestetico.com/te-llamamos/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="cookie_action_close_header"]').click() #Cookies
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

        #generali
        try:
            browser.get('https://www.generali.es/blog/tuasesorsalud/solicitar-informacion/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                time.sleep(2)
            except:
                pass
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[1]/div[2]/label').click()
            browser.find_element_by_xpath('//*[@id="cmb-form--name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="cmb-form--phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div[3]/select/option[2]').click()
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div[4]/select/option[2]').click()
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div[8]/div/label').click()
            browser.find_element_by_xpath('/html/body/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[3]/button/span').click()
            time.sleep(5)
            print('Generali: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Generali: Skipeado (ERROR)')

        #regal
        try:
            browser.get('https://te-llamamos.regal.es/user-details')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="primaryPhoneInput"][1]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="primaryPhoneInput"][2]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="continueButton"]')
            time.sleep(5)
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
            browser.quit()
            break

#Menu
def modo_automatico():
    print('Activando Modo automatico...')
    time.sleep(1)
    formulario()
    main()

def modo_porculero():
    print("MODO NO DISPONIBLE")
    time.sleep(2)

def modo_nocturno():
    print("MODO NO DISPONIBLE")
    time.sleep(2)


submenu_selection_menu = SelectionMenu(["subitem1", "subitem2", "subitem3"], title="Modo Contrareembolso")
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


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda sig, frame: handle_interrupt(browser))
    menu.show()
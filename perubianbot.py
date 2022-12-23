from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import keys_to_typing
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import requests

import time
import os
from os import system
system("title " 'PerubianBot')

#Ubicación Firefox
if os.name == 'nt':
    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
else:
    binary = FirefoxBinary('/usr/bin/firefox')

postalcode = '08002'
debug = 1  #1 = Enable     #0 = Disabled

prefijos = ('6', '7')

#Limite hora
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
start = '10:40:00'
end = '22:00:00'

global null
null = ''

version = '1.2'

print('PerubianBot V'+version+ '')
print('')

if(debug == 0):
    while True:
        number = input('Nº de Teléfono: ')
        if number and len(number) < 9:
            number = null
        if number and len(number) > 9:
            number = null
        if not number.startswith(prefijos):
            number = null
        if(number == null):
            print('')
            print('Número incorrecto')
        if number is not null:
            break
    name = input('Nombre de la persona: ')
    surname = input('Apellido: ')
    email = input('Correo: ')
    if(email == null):
        email = name+surname
    while True:
        repeat = input('Modo repetición [S/N]: ').lower()
        print('REPEAT: '+repeat)
        if repeat not in ('s', 'n', 'y', 'si' 'no', 'yes'):
            repeat = null
        if repeat in ('s', 'n', 'y'):
            print('Iniciando')
        if repeat is not null:
            break
if(debug == 1):
    print('DEBUG MODE ON')
    number = '666666666'
    name = 'NombrePrueba'
    surname = 'ApellidoPrueba'
    email = 'CorreoPruea@gmail.com'
    while True:
        repeat = input('Modo repetición [S/N]: ').lower()
        print('REPEAT: '+repeat)
        if repeat not in ('s', 'n', 'y', 'si' 'no', 'yes'):
            repeat = null
        if repeat in ('s', 'n', 'y'):
            print('Correcto')
        if repeat is not null:
            break
    print('DATOS: '+number+' '+name+' '+surname)
    print('REPEAT: '+repeat)

print('')

system("title " 'PerubianBot: '+number)

while True: #Modo Repetición
    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.autoplay.default", 0)
    profile.accept_untrusted_certs = True
    PATH_TO_DEV_NULL = 'nul'

    securitas = 'https://www.securitasdirect.es/'
    securitaserror = 'https://www.securitasdirect.es/error-envio'
    jazztel = 'http://llamamegratis.es/jazztel/v2/webphone.html?lang=es-ES&isLandingLander=1&widget=1197&wphUrl#https://www.contratarjazztel.es/'
    genesis = 'https://www.genesis.es/c2c'
    euskaltel = 'https://www.euskaltel.com/CanalOnline/particulares/general/tarifa-family-mas-lineas-adicionales?idioma=esp'
    itep = 'https://www.itep.es/llamada-gratuita'
    proyectosyseguros = 'https://www.proyectosyseguros.com/te-llamamos/'
    tutfgamedida = 'https://tutfgamedida.com/llamame/'
    prosegur = 'https://www.prosegur.es/esp/alarmahogar/sem'
    pepephone = 'https://www.pepephone.com/'
    lineadirecta = 'https://www.lineadirecta.com/te-llamamos-gratis.html?idServicio=http0036&from=B009975&indVehiculo=C'
    telecable = 'http://marcador-c2c.alisys.net/telecablec2c_v2/c2c.php'
    cofidis = 'https://www.cofidis.es/es/contactanos/telefono-cofidis.html'
    desguacesolivares = 'http://desguacesolivares.es/Llamame.aspx'
    mapfre = 'https://www.mapfre.es/boi/inicio.do?origen=autos_portalmapfre&destino=sgc_new&producto=autos'
    orange = 'https://selectra.es/internet-telefono/companias/orange/telefono'
    selectra = 'https://ww.selectra.es/contact-internet'
    carglass = 'https://www.carglass.es/contacto'
    iberdrola = 'https://www.iberdrola.es/'
    digi = 'https://www.digimobil.es/contacto.php?act=pag-detail&idPage=483'
    movistar = 'https://promomovistar.es/sem-empresas/oferta-empresas-fusionpro-300.php?sem=ddb-emp-fusionpro'
    ptv = 'https://ptvtelecom.com/wp-content/themes/divi/interesa.php'
    mfollanaortodoncia = 'https://www.mfollanaortodoncia.com/contactar/'
    autointegrale = 'https://autointegrale.com/llamada-gratuita/'
    isalud = 'https://www.isalud.com/llama-gratis'
    clinicaboccio = 'https://www.clinicaboccio.com/pide-cita/'
    pontgrup = 'https://www.pontgrup.com/contacto/'
    tarifasonline = 'https://www.tarifasonline.com/companias-telefonicas/pepephone/'
    generali = 'https://www.generali.es/blog/tuasesorsalud/solicitar-informacion/'
    doctorpuchol = 'https://www.doctorpuchol.es/le-llamamos-gratis/'
    vodafone = 'https://www.vodafone.es/c/empresas/pymes/es/conectividad/red-infinity/'
    masmovil = 'https://www.masmovil.es/contacto/'
    yoigo = 'https://www.yoigo.com/ayuda/como-contactar-con-atencion-al-cliente-de-yoigo'
    pelayo = 'https://www.pelayo.com/nosotros_te_llamamos/tellamamos'
    euroinnova = 'https://www.euroinnova.edu.es/formulario-llamamos-gratis#formulario'
    instalium = 'https://www.instalium.es/et-truquem-gratis/'
    obesan = 'https://obesan.com/te-llamamos-nosotros/'
    elpaso2000 = 'https://www.elpaso2000.com/te-llamamos/'
    urologiaclinicabilbao = 'https://www.urologiaclinicabilbao.com/te-llamamos.php'
    centrodermatologicoestetico = 'https://www.centrodermatologicoestetico.com/te-llamamos/'
    cerrajeriasoler = 'https://cerrajeriasoler.es/cerrajeria-urgente-24-horas/'
    audipro = 'http://audipro.es/te-llamamos-gratis/'
    aluminioscancuyas = 'http://www.aluminioscancuyas.com/te-llamamos-gratis/'
    repuestoschimeneas = 'https://repuestoschimeneas.es/tellamamos'
    emagister = 'https://www.emagister.com/'
    homeserve = 'https://www.homeserve.es/servicios-reparaciones/fontaneros'
    regal = 'https://te-llamamos.regal.es/user-details'
    virgin = 'https://virgintelco.es/contacto'

    profile.set_preference("media.volume_scale", "0.0")
    browser = webdriver.Firefox(firefox_binary=binary, executable_path = './geckodriver', firefox_profile=profile, service_log_path=PATH_TO_DEV_NULL)


    #SECURITAS DIRECT
    try:
        browser.get(securitas)
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click() #Cookies
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="edit-telefono1"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="edit-submit"]').click()
        time.sleep(1)
        if(browser.current_url == securitaserror):
            print('Securitas Direct: Skipeado (Limite Excedido)')
        else:
            print('Securitas Direct: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Securitas Direct: Skipeado (ERROR)')

    #Vodafone
    try:
        browser.get(vodafone)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div/div/div/span/div/div/section/div[2]/div[2]/div[2]/div/div/div/div[2]/form/div/div[1]/div/div/div[2]/div[2]/button').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div/main/div[5]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[1]/div[2]/label').click()
        browser.find_element_by_xpath('//*[@id="facade-firstName"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="facade-lastName"]').send_keys(surname)
        browser.find_element_by_xpath('//*[@id="facade-entreprise"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="facade-phoneNumber"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="facade-email"]').send_keys(email)
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div/main/div[5]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[9]/div[1]/label').click()
        browser.find_element_by_xpath('/html/body/div[1]/div/main/div[5]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[9]/div[2]/label').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div/main/div[5]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[10]/button/span[1]').click()
        time.sleep(5)
        print('Vodafone: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Vodafone: Skipeado (ERROR)')


    """#Doctor Puchol
    try:
        browser.get(doctorpuchol)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="cookie-law-button-ok"]').click() #Cookies
        browser.find_element_by_xpath('//*[contains(@id,"iphorm_1_3_")]').send_keys(name)
        browser.find_element_by_xpath('//*[contains(@id,"iphorm_1_4_")]').send_keys(surname)
        browser.find_element_by_xpath('//*[contains(@id,"iphorm_1_5_")]').send_keys(number)
        browser.find_element_by_xpath('//*[contains(@id,"iphorm_1_17_")]').send_keys(email)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div[2]/div[3]/div/div/div[1]/div/div[1]/div/select/option[2]').click()
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form/div/div[2]/div[8]/div[1]/button/span/em').click()
        time.sleep(3)
        print('Doctor Puchol: OK')
    except TimeoutException:
        pass
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Doctor Puchol: Skipeado (ERROR)')
        time.sleep(10)"""

    """#Carglass
    try:
        browser.get(carglass)
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="btn_accept_cookies"]').click() #Cookies
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div/article/div/div[4]/div/div/section[3]/div/div[2]/div[1]').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="edit-nombre"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="edit-apellido"]').send_keys(surname)
        browser.find_element_by_xpath('//*[@id="edit-telefono"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="edit-actions-submit"]').click()
        time.sleep(3)
        print('Carglass: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Carglass: Skipeado (ERROR)')"""

    #euroinnova
    try:
        browser.get(euroinnova)
        time.sleep(3)
        #browser.find_element_by_xpath('/html/body/section/article/div[5]/div[2]/div/div[1]/div[2]/div/div/div/div[6]/a').click()
        #time.sleep(1)
        browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="mail"]').send_keys(email)
        browser.find_element_by_xpath('//*[@id="tel"]').send_keys(number)
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="privacidad"]').click()
        browser.find_element_by_xpath('//*[@id="btn_enviar"]').click()
        time.sleep(3)
        print('Euroinnova: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Euroinnova: Skipeado (ERROR)')

    #Digi
    """try:
        browser.get(digi)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[4]/div/p[2]/a').click() #Cookies
        browser.find_element_by_xpath('/html/body/div[1]/nav/div[2]/div/ul[3]/li[4]/a/b').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="num"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/form/div[3]/div/label/span').click()
        browser.find_element_by_xpath('//*[@id="btn_c2c_send"]').click()
        time.sleep(3)
        print('Digi: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Digi: Skipeado (ERROR)')

    #MásMóvil
    try:
        browser.get(masmovil)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/mm-ui-cookie-disclaimer/div/div/div/div/div/div[2]/div/button').click() #Cookies
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/ui-view/div/div[1]/mm-ui-menu-top/div/div/div/div[2]/a[2]').click()
        browser.find_element_by_xpath('//*[contains(@id,"frm_phoneBySideData_")]').send_keys(number)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[7]/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[3]/input').click()
        time.sleep(3)
        print('MásMóvil: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('MásMóvil: Skipeado (ERROR)')"""

    #GENESIS
    try:
        if current_time > start and current_time < end:
            browser.get(genesis)
            time.sleep(8)
            browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/section/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/form/span/div[1]/div[1]/div[4]/select/option[2]').click()
            browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/section/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/form/span/div[1]/div[2]/div/button').click()
            time.sleep(1)
            print('Genesis: OK')
        else:
            print('Genesis: Skipeado (Fuera de Horario)')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Genesis: Skipeado (ERROR)')

    #JAZZTEL
    try:
        browser.get(jazztel)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="phoneNumber"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="env"]').click()
        time.sleep(3)
        jazztelerror = browser.find_element_by_xpath('//*[@id="statusErrorTitle"]')
        if jazztelerror.is_displayed():
            print('Jazztel: Skipeado (Error Interno)')
        else:
            print('Jazztel: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Jazztel: Skipeado (ERROR)')


    #Euskaltel
    try:
        browser.get(euskaltel)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cookies
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div/input').send_keys(number)
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/a').click()
        time.sleep(3)
        print('Euskaltel OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Euskaltel Skipeado: ERROR')

    #cerrajeriasoler
    """try:
        browser.get(cerrajeriasoler)
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[3]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/form/div[2]/span/input').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[3]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/form/div[3]/input').click()
        time.sleep(3)
        print('cerrajeriasoler: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('cerrajeriasoler: Skipeado (ERROR)')"""


    #instalium
    try:
        browser.get(instalium)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="avia_1_1"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="avia_2_1"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="avia_3_1"]').send_keys(email)
        browser.find_element_by_xpath('//*[@id="avia_4_1"]').send_keys('Me interesa')
        browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div/div/div[1]/form/fieldset/p[7]/input[2]').click()
        time.sleep(3)
        print('Instalium OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Instalium Skipeado: ERROR')

    #ITEP
    try:
        browser.get(itep)
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/button[1]').click() # Cookies
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[1]/div[1]/p/span/input').send_keys(name)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[2]/div[1]/p/span/input').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[2]/div[2]/p/span/div/select').click()
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/p[1]/span/div/select/option[3]').click()
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[6]/p/span/div/select/option[15]').click()
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/p[2]/span/div/select/option[1]').click()
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/p[3]/span[1]/span/span/label/input').click()
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/p[3]/span[2]/span/span/label/input').click()
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/p[4]/input').click()
        time.sleep(3)
        print('ITEP: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('ITEP Skipeado: ERROR')

    #Prosegur
    try:
        browser.get(prosegur)
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/button').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[2]/div/input').send_keys(number)
        browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[3]/div/fieldset/label/span').click()
        browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[4]/div/div/div/button/span').click()
        time.sleep(3)
        print('Prosegur: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('Prosegur: Skipeado (ERROR)')

    #LineaDirecta
    try:
        browser.get(lineadirecta)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="telefono"]').send_keys(number)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[1]/section/section/form/div[2]/div/div[2]/a').click()
        time.sleep(3)
        print('Linea Directa: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Linea Directa: Skipeado (ERROR)')


    #Telecable
    try:
        browser.get(telecable)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="numero"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/button').click()
        time.sleep(3)
        print('Telecable: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Telecable: Skipeado (ERROR)')


    #DesguacesOlivares
    """try:
        browser.get(desguacesolivares)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/form/div[4]/div/a[1]').click() #Cookies
        browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_TextBoxNombre"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_TextBoxTelefono"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/form/div[3]/div[1]/div/div[6]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/select/option[4]').click()
        browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_UEnviar1_SendData"]').click()
        time.sleep(3)
        print('Desguaces Olivares: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Desguaces Olivares: Skipeado (ERROR)')"""

    #Mapfre
    try:
        browser.get(mapfre)
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="nombre"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="primer_apellido"]').send_keys(surname)
        browser.find_element_by_xpath('//*[@id="codigo_postal"]').send_keys(postalcode)
        browser.find_element_by_xpath('//*[@id="tlfn"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="politicaprivacidad"]').click()
        browser.find_element_by_xpath('/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input').click()
        time.sleep(3)
        print('Mapfre: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Mapfre: Skipeado (ERROR)')

    #Orange
    try:
        browser.get(orange)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/button[1]').click() #Cookies
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/main/div[2]/div[1]/article/div/div[1]/p/a[2]').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="callback-modal__phone"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/section/div[3]/form/div[3]/label/span[1]').click()
        browser.find_element_by_xpath('//*[@id="callback-modal__submit"]').click()
        time.sleep(3)
        print('Orange: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Orange: Skipeado (ERROR)')

    #Selectra
    try:
        browser.get(selectra)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/input').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[2]/div/div/form/label/span[1]').click()
        browser.find_element_by_xpath('/html/body/div[2]/div/div/form/input[3]').click()
        time.sleep(3)
        print('Selectra: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Selectra: Skipeado (ERROR)')

    #Iberdrola
    try:
        browser.get(iberdrola)
        time.sleep(4)
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cookies
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="telf-lc-header"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div/div/div[3]/div/div[2]/form/div[2]/label').click()
        browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div/div/div[3]/div/div[2]/button/span').click()
        time.sleep(3)
        print('Iberdrola: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Iberdrola: Skipeado (ERROR)')

    #proyectosyseguros
    try:
        browser.get(proyectosyseguros)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/form/div[3]/div[2]/select/optgroup[1]/option[7]').click()
        browser.find_element_by_xpath('//*[@id="llamada-nombre"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="llamada-telefono"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="llamada-lopd"]').click()
        browser.find_element_by_xpath('//*[@id="llamada-enviar"]').click()
        time.sleep(3)
        print('Proyectos y Seguros: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Proyectos y Seguros: Skipeado (ERROR)')

    #Movistar
    """try:
        browser.get(movistar)
        time.sleep(2)
        movistartime = browser.find_element_by_xpath('//*[@id="horario"]')
        time.sleep(1)
        if movistartime.is_displayed():
            browser.find_element_by_xpath('//*[@id="txt_tlf"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/form/div[2]/div[2]/div[1]/select/option[2]').click()
            browser.find_element_by_xpath('//*[@id="chk_privacidad"]').click()
            browser.find_element_by_xpath('//*[@id="bt_go"]').click()
            time.sleep(5)
            print('Movistar: OK')
        else:
            browser.find_element_by_xpath('//*[@id="txt_tlf"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="chk_privacidad"]').click()
            browser.find_element_by_xpath('//*[@id="bt_go"]').click()
            time.sleep(5)
            print('Movistar: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Movistar: Skipeado (ERROR)')"""

    #aluminioscancuyas
    try:
        browser.get(aluminioscancuyas)
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="cookie_action_close_header"]').click() #Cookies
        browser.find_element_by_xpath('//*[@id="Telefono"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/section/div/div/div[2]/div/div/div/form/p[2]/span/input').send_keys(email)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/section/div/div/div[2]/div/div/div/form/p[3]/span/span/span/input').click()
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/section/div/div/div[2]/div/div/div/form/p[4]/span/span/span/input').click()
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/section/div/div/div[2]/div/div/div/form/p[5]/input').click()
        time.sleep(3)
        print('aluminioscancuyas: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('aluminioscancuyas: Skipeado (ERROR)')

    #urologiaclinicabilbao
    try:
        browser.get(urologiaclinicabilbao)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[1]/button[1]/span').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[1]/input').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[2]/input').send_keys(surname)
        browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[3]/input').send_keys(name)
        browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[2]/input').click()
        time.sleep(3)
        print('urologiaclinicaBilbao: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('urologiaclinicaBilbao: Skipeado (ERROR)')

    #repuestoschimeneas
    try:
        browser.get(repuestoschimeneas)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/section/form/ul/li[1]/input').send_keys(name)
        browser.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/section/form/ul/li[2]/input').send_keys(number)
        browser.find_element_by_xpath('//*[@id="boton-comprar"]').click()
        time.sleep(3)
        print('RepuestosChimeneas: OK')
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print('RepuestosChimeneas: Skipeado (ERROR)')

    #emagister
    try:
        browser.get(emagister)
        time.sleep(2)
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

    #mfollanaortodoncia
    try:
        browser.get(mfollanaortodoncia)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[1]/div[5]/a[1]').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="input_1_1"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="input_1_4"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div/div/div[2]/form/div[1]/ul/li[3]/div/div/select/option[1]').click()
        browser.find_element_by_xpath('//*[@id="input_1_5_1"]').click()
        browser.find_element_by_xpath('//*[@id="gform_submit_button_1"]').click()
        print('mfollanaortodoncia: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('mfollanaortodoncia: Skipeado (ERROR)')

    #homeserve
    try:
        browser.get(homeserve)
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/button').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[2]/select').click()
        browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[3]/input[1]').send_keys(name)
        browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[3]/input[2]').send_keys(surname)
        browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[4]/input[1]').send_keys(number)
        browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[4]/input[2]').send_keys(email)
        browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[5]/input').click()
        browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[6]/button').click()
        time.sleep(1)
        print('homeserve: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('homeserve: Skipeado (ERROR)')

    #isalud
    try:
        browser.get(isalud)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="email"]').send_keys(email)
        browser.find_element_by_xpath('/html/body/div[1]/section/div[2]/form/div/div[5]/div/a').click()
        browser.find_element_by_xpath('//*[@id="contact_freecall"]').click()
        print('iSalud: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('iSalud: Skipeado (ERROR)')

    #clinicaboccio
    try:
        browser.get(clinicaboccio)
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/button[1]').click() #Cokies
        browser.find_element_by_xpath('//*[@id="input_1_1"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="input_1_4"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div/div/div[2]/form/div[1]/ul/li[3]/div/div/select/option[1]').click()
        browser.find_element_by_xpath('//*[@id="input_1_5_1"]').click()
        browser.find_element_by_xpath('//*[@id="gform_submit_button_1"]').click()
        time.sleep(2)
        print('Clinica Boccio: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Clinica Boccio: Skipeado (ERROR)')

    #pontgrup
    try:
        browser.get(pontgrup)
        time.sleep(3)
        #browser.find_element_by_xpath('/html/body/div[3]/div[2]/button[2]').click() #Cookies
        browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/section/div[2]/div[2]/div/div/div/div/a').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="nombre-short"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="telefono-short"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="terminos-short"]').click()
        browser.find_element_by_xpath('//*[@id="btn-submit-short"]').click()
        time.sleep(2)
        print('PontGrup: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('PontGrup: Skipeado (ERROR)')

    #ElPaso2000
    try:
        browser.get(elpaso2000)
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[1]/input').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/label/span').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[3]/button/span').click()
        time.sleep(2)
        print('ElPaso2000: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('ElPaso2000: Skipeado (ERROR)')

    #centrodermatologicoestetico
    try:
        browser.get(centrodermatologicoestetico)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="cookie_action_close_header"]').click() #Cookies
        browser.find_element_by_xpath('//*[@id="form-field-nombre"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="form-field-telefono"]').send_keys(number)
        browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/div/div[3]/div/select/option[3]').click()
        browser.find_element_by_xpath('//*[@id="form-field-terminos"]').click()
        browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/div/div[5]/button/span/span[2]').click()
        time.sleep(2)
        print('centrodermatologicoestetico: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('centrodermatologicoestetico: Skipeado (ERROR)')

    #generali
    try:
        browser.get(generali)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[1]/div[2]/label').click()
        browser.find_element_by_xpath('//*[contains(@id,"email")]').send_keys(email)
        browser.find_element_by_xpath('//*[contains(@id,"firstname")]').send_keys(name)
        browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div/form/div[3]/div[1]/div/select/option[2]').click()
        browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div/form/div[3]/div[2]/div/select/option[2]').click()
        browser.find_element_by_xpath('//*[contains(@id,"phone")]').send_keys(number)
        browser.find_element_by_xpath('//*[contains(@id,"autorizacion_ofertas_comerciales")]').send_keys(number)
        browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div/form/div[16]/div[2]/input').click()
        time.sleep(5)
        print('Generali: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Generali: Skipeado (ERROR)')

    #regal
    try:
        browser.get(regal)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="primaryPhoneInput"]').send_keys(number)
        browser.find_element_by_xpath('//*[@id="continueButton"]')
        time.sleep(5)
        print('Regal: OK')
    except KeyboardInterrupt:
        quit()
    except:
        print('Regal: Skipeado (ERROR)')

    if repeat in ('y', 'yes', 's', 'si'):
        browser.close()
        print('Repeat ON')
    else:
        browser.quit()
        break

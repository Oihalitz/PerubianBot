from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime
import warnings
import requests
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import time
import os

def setup_firefox_profile():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.autoplay.default", 0)
    profile.accept_untrusted_certs = True
    return profile

def main():
    binary = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe' if os.name == 'nt' else '/usr/bin/firefox'
    prefijos = ('6', '7', '9')
    version = 'Beta 1.4'

    #Limite hora
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start = '10:40:00'
    end = '22:00:00'

    debug = 1
    if debug == 1:
        print('DEBUG MODE ON')
        number, name, surname, email = '666666666', 'NombrePrueba', 'ApellidoPrueba', 'CorreoPrueba@gmail.com'
    else:
        number = input('Nº de Teléfono: ')
        while len(number) != 9 or not number.startswith(prefijos):
            number = input('Número incorrecto. Ingrese Nº de Teléfono nuevamente: ')
        name = input('Nombre de la persona: ')
        surname = input('Apellido: ')
        email = input('Correo: ') or f'{name}{surname}@gmail.com'
        print('Iniciando')

    print(f'PerubianBot V{version}\n')
    print(f'PerubianBot: {number}')

    repeat = input('Modo repetición [S/N]: ').lower()

    while repeat in ('s', 'n', 'y'):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.autoplay.default", 0)
        profile.accept_untrusted_certs = True
        PATH_TO_DEV_NULL = 'nul'

        securitas = 'https://www.securitasdirect.es/'
        securitaserror = 'https://www.securitasdirect.es/error-envio'
        jazztel = 'https://www.telefonojazztel.es/'
        genesis = 'https://www.genesis.es/c2c'
        euskaltel = 'https://www.euskaltel.com/CanalOnline/particulares/general/tarifa-family-mas-lineas-adicionales?idioma=esp'
        itep = 'https://www.itep.es/'
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
        euroinnova = 'https://www.euroinnova.edu.es/cursos#formulario'
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
            browser.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/div/div/span/div/div/section/div[2]/div[2]/div[2]/div/div/div/div[2]/form/div/div[1]/div/div/div[2]/div[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[6]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[1]/div[2]/label').click()
            browser.find_element_by_xpath('//*[@id="facade-firstName"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="facade-lastName"]').send_keys(surname)
            browser.find_element_by_xpath('//*[@id="facade-entreprise"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="facade-phoneNumber"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="facade-email"]').send_keys(email)
            time.sleep(1)
            checkbox = browser.find_element_by_xpath("//input[@id='facade-legal']")
            browser.execute_script("arguments[0].click();", checkbox)
            checkbox = browser.find_element_by_xpath('//input[@id="facade-newsletter"]')
            browser.execute_script("arguments[0].click();", checkbox)
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[6]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[10]/button/span[1]').click()
            time.sleep(8)
            print('Vodafone: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Vodafone: Skipeado (ERROR)')

        #euroinnova
        try:
            browser.get(euroinnova)
            time.sleep(3)
            #browser.find_element_by_xpath('/html/body/section/article/div[5]/div[2]/div/div[1]/div[2]/div/div/div/div[6]/a').click()
            #time.sleep(1)
            browser.find_element_by_xpath('//*[@id="accept-cookies"]').click() #Cookies
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/button').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="mail"]').send_keys(email)
            browser.find_element_by_xpath('//*[@id="tel"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="privacidad"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="btn_enviar"]').click()
            time.sleep(3)
            print('Euroinnova: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Euroinnova: Skipeado (ERROR)')

        #GENESIS
        try:
            if current_time > start and current_time < end:
                browser.get(genesis)
                time.sleep(8)
                try:
                    browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/section/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/form/span/div[1]/div[1]/div[4]/select/option[3]').click()
                browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
                browser.find_element_by_xpath('//*[@id="phone"]').send_keys(number)
                browser.find_element_by_xpath('//*[@id="phoneConfirm"]').send_keys(number)

                browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/section/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/form/span/div[1]/div[2]/div/button').click()
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
            try:
                browser.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/div[2]/a[2]').click() #Cookies
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/header/div[1]/div/div/div[2]/a').click()
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="phoneNumber"]').send_keys(number)
            if(browser.find_element_by_xpath('//*[@id="multioption"]').is_displayed()):
                browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[3]/div/div[2]/form/div/div[3]/div/select/option[2]').click()
            time.sleep(2)
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
            try:
                browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/button[1]').click() # Cookies
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('/html/body/header/div/div[5]/div/p/button').click() # Solicitar Informacion
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="edit-email"]').send_keys(email)
            browser.find_element_by_xpath('//*[@id="edit-phone"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="edit-cp"]').send_keys(postalcode)
            browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/form/div[4]/select/optgroup[1]/option[1]').click()
            browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/form/div[5]/select/option[2]').click()
            browser.find_element_by_xpath('//*[@id="edit-conditions"]').click()
            browser.find_element_by_xpath('//*[@id="edit-educa-consent"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="edit-submit-lead-form-header-web-solicita-info-general-1"]').click()

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
            try:
                browser.find_element_by_xpath('//button[@id="didomi-notice-agree-button"]').click()
            except:
                pass
            browser.find_element_by_xpath('//*[@id="telefono"]').send_keys(number)
            time.sleep(2)
            try:
                browser.find_element_by_xpath('/html/body/div[1]/section/section/form/div[2]/div/div[2]/a').click() # Buttom 1
            except:
                browser.find_element_by_xpath('/html/body/div[3]/section/section/form/div[2]/div/div[2]/a').click() # Buttom 2
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
            browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/section[1]/div[2]/div/div/div[2]/form/div[2]/label').click()
            browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/section[1]/div[2]/div/div/div[2]/div/button/span').click()
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
            browser.find_element_by_xpath('//input[@id="primaryPhoneInput"][1]').send_keys(number)
            browser.find_element_by_xpath('//input[@id="primaryPhoneInput"][2]').send_keys(number)
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

if __name__ == "__main__":
    main()
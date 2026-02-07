"""
PerubianBot - Módulo de Webs
Todas las webs están aquí, separadas del core principal
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import random
import time
import requests


class WebBase:
    """Clase base con métodos comunes para todas las webs"""
    
    def __init__(self, nombre, url, habilitada=True, requiere_horario=False, hora_inicio=None, hora_fin=None):
        self.nombre = nombre
        self.url = url
        self.habilitada = habilitada
        self.requiere_horario = requiere_horario
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
    
    def verificar_horario(self, hora_actual):
        """Verifica si está dentro del horario permitido"""
        if not self.requiere_horario:
            return True
        if self.hora_inicio and self.hora_fin:
            return self.hora_inicio <= hora_actual <= self.hora_fin
        return True
    
    def click_seguro(self, browser, xpath, timeout=1):
        """Click con manejo de errores"""
        try:
            element = browser.find_element(By.XPATH, xpath)
            browser.execute_script("arguments[0].click();", element)
            time.sleep(timeout)
            return True
        except:
            return False
    
    def escribir_seguro(self, browser, xpath, texto, timeout=1):
        """Escribir con manejo de errores"""
        try:
            browser.find_element(By.XPATH, xpath).send_keys(texto)
            time.sleep(timeout)
            return True
        except:
            return False

    def escribir_lento(self, browser, xpath, texto, delay=0.15, timeout=1):
        """Escribe caracter a caracter para inputs que no aceptan pegado"""
        try:
            field = browser.find_element(By.XPATH, xpath)
            for char in texto:
                field.send_keys(char)
                time.sleep(delay)
            time.sleep(timeout)
            return True
        except:
            return False

    def limpiar_y_escribir_lento(self, browser, xpath, texto, delay=0.15, timeout=1):
        """Enfoca, limpia y escribe lento para inputs con mascara"""
        try:
            field = browser.find_element(By.XPATH, xpath)
            field.click()
            field.send_keys(Keys.COMMAND, 'a')
            field.send_keys(Keys.CONTROL, 'a')
            field.send_keys(Keys.BACKSPACE)
            for char in texto:
                field.send_keys(char)
                time.sleep(delay)
            time.sleep(timeout)
            return True
        except:
            return False

    def escribir_js(self, browser, xpath, texto, timeout=1):
        """Set value via JS and trigger input/change events"""
        try:
            field = browser.find_element(By.XPATH, xpath)
            browser.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                field,
                texto
            )
            time.sleep(timeout)
            return True
        except:
            return False

    def encontrar_elemento_visible(self, browser, selectors):
        """Devuelve el primer elemento visible para una lista de selectores"""
        for by, selector in selectors:
            try:
                elements = browser.find_elements(by, selector)
                for element in elements:
                    if element.is_displayed():
                        return element
            except:
                continue
        return None

    def escribir_lento_visible(self, browser, selectors, texto, delay=0.2, timeout=1):
        """Escribe lento en el primer input visible encontrado"""
        try:
            field = self.encontrar_elemento_visible(browser, selectors)
            if not field:
                return False
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
            field.click()
            field.send_keys(Keys.COMMAND, 'a')
            field.send_keys(Keys.CONTROL, 'a')
            field.send_keys(Keys.BACKSPACE)
            for char in texto:
                field.send_keys(char)
                time.sleep(delay)
            browser.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                field
            )
            time.sleep(timeout)
            return True
        except:
            return False
    
    def aceptar_cookies(self, browser, xpath):
        """Intenta aceptar cookies"""
        try:
            browser.find_element(By.XPATH, xpath).click()
            time.sleep(1)
            return True
        except:
            return False
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        """Método que debe implementar cada web"""
        raise NotImplementedError("Cada web debe implementar ejecutar()")


# ============================================================================
# WEBS - Cada una hereda de WebBase
# ============================================================================

class SecuritasDirect(WebBase):
    def __init__(self):
        super().__init__("Securitas Direct", "https://www.securitasdirect.es/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(5)
        self.aceptar_cookies(browser, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        
        if not self.escribir_seguro(browser, '//*[@id="edit-telefono1"]', telefono):
            return False, "No se pudo introducir el teléfono"
        
        if not self.click_seguro(browser, '//*[@id="edit-submit"]'):
            return False, "No se pudo enviar"
        
        time.sleep(1)
        if browser.current_url == 'https://www.securitasdirect.es/error-envio':
            return False, "Límite excedido"
        
        return True, "OK"


class Euroinnova(WebBase):
    def __init__(self):
        super().__init__("Euroinnova", "https://www.euroinnova.com/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="accept-cookies"]')
        
        if not self.click_seguro(browser, '/html/body/div[2]/div/div[2]/div[2]/button'):
            return False, "No se pudo abrir formulario"
        
        time.sleep(2)
        self.escribir_seguro(browser, '//*[@id="name"]', nombre)
        self.escribir_seguro(browser, '//*[@id="lastname"]', apellido)
        self.escribir_seguro(browser, '//*[@id="mail"]', email)
        self.escribir_seguro(browser, '//*[@id="tel"]', telefono)
        try:
            select_elem = browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[3]/form/div[4]/div[2]/div/select')
            Select(select_elem).select_by_index(9)
        except:
            return False, "No se pudo seleccionar el desplegable"
        time.sleep(1)
        self.click_seguro(browser, '//*[@id="privacidad"]')
        time.sleep(1)
        
        if not self.click_seguro(browser, '//*[@id="btn_enviar"]'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class Genesis(WebBase):
    def __init__(self):
        super().__init__("Genesis", "https://www.genesis.es/modal/c2c", 
                        requiere_horario=True, hora_inicio="10:40:00", hora_fin="22:00:00")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        time.sleep(1)

        try:
            select_elem = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/article/div/div/div/div/div/form/section/div/div[2]/div/select')
            Select(select_elem).select_by_index(1)
        except:
            return False, "No se pudo seleccionar el desplegable"
        self.escribir_seguro(browser, '//*[@id="edit-por-quien-preguntamos-"]', nombre)
        self.escribir_seguro(browser, '//*[@id="edit-phone"]', telefono)
        self.escribir_seguro(browser, '//*[@id="edit-phone-confirmation"]', telefono)
        self.click_seguro(browser, '/html/body/div[1]/div/main/div/div/div/article/div/div/div/div/div/form/section/div/div[7]/div/label')
        
        if not self.click_seguro(browser, '//*[@id="edit-actions-submit"]'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class RacctelPlus(WebBase):
    def __init__(self):
        super().__init__("Racctel+", "https://www.racctelplus.cat/es")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        time.sleep(2)
        
        selectors = [
            (By.CSS_SELECTOR, '#c2c-form #phone'),
            (By.XPATH, '//*[@id="c2c-form"]//*[@id="phone"]'),
            (By.XPATH, '(//*[@id="phone"])[1]')
        ]
        if not self.escribir_lento_visible(browser, selectors, telefono, delay=0.2):
            return False, "No se pudo introducir el teléfono"
        
        if not self.click_seguro(browser, '//*[@id="c2c-submit"]'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class Jazztel(WebBase):
    def __init__(self):
        super().__init__("Jazztel", "https://llamamegratis.es/jazztel/v2/webphone.html?lang=es-ES&isLandingLander=1&typeOrigin=wphFollow&widget=3294&wphUrl#https://www.telefonojazztel.es/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(1)
        
        if not self.escribir_seguro(browser, '//*[@id="phoneNumber"]', telefono):
            return False, "No se pudo introducir teléfono"
        
        time.sleep(1)
        self.click_seguro(browser, '/html/body/div[1]/div[1]/div[2]/div[3]/div/div[2]/form/div/div[3]/div/select/option[2]')
        time.sleep(1)
        
        if not self.click_seguro(browser, '//*[@id="env"]'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class Ford(WebBase):
    def __init__(self):
        super().__init__("Ford", "https://www.infoford.es/citataller_gux/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(4)
        self.aceptar_cookies(browser, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        
        try:
            field = browser.find_element(By.XPATH, '//*[@id="telefono"]')
            browser.execute_script("arguments[0].value = arguments[1];", field, telefono)
            self.click_seguro(browser, '//*[@id="legales"]')
            time.sleep(1)
            self.click_seguro(browser, '//*[@id="btn-enviar"]')
            time.sleep(5)
            return True, "OK"
        except:
            return False, "Error en formulario"


class Vodafone(WebBase):
    def __init__(self):
        super().__init__("Vodafone", "https://www.vodafone.es/c/empresas/es/marketing-online/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(1)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        
        if not self.click_seguro(browser, '/html/body/div[2]/main/div[1]/div/div[2]/div/div/div/section/div/div/div/div/div/a[1]/span[1]'):
            return False, "No se pudo abrir modal"
        
        time.sleep(2)
        if not self.escribir_seguro(browser, '//*[@id="phone"]', telefono):
            return False, "No se pudo introducir teléfono"
        
        try:
            checkbox_gdpr = browser.find_element(By.XPATH, '//*[@id="cmb-gdpr"]')
            browser.execute_script("arguments[0].click();", checkbox_gdpr)
            checkbox_commercial = browser.find_element(By.XPATH, '//*[@id="cmb-check"]')
            browser.execute_script("arguments[0].click();", checkbox_commercial)
        except:
            return False, "Error en checkboxes"
        
        time.sleep(1)
        if not self.click_seguro(browser, '/html/body/div[2]/main/div[14]/div/div/div/span/div/div[2]/div[1]/div/div/form/input[2]'):
            return False, "No se pudo enviar"
        
        time.sleep(4)
        return True, "OK"


class Euskaltel(WebBase):
    def __init__(self):
        super().__init__("Euskaltel", "https://www.euskaltel.com/?idioma=esp")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        time.sleep(2)
        
        selectors = [
            (By.CSS_SELECTOR, '#c2c-form #phone'),
            (By.XPATH, '//*[@id="c2c-form"]//*[@id="phone"]'),
            (By.XPATH, '(//*[@id="phone"])[1]')
        ]
        if not self.escribir_lento_visible(browser, selectors, telefono, delay=0.2):
            return False, "No se pudo introducir el teléfono"

        submit_selectors = [
            (By.CSS_SELECTOR, '#c2c-form #c2c-submit'),
            (By.XPATH, '//*[@id="c2c-form"]//*[@id="c2c-submit"]'),
            (By.XPATH, '(//*[@id="c2c-submit"])[1]')
        ]
        submit_button = self.encontrar_elemento_visible(browser, submit_selectors)
        if not submit_button:
            return False, "No se pudo encontrar el boton de envio"
        try:
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            browser.execute_script("arguments[0].click();", submit_button)
        except:
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class Pelayo(WebBase):
    def __init__(self):
        super().__init__("Pelayo", "https://www.pelayo.com/nosotros_te_llamamos/tellamamos")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(2)
        self.aceptar_cookies(browser, '/html/body/app-root/app-cookies-block/div[2]/div/div/a[1]')
        time.sleep(1)
        
        self.escribir_seguro(browser, '//*[@id="input3"]', telefono)
        
        if not self.click_seguro(browser, '/html/body/app-root/div/app-layout-click-to-call/main/div/div/app-ad-elem/app-panel-window-te-llamamos/form/div[2]/button'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class Movistar(WebBase):
    def __init__(self):
        super().__init__("Movistar", "https://www.movistar.es/estaticos/html/modal/modal-formulario-C2C-empresas-inside-sales-new.html")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(1)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        time.sleep(1)
        
        self.escribir_seguro(browser, '//*[@id="nameC2CplainModal_IS"]', nombre)
        self.escribir_seguro(browser, '//*[@id="tlfC2CplainModal_IS"]', telefono)
        time.sleep(1)
        self.escribir_seguro(browser, '//*[@id="cifC2CplainModal_IS"]', 'D09818238')
        try:
            select_elem = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/div[1]/div[4]/select')
            Select(select_elem).select_by_index(32)
        except:
            return False, "No se pudo seleccionar la provincia"
        
        if not self.click_seguro(browser, '//*[@id="modal__emp__cta"]'):
            return False, "No se pudo enviar"
        
        time.sleep(2)
        return True, "OK"


class Orange(WebBase):
    def __init__(self):
        super().__init__("Orange", "https://selectra.es/internet-telefono/companias/orange/telefono",
                        requiere_horario=True, hora_inicio="10:40:00", hora_fin="22:00:00")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(2)
        self.aceptar_cookies(browser, '/html/body/div[3]/div/div[2]/div/div[2]/div/div/div[3]/div/button[3]')
        time.sleep(1)
        
        self.click_seguro(browser, '/html/body/div[1]/div/div/div[1]/div/main/div[2]/div/article/div[4]/div[3]/a')
        time.sleep(3)
        self.escribir_seguro(browser, '//*[@id="callback-modal__phone"]', telefono)
        
        if not self.click_seguro(browser, '//*[@id="callback-modal__submit"]'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class Mapfre(WebBase):
    def __init__(self):
        super().__init__("Mapfre", "https://www.mapfre.es/boi/inicio.do?origen=autos_portalmapfre&destino=sgc_new&producto=autos")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(2)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        
        self.escribir_seguro(browser, '//*[@id="nombre"]', nombre)
        self.escribir_seguro(browser, '//*[@id="primer_apellido"]', apellido)
        self.escribir_seguro(browser, '//*[@id="codigo_postal"]', "08002")
        self.escribir_seguro(browser, '//*[@id="tlfn"]', telefono)
        self.click_seguro(browser, '//*[@id="marca_robinson"]')
        self.click_seguro(browser, '//*[@id="politicaprivacidad"]')
        
        if not self.click_seguro(browser, '/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class SantaLucia(WebBase):
    def __init__(self):
        super().__init__("SantaLucia", "https://seguro.santalucia.es/?utm_source=bing_santalucia_lbm_paid-search_bing_generica_multiramo_otros_na-site-section_na-ad-size_na-served-type_na-princing&msclkid=dac0ba5685891c9f6da6dd0efc479885")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(6)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        time.sleep(1)
        
        self.click_seguro(browser, '//*[@id="landings_ty_form115200807"]/div[1]/div/div[1]')
        time.sleep(2)
        self.escribir_seguro(browser, "//*[starts-with(@id, 'phone')]", telefono)
        self.click_seguro(browser, '/html/body/div[1]/div[3]/section/div[1]/div[1]/div/div/div/section/div/div[2]/div/div/div/section/div[1]/div/div[2]/form/div[1]/div/div[2]/label')
        time.sleep(1)
        self.click_seguro(browser, "//*[starts-with(@id, 'checkProteccion')]")
        self.click_seguro(browser, "//*[starts-with(@id, 'checkInformation')]")
        
        if not self.click_seguro(browser, '/html/body/div[1]/div[3]/section/div[1]/div[1]/div/div/div/section/div/div[2]/div/div/div/section/div[1]/div/div[2]/form/input'):
            return False, "No se pudo enviar"

        for _ in range(10):
            try:
                if "seguro.santalucia.es/gracias" in browser.current_url:
                    return True, "OK"
            except:
                pass
            time.sleep(0.5)

        time.sleep(2)
        return True, "OK"


class Asisa(WebBase):
    def __init__(self):
        super().__init__("Asisa", "https://asisa.contratarsegurodesalud.com/seguro-salud-pyme")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(5)
        self.aceptar_cookies(browser, '/html/body/div[1]/div/div[4]/div/div[2]/button[4]')
        time.sleep(1)
        
        self.escribir_seguro(browser, '//*[@id=":R2kla2l6:"]', telefono)
        time.sleep(1)
        self.click_seguro(browser, '/html/body/div/div/div[2]/div/div[3]/label/span[1]/input')
        
        if not self.click_seguro(browser, '/html/body/div/div/div[2]/div/div[4]/button/p'):
            return False, "No se pudo enviar"
        
        time.sleep(2)
        return True, "OK"


class ITEP(WebBase):
    def __init__(self):
        super().__init__("ITEP", "https://www.itep.es/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(4)
        self.aceptar_cookies(browser, '//*[@id="cookiesjsr"]/div/div/div[2]/button[3]')
        
        self.click_seguro(browser, '/html/body/header/div/div[5]/div/p/button')
        time.sleep(1)
        try:
            modal = browser.find_element(By.ID, 'header-form-modal')
        except:
            return False, "No se pudo abrir el formulario"
        try:
            modal.find_element(By.ID, 'edit-name').send_keys(nombre)
            modal.find_element(By.ID, 'edit-email').send_keys(email)
            modal.find_element(By.ID, 'edit-phone').send_keys(telefono)
            modal.find_element(By.ID, 'edit-cp').send_keys("08002")
        except:
            return False, "No se pudieron rellenar los campos"
        try:
            select_city = modal.find_element(By.ID, 'edit-city')
            city_options = [opt for opt in Select(select_city).options if opt.get_attribute('value')]
            if not city_options:
                return False, "No se pudo seleccionar la ciudad"
            city_value = random.choice(city_options).get_attribute('value')
            browser.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                select_city,
                city_value
            )
        except:
            return False, "No se pudo seleccionar la ciudad"
        time.sleep(1)
        try:
            select_titulation = modal.find_element(By.ID, 'edit-titulation')
            titulation_options = [opt for opt in Select(select_titulation).options if opt.get_attribute('value')]
            if not titulation_options:
                return False, "No se pudo seleccionar la titulacion"
            titulation_value = random.choice(titulation_options).get_attribute('value')
            browser.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                select_titulation,
                titulation_value
            )
        except:
            return False, "No se pudo seleccionar la titulacion"
        try:
            checkbox = modal.find_element(By.ID, 'edit-conditions--2')
            browser.execute_script("arguments[0].click();", checkbox)
        except:
            return False, "No se pudo aceptar condiciones"
        time.sleep(1)

        try:
            submit = modal.find_element(By.ID, 'edit-submit-lead-form-header-web-solicita-info-general-1')
            browser.execute_script("arguments[0].click();", submit)
        except:
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class MasMovilAlarmas(WebBase):
    def __init__(self):
        super().__init__("MasMovil Alarmas", "https://masmovilalarmas.es/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        
        self.click_seguro(browser, '/html/body/div[1]/div/div[2]/main/div/section[1]/div[2]/div[1]/div[2]/div/div[2]/div[1]/a')
        time.sleep(2)
        self.escribir_seguro(browser, "//*[starts-with(@id, 'BysidePhoneBySideData_')]", telefono)
        self.click_seguro(browser, "//*[starts-with(@id, 'BysideCallBtnBySideData_')]")
        
        try:
            self.click_seguro(browser, "/html/body/div[51]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[1]/input[1]")
            time.sleep(1)
        except:
            pass
        
        time.sleep(2)
        return True, "OK"


class Prosegur(WebBase):
    def __init__(self):
        super().__init__("Prosegur", "https://www.prosegur.es/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="didomi-notice-agree-button"]/span')
        time.sleep(1)
        
        # Intentar diseño 1
        try:
            self.escribir_seguro(browser, '//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[2]/div/input', telefono)
            self.click_seguro(browser, '//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[4]/div/fieldset/label/span')
            self.click_seguro(browser, '//*[@id="formulario-hero-composicion-prosegur-spain-cc-activo"]/div[2]/div[5]/div/div/div/button/span')
        except:
            pass
        
        # Intentar diseño 2
        try:
            self.escribir_seguro(browser, '/html/body/main/div/section/div/div/div[2]/section[2]/div/div/div/div/div[1]/div[2]/form/div[2]/div[2]/div/input', telefono)
            self.click_seguro(browser, '/html/body/main/div/section/div/div/div[2]/section[2]/div/div/div/div/div[1]/div[2]/form/div[2]/div[4]/div/fieldset/label/span')
            self.click_seguro(browser, '/html/body/main/div/section/div/div/div[2]/section[2]/div/div/div/div/div[1]/div[2]/form/div[2]/div[5]/div/div/div/button/span')
        except:
            pass
        
        time.sleep(3)
        return True, "OK"


class LineaDirecta(WebBase):
    def __init__(self):
        super().__init__("Linea Directa", "https://www.lineadirecta.com/te-llamamos-gratis.html?idServicio=http0036&from=B009975&indVehiculo=C")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(4)
        self.aceptar_cookies(browser, '//button[@id="didomi-notice-agree-button"]')
        
        self.escribir_seguro(browser, '//*[@id="telefono-numerico"]', telefono)
        time.sleep(1)
        
        if not self.click_seguro(browser, '//*[@id="txtBtn1"]'):
            return False, "No se pudo enviar"
        
        time.sleep(2)
        return True, "OK"


class Telecable(WebBase):
    def __init__(self):
        super().__init__("Telecable", "http://marcador-c2c.alisys.net/telecablec2c_v2/c2c.php")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        
        self.escribir_seguro(browser, '//*[@id="numero"]', telefono)
        
        if not self.click_seguro(browser, '/html/body/div[1]/div[3]/form/button'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class HomeGO(WebBase):
    def __init__(self):
        super().__init__("HomeGO", "https://homego.es/alarmas-para-casa-precios-no-cliente")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        
        browser.execute_script("window.scrollBy(0, 500);")
        time.sleep(3)
        
        try:
            self.click_seguro(browser, "//*[starts-with(@id, 'BysideScheduleBySideData_')]/option[2]")
        except:
            pass
        
        self.escribir_seguro(browser, "//*[starts-with(@id, 'BysidePhoneBySideData_')]", telefono)
        self.click_seguro(browser, "//*[starts-with(@id, 'BysideCallBtnBySideData_')]")
        
        try:
            self.click_seguro(browser, "/html/body/div[82]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/input[1]")
            time.sleep(2)
        except:
            pass
        
        time.sleep(1)
        return True, "OK"


class Iberdrola(WebBase):
    def __init__(self):
        super().__init__("Iberdrola", "https://www.rastreator.com/tarifas-energia/companias-electricas/iberdrola/atencion-cliente")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(4)
        self.aceptar_cookies(browser, '/html/body/div[5]/div/div[2]/button[3]')
        time.sleep(2)
        
        self.click_seguro(browser, '/html/body/article/div[2]/div/div[3]/div/div/div[1]/button')
        time.sleep(2)
        self.escribir_seguro(browser, '//*[@id="txtTel"]', telefono)
        self.click_seguro(browser, '/html/body/article/div[2]/div/div[2]/div/form/div[1]/div[5]/div/label/div/span[1]')
        self.click_seguro(browser, '//*[@id="btn_submit"]')
        
        if not self.click_seguro(browser, '//*[@id="btn_submit"]'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class ISalud(WebBase):
    """Web especial que usa HTTP POST en lugar de navegador"""
    def __init__(self):
        super().__init__("iSalud", "https://vsec.es")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        try:
            url = "https://vsec.es/llamada.php"
            payload = {
                "name": nombre,
                "surname": apellido,
                "email": email,
                "number": telefono
            }
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                return True, "OK"
            else:
                return False, f"Error HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)


class Recordador(WebBase):
    """Web especial que usa HTTP POST con headers"""
    def __init__(self):
        super().__init__("Recordador", "https://www.prosegur.es")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        try:
            headers = {
                'Referer': 'https://www.prosegur.es/smart-home/alarmas-para-el-hogar?vdm=1&gclid=CjwKCAjwq4imBhBQEiwA9Nx1BifzsVHzzkwkqCKxaM5iVvdP06q55rJwCEoKzaX0KiqG_LXdaKy1exoCxv0QAvD_BwE&gclsrc=aw.ds',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            url = "https://www.prosegur.es/api-servicio/prospector_lead/recordador-alarmas"
            data = {
                "phone": telefono,
                "acceptance_conditions": "on"
            }
            response = requests.post(url, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                return True, "OK"
            else:
                return False, f"Error HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)


class ProyectosYSeguros(WebBase):
    def __init__(self):
        super().__init__("Proyectos y Seguros", "https://www.proyectosyseguros.com/te-llamamos/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)

        self.escribir_seguro(browser, '//*[@id="Nombre"]', nombre)
        self.escribir_seguro(browser, '//*[@id="Email"]', email)
        self.escribir_seguro(browser, '//*[@id="Telefono"]', telefono)
        try:
            select_ramo = browser.find_element(By.ID, 'Ramo')
            Select(select_ramo).select_by_index(1)
        except:
            return False, "No se pudo seleccionar el ramo"
        try:
            select_cuando = browser.find_element(By.ID, 'Cuando')
            Select(select_cuando).select_by_index(0)
        except:
            return False, "No se pudo seleccionar la hora"
        self.click_seguro(browser, '//*[@id="acepto_condiciones"]')

        if not self.click_seguro(browser, '//*[@id="enviarformulario"]//button'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class MoneyGO(WebBase):
    def __init__(self):
        super().__init__("MoneyGO", "https://ctc.moneygo.es/money-go-ctc-web/ctc/04f25d44-f1ce-4554-ba40-57211f7133ce")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        
        self.escribir_seguro(browser, '//*[@id="telefono"]', telefono)
        self.click_seguro(browser, '/html/body/div[1]/create-ctc/div[2]/form/div[4]/div/label')
        
        if not self.click_seguro(browser, '/html/body/div[1]/create-ctc/div[2]/form/button'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class Emagister(WebBase):
    def __init__(self):
        super().__init__("emagister", "https://www.emagister.com/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(2)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        
        self.click_seguro(browser, '/html/body/header/div[2]/div/div[3]/div/nav/div[1]/div/div/section[2]/button')
        time.sleep(1)
        self.escribir_seguro(browser, '//*[@id="callMe-phone"]', telefono)
        self.click_seguro(browser, '/html/body/table/tbody/tr[2]/td[2]/div/div[2]/form/p/label/span[2]')
        
        if not self.click_seguro(browser, '/html/body/table/tbody/tr[2]/td[2]/div/div[2]/form/button'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class MundoR(WebBase):
    def __init__(self):
        super().__init__("Mundo-R", "https://mundo-r.com/es")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        time.sleep(2)
        
        selectors = [
            (By.CSS_SELECTOR, '#c2c-form #phone'),
            (By.XPATH, '//*[@id="c2c-form"]//*[@id="phone"]'),
            (By.XPATH, '(//*[@id="phone"])[1]')
        ]
        if not self.escribir_lento_visible(browser, selectors, telefono, delay=0.2):
            return False, "No se pudo introducir el teléfono"
        
        if not self.click_seguro(browser, '//*[@id="c2c-submit"]'):
            return False, "No se pudo enviar"
        
        time.sleep(3)
        return True, "OK"


class HomeServe(WebBase):
    def __init__(self):
        super().__init__("homeserve", "https://www.homeserve.es/servicios-reparaciones/fontaneros")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="basicCookies"]/div/div[2]/div[3]/div/button')
        time.sleep(1)
        
        try:
            select_elem = browser.find_element(By.XPATH, '/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[2]/select')
            Select(select_elem).select_by_index(1)
        except:
            return False, "No se pudo seleccionar el desplegable"
        self.escribir_seguro(browser, '/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[5]/input[1]', nombre)
        self.escribir_seguro(browser, '/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[5]/input[2]', apellido)
        self.escribir_seguro(browser, '/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[6]/input[1]', telefono)
        self.escribir_seguro(browser, '/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[6]/input[2]', email)
        self.click_seguro(browser, '/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[7]/input')
        
        if not self.click_seguro(browser, '/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[9]/button'):
            return False, "No se pudo enviar"
        
        time.sleep(1)
        return True, "OK"


class MasMovil(WebBase):
    def __init__(self):
        super().__init__("MasMovil", "https://www.masmovil.es/empresas/negocios-autonomos")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(2)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')

        phone_selectors = [
            (By.XPATH, "//*[starts-with(@id, 'CMPhoneBySideData_')]")
        ]
        if not self.escribir_lento_visible(browser, phone_selectors, telefono, delay=0.2):
            return False, "No se pudo introducir el teléfono"

        try:
            schedule_select = self.encontrar_elemento_visible(
                browser,
                [(By.XPATH, "//*[starts-with(@id, 'CMScheduleBySideData_')]")]
            )
            if schedule_select:
                schedule_options = [
                    opt for opt in Select(schedule_select).options if opt.get_attribute('value')
                ]
                if schedule_options:
                    Select(schedule_select).select_by_value(
                        random.choice(schedule_options).get_attribute('value')
                    )
        except:
            pass

        call_button = self.encontrar_elemento_visible(
            browser,
            [(By.XPATH, "//*[starts-with(@id, 'CMCallBtnBySideData_')]")]
        )
        if not call_button:
            return False, "No se pudo encontrar el boton de llamada"
        try:
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", call_button)
            browser.execute_script("arguments[0].click();", call_button)
        except:
            return False, "No se pudo enviar"

        time.sleep(2)
        return True, "OK"



class Alarmak(WebBase):
    def __init__(self):
        super().__init__("Alarmak", "https://segurma.com/alarmas/bilbao/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        
        time.sleep(2)
        self.escribir_seguro(browser, "//*[@id='input_2_5']", nombre)
        self.escribir_seguro(browser, "//*[@id='input_2_1']", telefono)
        self.escribir_seguro(browser, "//*[@id='input_2_7']", "48002")
        self.click_seguro(browser, "//*[@id='input_2_3_1']")
        
        try:
            self.click_seguro(browser, "//*[@id='gform_submit_button_2']")
            time.sleep(2)
        except:
            pass
        
        time.sleep(1)
        return True, "OK"


class CentroDermatologico(WebBase):
    def __init__(self):
        super().__init__("Centro Dermatologico Estetico", "https://www.centrodermatologicoestetico.com/te-llamamos/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="cookie_action_close_header"]')
        
        self.escribir_seguro(browser, '/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[5]', nombre)
        self.escribir_seguro(browser, '//*[@id="international_PhoneNumber_countrycode"]', telefono)
        self.escribir_seguro(browser, '/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[7]', email)
        self.click_seguro(browser, '/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/div/div/div/input')
        
        if not self.click_seguro(browser, '/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/button'):
            return False, "No se pudo enviar"
        
        time.sleep(2)
        return True, "OK"


class MutuaMadrilena(WebBase):
    def __init__(self):
        super().__init__("Mutua Madrileña", "https://www.mutua.es/recursos/html/404.htm")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="consent_prompt_submit"]')
        
        self.escribir_seguro(browser, '//*[@id="nombreformC2C2"]', nombre)
        self.escribir_seguro(browser, '//*[@id="telefonoformC2C2"]', telefono)
        self.click_seguro(browser, '/html/body/section[1]/div/div[2]/form/div/div/div/div[4]/div[3]/label')
        
        if not self.click_seguro(browser, '/html/body/section[1]/div/div[2]/form/div/div/div/div[5]/div/a'):
            return False, "No se pudo enviar"
        
        time.sleep(2)
        return True, "OK"


class Generali(WebBase):
    def __init__(self):
        super().__init__("Generali", "https://www.generali.es/blog/tuasesorsalud/solicitar-informacion/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')

        self.escribir_seguro(browser, '//*[@id="Email"]', email)
        self.escribir_seguro(browser, '//*[@id="FirstName"]', nombre)
        self.escribir_seguro(browser, '//*[@id="PhoneNumber"]', telefono)

        try:
            select_cliente = browser.find_element(By.ID, 'Eres_cliente_de_Generali')
            Select(select_cliente).select_by_index(2)
        except:
            return False, "No se pudo seleccionar cliente"

        try:
            select_seguro = browser.find_element(By.ID, 'Tienes_tu_seguro_de_salud_con_Generali')
            Select(select_seguro).select_by_index(2)
        except:
            return False, "No se pudo seleccionar seguro"

        try:
            select_seguro_actual = browser.find_element(By.ID, 'Que_seguro_tienes_ahora')
            Select(select_seguro_actual).select_by_index(1)
        except:
            return False, "No se pudo seleccionar seguro actual"

        try:
            select_hora = browser.find_element(By.ID, 'Agendar_llamada')
            Select(select_hora).select_by_index(1)
        except:
            return False, "No se pudo seleccionar la hora"

        try:
            checkbox = browser.find_element(By.ID, 'autorizacion_ofertas_comerciales-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df')
            browser.execute_script("arguments[0].click();", checkbox)
        except:
            return False, "No se pudo aceptar condiciones"

        try:
            submit = browser.find_element(By.CSS_SELECTOR, '#smartcapture-block-awjlkpfmvw9 .sc-button')
            browser.execute_script("arguments[0].click();", submit)
        except:
            return False, "No se pudo enviar"

        time.sleep(5)
        return True, "OK"


class FiNetwork(WebBase):
    def __init__(self):
        super().__init__("FiNetwork", "https://www.finetwork.com/")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(2)
        self.aceptar_cookies(browser, '//*[@id="accept-button"]')
        if not self.click_seguro(browser, '/html/body/div[2]/div[12]/header/div[1]/div[2]/span/div'):
            return False, "No se pudo abrir 'Te llamamos'"
        if not self.escribir_seguro(browser, '//*[@id="input-call-me-back-form-contactPhone"]', telefono):
            return False, "No se pudo introducir el teléfono"
        if not self.click_seguro(browser, '//*[@id="input-check-call-me-back-form-acceptPrivacyCheck"]'):
            return False, "No se pudo aceptar términos"
        if not self.click_seguro(browser, '//*[@id="submit-call-me-back-form"]'):
            return False, "No se pudo enviar"
        
        time.sleep(1)
        return True, "OK"


class Regal(WebBase):
    def __init__(self):
        super().__init__("Regal", "https://te-llamamos.regal.es/user-details")
    
    def ejecutar(self, browser, nombre, apellido, telefono, email):
        browser.get(self.url)
        time.sleep(3)
        self.aceptar_cookies(browser, '//*[@id="onetrust-accept-btn-handler"]')
        
        self.escribir_seguro(browser, '(//*[@id="primaryPhoneInput"])[1]', telefono)
        self.escribir_seguro(browser, '(//*[@id="primaryPhoneInput"])[2]', telefono)
        
        if not self.click_seguro(browser, '//*[@id="continueButton"]'):
            return False, "No se pudo enviar"
        
        time.sleep(2)
        return True, "OK"


# ============================================================================
# LISTA DE TODAS LAS WEBS
# Para añadir una web nueva, créala arriba y agrégala a esta lista
# ============================================================================

def obtener_todas_las_webs():
    """Retorna lista con todas las webs disponibles"""
    return [
        SecuritasDirect(),
        Euroinnova(),
        Genesis(),
        RacctelPlus(),
        Jazztel(),
        Ford(),
        Vodafone(),
        Euskaltel(),
        Pelayo(),
        Movistar(),
        SantaLucia(),
        Asisa(),
        ITEP(),
        MasMovilAlarmas(),
        Prosegur(),
        LineaDirecta(),
        Telecable(),
        Mapfre(),
        Orange(),
        HomeGO(),
        Iberdrola(),
        ISalud(),
        Recordador(),
        ProyectosYSeguros(),
        MoneyGO(),
        Emagister(),
        MundoR(),
        HomeServe(),
        MasMovil(),
        Alarmak(),
        CentroDermatologico(),
        MutuaMadrilena(),
        Generali(),
        FiNetwork(),
        Regal(),
    ]


def ejecutar_todas(browser, nombre, apellido, telefono, email, hora_actual):
    """
    Ejecuta todas las webs habilitadas
    
    Returns:
        dict con estadísticas de ejecución
    """
    webs = obtener_todas_las_webs()
    resultados = []
    
    for web in webs:
        # Si está deshabilitada, skip
        if not web.habilitada:
            print(f"{web.nombre}: Deshabilitada")
            resultados.append({'web': web.nombre, 'estado': 'deshabilitada'})
            continue
        
        # Verificar horario si es necesario
        if web.requiere_horario and not web.verificar_horario(hora_actual):
            print(f"{web.nombre}: Skipeado (Fuera de Horario)")
            resultados.append({'web': web.nombre, 'estado': 'fuera_horario'})
            continue
        
        # Ejecutar la web
        try:
            exito, mensaje = web.ejecutar(browser, nombre, apellido, telefono, email)
            if exito:
                print(f"{web.nombre}: OK")
                resultados.append({'web': web.nombre, 'estado': 'exito'})
            else:
                print(f"{web.nombre}: Skipeado ({mensaje})")
                resultados.append({'web': web.nombre, 'estado': 'fallido', 'mensaje': mensaje})
        except Exception as e:
            print(f"{web.nombre}: Skipeado (ERROR)")
            resultados.append({'web': web.nombre, 'estado': 'error', 'mensaje': str(e)})
    
    # Calcular estadísticas
    total = len(resultados)
    exitos = sum(1 for r in resultados if r['estado'] == 'exito')
    fallos = sum(1 for r in resultados if r['estado'] in ['fallido', 'error'])
    skipeados = total - exitos - fallos
    
    return {
        'total': total,
        'exitos': exitos,
        'fallos': fallos,
        'skipeados': skipeados,
        'resultados': resultados
    }

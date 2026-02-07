#!/usr/bin/env python3
"""
PerubianBot - Sistema automatizado de peticiones
Solo 2 archivos: este (núcleo) y webs.py (todas las webs)
"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import sys
import time
import signal
import argparse
import requests
import re
from datetime import datetime
from colorama import Fore, Style
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from unidecode import unidecode

# Importar módulo de webs
import webs

# ============= CONFIGURACIÓN =============
VERSION = '3.0'
GIST_VERSION_URL = "https://gist.githubusercontent.com/Oihalitz/06b39df2b15439c8aa0c6419e5565341/raw/versionperubian.json"

PERUBIAN_BANNER = Fore.MAGENTA + Style.BRIGHT + r"""
  _____                _     _               ____      ___  
 |  __ \              | |   (_)             |___ \    / _ \ 
 | |__) |__ _ __ _   _| |__  _  __ _ _ __    __) |  | | | |
 |  ___/ _ \ '__| | | | '_ \| |/ _` | '_ \  |__ <   | | | |
 | |  |  __/ |  | |_| | |_) | | (_| | | | | ___) | _| |_| |
 |_|   \___|_|   \__,_|_.__/|_|\__,_|_| |_| |____(_)\___/  
""" + Style.RESET_ALL

# ============= VARIABLES GLOBALES =============
browser = None
interrupted = False
debug_mode = False
headless_mode = False

# ============= FUNCIONES NAVEGADOR =============

def configurar_navegador():
    """Configura y retorna el navegador (Firefox o Chrome)"""
    global browser
    
    # Intentar Firefox primero
    if os.name == 'nt':
        firefox_binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        PATH_TO_DEV_NULL = 'nul'
    elif os.uname().sysname == 'Darwin':
        firefox_binary = '/Applications/Firefox.app/Contents/MacOS/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    else:
        firefox_binary = '/usr/bin/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    
    if os.path.exists(firefox_binary):
        try:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("media.autoplay.default", 0)
            profile.accept_untrusted_certs = True
            profile.set_preference("media.volume_scale", "0.0")
            profile.set_preference("dom.webnotifications.enabled", False)
            
            geckodriver_path = './geckodriver' if not getattr(sys, 'frozen', False) else os.path.join(sys._MEIPASS, 'geckodriver')
            
            options = webdriver.FirefoxOptions()
            if headless_mode:
                options.headless = True
            
            browser = webdriver.Firefox(
                firefox_binary=firefox_binary,
                executable_path=geckodriver_path,
                firefox_profile=profile,
                service_log_path=PATH_TO_DEV_NULL,
                options=options
            )
            return browser
        except Exception as e:
            print(f"Error con Firefox: {e}")
    
    # Si Firefox falla, usar Chrome
    print("Usando Chrome...")
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--silent')
    if headless_mode:
        chrome_options.add_argument('--headless')
    
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


def cerrar_navegador():
    """Cierra el navegador de forma segura"""
    global browser
    if browser:
        try:
            browser.quit()
        except:
            pass
        browser = None


# ============= FUNCIONES FORMULARIO =============

def limpiar_consola():
    """Limpia la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def normalizar_texto(texto):
    """Elimina tildes y caracteres especiales"""
    texto = unidecode(texto)
    texto = re.sub(r'[^a-zA-Z0-9]', '', texto)
    return texto


def capturar_datos(datos_iniciales=None):
    """
    Captura los datos del usuario
    
    Returns:
        dict con nombre, apellido, telefono, email
    """
    if datos_iniciales:
        nombre, apellido, telefono, email = datos_iniciales
        return {
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'email': email
        }
    
    if debug_mode:
        limpiar_consola()
        print(PERUBIAN_BANNER)
        print('DEBUG MODE ON')
        return {
            'nombre': 'NombrePrueba',
            'apellido': 'ApellidoPrueba',
            'telefono': '666666666',
            'email': 'CorreoPrueba@gmail.com'
        }
    
    # Captura normal
    datos_mostrar = ''
    
    # Teléfono
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print(Fore.YELLOW + Style.BRIGHT + "Nº de Teléfono:")
    telefono = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL)
    
    prefijos = ('6', '7', '9')
    while len(telefono) != 9 or not telefono.isdigit() or telefono[0] not in prefijos:
        limpiar_consola()
        print(PERUBIAN_BANNER)
        print(Fore.RED + "Número incorrecto. Debe ser 9 dígitos y empezar por 6, 7 o 9" + Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + "Nº de Teléfono:")
        telefono = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL)
    
    datos_mostrar += Fore.WHITE + Style.BRIGHT + f"Nº de Teléfono: {telefono}\n" + Style.RESET_ALL
    
    # Nombre
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print(datos_mostrar)
    print(Fore.YELLOW + Style.BRIGHT + "Nombre de la persona:")
    nombre = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL).strip()
    while not nombre:
        print(Fore.RED + "El nombre no puede estar vacío" + Style.RESET_ALL)
        nombre = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL).strip()
    
    # Apellido
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print(datos_mostrar)
    print(Fore.YELLOW + Style.BRIGHT + "Apellido:")
    apellido = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL).strip()
    while not apellido:
        print(Fore.RED + "El apellido no puede estar vacío" + Style.RESET_ALL)
        apellido = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL).strip()
    
    datos_mostrar += Fore.WHITE + Style.BRIGHT + f"Nombre: {nombre} {apellido}\n" + Style.RESET_ALL
    
    # Normalizar para email
    nombre_norm = normalizar_texto(nombre.lower())
    apellido_norm = normalizar_texto(apellido.lower())
    
    # Email
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print(datos_mostrar)
    print(Fore.YELLOW + Style.BRIGHT + f"Si no indicas email se usará: {nombre_norm}.{apellido_norm}@gmail.com")
    print("Correo:")
    email = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL).strip()
    
    if not email:
        email = f'{nombre_norm}.{apellido_norm}@gmail.com'
    
    datos_mostrar += Fore.WHITE + Style.BRIGHT + f"Correo: {email}\n" + Style.RESET_ALL
    
    # Mostrar resumen
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print(datos_mostrar)
    
    return {
        'nombre': nombre_norm,
        'apellido': apellido_norm,
        'telefono': telefono,
        'email': email
    }


# ============= FUNCIONES AUXILIARES =============

def configurar_titulo_terminal():
    """Establece el título de la terminal"""
    if os.name == 'nt':
        os.system(f"title PerubianBot v{VERSION}")
    else:
        os.system(f"echo -e '\\033]2;PerubianBot v{VERSION}\\007'")


def verificar_version():
    """Verifica si hay nueva versión disponible"""
    try:
        current_version_num = VERSION.split(" ")[0]
        response = requests.get(GIST_VERSION_URL, timeout=5)
        response.raise_for_status()
        latest_version = response.json().get("latest_version")
        
        if not latest_version:
            return ""
        
        if current_version_num < latest_version:
            return f"¡Nueva versión disponible! (Actual: {VERSION}, Nueva: {latest_version})"
        else:
            return ""
    except:
        return ""


def manejar_interrupcion(sig, frame):
    """Maneja Ctrl+C"""
    global interrupted
    interrupted = True
    print("\n\nInterrumpido por el usuario. Cerrando navegador...")
    cerrar_navegador()
    print("¡Hasta pronto!")
    sys.exit(0)


# ============= FUNCIONES PRINCIPALES =============

def ejecutar_peticiones(datos, repetir=False):
    """Ejecuta las peticiones en todas las webs"""
    global interrupted
    
    while not interrupted:
        # Configurar navegador
        try:
            configurar_navegador()
        except Exception as e:
            print(f"Error configurando navegador: {e}")
            return
        
        # Obtener hora actual
        now = datetime.now()
        hora_actual = now.strftime("%H:%M:%S")
        
        print(f"\n{'='*60}")
        print(f"Iniciando peticiones - {hora_actual}")
        print(f"Datos: {datos['telefono']}")
        print(f"{'='*60}\n")
        
        # Ejecutar todas las webs
        stats = webs.ejecutar_todas(
            browser,
            datos['nombre'],
            datos['apellido'],
            datos['telefono'],
            datos['email'],
            hora_actual
        )
        
        # Mostrar estadísticas
        print(f"\n{'='*60}")
        print(f"ESTADÍSTICAS:")
        print(f"  Total: {stats['total']}")
        print(f"  Éxito: {stats['exitos']}")
        print(f"  Fallidos: {stats['fallos']}")
        print(f"  Skipeados: {stats['skipeados']}")
        if stats['total'] > 0:
            tasa = (stats['exitos'] / stats['total'] * 100)
            print(f"  Tasa de éxito: {tasa:.1f}%")
        print(f"{'='*60}\n")
        
        # Cerrar navegador
        cerrar_navegador()
        
        # Si no es repetición, salir
        if not repetir:
            break
        
        print("Modo repetición activado. Esperando para siguiente ronda...")
        time.sleep(5)


def modo_automatico():
    """Modo automático - captura datos y ejecuta"""
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print('Activando Modo Automático...\n')
    time.sleep(0.5)
    
    # Capturar datos
    datos = capturar_datos()
    
    # Preguntar por repetición
    if not debug_mode:
        repetir = input('\nModo repetición [S/N]: ').lower()
        repetir = repetir in ('y', 'yes', 's', 'si')
    else:
        repetir = False
    
    # Ejecutar
    ejecutar_peticiones(datos, repetir=repetir)
    
    input("\nPresiona ENTER para volver al menú...")


def listar_webs():
    """Lista todas las webs disponibles"""
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print('WEBS DISPONIBLES\n')
    
    lista_webs = webs.obtener_todas_las_webs()
    
    for i, web in enumerate(lista_webs, 1):
        status = "✓" if web.habilitada else "✗"
        horario = ""
        if web.requiere_horario:
            horario = f" (Horario: {web.hora_inicio} - {web.hora_fin})"
        
        print(f"{i}. {status} {web.nombre}{horario}")
    
    print(f"\nTotal: {len(lista_webs)} webs")
    input("\nPresiona ENTER para volver al menú...")


def ver_info():
    """Muestra información del sistema"""
    limpiar_consola()
    print(PERUBIAN_BANNER)
    print('INFORMACIÓN DEL SISTEMA\n')
    print(f"Versión: {VERSION}")
    print(f"Debug: {'Activado' if debug_mode else 'Desactivado'}")
    print(f"Headless: {'Activado' if headless_mode else 'Desactivado'}")
    print(f"Webs disponibles: {len(webs.obtener_todas_las_webs())}")
    print(f"\nArchivo de webs: webs.py")
    print(f"Archivo principal: {__file__}")
    
    input("\nPresiona ENTER para volver al menú...")


# ============= PROGRAMA PRINCIPAL =============

def main():
    """Función principal"""
    global debug_mode, headless_mode
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(description='PerubianBot - Sistema automatizado')
    parser.add_argument('--debug', action='store_true', help="Modo debug")
    parser.add_argument('--headless', action='store_true', help="Modo headless")
    parser.add_argument('--start', nargs=4, metavar=('nombre', 'apellido', 'telefono', 'email'),
                       help="Iniciar con datos: nombre apellido telefono email")
    
    args = parser.parse_args()
    
    debug_mode = args.debug
    headless_mode = args.headless
    
    # Configurar terminal
    configurar_titulo_terminal()
    
    # Manejar Ctrl+C
    signal.signal(signal.SIGINT, manejar_interrupcion)
    
    # Si se proporcionaron datos de inicio, ejecutar directamente
    if args.start:
        datos = capturar_datos(datos_iniciales=args.start)
        ejecutar_peticiones(datos, repetir=False)
        sys.exit(0)
    
    # Crear menú
    version_info = verificar_version()
    menu = ConsoleMenu(
        Fore.YELLOW + PERUBIAN_BANNER + version_info,
        "Seleccione una opción" + Style.RESET_ALL
    )
    
    # Añadir opciones
    item1 = FunctionItem("Modo Automático", modo_automatico)
    item2 = FunctionItem("Listar Webs Disponibles", listar_webs)
    item3 = FunctionItem("Información del Sistema", ver_info)
    
    menu.append_item(item1)
    menu.append_item(item2)
    menu.append_item(item3)
    
    # Mostrar menú
    menu.show()


if __name__ == "__main__":
    main()

import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

# Escuchar nuestro micro y devolver texto
def transformar_audio_texto():

    # Almacenar el recogniser en una variable
    r = sr.Recognizer()
    # Config. micro
    with sr.Microphone() as origen:
        # Tiempo espera
        r.pause_threshold = 0.8
        print("Ya puedes hablar")

        # Guardar audio en variable
        audio = r.listen(origen)

        try:
            # Buscar en google
            pedido = r.recognize_google_cloud(audio, lenguaje = "es-es")

            # Prueba de que pudo ingresar
            print("Dijistes: " + pedido)

            # Devolver pedido
            return pedido

        except sr.UnknownValueError:

            print("Ups, no entendi")

            return "Sigo esperando"

        except sr.RequestError:

            print("Ups, no hay servicio")

            return "Sigo esperando"

        except:

            print("Ups, algo ha salido mal")

            return "Sigo esperando"

#funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)

# Informar el dia
def pedir_dia():
    dia=datetime.datetime.today()
    print(dia)

    dia_semana = dia.weekday()
    print(dia_semana)

    calendario = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}

    hablar(f'Hoy es {calendario[dia_semana]}')

def pedir_hora():
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)
    hablar(hora)

def saludo_inicial():

    #variable con datos d ehora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buenos días"
    else:
        momento = "Buenas tardes"


    hablar(f"{momento} soy Helena, tu asistente personal, por favor, dime en que te puedo ayudar")

def pedir_cosas():

    saludo_inicial()

    comenzar = True

    while comenzar:

        #Activar el micro y guardar el pedido en un string
        pedido = transformar_audio_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar ("claro, estoy en eso")
            webbrowser.open('https://www.google.com')
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es hoy' in pedido:
            pedir_hora()
            continue
        elif 'buscar en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar(' Ya mismo estoy en ello')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit. search(pedido)
            hablar('esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar("Buena idea, ya comienzo a reproducirlo")
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
            except:
                print('Lo siento, no lo he encontrado')
        elif 'adios' in pedido:
            hablar('Me voy a descansar, si necesita ayuda, aquí estaré')
            break

pedir_cosas()


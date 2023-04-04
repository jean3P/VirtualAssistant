import pyaudio
import speech_recognition as sr
from langdetect import detect
import openai
from gtts import gTTS
import os
import simpleaudio as sa
from pydub import AudioSegment

openai.api_key = ''


def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return None


def listar_microfonos():
    mic_list = sr.Microphone.list_microphone_names()
    for idx, mic in enumerate(mic_list):
        print(f"Índice: {idx} - Nombre: {mic}")

def reconocer_voz(idioma, mic_index):
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=mic_index) as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=idioma)
            print(f"Usted dijo: {text}")
            return text
        except:
            print("Lo siento, no pude entender lo que dijiste.")
            return None

def listar_dispositivos_salida():
    pa = pyaudio.PyAudio()
    for idx in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(idx)
        if device_info.get('maxOutputChannels') > 0:
            print(f"Índice: {idx} - Nombre: {device_info['name']}")

def mapear_idioma(lang):
    if lang == "en":
        return "en-GB"
    elif lang == "es":
        return "es-ES"
    elif lang == "de":
        return "de-DE"
    elif lang == "fr":
        return "fr-FR"
    else:
        return "en-GB"  # Por defecto, usar inglés


def chat_gpt(texto_usuario, idioma):
    respuesta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"[{idioma}] Usuario: {texto_usuario}\nAsistente:",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return respuesta.choices[0].text.strip()


import pygame

def hablar(texto, idioma, output_device_index=None):
    tts = gTTS(text=texto, lang=idioma, slow=False)
    tts.save("respuesta.mp3")

    # Inicializar pygame y cargar el archivo MP3
    pygame.mixer.init()
    pygame.mixer.music.load("respuesta.mp3")

    # Establecer el índice del dispositivo de salida si se proporciona
    if output_device_index is not None:
        pygame.mixer.set_num_channels(output_device_index)

    # Reproducir el archivo MP3
    pygame.mixer.music.play()

    # Esperar a que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Detener la reproducción y terminar pygame
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Eliminar el archivo MP3
    os.remove("respuesta.mp3")



def main():
    while True:
        print("Por favor, diga algo en inglés, español, alemán o francés:")
        texto_inicial = reconocer_voz("en-GB", 1)  # Utilizar inglés británico como idioma predeterminado para la detección inicial
        if texto_inicial is not None:
            idioma_detectado = detectar_idioma(texto_inicial)
            if idioma_detectado:
                idioma = mapear_idioma(idioma_detectado)
                print(f"Idioma detectado: {idioma_detectado}")
                texto_usuario = reconocer_voz(idioma, 1)
                if texto_usuario is not None:
                    respuesta = chat_gpt(texto_usuario, idioma_detectado)  # Utilizar el idioma detectado en la función chat_gpt()
                    print(f"Asistente: {respuesta}")
                    hablar(respuesta, idioma_detectado, 0)  # Utilizar el idioma detectado en la función hablar()


if __name__ == "__main__":
    # listar_microfonos()
    # listar_dispositivos_salida()
    # hablar("Hola, estoy utilizando la salida de audio del monitor.", "es", 0)
    texto_usuario = "What's the weather like today?"
    idioma = "en"

    respuesta_asistente = chat_gpt(texto_usuario, idioma)
    print(f"Asistente: {respuesta_asistente}")
    # main()
import gradio as gr
import speech_recognition as sr
from moviepy.editor import VideoFileClip
import math
import time

def convert_video_to_wav(input_path, output_path):
    print("Convertendo vídeo para WAV...")
    video_clip = VideoFileClip(input_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='pcm_s16le')
    print("Conversão concluída.")

def audio_to_text(audio_chunk):
    recognizer = sr.Recognizer()

    try:
        print("Realizando reconhecimento de fala...")
        text = recognizer.recognize_google(audio_chunk, language='pt-BR')
        print("Reconhecimento de fala concluído.")
        return text
    except sr.UnknownValueError as unknown_error:
        print("Erro de reconhecimento de fala:", unknown_error)
        return "Não foi possível reconhecer fala no trecho de áudio."
    except sr.RequestError as request_error:
        print("Erro ao fazer a requisição ao serviço de reconhecimento:", request_error)
        return f"Erro ao fazer a requisição ao serviço de reconhecimento: {request_error}"

def process_media(media_file):
    print("Processando mídia...")
    # Convert video to WAV
    wav_output_path = "output_audio.wav"
    convert_video_to_wav(media_file.name, wav_output_path)

    # Load audio
    audio_clip = AudioFileClip(wav_output_path)
    chunk_duration = 30  # 30 segundos

    transcribed_text = ""
    num_chunks = math.ceil(audio_clip.duration / chunk_duration)
    
    for i in range(num_chunks):
        chunk_start = i * chunk_duration
        chunk_end = min((i + 1) * chunk_duration, audio_clip.duration)
        chunk = audio_clip.subclip(chunk_start, chunk_end)
        chunk_text = audio_to_text(chunk)
        transcribed_text += chunk_text + " "
        
        # Aguarda a resposta da API antes de continuar para o próximo trecho
        time.sleep(2)  # Espera 2 segundos entre as requisições
    
    return transcribed_text

iface = gr.Interface(
    fn=process_media,
    inputs="file",
    outputs="text",
    title="Transcrição de Vídeo para Texto",
    description="Carregue um arquivo de vídeo e obtenha a transcrição de áudio.",
)

if __name__ == "__main__":
    iface.launch(share=True)  # Inicia no navegador

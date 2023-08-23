import gradio as gr
import speech_recognition as sr
from moviepy.editor import VideoFileClip

def convert_video_to_wav(input_path, output_path):
    print("Convertendo vídeo para WAV...")
    video_clip = VideoFileClip(input_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='pcm_s16le')
    print("Conversão concluída.")

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        print("Realizando reconhecimento de fala...")
        text = recognizer.recognize_google(audio, language='pt-BR')
        print("Reconhecimento de fala concluído.")
        return text
    except sr.UnknownValueError as unknown_error:
        print("Erro de reconhecimento de fala:", unknown_error)
        return "Não foi possível reconhecer fala no arquivo de áudio."
    except sr.RequestError as request_error:
        print("Erro ao fazer a requisição ao serviço de reconhecimento:", request_error)
        return f"Erro ao fazer a requisição ao serviço de reconhecimento: {request_error}"

def process_media(media_file):
    print("Processando mídia...")
    # Convert video to WAV
    wav_output_path = "output_audio.wav"
    convert_video_to_wav(media_file.name, wav_output_path)

    # Transcribe audio
    transcribed_text = audio_to_text(wav_output_path)

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
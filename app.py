import gradio as gr
import soundfile as sf
from kokoro import KPipeline
import os

# โหลด Pipeline สำหรับภาษาอังกฤษ
pipeline = KPipeline(lang_code='a')

def predict(text, voice, base_filename):
    if not base_filename.strip():
        base_filename = "output"
    
    generator = pipeline(text, voice=voice, speed=1.0)
    
    saved_files = []
    first_audio_path = None
    
    for i, (gs, ps, audio) in enumerate(generator):
        filename = f"{base_filename}_{i+1}.wav"
        sf.write(filename, audio, 24000)
        saved_files.append(filename)
        if first_audio_path is None:
            first_audio_path = filename  # เก็บไฟล์แรกไว้สำหรับกด Play ฟังตัวอย่าง

    # ส่งคืนทั้งไฟล์แรก (สำหรับเล่นเสียง) และรายการไฟล์ทั้งหมด (สำหรับดาวน์โหลด)
    return first_audio_path, saved_files

# สร้างหน้าเว็บ Gradio
demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Textbox(label="Enter Text", value="Hello! Kokoro is running locally on Windows 11. This tool can split your long text into multiple audio files automatically.", lines=5),
        gr.Dropdown(
            choices=[
                # American Female
                "af_heart", "af_bella", "af_nicole", "af_sarah", "af_sky", "af_alloy", "af_aoede", "af_jessica", "af_kore",
                # American Male
                "am_adam", "am_michael", "am_fenrir", "am_puck", "am_eric", "am_liam", "am_onyx", "am_echo",
                # British Female
                "bf_emma", "bf_isabella", "bf_alice", "bf_lily",
                # British Male
                "bm_george", "bm_lewis", "bm_fable", "bm_daniel"
            ], 
            label="Select Voice", 
            value="af_heart"
        ),
        gr.Textbox(label="Custom File Name (ชื่อไฟล์ที่ต้องการตั้ง เช่น my_audio)", value="my_audio")
    ],
    outputs=[
        gr.Audio(label="Play First Audio (กดฟังเสียงตัวอย่างท่อนแรก)"),
        gr.Files(label="All Generated Audio Files (ดาวน์โหลดไฟล์ทั้งหมดแยกตามท่อน)")
    ],
    title="Kokoro-82M Local TTS"
)

if __name__ == "__main__":
    demo.launch(inbrowser=True)

import assemblyai as aai
import torch
from mmtafrica.mmtafrica import load_params, translate
from huggingface_hub import hf_hub_download
import sys
import os
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from .lib import *


class Genetator : 

    def __init__(self , filename) -> None:
        self.filename = filename

    
    def run(self):
        self.generateSubtitile(filename=self.filename)
        self.add_subtitles_to_video(
            subtitles_path=self.subtitle_fon , 
            output_path=self.filename_name+"(fon).mp4"
        )
        
        
    def generateSubtitile(self , filename) :
        aai.settings.api_key = "3bc5ca9c34754d5baa7dae38b6041003"
        filename_parent =  Path(filename).parent
        filename_name =  Path(filename).stem
        self.filename_name = filename
        
        transcript = aai.Transcriber().transcribe(rf"{filename}")
        subtitles = transcript.export_subtitles_srt()

        subtitles_path = filename_parent / f"{filename_name}.srt"
        with open(subtitles_path , "w") as f : 
            f.write(subtitles)


        # Define language map and model parameters
        self.language_map = {'English': 'en', 'Fon': 'fon'}
        checkpoint = hf_hub_download(repo_id="chrisjay/mmtafrica", filename="mmt_translation.pt")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.params = load_params({'checkpoint': checkpoint, 'device': device})
        
        self.subtitle_fon = filename_parent / f"{filename_name}(fon).srt"

        self.process_srt_file(
            input_file_path=self.filename , 
            output_file_path=self.subtitle_fon , 
        )
        
    def get_translation(self , source_language, target_language, source_sentence):
        '''
        Function to get translation using the mmtafrica model.
        '''
        source_lang = self.language_map[source_language]
        target_lang = self.language_map[target_language]
        return translate(self.params, source_sentence, source_lang=source_lang, target_lang=target_lang)


    def process_srt_file(self , input_file_path, output_file_path):
        '''
        Process and translate an SRT file from English to Fon.
        '''
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            buffer = []
            for line in lines:
                if line.strip().isdigit():
                    if buffer:
                        translated_text = self.get_translation('English', 'Fon', ' '.join(buffer))
                        out_file.write(f"{index}{timeframe}{translated_text}\n\n")
                        buffer = []
                    index = line
                elif '-->' in line:
                    timeframe = line
                elif line.strip() == '':
                    continue
                else:
                    buffer.append(line.strip())

            # Translate and write the last buffered subtitle if any
            if buffer:
                translated_text = self.get_translation('English', 'Fon', ' '.join(buffer))
                out_file.write(f"{index}\n{timeframe}\n{translated_text}\n\n")
        


    def add_subtitles_to_video(video_path, subtitles_path, output_path):
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"subtitles={subtitles_path}",
            output_path
        ]
        return " ".join(command)



class Worker(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self) : 
        try : 
            self.generator = Genetator(self.filename)
            self.finished.emit(True)
        except Exception as e :
            self.finished.emit(False)
            print(e)
        
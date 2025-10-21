# autogram/tools/veo_tool.py
import time
from google import genai
from google.genai import types

class VeoTool:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_video(self, prompt: str = None, from_file: str = None, output_file: str = "autogram_output.mp4"):
        """
        Generates a video using Google Veo 3 based on a text prompt or a script file.
        """
        # Read from file if provided
        if from_file and not prompt:
            with open(from_file, "r", encoding="utf-8") as f:
                prompt = f.read().strip()

        if not prompt:
            raise ValueError("No prompt provided to VeoTool. Please pass a text prompt or file path.")

        print("Generating video from script...")

        operation = self.client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
        )

        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            operation = self.client.operations.get(operation)

        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video)
        generated_video.video.save(output_file)
        print(f"Video saved to {output_file}")
        return output_file


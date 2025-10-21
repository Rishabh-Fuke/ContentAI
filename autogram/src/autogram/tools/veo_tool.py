# autogram/tools/veo_tool.py
import time
from typing import Any, Optional

from crewai.tools.base_tool import BaseTool
from google import genai
from google.genai import types


class VeoTool(BaseTool):
    """Generates videos using Google Veo 3 as a CrewAI tool."""

    name: str = "veo_tool"
    description: str = "Generates a video using Google Veo 3 based on a text prompt or a script file."

    # Pydantic (BaseTool) requires model fields to be declared. Declare runtime fields here.
    api_key: Optional[str] = None
    client: Optional[Any] = None

    def __init__(self, api_key: str):
        # Initialize pydantic BaseModel parent
        super().__init__()
        # Assign declared model fields
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)

    def _run(self, prompt: str | None = None, from_file: str | None = None, output_file: str = "autogram_output.mp4") -> str:
        """
        CrewAI will call this method internally when the agent uses the tool.

        Provide either `prompt` or `from_file` (path to a text file containing the prompt).
        Returns the path to the generated video file.
        """

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

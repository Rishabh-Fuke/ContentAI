from crewai.tools import BaseTool #type: ignore
from pydantic import BaseModel, Field
from typing import Type
import os

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class SummarizerToolInput(BaseModel):
    text: str = Field(..., description="Text to summarize")
    max_tokens: int = Field(100, description="Maximum tokens for the summary") #Cap at 100 for short videos


class SummarizerTool(BaseTool):
    name: str = "summarizer"
    description: str = "Summarize provided text using OpenAI (requires OPENAI_API_KEY)."
    args_schema: Type[BaseModel] = SummarizerToolInput

    def _run(self, text: str, max_tokens: int = 100) -> str:
        key = os.environ.get('OPENAI_API_KEY')
        if not key:
            return "ERROR: OPENAI_API_KEY not set in environment. Set OPENAI_API_KEY in autogram/.env or the shell."

        if OpenAI is None:
            return "ERROR: openai package is not available in the environment."

        try:
            client = OpenAI(api_key=key)
            prompt = (
                "Summarize the following content in a concise, structured way suitable for a social media caption:\n\n"
                + text
            )
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
         
            if hasattr(resp, 'choices') and resp.choices:
                return resp.choices[0].message.content
            return str(resp)
        except Exception as e:
            return f"ERROR: openai summary failed: {e}"

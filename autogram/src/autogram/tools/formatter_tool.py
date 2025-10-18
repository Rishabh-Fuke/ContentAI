from crewai.tools import BaseTool #type:ignore
from pydantic import BaseModel, Field
from typing import Type
import textwrap


class FormatterToolInput(BaseModel):
    text: str = Field(..., description="Text to format")
    style: str = Field('markdown', description="Formatting style: 'markdown' or 'plain'")


class FormatterTool(BaseTool):
    name: str = "formatter"
    description: str = "Format text into Markdown or plain text for display."
    args_schema: Type[BaseModel] = FormatterToolInput

    def _run(self, text: str, style: str = 'markdown') -> str:
        if style == 'plain':
            return textwrap.fill(text, width=80)

       
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        md = []
        for p in paragraphs:
            md.append(p)

        return "\n\n".join(md)

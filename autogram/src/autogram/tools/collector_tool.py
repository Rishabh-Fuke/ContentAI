from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os
import requests





class CollectorToolInput(BaseModel):
    """Input schema for CollectorTool."""
    query: str = Field(..., description="Search query or URL to collect from")
    num_results: int = Field(3, description="Number of results to return")


class CollectorTool(BaseTool):
    name: str = "web_collector"
    description: str = (
        "Collect web content using Serper (accepts SERPER_API_KEY or SERPER_KEY in environment)."
    )
    args_schema: Type[BaseModel] = CollectorToolInput

    def _run(self, query: str, num_results: int = 3) -> str:
    
        key = os.environ.get('SERPER_API_KEY') or os.environ.get('SERPER_KEY')
        if not key:
            return "ERROR: SERPER API key not set. Set SERPER_API_KEY or SERPER_KEY in autogram/.env or the shell."

        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": key, "Content-Type": "application/json"}
        payload = {"q": query, "num": num_results}

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return f"ERROR: failed to fetch from Serper: {e}"

     
        snippets = []
        try:
            if isinstance(data, dict):
               
                for section in ('organic', 'items', 'results'):
                    if section in data and isinstance(data[section], list):
                        for item in data[section][:num_results]:
                            if isinstance(item, dict):
                                text = item.get('snippet') or item.get('description') or item.get('title') or ''
                                link = item.get('link') or item.get('url')
                                if text:
                                    snippets.append(text + (f" (source: {link})" if link else ""))
                        break

           
            if not snippets:
                snippets.append(str(data)[:2000])
        except Exception:
            snippets.append(str(data))

        return "\n\n".join(snippets)

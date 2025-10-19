#!/usr/bin/env python3
"""Simple demo runner: collect -> summarize -> format -> write report.md

This script adjusts sys.path so it can be run from the project root without needing
PYTHONPATH set externally. It expects the environment keys to be available via
`autogram/.env` (autogram package loads it) or the shell.
"""
from __future__ import annotations
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
# Ensure autogram/src is importable without requiring PYTHONPATH externally
sys.path.insert(0, str(root / 'autogram' / 'src'))

from autogram.tools.collector_tool import CollectorTool
from autogram.tools.summarizer_tool import SummarizerTool
from autogram.tools.formatter_tool import FormatterTool


def main() -> None:
    query = "recent advances in neuroscience"
    collector = CollectorTool()
    summarizer = SummarizerTool()
    formatter = FormatterTool()

    print("[demo] Collecting web content for query:", query)
    collected = collector._run(query=query, num_results=3)
    if isinstance(collected, str) and collected.startswith("ERROR"):
        print("[demo] Collector error:", collected)
        return

    print("[demo] Collected length:", len(collected))

    # 1) Research summary (structured, cite sources)
    print("[demo] Creating structured research summary...")
    research_prompt = (
        "You are an expert neuroscience researcher. Read the collected web snippets below and produce:\n"
        "1) A concise research summary (3-6 bullet findings) with citations in parentheses when sources are present;\n"
    "2) A short 'elevator pitch' (1-2 sentences) suitable as a social media hook;\n"
        "3) A list of the original sources (URLs) identified in the collected text.\n\n"
        "Collected content:\n\n"
        + collected
    )

    research = summarizer._run(text=research_prompt, max_tokens=600)
    if isinstance(research, str) and research.startswith("ERROR"):
        print("[demo] Summarizer error (research):", research)
        return

    # 2) Create a full educational video script (wizard goat persona) from the research
    print("[demo] Creating full educational video script (wizard goat)...")
    script_prompt = (
        "Using the research summary below, write a full, detailed educational video script for a character: the 'Wizard Goat'.\n"
        "Include: character description, scene directions, full dialogue (with timestamps or cue lines), visual notes, pacing cues, and a short call-to-action at the end.\n\n"
        "Research summary:\n\n"
        + research
    )

    script = summarizer._run(text=script_prompt, max_tokens=1200)
    if isinstance(script, str) and script.startswith("ERROR"):
        print("[demo] Summarizer error (script):", script)
        return

    # Format both outputs
    print("[demo] Formatting outputs for report")
    formatted_research = formatter._run(text=research, style='markdown')
    formatted_script = formatter._run(text=script, style='markdown')

    # Tool trace (which env vars we saw)
    import os
    from datetime import datetime

    trace_lines = [
        f"Generated: {datetime.utcnow().isoformat()} UTC",
        f"SERPER_KEY present: {bool(os.environ.get('SERPER_KEY'))}",
        f"SERPER_API_KEY present: {bool(os.environ.get('SERPER_API_KEY'))}",
        f"OPENAI_API_KEY present: {bool(os.environ.get('OPENAI_API_KEY'))}",
    ]

    out_path = root / 'report.md'
    with out_path.open('w', encoding='utf-8') as f:
        f.write('# Autogram Demo Report\n\n')
        f.write(f'**Query:** {query}\n\n')
        f.write('---\n\n')
        f.write('## Research Summary\n\n')
        f.write(formatted_research + '\n\n')
        f.write('---\n\n')
        f.write('## Educational Video Script (Wizard Goat)\n\n')
        f.write(formatted_script + '\n\n')
        f.write('---\n\n')
        f.write('## Tool trace\n\n')
        for line in trace_lines:
            f.write(f'- {line}\n')

    print(f"[demo] Report written to: {out_path}")


if __name__ == '__main__':
    main()

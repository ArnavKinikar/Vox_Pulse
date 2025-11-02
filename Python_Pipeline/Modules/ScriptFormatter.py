import os
import re
from langchain_ollama import ChatOllama


class ScriptFormatter:
    def __init__(self, model_name="deepseek-r1:1.5b", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.model = ChatOllama(model=model_name, temperature=temperature)

    @staticmethod
    def remove_think_tags(text):
        """Removes <think>...</think> sections from model output."""
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    def format_to_script(self, title, summary):
        """Convert a summary into a podcast-style two-speaker dialogue."""
        print(f"🎙️ Using model '{self.model_name}' to generate dialogue script...")

        speech_prompt = f"""You are an AI narrator that turns factual news articles into realistic, natural podcast dialogues
between two speakers.

Follow these rules exactly:

1. Output ONLY a Python-style list of tuples — NO explanations, markdown, or extra text.
2. Format strictly as:
   [ ("en_speaker_0", "line 1"), ("en_speaker_1", "line 2"), ("en_speaker_0", "line 3"), ]
3. Alternate speakers naturally — one speaks, then the other responds.
4. Begin with en_speaker_0 introducing the article title conversationally.
5. Write like two hosts discussing a story, not reading a report.
6. Use curiosity, reactions, short questions, and small talk.
7. Break long or dense information into small, interactive exchanges.
8. Each line must sound spoken — under 25 words.
9. Do not summarize or skip content — include all major points conversationally.
10. Aim for 16–24 total dialogue lines for a balanced podcast segment.
11. Absolutely no triple backticks, markdown, or narration outside the tuple list.

Content Title: {title}

Content:
{summary}
"""
        response = self.model.invoke(speech_prompt)
        script = self.remove_think_tags(response.content.strip())
        return script

    def format_file(self, summary_file_path, output_folder="Speeches"):
        """Read a summary file, convert it to dialogue format, and save to file."""
        os.makedirs(output_folder, exist_ok=True)
        file_name = os.path.basename(summary_file_path)
        output_path = os.path.join(output_folder, file_name)

        with open(summary_file_path, "r", encoding="utf-8") as f:
            summary = f.read()

        # Use the file name (without extension) as a fallback title
        title = os.path.splitext(file_name)[0]

        script = self.format_to_script(title, summary)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script)

        print(f"✅ Speech script saved to: {output_path}")
        return output_path, script

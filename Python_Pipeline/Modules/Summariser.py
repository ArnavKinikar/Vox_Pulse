import os
import re
from langchain_ollama import ChatOllama


class Summariser:
    def __init__(self, model_name="PodSummariser", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.model = ChatOllama(model=model_name, temperature=temperature)

    @staticmethod
    def remove_think_tags(text):
        """Removes <think>...</think> sections from model output."""
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    def summarize_text(self, text):
        """Generate a concise summary of the provided text."""
        print(f"🧠 Using model '{self.model_name}' to summarize text...")
        summary_prompt = f"Please summarize the following text into 3 big paragraphs:\n\n{text}"
        response = self.model.invoke(summary_prompt)
        summary = self.remove_think_tags(response.content.strip())
        return summary

    def summarize_file(self, input_file_path, output_folder="Summaries"):
        """Read a file, summarize it, and save the summary to a file."""
        os.makedirs(output_folder, exist_ok=True)
        file_name = os.path.basename(input_file_path)
        output_path = os.path.join(output_folder, file_name)

        with open(input_file_path, "r", encoding="utf-8") as f:
            text = f.read()

        summary = self.summarize_text(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"✅ Summary saved to: {output_path}")
        return output_path, summary

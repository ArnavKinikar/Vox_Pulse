import logging
import os
import re
import json
from Pipeline.Modules.Fetcher import NewsFetcher
from Pipeline.Modules.Scraper import NewsScraper
from Pipeline.Modules.Summariser import Summariser
from Pipeline.Modules.ScriptFormatter import ScriptFormatter
from Pipeline.Modules.TTSGenerator import TTSGenerator
from Pipeline.Individual_Items import NewsItem
from Pipeline.Modules.InsertDatabase import save_news_to_db


class NewsPipeline:
    """
    Orchestrates the full AI podcast pipeline:
    1. Fetch titles via NewsAPI
    2. Scrape related articles
    3. Summarize text
    4. Convert summary to podcast dialogue script
    5. Generate final TTS audio file
    6. Save all data to JSON file
    """

    def __init__(self, output_dir="Outputs"):
        self.fetcher = NewsFetcher()
        self.scraper = NewsScraper()
        self.summarizer = Summariser()
        self.formatter = ScriptFormatter()
        self.tts = TTSGenerator()
        self.output_dir = output_dir

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def run(self, category):
        print(f"\n🚀 --- Starting News Pipeline for '{category}' ---")

        # 1. Fetch titles
        titles = self.fetcher.fetch_titles(category=category)
        if not titles:
            print("❌ No titles fetched. Exiting pipeline.")
            return []

        all_items = []

        for i, title_item in enumerate(titles, start=1):
            title = title_item.title if isinstance(title_item, NewsItem) else title_item
            print(f"\n📰 Processing: {i}: {title}")

            # Initialize NewsItem
            item = NewsItem(title=title)
            item.category = category
            # 2. Scrape related articles for the title
            articles = self.scraper.get_articles_for_heading(title)
            if not articles:
                print("⚠️ No articles found for this title. Skipping...")
                continue

            # Save URLs and combined content
            item.url = [a["url"] for a in articles]
            item.content = "\n".join([a["text"] for a in articles])

            # 3. Summarize the combined text
            print("🧠 Summarizing...")
            item.summary = self.summarizer.summarize_text(item.content)

            # 4. Convert summary into podcast-style dialogue
            print("🗣️ Formatting script...")
            item.script = self.formatter.format_to_script(item.title, item.summary)

            # 5. Generate TTS audio
            print("🎧 Generating audio...")
            audio_dir = os.path.join(self.output_dir)
            os.makedirs(audio_dir, exist_ok=True)

            safe_title = self._sanitize_filename(item.title)
            audio_name = f"http://192.168.1.35:5000/api/audio/{safe_title}.wav"

            # Try to generate the audio
            output_path = self.tts.generate_conversation(item.script, output_name=f"{safe_title}.wav")

            # Only proceed if audio was actually created
            if output_path is None:
                print(f"⚠️ Skipping database entry for '{item.title}' — audio generation failed.")
                logging.warning(f"Skipped database entry for '{item.title}' (no audio generated).")
                return  # <-- stop right here, don’t insert or save anything

            # Otherwise, safe to assign and insert
            item.audio_file = audio_name
            print(f"✅ Audio generated successfully for: {item.title}")

            # 6. Save NewsItem to JSON file
            json_path = os.path.join(self.output_dir, f"{safe_title}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump({
                    "title": item.title,
                    "category": item.category,
                    "url": item.url,
                    "content": item.content,
                    "summary": item.summary,
                    "script": item.script,
                    "audio_file": item.audio_file
                }, f, ensure_ascii=False, indent=4)

            print(f"✅ Saved data for '{item.title}' to {json_path}")

            # 7. Save NewsItem to Database
            save_news_to_db(item)

            # Add to final list
            all_items.append(item)

        print(f"\n✅ --- Pipeline complete for '{category}' ---")
        return all_items

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize filenames by removing or replacing illegal and unsafe characters."""

        # Separate extension if present
        base, ext = os.path.splitext(name)

        # Replace spaces with underscores
        base = base.replace(' ', '_')

        # Replace common problematic symbols
        base = re.sub(r'[<>:"/\\|?*&£@#%]', '_', base)

        # Replace multiple underscores with a single one
        base = re.sub(r'_+', '_', base)

        # Strip underscores or dots from the beginning and end
        base = base.strip('._')

        # Recombine and return
        return f"{base}{ext}"


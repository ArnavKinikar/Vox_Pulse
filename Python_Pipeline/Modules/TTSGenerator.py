import os
import re
import numpy as np
import logging
from bark import generate_audio, preload_models
from scipy.io.wavfile import write


class TTSGenerator:
    """
    Converts a script (as text or list of (speaker, text) tuples)
    into a single audio file using Bark.
    """

    def __init__(self, sample_rate=22050, silence_duration=0.5, output_folder="AudioOutput"):
        self.sample_rate = sample_rate
        self.silence_duration = silence_duration
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

        # --- Logging Setup ---
        log_file = os.path.join(self.output_folder, "tts_log.log")
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            filemode="a"
        )

        print("🎧 Preloading Bark models (first time may take a few minutes)...")
        preload_models()

    # -------------------------------------------------------
    # CLEANING HELPERS
    # -------------------------------------------------------

    def _extract_valid_tuples(self, text):
        """
        Extracts valid (speaker, text) tuples from messy AI output.
        Handles extra parentheses, junk, or triple-element tuples.
        """
        pattern = r'\(\s*"(en_speaker_[01])"\s*,\s*"([^"]+)"'
        matches = re.findall(pattern, text)
        return [(speaker, line.strip()) for speaker, line in matches]

    def _parse_dialogue_string(self, dialogue_str):
        """
        Cleans and parses AI-generated text safely into a valid list of tuples.
        """
        cleaned = dialogue_str.replace("```python", "").replace("```", "").strip()
        cleaned = re.sub(r'["]{3,}', '"', cleaned)
        cleaned = re.sub(r"[']{3,}", "'", cleaned)

        # Extract valid (speaker, text) pairs
        dialogue_list = self._extract_valid_tuples(cleaned)

        if not dialogue_list:
            raise ValueError("No valid dialogue lines found in model output.")

        return dialogue_list

    # -------------------------------------------------------
    # AUDIO GENERATION
    # -------------------------------------------------------

    def _generate_segment(self, speaker, text):
        """
        Generate one audio segment for a single line of dialogue.
        """
        audio = generate_audio(text, history_prompt=f"v2/{speaker}")
        audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
        return audio

    def generate_conversation(self, dialogue, output_name="conversation.wav"):
        """
        Takes either:
          - a list of (speaker, text) tuples, OR
          - a messy string representation of such a list (from LLM output),
        and generates a full conversation WAV file.
        """
        print("🎙️ Generating AI voice conversation...")

        # Step 1: Handle string input safely
        if isinstance(dialogue, str):
            try:
                dialogue = self._parse_dialogue_string(dialogue)
            except Exception as e:
                print(f"⚠️ Skipping audio generation — failed to parse dialogue string: {e}")
                logging.warning(f"Skipped generation for {output_name}: failed to parse dialogue ({e})")
                return None  # <-- Stop here (no audio generated)

        # Step 2: Validate dialogue format
        if not isinstance(dialogue, list) or not all(isinstance(i, tuple) and len(i) == 2 for i in dialogue):
            print("⚠️ Skipping audio generation — invalid dialogue format.")
            logging.warning(f"Skipped generation for {output_name}: invalid dialogue format.")
            return None  # <-- Stop here (no audio generated)

        segments = []
        silence = np.zeros(int(self.sample_rate * self.silence_duration), dtype=np.int16)

        for i, (speaker, text) in enumerate(dialogue, 1):
            print(f"🔊 [{i}/{len(dialogue)}] {speaker}: {text}")
            try:
                segment = self._generate_segment(speaker, text)
                segments.append(segment)
                segments.append(silence)
            except Exception as e:
                print(f"⚠️ Failed to generate audio for line {i}: {e}")
                logging.error(f"Line {i} failed: {e}")

        if not segments:
            print("⚠️ No audio segments generated — skipping file creation.")
            logging.warning(f"No audio segments generated for {output_name}.")
            return None

        full_audio = np.concatenate(segments)
        output_path = os.path.join(r"C:\Programs\Node\VoxPulse_Backend\audio", output_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write(output_path, self.sample_rate, full_audio)

        print(f"\n✅ Conversation generated successfully at: {output_path}")
        return output_path
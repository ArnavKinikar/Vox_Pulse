Vox Pulse

Vox Pulse is an AI-powered podcast generation system that automatically converts current news articles and research content into narrated podcast episodes.
It integrates AI models, web scraping, and text-to-speech synthesis to produce complete spoken summaries in real time.

🧩 Project Overview

Vox Pulse automates the process of turning written information into an engaging podcast experience.
The system performs the following steps:

Collects news and article data from the web.

Summarizes and script-writes the content using advanced language models.

Generates speech from the scripts using a realistic AI voice.

Makes episodes playable within the Flutter mobile application.

⚙️ Development Summary

Frontend (Flutter):
Built using the Flutter framework to create a responsive cross-platform mobile app.
The app displays generated podcast titles, descriptions, and playback controls, allowing users to stream AI-generated episodes.

Backend (Node.js + MySQL):
Node.js is used to serve APIs and manage data flow between the Flutter app and the database.
MySQL (through XAMPP) stores metadata such as episode titles, descriptions, audio URLs, and timestamps.

AI & Automation Pipeline (Python):
The Python pipeline handles the core generative process:

DuckDuckGo Search for gathering recent web content and articles.

Ollama DeepSeek R1 for summarization and script writing.

Bark (by Suno) for generating natural-sounding speech from the script.
The generated audio files are saved locally and registered in the database for playback through the app.

🧠 Technologies Used
Component	Technology / Tool
Frontend	Flutter (Dart), ExoPlayer
Backend	Node.js (Express), MySQL (XAMPP)
AI Pipeline	Python
Summarization & Scriptwriting	Ollama DeepSeek R1
Web Scraping	DuckDuckGo Search
Text-to-Speech	Bark by Suno
Data Handling	REST API, JSON
🎯 Objective
To create an end-to-end automated system that generates spoken podcast episodes from online text sources using AI for writing and voice generation, providing an efficient and accessible way to consume daily information. create an end-to-end automated system that generates spoken podcast episodes from online text sources using AI for writing and voice generation, providing an efficient and accessible way to consume daily information.

Would you like me to make this one slightly more academic and formal (like something you’d att

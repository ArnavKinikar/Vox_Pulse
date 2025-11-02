# **Vox Pulse**

Vox Pulse is an AI-powered podcast generation system that automatically converts current news articles and research content into narrated podcast episodes.
It integrates AI models, web scraping, and text-to-speech synthesis to produce complete spoken summaries in real time.

## **Project Overview**

Vox Pulse automates the process of transforming written information into an engaging podcast experience.
The system performs the following steps:

Collects news and article data from the web.

Summarizes and script-writes the content using advanced AI language models.

Generates speech from the script using realistic AI voice synthesis.

Makes episodes playable within a Flutter-based mobile app.

## **Development Summary**
### **Frontend (Flutter)**

Developed using the Flutter framework to build a responsive, cross-platform mobile application.
The app displays generated podcast titles, descriptions, and provides playback controls using ExoPlayer, enabling users to stream AI-generated episodes.

### **Backend (Node.js + MySQL)**

The backend is built with Node.js (Express) and uses MySQL (via XAMPP) for data storage.
It handles:

REST API communication between the Flutter app and the database.

Storage of episode metadata such as titles, descriptions, audio URLs, and timestamps.

### **AI & Automation Pipeline (Python)**

The Python pipeline manages the content generation workflow:

DuckDuckGo Search for retrieving recent and relevant web content.

Ollama DeepSeek R1 for summarization and scriptwriting.

Bark (by Suno) for text-to-speech conversion, generating natural-sounding audio.

The produced .wav files are stored locally and registered in the database for playback through the app.

## **Technologies Used**
Component	Technology / Tool
Frontend	Flutter (Dart), ExoPlayer
Backend	Node.js (Express), MySQL (XAMPP)
AI Pipeline	Python
Summarization & Scriptwriting	Ollama DeepSeek R1
Web Scraping	DuckDuckGo Search
Text-to-Speech	Bark by Suno
Data Handling	REST API, JSON
## **Objective**
To develop an end-to-end automated system that generates spoken podcast episodes from online text sources using AI-driven writing and voice generation.
The goal is to provide a fast, intelligent, and accessible way to consume daily information through audio.
To develop an end-to-end automated system that generates spoken podcast episodes from online text sources using AI-driven writing and voice generation.
The goal is to provide a fast, intelligent, and accessible way to consume daily information through audio.

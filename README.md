# Air File Transfer – Gesture-Controlled Wireless Transfer

A **contactless, gesture-controlled file transfer system** that enables wireless file sharing between a laptop and a mobile device using **real-time hand gesture recognition**. The system leverages computer vision to detect **grab** and **release** gestures, creating an intuitive “air-based” interaction paradigm.

---

## 🚀 Project Overview

This project implements a novel file transfer mechanism where users can **transfer files without touching any device**, relying entirely on hand gestures captured through device cameras.

- **Laptop** detects a **grab gesture** using its webcam
- **Mobile device** detects a **release gesture** using its camera
- A backend service coordinates the gesture events and file transfer in real time

The application is designed to be fast, responsive, and practical, achieving **sub-1-second latency** from gesture detection to file transfer.

---

## 🧠 Key Features

- ✋ **Real-time hand tracking** using MediaPipe
- 📁 **Contactless file transfer** via grab & release gestures
- ⚡ **Low-latency communication** using FastAPI and polling-based updates
- 📱 **Dual-device interaction**
  - Laptop webcam → grab gesture
  - Mobile camera → release gesture
- 🌐 **Responsive web frontend** for cross-device usability

---

## 🏗️ System Architecture

1. **Computer Vision Layer**
   - MediaPipe + OpenCV process live camera frames
   - Gesture recognition logic identifies grab and release actions

2. **Backend (FastAPI)**
   - Handles gesture events and file transfer coordination
   - Provides APIs for gesture status and file transmission
   - Optimized for near real-time performance

3. **Frontend (Web)**
   - Lightweight, responsive UI
   - Polls backend for gesture events
   - Enables seamless interaction across laptop and mobile browsers

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI  
- **Computer Vision:** MediaPipe, OpenCV  
- **Frontend:** HTML, CSS, JavaScript  
- **Communication:** HTTP APIs with polling (WebSocket-like behavior)

---

## ▶️ How It Works

1\. The laptop webcam continuously monitors the user's hand

2\. A **grab gesture** signals the intent to send a file

3\. The backend registers the grab event

4\. The mobile device camera waits for a **release gesture**

5\. On release detection, the backend initiates file transfer

6\. The file is transmitted wirelessly to the target device

---

## ⚙️ Setup & Run (Basic)

### Backend

pip install -r requirements.txt

uvicorn main:app --reload

Frontend

Open index.html in a browser (mobile & laptop)

Ensure both devices are on the same network

💡 Use Cases

Touch-free file sharing

Accessibility-focused interactions

Gesture-based HCI (Human--Computer Interaction) research

Computer vision + full-stack system demonstrations

🚧 Future Improvements

Replace polling with WebSockets for true real-time communication

Add gesture confidence scoring

Support multiple file transfers

Improve mobile camera performance optimization

Add authentication & encryption

📌 Author

Developed as a Computer Vision + Full-Stack project demonstrating real-time gesture recognition, system design, and cross-device interaction.

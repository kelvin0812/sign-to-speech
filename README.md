# 🤟 Sign to Speech

**A 100% Offline, Real-Time Edge AI Sign Language Translator.**
*Official Submission for the AI Ready ASEAN Grand National Convening & Innovation Challenge (GNCIC) 2026 by Team TENRA.*

[![Flutter Version](https://img.shields.io/badge/Flutter-v3.x-02569B?logo=flutter)](https://flutter.dev/)
[![TensorFlow Lite](https://img.shields.io/badge/TensorFlow_Lite-Edge_AI-FF6F00?logo=tensorflow)](https://www.tensorflow.org/lite)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Holistic-00A67E?logo=google)](https://developers.google.com/mediapipe)
[![Python ML](https://img.shields.io/badge/Python-3.x-3776AB?logo=python)](https://www.python.org/)

---

## 📖 About the Project

For millions of individuals across ASEAN, the communication gap between the Deaf community and the hearing world creates massive systemic inequalities in healthcare, education, and public services. Current solutions are often prohibitively expensive or completely break down without a high-speed internet connection. 

**Sign to Speech** breaks the "Silent Barrier" by providing a reliable, instantaneous bridge. We have engineered a dual-engine Artificial Intelligence pipeline compressed into a lightweight mobile ecosystem and dedicated edge computing hardware—requiring absolutely no cloud processing or Wi-Fi.

### 🎯 Key Objectives
* **100% Offline Inference:** Ensuring absolute data privacy and accessibility in rural clinics and areas with poor infrastructure.
* **Zero-Latency Translation:** Utilizing edge-optimized models to process dynamic human motion in real-time.
* **ASEAN Inclusivity:** Multi-language UI localization (e.g., Bahasa Melayu) to cross regional borders.

---

## 🧠 The AI Architecture (Dual-Engine Pipeline)

Standard AI classifiers fail at conversational sign language because it is a fluid language of motion. To solve this, we engineered our own custom data extraction pipeline. 

1.  **Static Fingerspelling Engine:** A Convolutional Neural Network (CNN) trained on open-source datasets to accurately identify static hand poses.
2.  **Dynamic Action Engine:** * We utilize **Google MediaPipe** to extract a precise mathematical skeleton, mapping **258 spatial coordinates** across the torso, arms, and finger joints in real-time.
    * We capture a continuous rolling memory buffer of **40 frames**.
    * This sequential tensor data `[1, 40, 258]` is fed into a **Long Short-Term Memory (LSTM)** neural network, allowing the AI to understand speed, trajectory, and direction with exceptional accuracy.

Both models are compressed into highly optimized TensorFlow Lite (`.tflite`) formats for mobile deployment.

---

## 📱 The Software Ecosystem

We built a complete accessibility ecosystem deployed via a custom Flutter application:

* 📷 **Translation Page:** Runs live AI inference offline with a strict 85% confidence filter and a Text-to-Speech engine.
* 📖 **Dictionary Page:** A searchable visual reference guide categorized into greetings, alphabets, and numbers.
* 🎓 **Study Page:** Gamified interactive flashcards for hearing users to actively learn sign language.
* ⚙️ **Profile Page:** Tracks user progress (streaks/accuracy) and features deep localization settings for true ASEAN accessibility.

---

## 📟 The Hardware Vision (Edge Computing)

To make this truly accessible as a public utility, we designed our own standalone hardware to run our AI models.

* **Core Unit:** Sipeed MaixCAM edge board (SOPHGO SG2002).
* **Components:** 4-megapixel camera, 2.4" IPS touchscreen, and tactile triggers housed in a custom 3D-printed case.
* **Sustainability:** Runs on practically zero power without needing to ping a cloud server, making it highly affordable to mass-produce and deploy in rural environments.

---

## 📂 Repository Structure

This is a monorepo containing both the Flutter application and the Python machine learning training environment.

```text
📦 sign-to-speech
 ┣ 📂 ai_model/                 # Python Machine Learning Pipeline
 ┃ ┣ 📂 dynamic_sign_model/     # Custom LSTM training pipeline (MediaPipe)
 ┃ ┗ 📂 static_sign_model/      # CNN training pipeline for alphabet
 ┣ 📂 android/                  # Native Android build files
 ┣ 📂 assets/                   # App assets and exported TFLite models
 ┃ ┣ 📜 dynamic_sign_model.tflite     # Compressed LSTM model for dynamic signs
 ┃ ┗ 📜 static_sign_model.tflite       # Compressed CNN model for static signs
 ┣ 📂 ios/                      # Native iOS build files
 ┣ 📂 lib/                      # Flutter Dart source code
 ┃ ┣ 📂 screens/                # UI Pages (Translate, Dictionary, Study, Profile)
 ┃ ┗ 📜 main.dart               # App entry point
 ┗ 📜 pubspec.yaml              # Flutter dependencies

## 🚀 How to Run the Project

We’ve designed this repository to be fully modular. Whether you want to test the raw AI inference on your computer or install the complete mobile ecosystem on your phone, here is how to get started.

### 🧠 Testing the Live AI Pipeline (Webcam Required)
If you want to experience our zero-latency sign language translation immediately, you can run our Python edge-inference scripts directly using your computer's webcam.

First, open your terminal to download the project, and navigate directly into the specific model folder you want to test (for example, the static alphabet model):
```bash
git clone [https://github.com/kelvin0812/sign-to-speech.git](https://github.com/kelvin0812/sign-to-speech.git)
cd sign-to-speech/ai_model/static_sign_model
py -3.11 -m venv env
.\env\Scripts\activate
pip install tensorflow==2.15.0 mediapipe==0.10.8 protobuf==3.20.3 opencv-python numpy pandas scikit-learn
python test_model.py

Running the Mobile Ecosystem (Flutter)
flutter run

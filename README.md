
<img width="1220" height="780" alt="Final_Result" src="https://github.com/user-attachments/assets/7a2f3753-55fc-444e-81f7-eb2caaff02e3" />
<img width="732" height="288" alt="Screenshot_2025-07-06_21-43-52" src="https://github.com/user-attachments/assets/c001c6df-8f04-4bf0-a5bd-06ef0660bda9" />


````markdown
# Text-to-Speech Streamlit App

A Python-based web application that converts text input into speech using Streamlit and TTS libraries.

## Features

- Convert text input to speech instantly.
- Select different voices (if supported by the TTS engine).
- Adjust speed of the speech.
- Play audio directly in the browser.
- Download generated speech as an audio file.

## Demo

![Demo](demo.gif) *(Optional: Add a GIF or screenshot showing the app)*

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/blackXmask/Text-to-Speech.git
cd Text-to-Speech<img width="293" height="281" alt="c2" src="https://github.com/user-attachments/assets/99e46053-c144-4f90-bfde-be6a5d757e5c" />

````

2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501`.

## Project Structure

```
Text-to-Speech/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
├── assets/             # Optional: images, icons, audio files
├── models/             # Optional: pre-trained TTS models
└── README.md           # Project documentation
```

## Dependencies

* Python 3.8+
* Streamlit
* pyttsx3 (or any TTS library you use)
* numpy
* soundfile

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Contributions are welcome! Feel free to open issues or submit pull requests.


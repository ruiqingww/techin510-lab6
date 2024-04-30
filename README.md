# MusicGen for Running

A real-time running music prompt generator that can take the user’s request and give a professional music description for later music generation. Users can directly download the response's text file.

## Getting Started

### First time setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Future runs

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run llm_app.py
```


## Lessons Learned
How to create a streamlit app using Gemini API.

By creating an input prompt template, send all the information to the API, and download the response with one click.

## Future Improvements
Add a music API to the web to generate music directly.

Receive real-time data from AWS and input them into the template instead of manually choosing the cadence and heart rate.
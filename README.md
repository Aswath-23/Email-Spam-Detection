# Spam Email Detection

A machine learning model to classify emails as spam or ham (non-spam) using Naive Bayes classification.

## Features
- TF-IDF vectorization of email content
- Keyword-based feature extraction
- Link detection
- Naive Bayes classification

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Place your email dataset in the `data` directory
2. Run the model in command prompt:
```bash
python spam_detector.py
```
3. Run in Website:
```bash
python app.py
```



## Data Format
The model expects a CSV file with the following columns:
- subject: Email subject line
- body: Email content
- label: 'spam' or 'ham' 

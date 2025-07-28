from flask import Flask, render_template, request, jsonify
from spam_detector import SpamDetector
import pandas as pd
import os

app = Flask(__name__)

# Initialize the spam detector
detector = None

def initialize_detector():
    global detector
    if detector is None:
        # Load and prepare data
        df = pd.read_csv('data/emails.csv', encoding='latin-1')
        df = df.dropna()
        df['label'] = df['label'].astype(str).str.lower().str.strip()
        
        # Initialize and train detector
        detector = SpamDetector()
        X = detector.extract_features(df)
        y = df['label']
        detector.train(X, y)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if detector is None:
        initialize_detector()
    
    data = request.json
    subject = data.get('subject', '')
    body = data.get('body', '')
    
    prediction, probability = detector.predict_single_email(subject, body)
    # Convert numeric prediction to label
    if prediction == 1 or str(prediction).lower() == 'spam':
        pred_label = 'spam'
    else:
        pred_label = 'ham'

    # Analyze warning signs
    warning_signs = []
    if pred_label == 'spam':
        if 'http' in body.lower():
            warning_signs.append("Contains links")
        if any(word in subject.lower() for word in ['urgent', 'important', 'alert']):
            warning_signs.append("Urgency indicators in subject")
        if any(word in body.lower() for word in ['offer', 'deal', 'discount', 'free']):
            warning_signs.append("Contains promotional language")

    return jsonify({
        'prediction': pred_label,
        'confidence': float(probability[1 if pred_label == 'spam' else 0]),
        'warning_signs': warning_signs
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True) 
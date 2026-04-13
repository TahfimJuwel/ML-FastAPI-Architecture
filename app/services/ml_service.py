from textblob import TextBlob
import time

def analyze_sentiment(raw_text: str):
    blob = TextBlob(raw_text)
    polarity_score = blob.sentiment.polarity
    
    if polarity_score > 0:
        final_label = "Positive"
    elif polarity_score < 0:
        final_label = "Negative"
    else:
        final_label = "Neutral"
        
    return polarity_score, final_label


def run_heavy_ml_in_background(raw_text: str, user_email: str):
    print(f"🤖 [AI START] Loading 50GB Deep Learning Model for user {user_email}...")
    
    # Simulating a heavy 10-second AI process
    time.sleep(10) 
    
    # Now it actually runs the ML model
    blob = TextBlob(raw_text)
    score = blob.sentiment.polarity
    label = "Positive" if score > 0 else "Negative"
    
    # In a real app, we would save this to the database here!
    print(f"✅ [AI FINISHED] The text '{raw_text}' is {label} (Score: {score})")
    print(f"✉️ [EMAIL SENT] 'Dear {user_email}, your AI video analysis is complete!'")
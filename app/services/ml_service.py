from textblob import TextBlob

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
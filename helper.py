import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import emoji
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

STOP_WORDS = [
    "hai","ki","ka","ke","ko","se","aur","to","me","mai","main","is","the","a","an","of","for",
    "in","on","at","ho","ha","h","ya","na","bhai", "and", "bhi", "you", "hi", "i", "<media", 
    "omitted>", "nahi", "toh", "nhi", "mein", "tha", "are", "kya", "was", "but", "ye", "wo", "kuch"
]

def fetch_stats(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    num_messages = df.shape[0]
    
    words = []
    for msg in df['message']:
        words.extend(msg.split())
        
    num_media = df[df['message'].str.contains('<Media omitted>', case=False, na=False)].shape[0]
    
    links = []
    for msg in df['message']:
        links.extend(re.findall(r'https?://\S+', msg))
        
    return num_messages, len(words), num_media, links

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    df_filtered = df[(df['user'] != 'group_notification') & (~df['message'].str.contains('<Media omitted>', na=False))]
    
    def clean_text(text):
        return " ".join([w.lower() for w in text.split() if w.lower() not in STOP_WORDS and len(w) > 2])
        
    df_filtered['clean_message'] = df_filtered['message'].apply(clean_text)
    
    wc = WordCloud(width=600, height=400, background_color='black', min_font_size=10)
    return wc.generate(df_filtered['clean_message'].str.cat(sep=" "))

def most_common_words(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    df_filtered = df[(df['user'] != 'group_notification') & (~df['message'].str.contains('<Media omitted>', na=False))]
    
    words = []
    for msg in df_filtered['message']:
        for word in msg.lower().split():
            if word not in STOP_WORDS and len(word) > 2:
                words.append(word)
                
    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])

def emoji_helper(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if emoji.is_emoji(c)])
        
    return pd.DataFrame(Counter(emojis).most_common(10), columns=['Emoji', 'Count'])

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time_labels = [f"{row['month']}-{row['year']}" for _, row in timeline.iterrows()]
    timeline['time'] = time_labels
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    df['only_date'] = df['message_date'].dt.date
    daily_time = df.groupby('only_date').count()['message'].reset_index()
    return daily_time

def daily_activity_map(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    heatmap_df = df.groupby(['day_name', 'hour']).count()['message'].reset_index()
    user_heatmap = heatmap_df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='sum').fillna(0)
    return user_heatmap

def analyze_sentiment(selected_user, df):
    if selected_user != 'Overall Group Stats':
        df = df[df['user'] == selected_user]
        
    df_filtered = df[df['user'] != 'group_notification']
    sia = SentimentIntensityAnalyzer()
    
    pos, neg, neu = 0, 0, 0
    for msg in df_filtered['message']:
        score = sia.polarity_scores(msg)['compound']
        if score >= 0.05:
            pos += 1
        elif score <= -0.05:
            neg += 1
        else:
            neu += 1
            
    total = pos + neg + neu
    if total == 0:
        return 0, 0, 0
    return round((pos/total)*100, 2), round((neg/total)*100, 2), round((neu/total)*100, 2)

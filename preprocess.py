import re
import pandas as pd

def preprocess(data):
    # Regex pattern: "dd/mm/yyyy, hh:mm - " format track karne ke liye
    pattern = r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - '
    
    messages = re.split(pattern, data)
    dates = messages[1::2]
    message_text = messages[2::2]
    
    df = pd.DataFrame({'message_date': dates, 'user_message': message_text})
    
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message)
        if len(entry) >= 3:
            users.append(entry[1])
            messages.append(entry[2].strip())
        else:
            users.append('group_notification')
            messages.append(message.strip())
            
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    # Date-time features extraction matrix
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M', errors='coerce')
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['month_num'] = df['message_date'].dt.month
    
    return df
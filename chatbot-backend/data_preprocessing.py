import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

def load_and_preprocess_data():
    with open('chat_logs.json', 'r') as file:
        data = json.load(file)

    rows = []
    for key, conversation in data.items():
        for message in conversation['messages']:
            rows.append({
                'user_id': conversation['user_id'],
                'role': message['role'],
                'message': message['message'],
                'feedback': conversation.get('feedback', None)
            })
    
    df = pd.DataFrame(rows)
   
    df['processed_message'] = df['message'].apply(preprocess_text)
    
    return df

if __name__ == "__main__":
    df = load_and_preprocess_data()
    print(df.head()) 

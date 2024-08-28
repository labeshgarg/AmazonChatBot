import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle
from data_preprocessing import load_and_preprocess_data

def train_response_classification_model():
    df = load_and_preprocess_data()
    
    df_bot = df[df['role'] == 'bot']

    df_bot['response_type'] = df_bot['message'].apply(lambda x: 'product_suggestion' if 'here are' in x.lower() else 'other')

    X = df_bot['processed_message']
    y = df_bot['response_type']
 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)
    
    y_pred = model.predict(X_test_vec)
    print(classification_report(y_test, y_pred))
    
    with open('response_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    
    with open('response_vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)
    
    return model, vectorizer

if __name__ == "__main__":
    model, vectorizer = train_response_classification_model()

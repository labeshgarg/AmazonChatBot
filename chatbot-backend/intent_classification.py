import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle
from data_preprocessing import load_and_preprocess_data

def train_intent_classification_model():
    df = load_and_preprocess_data()

    df_user = df[df['role'] == 'user']

    df_user['intent'] = df_user['message'].apply(lambda x: 'product_search' if 'want' in x.lower() or 'looking for' in x.lower() else 'other')
    X = df_user['processed_message']
    y = df_user['intent']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)
    
    y_pred = model.predict(X_test_vec)
    print(classification_report(y_test, y_pred))
   
    with open('intent_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    
    with open('vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)
    
    return model, vectorizer

if __name__ == "__main__":
    train_intent_classification_model()

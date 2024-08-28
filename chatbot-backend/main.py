from intent_classification import train_intent_classification_model
from response_classification import train_response_classification_model
from data_preprocessing import load_and_preprocess_data

def main():

    intent_model, intent_vectorizer = train_intent_classification_model()
   
    response_model, response_vectorizer = train_response_classification_model()
    
    print("Both models trained successfully.")

if __name__ == "__main__":
    main()

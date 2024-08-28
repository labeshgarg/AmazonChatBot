
import requests
import openai
from dotenv import load_dotenv
import os
from datetime import datetime
from chat_logger import log_chat  

load_dotenv()

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')  
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')  
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  


openai.api_key = OPENAI_API_KEY

def fetch_product_details(query, page=1):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    querystring = {
        "query": query,
        "page": str(page),
        "country": "IN",
        "sort_by": "RELEVANCE",
        "product_condition": "ALL",
        "is_prime": "false"
    }

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": "Product search failed or API error"}

# Function to generate responses using GPT-4
def generate_gpt_response(prompt, conversation_history):
    conversation_history.append({"role": "user", "content": prompt})
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_history,
        max_tokens=150
    )
    
    gpt_message = response.choices[0].message['content'].strip()
    conversation_history.append({"role": "assistant", "content": gpt_message})
    
    return gpt_message

# Function to display product details in a conversational manner
def display_product_details(product_data):
    if product_data and 'data' in product_data and 'products' in product_data['data']:
        products = product_data['data']['products']
        
        if products:
            product_list = []
            for product in products[:5]:  # Limit to first 5 results
                price = product.get('product_price', 'Price not available')
                if not price:
                    price = "Price not available"
                product_info = (
                    f"Title: {product.get('product_title', 'N/A')}\n"
                    f"Price: {price}\n"
                    f"Rating: {product.get('product_star_rating', 'N/A')} "
                    f"({product.get('product_num_ratings', 'N/A')} ratings)\n"
                    f"Link: {product.get('product_url', 'N/A')}\n"
                    f"Availability: {product.get('delivery', 'N/A')}\n"
                    "------------------------------"
                )
                product_list.append(product_info)
            return "\n\n".join(product_list)
        else:
            return "No products found."
    else:
        return "An error occurred while searching for products."

# Function to get time-based greeting
def get_greeting():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

#Main chatbot function
def chat_bot(user_input, conversation_id="unique_id_1", user_id="user_1", conversation_history=None, state=None):
    if conversation_history is None:
        conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Default state if none is provided
    if state is None:
        state = {
            "stage": "greeting",  
            "user_preferences": {
                "product_type": None,
                "budget": None,
                "brand": None,
                "features": None,
            }
        }
    
    
    log_chat(conversation_id, user_id, "user", user_input)
    
    response_message = ""  

    # Handle each stage in the conversation
    if state["stage"] == "greeting":
        response_message = "Hello! What type of product are you looking for today?"
        state["stage"] = "asking_product_type"  

    elif state["stage"] == "asking_product_type":
        state["user_preferences"]["product_type"] = user_input
        state["stage"] = "asking_budget"
        response_message = "What is your budget for the product?"
    
    elif state["stage"] == "asking_budget":
        state["user_preferences"]["budget"] = user_input
        state["stage"] = "asking_brand"
        response_message = "Do you have any preferred brands?"
    
    elif state["stage"] == "asking_brand":
        state["user_preferences"]["brand"] = user_input
        state["stage"] = "asking_features"
        response_message = "Are there any specific features you are looking for?"
    
    elif state["stage"] == "asking_features":
        state["user_preferences"]["features"] = user_input
        state["stage"] = "final_recommendation"
     
        query = f"{state['user_preferences']['product_type']} {state['user_preferences']['brand']} {state['user_preferences']['features']}"
     
        product_details = fetch_product_details(query)
    
        products_within_budget = []
        for product in product_details.get('data', {}).get('products', []):
            product_price = product.get('product_price')
            if product_price and is_within_budget(product_price, state['user_preferences']['budget']):
                products_within_budget.append(product)

        if products_within_budget:
            final_product = products_within_budget[0]  
            final_recommendation = display_product_details({"data": {"products": [final_product]}})
            log_chat(conversation_id, user_id, "bot", final_recommendation)
            response_message = f"Based on your preferences, I recommend the following product:\n\n{final_recommendation}"
        else:
            response_message = "I couldn't find a product within your budget and preferences. Could you please refine your requirements?"
    
    else:
       
        response_message = generate_gpt_response(user_input, conversation_history)
    
    log_chat(conversation_id, user_id, "bot", response_message)

    return {"message": response_message, "state": state}

def is_within_budget(product_price, user_budget):
    try:
        price_int = int(product_price.replace("₹", "").replace(",", "").strip())
        budget_int = int(user_budget.replace("₹", "").replace(",", "").strip())
        return price_int <= budget_int
    except ValueError:
        return False
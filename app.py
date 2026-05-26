from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__, template_folder='.')
CORS(app) 

@app.route('/search', methods=['GET'])
def search_prices():
    search_query = request.args.get('item', '').strip()
    if not search_query:
        return jsonify({"error": "No search item provided"}), 400

    query_lower = search_query.lower()
    results = []

    # Generates a dynamic list of 4 different product match variations
    for i in range(1, 5):  
        rand_discount_jumia = random.randint(5, 35)
        rand_discount_jiji = random.randint(40, 85)
        
        # 1. Custom variation names based on the search query
        if "phone" in query_lower or "iphone" in query_lower or "samsung" in query_lower:
            item_name = f"Apple iPhone 13 ({128 * (i if i <=2 else 2)}GB Premium)" if "iphone" in query_lower else f"Samsung Galaxy S22 Ultra (Model variant {i})"
            base_price = 650000 if "iphone" in query_lower else 450000
            j_price = f"{base_price - (rand_discount_jumia * 1000):,}"
            ji_price = f"₦ {base_price - (rand_discount_jiji * 1000):,} - {base_price - ((rand_discount_jiji - 15) * 1000):,}"
            j_img = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=200&auto=format&fit=crop"
        elif "shoe" in query_lower or "sneaker" in query_lower:
            item_name = f"Air Max Comfort Sport Sneakers - Style {i}x"
            j_price = f"{35000 - (rand_discount_jumia * 200):,}"
            ji_price = f"₦ {22000 - (rand_discount_jumia * 150):,} - Negotiable"
            j_img = "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200&auto=format&fit=crop"
        else:
            item_name = f"Premium Grade {search_query.capitalize()} (Option {i})"
            j_price = f"{25000 - (rand_discount_jumia * 300):,}"
            ji_price = f"₦ {18000 - (rand_discount_jumia * 200):,} - Open to Offers"
            j_img = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=200&auto=format&fit=crop"

        # 2. Package everything beautifully for the frontend
        results.append({
            "name": item_name,
            "image": j_img,
            "jumiaPrice": j_price,
            "jumiaLink": f"https://www.jumia.com.ng/catalog/?q={search_query}",
            "jijiPrice": ji_price,
            "jijiLink": f"https://jiji.ng/search?query={search_query}"
        })
    
    return jsonify(results)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

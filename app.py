from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app) # Allows our frontend to talk to this script securely

@app.route('/search', methods=['GET'])
def search_prices():
    search_query = request.args.get('item')
    if not search_query:
        return jsonify({"error": "No search item provided"}), 400

    # 1. SCRAPE JUMIA NIGERIA
    j_name = f"{search_query.capitalize()} Not Found"
    j_price = "N/A"
    j_img = "https://via.placeholder.com/150"
    jumia_url = f"https://www.jumia.com.ng/catalog/?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        jumia_response = requests.get(jumia_url, headers=headers)
        jumia_soup = BeautifulSoup(jumia_response.text, 'html.parser')
        
        # Extract the first matching item from Jumia
        name_el = jumia_soup.find('h3', class_='name')
        price_el = jumia_soup.find('div', class_='prc')
        img_el = jumia_soup.find('img', class_='img')
        
        if name_el:
            j_name = name_el.text
        if price_el:
            j_price = price_el.text
        if img_el:
            j_img = img_el.get('data-src') or img_el.get('src') or j_img
    except Exception:
        pass

    # 2. CREATE THE RESPONSE PACKAGE
    # This matches the names our frontend JavaScript expects to receive!
    results = [
        {
            "name": j_name,
            "image": j_img,
            "jumiaPrice": j_price.replace("₦", "").strip(),
            "jumiaLink": jumia_url,
            "jijiPrice": "Calculating Best Deal...", 
            "jijiLink": f"https://jiji.ng/search?query={search_query}"
        }
    ]
    
    return jsonify(results)

# --- NEW ROOT ROUTE ADDED HERE TO FIX THE 404 ERROR ---
@app.route('/')
def home():
    return "Price Scraper Backend is running successfully!"

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

# Look for index.html in the main folder
app = Flask(__name__, template_folder='.')
CORS(app) 

@app.route('/search', methods=['GET'])
def search_prices():
    search_query = request.args.get('item')
    if not search_query:
        return jsonify({"error": "No search item provided"}), 400

    # Defaults in case the scrape fails completely
    j_name = f"{search_query.capitalize()} Not Found"
    j_price = "N/A"
    j_img = "https://via.placeholder.com/150"
    jumia_url = f"https://www.jumia.com.ng/catalog/?q={search_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }
    
    try:
        jumia_response = requests.get(jumia_url, headers=headers, timeout=10)
        jumia_soup = BeautifulSoup(jumia_response.text, 'html.parser')
        
        # Smart Fix: Find the first product article card container
        product_card = jumia_soup.find('article', class_='prd')
        
        if product_card:
            # Look for data attributes or standard class configurations inside the card
            name_el = product_card.find('div', class_='name') or product_card.find('h3', class_='name')
            price_el = product_card.find('div', class_='prc')
            img_el = product_card.find('img', class_='img')
            
            if name_el:
                j_name = name_el.text.strip()
            if price_el:
                j_price = price_el.text.strip()
            if img_el:
                j_img = img_el.get('data-src') or img_el.get('src') or j_img
    except Exception as e:
        print(f"Scraping error: {e}")

    # Send the clean package back to our frontend
    results = [
        {
            "name": j_name,
            "image": j_img,
            "jumiaPrice": j_price.replace("₦", "").strip(),
            "jumiaLink": jumia_url,
            "jijiPrice": "Check Best Deals", 
            "jijiLink": f"https://jiji.ng/search?query={search_query}"
        }
    ]
    
    return jsonify(results)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

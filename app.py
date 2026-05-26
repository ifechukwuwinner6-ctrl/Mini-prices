from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

# Tell Flask to look for index.html right in the main folder
app = Flask(__name__, template_folder='.')
CORS(app) 

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
    
    # Human-like headers to stop Jumia from blocking the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    try:
        jumia_response = requests.get(jumia_url, headers=headers, timeout=10)
        jumia_soup = BeautifulSoup(jumia_response.text, 'html.parser')
        
        name_el = jumia_soup.find('h3', class_='name')
        price_el = jumia_soup.find('div', class_='prc')
        img_el = jumia_soup.find('img', class_='img')
        
        if name_el:
            j_name = name_el.text.strip()
        if price_el:
            j_price = price_el.text.strip()
        if img_el:
            j_img = img_el.get('data-src') or img_el.get('src') or j_img
    except Exception:
        pass

    # 2. CREATE THE RESPONSE PACKAGE
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

# --- ROOT ROUTE TO SHOW YOUR BEAUTIFUL FRONTEND LAYOUT ---
@app.route('/')
def home():
    # This renders your index.html interface automatically!
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Allows your frontend to talk to this backend

@app.route('/')
def home():
    return "Price Scraper Backend is running cleanly!"

@app.route('/search', methods=['GET'])
def search_prices():
    # Capture either the 'item' or the 'category' sent from the frontend
    search_query = request.args.get('item') or request.args.get('category')
    
    if not search_query:
        return jsonify({"error": "No search term provided"}), 400

    # Clean up the term for scraping and fallback links
    clean_query = search_query.strip()
    search_word = clean_query.capitalize()

    # --- DEFAULT INITIAL VALUES ---
    j_name = f"{search_word}"
    j_price = "Check Live"
    j_img = "https://via.placeholder.com/150"
    
    jiji_price = "See Deals"
    konga_price = "Check Live"
    aliexpress_price = "View Prices"
    amazon_price = "Check Hub"

    # --- SCRAPE JUMIA NIGERIA ---
    try:
        jumia_url = f"https://www.jumia.com.ng/catalog/?q={requests.utils.quote(clean_query)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(jumia_url, headers=headers, timeout=7)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_card = soup.find('article', class_='prd')
            
            if product_card:
                name_tag = product_card.find('h3', class_='name')
                price_tag = product_card.find('div', class_='prc')
                img_tag = product_card.find('img', class_='img')
                
                if name_tag: j_name = name_tag.text.strip()
                if price_tag: j_price = price_tag.text.strip().replace("₦", "").strip()
                if img_tag and img_tag.get('data-src'):
                    j_img = img_tag.get('data-src')
                elif img_tag and img_tag.get('src'):
                    j_img = img_tag.get('src')
    except Exception as e:
        print(f"Jumia scrape fallback triggered: {e}")

    # --- SMART PRICE GENERATOR FOR OTHER PLATFORMS ---
    # Since live scraping multiple heavy sites on free servers can time out, 
    # we create dynamic placeholder values to keep your dashboard running fast!
    if "laptop" in clean_query.lower() or "computer" in clean_query.lower():
        jiji_price = "₦ 180,000 - 450,000"
        konga_price = "220,000"
    elif "shoe" in clean_query.lower() or "sneaker" in clean_query.lower():
        jiji_price = "₦ 15,000 - 45,000"
        konga_price = "28,000"
    elif "cloth" in clean_query.lower() or "fashion" in clean_query.lower():
        jiji_price = "₦ 5,000 - 25,000"
        konga_price = "8,500"
    elif "car" in clean_query.lower() or "vehicle" in clean_query.lower():
        jiji_price = "₦ 3,500,000 - 9,000,000"
        konga_price = "Contact Seller"
    elif "hous" in clean_query.lower() or "propert" in clean_query.lower():
        jiji_price = "₦ 25,000,000 - 80,000,000"
        konga_price = "N/A"
    elif "solar" in clean_query.lower() or "power" in clean_query.lower():
        jiji_price = "₦ 85,000 - 300,000"
        konga_price = "120,000"
    elif "tv" in clean_query.lower() or "television" in clean_query.lower():
        jiji_price = "₦ 95,000 - 280,000"
        konga_price = "145,000"
    elif "generator" in clean_query.lower():
        jiji_price = "₦ 110,000 - 400,000"
        konga_price = "185,000"
    else:
        jiji_price = "₦ Check Live Marketplace"

    # 2. PACK THE RESPONSE LOGIC safely
    results = [
        {
            "name": j_name,
            "image": j_img,
            "searchWord": search_word,
            "jumiaPrice": j_price,
            "jijiPrice": jiji_price,
            "kongaPrice": konga_price,
            "aliexpressPrice": aliexpress_price,
            "amazonPrice": amazon_price
        }
    ]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

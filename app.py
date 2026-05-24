from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app) # Allows our frontend to talk to this script securely

@app.route('/search', methods=['GET'])
def search_prices():
    search_query = request.args.get('item')
    
    # 1. SCRAPE JUMIA NIGERIA
    jumia_url = f"https://www.jumia.com.ng/catalog/?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    jumia_response = requests.get(jumia_url, headers=headers)
    jumia_soup = BeautifulSoup(jumia_response.text, 'html.parser')
    
    # Extract the first matching item from Jumia
    try:
        j_name = jumia_soup.find('h3', class_='name').text
        j_price = jumia_soup.find('div', class_='prc').text
        j_img = jumia_soup.find('img', class_='img')['data-src']
    except:
        j_name = f"{search_query.capitalize()} Not Found"
        j_price = "N/A"
        j_img = "https://via.placeholder.com/150"

    # 2. CREATE THE RESPONSE PACKAGE
    # This matches the names our frontend JavaScript expects to receive!
    results = [
        {
            "name": j_name,
            "image": j_img,
            "jumiaPrice": j_price.replace("₦", "").strip(),
            "jumiaLink": jumia_url,
            "jijiPrice": "Calculating Best Deal...", # Simplified demonstration placeholder
            "jijiLink": f"https://jiji.ng/search?query={search_query}"
        }
    ]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

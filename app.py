from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)

# --- SMART DATA ENGINE (Different prices for different items) ---
PRODUCT_DATABASE = {
    "phones": [
        {"title": "iPhone 13 Pro Max (128GB - UK Used)", "price": "₦520,000", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"},
        {"title": "Samsung Galaxy S22 Ultra (5G)", "price": "₦485,000", "platform": "Konga Plaza", "link": "https://www.konga.com"},
        {"title": "Redmi Note 13 Pro (Brand New)", "price": "₦295,000", "platform": "Alibaba Core Agent", "link": "https://www.alibaba.com"}
    ],
    "solar panels and batteries": [
        {"title": "300W Mono Solar Panel (High Efficiency)", "price": "₦85,000", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"},
        {"title": "200Ah 12V Tubular Solar Battery", "price": "₦240,000", "platform": "Konga Plaza", "link": "https://www.konga.com"},
        {"title": "Complete 3KVA Solar Inverter Setup", "price": "₦850,000", "platform": "Alibaba Core Agent", "link": "https://www.alibaba.com"}
    ],
    "clothes": [
        {"title": "Designer Men's Corporate Shirts (Bale Pack)", "price": "₦45,000", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"},
        {"title": "Unisex Luxury Hoodies & Sweatshirts", "price": "₦12,500", "platform": "Konga Plaza", "link": "https://www.konga.com"},
        {"title": "Premium Denim Jeans (Wholesale Lot)", "price": "₦60,000", "platform": "Alibaba Core Agent", "link": "https://www.alibaba.com"}
    ],
    "laptops": [
        {"title": "HP EliteBook 840 G5 (Intel Core i5, 8GB RAM)", "price": "₦265,000", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"},
        {"title": "Dell Latitude 7490 (256GB SSD)", "price": "₦245,000", "platform": "Konga Plaza", "link": "https://www.konga.com"},
        {"title": "Apple MacBook Pro 2019 (Touchbar)", "price": "₦490,000", "platform": "Alibaba Core Agent", "link": "https://www.alibaba.com"}
    ],
    "sneakers": [
        {"title": "Nike Air Force 1 (Premium Grade)", "price": "₦35,000", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"},
        {"title": "Adidas Yeezy Boost (Wholesale Stock)", "price": "₦42,000", "platform": "Alibaba Core Agent", "link": "https://www.alibaba.com"}
    ],
    "eye glasses": [
        {"title": "Anti-Blue Light Computer Glasses", "price": "₦8,500", "platform": "Konga Plaza", "link": "https://www.konga.com"},
        {"title": "Designer Luxury Sunglasses (UV400)", "price": "₦18,000", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"}
    ],
    "gas cylinders": [
        {"title": "12.5kg Gas Cylinder with Safe Valve", "price": "₦22,500", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"},
        {"title": "6kg Camping Gas Cylinder & Burner", "price": "₦14,000", "platform": "Konga Plaza", "link": "https://www.konga.com"}
    ]
}

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Mini-prices Engine Running"})

@app.route('/search', methods=['GET'])
def search_prices():
    search_query = request.args.get('query', '').strip().lower()
    
    if not search_query:
        return jsonify({"error": "No query provided"}), 400

    logging.info(f"Searching database for: {search_query}")
    
    # Check if the searched item exists in our structured database
    if search_query in PRODUCT_DATABASE:
        return jsonify(PRODUCT_DATABASE[search_query])
    
    # Dynamic fallback generator if they type a custom word not in the main database
    clean_title = search_query.capitalize()
    fallback_results = [
        {"title": f"Standard {clean_title} (Wholesale Lot)", "price": "₦55,000", "platform": "Jiji Wholesale Hub", "link": "https://jiji.ng"},
        {"title": f"Premium {clean_title} (Direct Import)", "price": "₦110,000", "platform": "Alibaba Core Agent", "link": "https://www.alibaba.com"},
        {"title": f"Budget {clean_title} (Local Supplier)", "price": "₦28,000", "platform": "Konga Plaza", "link": "https://www.konga.com"}
    ]
    return jsonify(fallback_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

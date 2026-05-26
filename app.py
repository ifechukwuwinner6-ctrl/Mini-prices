from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random

app = Flask(__name__, template_folder='.')
CORS(app) 

@app.route('/search', methods=['GET'])
def search_prices():
    search_query = request.args.get('item', '').strip()
    category = request.args.get('category', '').strip()
    
    # If no search query but a category card was clicked, use the category name
    if not search_query and category:
        search_query = category
        
    if not search_query:
        return jsonify({"error": "No search item provided"}), 400

    query_lower = search_query.lower()
    results = []

    # Generate a rich list of 4 distinct matching items across different platforms
    for i in range(1, 5):  
        rand_discount = random.randint(5, 30)
        
        # Determine the name, base price, and image based on what is searched
        if "phone" in query_lower or "iphone" in query_lower or "samsung" in query_lower:
            item_name = f"Apple iPhone 14 Pro ({128 * i}GB Choice Pack)" if "iphone" in query_lower else f"Samsung Galaxy S23 Ultra (Grade A variant {i})"
            base_price = 780000 if "iphone" in query_lower else 590000
            j_img = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=200&auto=format&fit=crop"
        elif "watch" in query_lower or "smartwatch" in query_lower or "accessory" in query_lower:
            item_name = f"Series 9 Ultra Smart Watch Pro - Edition v{i}"
            base_price = 45000
            j_img = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=200&auto=format&fit=crop"
        elif "shoe" in query_lower or "sneaker" in query_lower:
            item_name = f"Air Max Premium Run Luxury Sneakers (Model {i})"
            base_price = 38000
            j_img = "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200&auto=format&fit=crop"
        else:
            item_name = f"High-Quality Designer {search_query.capitalize()} (Selection {i})"
            base_price = 28000
            j_img = "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=200&auto=format&fit=crop"

        # Dynamically distribute prices realistically across all 5 requested platforms
        results.append({
            "name": item_name,
            "image": j_img,
            "jumiaPrice": f"{base_price - (rand_discount * 400):,}",
            "jijiPrice": f"₦ {base_price - (rand_discount * 650):,} - Negotiable",
            "kongaPrice": f"{base_price - (rand_discount * 200):,}",
            "aliexpressPrice": f"₦ {random.randint(15, 45):,}.00 (Direct Shipping)",
            "amazonPrice": f"${random.randint(40, 199)} (Import Fees Incl.)",
            "searchWord": search_query
        })
    
    return jsonify(results)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

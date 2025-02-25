from flask import Flask, jsonify, request
from Clothing_Recommendation_System import ClothingRecommender

app = Flask(__name__)

def recommend_items_with_images(body_type, count):
    """
    Returns a list of dictionaries with 'barcode' and 'image_url' keys
    for the top recommended items.
    """
    data_path = "C:/Users/Sifeddine/Desktop/assignment/contourlab_assignment/Solution/Data/dataset_droped.csv"  # Ensure this path is correct.
    recommender = ClothingRecommender()
    data = recommender.load_clothing_data(data_path)
    recommendations = recommender.get_recommendations(data, body_type, top_n=count)
    
    # Build a list of recommendations including barcode and image URL.
    results = []
    for rec in recommendations:
        item = rec['item']
        results.append({
            "barcode": item.get("barcode", ""),
            "image_url": item.get("image_url_1", "")
        })
    return results

@app.route('/')
def home():
    return """
    <h1>Welcome to the Clothing Recommendation API</h1>
    <p>To get recommendations in JSON, use the endpoint:</p>
    <code>/recommend?bodytype=&lt;body_type&gt;</code>
    <p>Example: <a href="/recommend?bodytype=hourglass">/recommend?bodytype=hourglass</a></p>
    <p>To view recommendations with clickable images, use the endpoint:</p>
    <code>/recommend_html?bodytype=&lt;body_type&gt;</code>
    <p>Example: <a href="/recommend_html?bodytype=hourglass">/recommend_html?bodytype=hourglass</a></p>
    """

@app.route('/recommend', methods=['GET'])
def recommend():
    body_type = request.args.get('bodytype')
    if not body_type:
        return jsonify({"error": "Missing 'bodytype' query parameter"}), 400

    try:
        recommended_items = recommend_items_with_images(body_type.strip().lower(), 11)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"recommended_items": recommended_items})

@app.route('/recommend_html', methods=['GET'])
def recommend_html():
    body_type = request.args.get('bodytype')
    if not body_type:
        return "Missing 'bodytype' query parameter", 400
    try:
        recommended_items = recommend_items_with_images(body_type.strip().lower(), 11)
    except Exception as e:
        return f"Error: {str(e)}", 500

    # Build an HTML page with clickable image links.
    html_content = f"""
    <html>
      <head>
        <title>Recommendations for {body_type.capitalize()}</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
          }}
          ul {{
            list-style: none;
            padding: 0;
          }}
          li {{
            margin-bottom: 20px;
          }}
          img {{
            max-width: 200px;
            border: 1px solid #ccc;
          }}
        </style>
      </head>
      <body>
        <h1>Recommendations for {body_type.capitalize()}</h1>
        <ul>
    """

    for item in recommended_items:
        barcode = item["barcode"]
        image_url = item["image_url"]
        html_content += f"""
          <li>
            <a href="{image_url}" target="_blank">
              <img src="{image_url}" alt="Item {barcode}">
            </a>
            <p>Barcode: {barcode}</p>
          </li>
        """
    html_content += """
        </ul>
      </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(debug=True)


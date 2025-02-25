Below is a Markdown explanation of how the API works:

---

# Clothing Recommendation API Explanation

This API is built using Flask and integrates a clothing recommendation system provided by the `Clothing_Recommendation_System` module. It reads clothing data from a CSV file, computes recommendations based on a given body type, and returns the results in two formats: JSON and an HTML page with clickable image links.

## Overview

- **Flask Application:**  
  The API uses Flask to define HTTP endpoints.
  
- **Recommendation Functionality:**  
  The `ClothingRecommender` class (imported from `Clothing_Recommendation_System`) is used to load data from a CSV file and generate recommendations based on a given body type.

- **Data Source:**  
  The API expects the CSV file to be located at  
  `C:/Users/Sifeddine/Desktop/assignment/contourlab_assignment/Solution/Data/dataset_droped.csv`  
  and assumes that the file contains at least the columns `barcode` and `image_url_1`.

- **Endpoints Provided:**  
  1. **Home (`/`)**  
     Provides instructions and example links.
  2. **JSON Endpoint (`/recommend`)**  
     Returns a JSON response with recommended items.
  3. **HTML Endpoint (`/recommend_html`)**  
     Returns an HTML page with clickable images linking to the item URLs.

## Detailed Code Explanation

### 1. Importing Dependencies

```python
from flask import Flask, jsonify, request
from Clothing_Recommendation_System import ClothingRecommender
```

- **Flask, jsonify, request:**  
  These are used to create the API, format responses as JSON, and access request parameters.
  
- **ClothingRecommender:**  
  This class contains the logic to load data and compute recommendations.

### 2. The `recommend_items_with_images` Function

This function loads the clothing dataset, generates recommendations, and extracts each item's barcode and image URL:

```python
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
```

- **Loading Data:**  
  The CSV file is loaded using `load_clothing_data`.
  
- **Generating Recommendations:**  
  Recommendations are computed using the `get_recommendations` method.
  
- **Result Construction:**  
  Each recommended item is represented as a dictionary with its `barcode` and `image_url` (retrieved from the `image_url_1` column).

### 3. Home Endpoint (`/`)

This endpoint provides a simple HTML page with instructions and example links for both JSON and HTML endpoints:

```python
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
```

### 4. JSON Endpoint (`/recommend`)

This endpoint accepts a `bodytype` query parameter and returns the recommended items in JSON format:

```python
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
```

- **Query Parameter Validation:**  
  Checks if `bodytype` is provided.
  
- **Error Handling:**  
  Catches and returns errors as JSON with appropriate HTTP status codes.
  
- **Response Format:**  
  Returns a JSON object with a key `"recommended_items"` containing the list of recommended items.

### 5. HTML Endpoint (`/recommend_html`)

This endpoint returns an HTML page that displays each recommended item as a clickable image:

```python
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
```

- **HTML Construction:**  
  An HTML string is built dynamically to include each recommendation.
  
- **Clickable Images:**  
  Each image is wrapped in an `<a>` tag with `target="_blank"`, making it clickable and ensuring it opens in a new tab.
  
- **Display Details:**  
  Each list item shows the image and the corresponding barcode.

### 6. Running the Application

The application is started with the following block:

```python
if __name__ == '__main__':
    app.run(debug=True)
```

- **Debug Mode:**  
  The app runs in debug mode to help with development and troubleshooting.
  
- **Local Server:**  
  The API is served locally (typically at `http://127.0.0.1:5000/`).

## How to Test the API

1. **Run the API:**
   - Ensure that the CSV file exists at the specified path.
   - Run the application using:
     ```bash
     python your_api_script.py
     ```

2. **JSON Response:**
   - Open your browser or use a terminal tool like `curl`:
     ```bash
     curl -X GET "http://127.0.0.1:5000/recommend?bodytype=hourglass"
     ```
   - You should receive a JSON response with recommended items.

3. **HTML Response with Clickable Images:**
   - Open your browser and navigate to:
     ```
     http://127.0.0.1:5000/recommend_html?bodytype=hourglass
     ```
   - You will see an HTML page displaying each item as a clickable image. Clicking on an image opens it in a new tab.

## Conclusion

This API provides a robust way to generate clothing recommendations based on a body type. It leverages a pre-built recommendation system and exposes the functionality through both JSON and HTML endpoints, making it versatile for different use cases. Make sure the dataset and module paths are configured correctly for the API to work as expected.

--- 

This Markdown explanation covers the structure and functionality of your API code in detail.
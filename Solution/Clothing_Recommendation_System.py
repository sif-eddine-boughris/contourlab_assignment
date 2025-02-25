import sys
import pandas as pd
import numpy as np

class ClothingRecommender:
    def __init__(self):
        # Rules for each body type using our dataset attributes.
        # We consider: category, style, colors, fit, Type, lenghth, and pattern.
        self.body_type_rules = {
            'hourglass': {
                'category': {'dress': 10, 'blouse': 9, 'skirt': 8},
                'style': {'feminine': 10, 'sophisticated': 9, 'casual': 7},
                'colors': {'black': 10, 'navy': 9, 'red': 8, 'gray': 8, 'white': 7},
                'fit': {'Regular_Fit': 10, 'Slim_Fit': 9, 'Flared_Fit': 7, 'Oversized_Fit': 5},
                'Type': {'v-neck': 10, 'a-line': 9, 'wrap': 10, 'bodycon': 9},
                'lenghth': {'midi': 10, 'full-length': 9, 'knee': 8, 'mini': 6, 'cropped': 5},
                'pattern': {'plain': 10, 'vertical-stripes': 9, 'floral': 8}
            },
            'rectangle': {
                'category': {'shirt': 9, 't-shirt': 8, 'tops': 9, 'jumpsuit': 7},
                'style': {'minimalism': 10, 'business': 9, 'casual': 8},
                'colors': {'blue': 9, 'black': 8, 'gray': 8},
                'fit': {'Regular_Fit': 10, 'Slim_Fit': 9, 'Flared_Fit': 8, 'Oversized_Fit': 6},
                'Type': {'crew-neck': 10, 'pencil': 9, 'flutter-sleeve': 8},
                'lenghth': {'cropped': 10, 'mini': 9, 'short': 8},
                'pattern': {'horizontal-stripes': 10, 'geometric': 9, 'plain': 8}
            },
            'apple': {
                'category': {'tunic': 10, 'jumpsuit': 9, 'overclothes-sleeveless': 8},
                'style': {'modest': 10, 'casual': 9},
                'colors': {'black': 10, 'navy': 9, 'gray': 8},
                'fit': {'Oversized_Fit': 10, 'Regular_Fit': 8, 'Slim_Fit': 5, 'Flared_Fit': 7},
                'Type': {'v-neck': 10},  # For apple types, v-neck is strongly preferred.
                'lenghth': {'maxi': 10, 'full-length': 9, 'long': 8},
                'pattern': {'vertical-stripes': 10, 'plain': 9}
            }
        }
        
        # Overall attribute importance weights (summing to 1.0)
        self.attribute_importance = {
            'category': 0.15,
            'style': 0.15,
            'colors': 0.10,
            'fit': 0.20,
            'Type': 0.20,
            'lenghth': 0.10,
            'pattern': 0.10
        }
    
    def load_clothing_data(self, csv_file_path):
        """Load clothing data from a CSV file into a DataFrame."""
        return pd.read_csv(csv_file_path)
    
    def calculate_item_score(self, item, body_type):
        """Calculate the weighted suitability score of an item for a given body type."""
        if body_type not in self.body_type_rules:
            raise ValueError(f"Body type '{body_type}' not supported")
        
        total_score = 0
        rules = self.body_type_rules[body_type]
        
        # Iterate through each attribute of interest.
        for attr, importance in self.attribute_importance.items():
            if attr in item and pd.notnull(item[attr]):
                value = item[attr].strip().lower()
                # For the 'Type' attribute, allow substring matching.
                if attr == 'Type':
                    matched = False
                    for key, score_val in rules[attr].items():
                        if key.lower() in value:
                            raw_score = score_val
                            matched = True
                            break
                    if not matched:
                        raw_score = 0
                else:
                    rule_dict = {k.lower(): v for k, v in rules[attr].items()}
                    raw_score = rule_dict.get(value, 0)
                total_score += raw_score * importance
        # The maximum possible score per attribute is 10, so the maximum total score is 10.
        normalized_score = round(total_score, 1)
        return normalized_score
    
    def get_recommendations(self, clothing_data, body_type, top_n=5):
        """Filter, rank, and return the top recommendations for a given body type."""
        recommendations = []
        for _, row in clothing_data.iterrows():
            item = row.to_dict()
            score = self.calculate_item_score(item, body_type)
            recommendations.append({'item': item, 'score': score})
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]

def recommend_barcodes(body_type, count):
    """
    Given a body type (e.g. 'hourglass', 'rectangle', or 'apple') and the number
    of items requested, this function returns a list of barcodes for the top ranked items.
    """
    data_path = "C:/Users/Sifeddine/Desktop/assignment/contourlab_assignment/Solution/Data/dataset_droped.csv"
    recommender = ClothingRecommender()
    data = recommender.load_clothing_data(data_path)
    recommendations = recommender.get_recommendations(data, body_type, top_n=count)
    return [rec['item']['barcode'] for rec in recommendations]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Clothing_Recommendation_System.py <body_type> <count>")
        sys.exit(1)
    body_type = sys.argv[1].strip().lower()
    try:
        count = int(sys.argv[2])
    except ValueError:
        print("Count must be an integer.")
        sys.exit(1)
    
    barcodes = recommend_barcodes(body_type, count)
    print("Recommended Barcodes:")
    for code in barcodes:
        print(code)

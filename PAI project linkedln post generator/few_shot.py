import pandas as pd
import json
import os

class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)  # Load data immediately on initialization

    def load_posts(self, file_path):
        try:
            with open(file_path, encoding='utf-8') as f:
                posts = json.load(f)    
                self.df = pd.json_normalize(posts)
                self.df["length"] = self.df["line_count"].apply(self.categorize_length)
                all_tags = self.df['tags'].apply(lambda x: x).sum()
                self.unique_tags = set(list(all_tags))
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found at: {file_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in the file")
        except Exception as e:
            raise ValueError(f"Error loading posts: {e}")

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags    

    def get_filtered_posts(self, length, language, tag):
        if self.df is None:
            raise ValueError("DataFrame not loaded - please load data first")
        df_filtered = self.df[
            (self.df['length'] == length) &
            (self.df['language'] == language) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        return df_filtered.to_dict(orient="records")

if __name__ == "__main__":   
    # Update the path to your JSON file
    json_path = r"c:\Users\A B\Desktop\linkedln post generator\data\processed_posts.json"
    
    fs = FewShotPosts(json_path)  # Initialize and load data
    posts = fs.get_filtered_posts("Short", "English", "Motivation")
    print(posts)
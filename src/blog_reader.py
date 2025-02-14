import os
import yaml
from typing import List

class BlogPost:
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = ""
        self.metadata = {}
        self.parse_file()
    
    def parse_file(self):
        try:
            with open(self.filepath, 'r') as file:
                content = file.read()
                # Split front matter and content
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        self.metadata = yaml.safe_load(parts[1]) or {}
                        if not isinstance(self.metadata, dict):
                            self.metadata = {}
                    except yaml.YAMLError:
                        self.metadata = {}
                    self.content = parts[2]
                else:
                    self.content = content
        except Exception as e:
            print(f"Error reading file {self.filepath}: {e}")
            self.content = ""
            self.metadata = {}

def get_blog_posts(directory: str) -> List[BlogPost]:
    """Get all markdown files from the specified directory."""
    blog_posts = []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            blog_posts.append(BlogPost(filepath))
    return blog_posts

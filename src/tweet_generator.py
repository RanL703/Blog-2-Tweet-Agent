import google.generativeai as genai
from typing import List
import os
import re

class TweetGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def clean_tweet(self, tweet: str) -> str:
        """Clean tweet text and ensure it's under character limit."""
        # Remove tweet numbering and labels
        tweet = re.sub(r'^(Tweet \d+:|Step \d+:|#\d+:)', '', tweet)
        
        # Remove markdown formatting
        tweet = re.sub(r'\*\*(.*?)\*\*', r'\1', tweet)
        tweet = re.sub(r'\*(.*?)\*', r'\1', tweet)
        
        # Clean up any double spaces or newlines
        tweet = re.sub(r'\s+', ' ', tweet).strip()
        
        # Ensure tweet is under limit
        if len(tweet) > 280:
            cutoff = tweet[:277].rfind(' ')
            if cutoff == -1:
                cutoff = 277
            tweet = tweet[:cutoff] + "..."
        
        return tweet

    def generate_tweets(self, blog_post) -> List[str]:
        metadata = blog_post.metadata or {}
        title = metadata.get('title', '') if isinstance(metadata, dict) else ''
        
        prompt = f"""
        Generate an engaging Twitter thread about this blog post.
        Format as [MAIN] for first tweet and [REPLY] for subsequent tweets.

        Guidelines:
        - First tweet should hook readers with the main value proposition
        - Each subsequent tweet should dive deep into specific aspects
        - Use full 280 characters when needed for detailed explanations
        - Make it conversational yet informative
        - Include emojis and hashtags naturally
        - Add specific examples and key points
        - Main tweet should include 2-3 relevant hashtags
        - Break complex ideas into digestible chunks
        - End with a compelling call to action
        
        DO NOT include labels like "Tweet 1:" or "Step 1:"
        Each tweet should read naturally as part of a thread.

        Blog title: {title}
        Blog content:
        {blog_post.content}
        """

        try:
            response = self.model.generate_content(prompt)
            tweets = []
            
            for line in response.text.split('\n'):
                line = line.strip()
                if line.startswith('[MAIN]') or line.startswith('[REPLY]'):
                    clean_text = self.clean_tweet(
                        line.replace('[MAIN]', '').replace('[REPLY]', '').strip()
                    )
                    if clean_text and len(clean_text) > 10:  # Ensure meaningful content
                        tweets.append(clean_text)
            
            if not tweets:
                raise ValueError("No valid tweets generated")
                
            return tweets
            
        except Exception as e:
            print(f"Error generating tweets: {e}")
            # Return a basic tweet as fallback
            return [f"📝 New blog post: {title}\n\n#tech #coding #programming"]

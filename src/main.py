import os
import argparse
from dotenv import load_dotenv
from blog_reader import get_blog_posts
from tweet_generator import TweetGenerator
from twitter_poster import TwitterPoster

def process_blog_posts(directory: str, dry_run: bool):
    print(f"Processing blog posts from: {directory}")
    
    # Get all blog posts
    posts = get_blog_posts(directory)
    
    if not posts:
        print("No markdown files found in the specified directory")
        return

    # Initialize generators
    generator = TweetGenerator()
    poster = TwitterPoster()

    # Process each post
    for post in posts:
        print(f"Processing: {os.path.basename(post.filepath)}")
        tweets = generator.generate_tweets(post)
        
        if dry_run:
            print("\nGenerated tweets (dry run):")
            for i, tweet in enumerate(tweets):
                print(f"\nTweet {i+1}:\n{tweet}")
        else:
            poster.post_tweets(tweets)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', 
                       help='Generate tweets without posting')
    args = parser.parse_args()
    
    load_dotenv()
    
    posts_path = os.getenv('BLOG_POSTS_PATH')
    if not posts_path:
        raise ValueError("BLOG_POSTS_PATH not set in .env file")
    
    if not os.path.exists(posts_path):
        raise ValueError(f"Directory does not exist: {posts_path}")

    process_blog_posts(posts_path, args.dry_run)

if __name__ == "__main__":
    main()

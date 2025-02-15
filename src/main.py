import os
import argparse
import time
from dotenv import load_dotenv
from blog_reader import monitor_blog_directory, BlogPost
from tweet_generator import TweetGenerator
from twitter_poster import TwitterPoster

def process_blog_post(post: BlogPost, dry_run: bool):
    """Process a single blog post."""
    print(f"Processing: {os.path.basename(post.filepath)}")
    
    generator = TweetGenerator()
    tweets = generator.generate_tweets(post)
    
    if dry_run:
        print("\nGenerated tweets (dry run):")
        for i, tweet in enumerate(tweets):
            print(f"\nTweet {i+1}:\n{tweet}")
    else:
        poster = TwitterPoster()
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

    print(f"Starting blog monitor on {posts_path}")
    observer = monitor_blog_directory(
        posts_path,
        lambda post: process_blog_post(post, args.dry_run)
    )
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping blog monitor...")
    observer.join()

if __name__ == "__main__":
    main()

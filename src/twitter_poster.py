import tweepy
import os
import time
from typing import List
import random
from datetime import datetime, timezone

class TwitterPoster:
    def __init__(self):
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Missing Twitter API credentials in .env file")

        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )

        # Add v1 API for rate limit checking
        self.api = tweepy.API(auth)

        # Verify credentials
        try:
            self.client.get_me()
            print("Successfully authenticated with Twitter API")
        except tweepy.Forbidden:
            print("""
ERROR: Twitter API authentication failed due to permissions issue.
Please check your Twitter Developer Portal settings:
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Select your app
3. Go to "User authentication settings"
4. Enable OAuth 1.0a
5. Set App permissions to "Read and write"
6. Set Type of App to "Web App, Automated App or Bot"
7. Save changes and regenerate tokens if needed
            """)
            raise
        except Exception as e:
            print(f"Twitter API authentication failed: {str(e)}")
            raise

        # Get user info during initialization
        try:
            self.user_info = self.client.get_me().data
            self.username = self.user_info.username
            print(f"Authenticated as @{self.username}")
        except Exception as e:
            print(f"Error getting user info: {str(e)}")
            raise

    def check_rate_limits(self):
        """Check current rate limits and wait if needed."""
        try:
            limits = self.api.rate_limit_status()
            tweets_remaining = limits['resources']['tweets']['/tweets']['remaining']
            reset_time = limits['resources']['tweets']['/tweets']['reset']
            
            if tweets_remaining == 0:
                reset_datetime = datetime.fromtimestamp(reset_time, timezone.utc)
                now = datetime.now(timezone.utc)
                wait_seconds = (reset_datetime - now).total_seconds() + 10  # Add buffer
                
                print(f"Rate limit reached. Waiting {wait_seconds:.0f} seconds until {reset_datetime} UTC")
                time.sleep(wait_seconds)
                return False
            
            print(f"Rate limits: {tweets_remaining} tweets remaining")
            return True
            
        except Exception as e:
            print(f"Error checking rate limits: {e}")
            return True  # Continue if we can't check

    def post_with_retry(self, tweet_func, max_retries=5, initial_delay=15):
        """Post with exponential backoff retry logic and jitter."""
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return tweet_func()
            except tweepy.TooManyRequests:
                if attempt == max_retries - 1:
                    raise
                # Add jitter to avoid thundering herd
                jitter = random.uniform(0, 5)
                wait_time = delay + jitter
                print(f"Rate limit hit, waiting {wait_time:.1f} seconds (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                delay *= 2  # Exponential backoff
            except Exception as e:
                print(f"Error: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay)

    def post_tweets(self, tweets: List[str]):
        if not tweets:
            return
            
        # Check rate limits before starting
        if not self.check_rate_limits():
            print("Rate limits exhausted, try again later")
            return
            
        try:
            # Add initial delay before starting
            time.sleep(5)
            
            # Post the main tweet first
            main_response = self.post_with_retry(
                lambda: self.client.create_tweet(text=tweets[0])
            )
            main_tweet_id = main_response.data['id']
            print(f"Main tweet posted: {tweets[0][:50]}...")
            
            # Post replies with rate limit checking between each
            for i, tweet in enumerate(tweets[1:], 1):
                # Check rate limits before each reply
                if not self.check_rate_limits():
                    print(f"Stopping after {i} replies due to rate limits")
                    break
                
                try:
                    base_delay = min(15 + (i * 5), 30)  # Increased delays
                    jitter = random.uniform(0, 5)
                    time.sleep(base_delay + jitter)
                    
                    response = self.post_with_retry(
                        lambda: self.client.create_tweet(
                            text=tweet,
                            in_reply_to_tweet_id=main_tweet_id
                        )
                    )
                    main_tweet_id = response.data['id']
                    print(f"Reply {i} posted: {tweet[:50]}...")
                    
                except Exception as e:
                    print(f"Error posting reply {i}: {str(e)}")
                    time.sleep(60)  # Longer wait after errors
                    
        except Exception as e:
            print(f"Error in tweet thread: {str(e)}")

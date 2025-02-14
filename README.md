# 🤖 Blog to Twitter Bot

Turn your blog posts into engaging Twitter threads automatically! This AI-powered bot uses Google's Gemini AI to transform your blog content into perfectly crafted tweet threads, making your content sharing smarter and more efficient.

📖 **Follow my blog**: [TheRanLBlog](https://theranlblog-psi-inky.vercel.app/) - Where I share my tech adventures and insights!

## ✨ Features

- 🧠 AI-powered tweet generation using Google's Gemini
- 🧵 Automatically creates threaded tweets
- 📝 Processes markdown files from your blog
- ⏱️ Smart rate limiting and error handling
- 🔄 Supports dry run mode for testing
- 🎯 Optimized for engagement and readability

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd twitter_bot
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Your Credentials**
   - Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```
   - Get your Twitter API credentials:
     1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
     2. Create a new app or select existing one
     3. Enable OAuth 1.0a with Read & Write permissions
     4. Generate API Key, API Secret, Access Token, and Access Token Secret

   - Get your Gemini API key:
     1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
     2. Create a new API key

   - Update `.env` with your credentials:
     ```properties
     TWITTER_API_KEY=your_api_key
     TWITTER_API_SECRET=your_api_secret
     TWITTER_ACCESS_TOKEN=your_access_token
     TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
     GEMINI_API_KEY=your_gemini_api_key
     BLOG_POSTS_PATH=/path/to/your/blog/posts
          ```

## 💡 Usage

### Test Mode (Recommended First Run)
```bash
python src/main.py --dry-run
```
This will show you the generated tweets without posting them.

### Production Mode
```bash
python src/main.py
```
This will generate and post the tweets.

## 🛠️ How It Works

1. **Blog Post Processing**
   - Scans your specified directory for markdown files
   - Extracts frontmatter metadata and content
   - Supports Hugo-style blog posts

2. **AI Tweet Generation**
   - Uses Gemini AI to analyze your blog content
   - Generates engaging, conversational tweet threads
   - Maintains natural flow while preserving key information
   - Automatically includes relevant hashtags

3. **Smart Twitter Posting**
   - Creates a main tweet followed by threaded replies
   - Handles rate limiting intelligently
   - Implements exponential backoff for reliability
   - Provides detailed progress feedback

## ⚙️ Customization

Want to tweak how your tweets are generated? The bot is highly customizable:

1. **Tweet Style**: Modify the prompt in `tweet_generator.py`
2. **Posting Behavior**: Adjust delays and retry logic in `twitter_poster.py`
3. **Content Processing**: Customize blog parsing in `blog_reader.py`

## 📌 Best Practices

- Run with `--dry-run` first to review generated tweets
- Keep your API keys secure and never commit them
- Monitor your Twitter API usage limits
- Regular updates to your blog directory path as needed

## 🤝 Contributing

Found a bug or have an improvement in mind? Contributions are welcome! 

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🌟 Star the Repository

If you find this bot useful, don't forget to star the repository! It helps others discover this tool.

---

Built with ❤️ for bloggers who love automation

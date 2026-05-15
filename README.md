MovieResys

MovieResys is an AI-powered movie recommendation platform that combines machine learning, Reddit sentiment analysis, and large language models to generate intelligent movie recommendations based on genre and real audience opinions. Unlike traditional recommendation systems that rely only on ratings or popularity, MovieIQ analyzes real Reddit discussions to understand audience reactions, strengths, criticisms, and viewing experiences for each movie.

The project integrates TMDB movie datasets, Tavily Search API, Groq LLMs, Flask, and a cinematic frontend interface to create an interactive recommendation experience with animated genre-based visuals and AI-generated review summaries.

1. Features
Genre-Based Recommendations
Users can search movies by genres such as:
Horror
Action
Comedy
Thriller
Romance
Fantasy
Science Fiction
Mystery
Drama
Adventure

Reddit-Powered Movie Analysis
MovieIQ searches Reddit discussions using Tavily Search API to collect:
Real user reviews
Viewer discussions
Audience opinions
Watch recommendations
Positive and negative reactions
AI-Powered Review Summarization

Using Groq LLMs, the system generates:
Overall audience verdict
What viewers liked
What viewers disliked
Positive Reddit snippets
Negative Reddit snippets
Viewer recommendation summaries

Cinematic Frontend Interface

The frontend includes:

Animated atmospheric backgrounds
Genre-specific color themes
Interactive review tabs
Dynamic movie cards
Responsive design
Reddit source links
2. Tech Stack
Backend
Python
Flask
Pandas
Requests
BeautifulSoup
AI and APIs
Groq API
Tavily Search API
TMDB API
OMDb API
Frontend
HTML
CSS
JavaScript
Jinja2 Templates
Machine Learning
Scikit-learn
TF-IDF Vectorizer
Logistic Regression

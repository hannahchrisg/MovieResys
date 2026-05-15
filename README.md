# MovieResys

MovieResys is an AI-powered movie recommendation system that combines machine learning, Reddit sentiment analysis, and large language models to generate intelligent movie recommendations based on genre and real audience opinions.

Unlike traditional recommendation systems that rely only on ratings or popularity, MovieResys analyzes real Reddit discussions to understand audience reactions, strengths, criticisms, and viewing experiences for each movie.

The project integrates TMDB movie datasets, Tavily Search API, Groq LLMs, Flask, and a cinematic frontend interface to create an interactive recommendation experience with animated genre-based visuals and AI-generated review summaries.

---

# Features

## 1. Genre-Based Movie Recommendations
Users can search movies by genres such as:

- Horror
- Action
- Comedy
- Thriller
- Romance
- Fantasy
- Science Fiction
- Mystery
- Drama
- Adventure

The system ranks movies using:
- TMDB ratings
- Popularity scores
- Vote counts

---

## 2. Reddit-Powered Movie Analysis

MovieResys searches Reddit discussions using Tavily Search API to collect:

- Real user reviews
- Viewer discussions
- Audience opinions
- Watch recommendations
- Positive and negative reactions

---

## 3. AI-Powered Review Summarization

Using Groq LLMs, the system generates:

- Overall audience verdict
- What viewers liked
- What viewers disliked
- Positive Reddit snippets
- Negative Reddit snippets
- Viewer recommendation summaries

---

# Frontend Features

The frontend includes:

- Animated atmospheric backgrounds
- Genre-specific color themes
- Interactive review tabs
- Dynamic movie cards
- Responsive design
- Reddit source links

---

# Tech Stack

## Backend
- Python
- Flask
- Pandas
- Requests
- BeautifulSoup
- Groq API
- Tavily Search API
- TMDB API
- OMDb API

## Frontend
- HTML
- CSS
- JavaScript
- Jinja2 Templates

## Machine Learning
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression

---

# Dataset Sources

The project uses:
- TMDB movie datasets
- IMDb sentiment dataset
- Reddit discussions collected through Tavily Search API

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/hannahchrisg/MovieResys.git
cd MovieResys
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Create Environment File

Create a `.env` file and add:

```env
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
TMDB_API_KEY=your_key
```

---

# Run the Project

```bash
python app.py
```

Open:

```bash
http://127.0.0.1:5000
```

---

# Project Workflow

1. User enters a movie genre.
2. Flask backend filters top-ranked movies from dataset.
3. Tavily searches Reddit discussions.
4. Groq LLM analyzes Reddit opinions.
5. Frontend displays movie recommendations with summaries and snippets.

---

# Future Improvements

- Mood-based recommendations
- User authentication
- Watchlist system
- Streaming platform integration
- Collaborative filtering
- Advanced NLP sentiment analysis

---

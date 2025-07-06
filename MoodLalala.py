import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def main():
    # Read the files in Pandas
    books_df = pd.read_csv("books.csv")
    movies_df = pd.read_csv("movies_metadata.csv")


    # Cleaning and Preparing the Data
    movies_df.columns
    # Limiting to 5000 rows
    movies_df = movies_df.head(5000)
    movies_df = movies_df[['title', 'genres', 'runtime', 'overview', 'vote_average']]

    # Renaming columns
    movies_df = movies_df.rename(columns={
        'genres' : 'genre',
        'overview' : 'description',
        'runtime': 'duration',
        'vote_average': 'rating'
    })

    # Dropping Rows with Missing Info
    movies_df = movies_df.dropna(subset=['title', 'genres', 'description', 'duration'])

    movies_df['description'] = movies_df['description'].fillna('')
    movies_df['rating'] = pd.to_numeric(movies_df['rating'], errors='coerce')
    movies_df['duration'] = pd.to_numeric(movies_df['duration'], errors='coerce')
    movies_df = movies_df.dropna(subset=['rating', 'duration'])
    # Resetting Index
    movies_df.reset_index(drop=True, inplace=True)

    books_df = books_df.rename(columns={'Name': 'title', 'Genre':'genre'}) # renaming a coloumn
    # Clean the book titles
    books_df['title'] = books_df['title'].apply(lambda x:x.split('(')[0].strip())

    # Getting Book Info from Google Books API
    api_key = "AIzaSyALm7S7u4xG0lNXyT7jT1V9nWGXUGVezvI"

    books_df[['description', 'pages', 'rating']] = books_df['title'].apply(
      lambda x: pd.Series(fetchBookInfo(x, api_key)))

    books_df['description'] = books_df['description'].fillna('')

    # Creating duration columns in Books (converting page number into time)
    books_df['pages'] = pd.to_numeric(books_df['pages'], errors='coerce')
    books_df = books_df.dropna(subset=['pages'])

    books_df['duration'] = books_df['pages'] * 2 # Estimated reading time

    # Streamlit Code
    st.title("✨ ModeLalala: Your Mood-Based Recommender 🎬📚")

    # Mood Input
    user_mood = st.text_input("💭 How are you feeling today?")

    # Genre Input
    genre_list = list(set(
        pd.concat([books_df['genre'], movies_df['genre']])
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    ))

    user_genre = st.selectbox("🎭 Choose a Genre", options=genre_list)

    # Time Input
    user_time = st.slider("⏱️ Max time you can spend (in minutes):", 10, 300, 60)

    if st.button("🎁 Get Recommendations!"):
        books = recommend_books_by_mood(user_mood, books_df)
        movies = recommend_movies_by_mood(user_mood, movies_df)

        filtered_books = filter_results(books, user_genre, user_time)
        filtered_movies = filter_results(movies, user_genre, user_time)

        st.subheader("📚 Book Recommendations")
        st.dataframe(filtered_books[['title', 'genre', 'description', 'pages', 'rating']])

        st.subheader("🎬 Movie Recommendations")
        st.dataframe(filtered_movies[['title', 'genre', 'description', 'duration', 'rating']])



def fetchBookInfo(title, api_key):
  # Getting info from Google Books API (not scraping kez goodreads block scra)
  try:
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'items' in data:
      book = data['items'][0]['volumeInfo'] # get first book in results list and focus on volumeInfo section
      description = book.get('description', 'No description available')
      pages = book.get('pageCount', 'Unknown')
      rating = book.get('averageRating', 'Not rated')

      return description, pages, rating
    else:
      return 'No description', 'Unkown', 'Not rated'

  except Exception as e:
    print(f"Error fetching for {title}: e")
    return 'Error fectching', 'Error', 'Error' # Error response in case of something breaks
  
def recommend_books_by_mood(user_input, df, top_n=100):
  tfidf = TfidfVectorizer(stop_words='english')

  # Fit on all descriptions
  tfidf_matrix = tfidf.fit_transform(df['description'])

  # Transform user input into same vector space
  user_vec = tfidf.transform([user_input])

  # Calculate similarity scores
  similarity_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()

  # Attach scores to DataFrame
  result_df = df.copy()
  result_df['similarity'] = similarity_scores

  # Return top matches
  return result_df.sort_values(by='similarity', ascending=False)[['title', 'Genre', 'description', 'pages', 'rating']].head(top_n)

def recommend_movies_by_mood(user_input, df, top_n=100):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description'])
    user_vec = tfidf.transform([user_input])
    similarity_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
    result_df = df.copy()
    result_df['similarity'] = similarity_scores
    return result_df.sort_values(by='similarity', ascending=False)[['title', 'genres', 'description', 'duration', 'rating']].head(top_n)

def filter_results(df, selected_genre=None, max_time=None):
  if selected_genre:
    df = df[df['genre']].str.contains(selected_genre, case=False, na=False)
  if max_time:
    df = df[df['duration']] <= max_time
  return df.head(5)


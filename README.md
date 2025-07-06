# ✨ MoodLalala: Your Mood-Based Recommender 🎬📚

**MoodLalala** is a Streamlit-based mood-aware recommendation system that suggests **books** and **movies** tailored to your current mood, favorite genre, and available time. Whether you're feeling joyful, curious, or melancholic — MoodLalala helps you find a story that matches.

## 🚀 Features
- Mood-based recommendations using **TF-IDF** and **cosine similarity**
- Retrieves book info using **Google Books API**
- Movie metadata from **TMDb**
- Genre and time filtering
- Interactive web app built with **Streamlit**

## 📁 Datasets
- `books_cleaned.csv`: Contains book titles, genres, and other info
- `movies_metadata_reduced.csv`: Trimmed movie metadata with title, genre, runtime, etc.
- Descriptions for books are fetched via Google Books API
  

## 📊 How It Works

1. **User Input**  
   👉 Enter your current mood (e.g., "adventurous", "cozy")  
   👉 Select a genre from the dropdown  
   👉 Set available time using the slider  

2. **AI Processing**  
   🧠 TF-IDF vectorizer analyzes mood + content descriptions  
   🔍 Cosine similarity matches your input with books/movies  

3. **Smart Filtering**  
   ⏱️ Exceeds time limit? Removed!  
   🎭 Wrong genre? Filtered out!  

4. **Results Display**  
   📚 Top book recommendations  
   🎬 Top movie suggestions  

## 🎯 Example Use Case

**Input**:  
- Mood: _"adventurous"_  
- Genre: _"thriller"_  
- Time: _90 minutes_  

**Output**:  
**Books**:  
1. _Into the Wild_ (Adventure, 180 pages)  
2. _The Hunger Games_ (Thriller, 150 pages)  
...  

**Movies**:  
1. _Jurassic Park_ (1h 47min)  
2. _Indiana Jones_ (1h 35min)  
...


---

✍️ **Author**: [Syeda Khadija Hassan](mailto:iamsyedq@gmail.com)  
🤖 _AI Program (2024-2028)_  
💡 _For inquiries contact at: iamsyedq@gmail.com_  























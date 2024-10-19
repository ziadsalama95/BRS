import streamlit as st
import pickle
import numpy as np
from PIL import Image

# Load the pre-trained model and data
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_name = pickle.load(open('artifacts/book_name.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
final_ratings = pickle.load(open('artifacts/final_ratings.pkl', 'rb'))

# Function to recommend books
def recommend_book(book_name, n_neighbors=6):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1, -1), n_neighbors=n_neighbors+1)
    recommended_books = [book_pivot.index[book] for book in suggestion[0]]
    return recommended_books[1:]  # Exclude the first one as it is the input book

# Improved Streamlit UI
st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="centered")

# Title and description
st.title('📚 Book Recommendation System')
st.markdown("""
Welcome to the **Book Recommendation System**! Enter a book title, choose the number of recommendations you'd like, 
and we'll suggest similar books. You can even see the book covers (if available).
""")

# Input section
st.sidebar.header("User Input")
book_input = st.sidebar.text_input("Enter a book name:")
num_recommendations = st.sidebar.slider("Number of recommendations", 2, 20, 5)

# Main section for displaying recommendations
if st.sidebar.button('Recommend'):
    st.subheader(f"Recommendations for: **{book_input}**")
    
    if book_input in book_name.values:
        recommendations = recommend_book(book_input, n_neighbors=num_recommendations)
        
        st.write(f"We found **{len(recommendations)}** recommendations for you:")
        
        for rec in recommendations:
            st.markdown(f"**{rec}**")
            
            # Display book image if available
            try:
                image_url = final_ratings[final_ratings['title'] == rec]['image-url'].iloc[0]
                st.image(image_url, width=150, caption=rec)
            except:
                st.write("*(Image not available)*")
    else:
        st.error("Book not found. Please check the name or try another title.")
else:
    st.sidebar.info("Enter a book title and hit 'Recommend' to get book suggestions.")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ by [Ziad Salama](https://www.linkedin.com/in/ziadsalama/)")

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

# Custom CSS for styling
st.markdown("""
    <style>
        .font {
            font-family: 'Courier New', Courier, monospace;
        }
        .book-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .book {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            width: 150px;
            text-align: center;
            transition: transform 0.2s;
        }
        .book:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .book-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .placeholder-image {
            background-color: #f0f0f0;
            width: 120px;
            height: 180px;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 1px dashed #ccc;
            margin: auto;
        }
        footer {
            text-align: center;
            font-size: 12px;
            color: #777;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title('📚 Book Recommendation System')
st.markdown("""
Welcome to the **Book Recommendation System**! Enter a book title, choose the number of recommendations you'd like, 
and we'll suggest similar books. You can even see the book covers (if available).
""", unsafe_allow_html=True)

# Input section with autocomplete
st.sidebar.header("User Input")
book_input = st.sidebar.text_input("Enter a book name:")
num_recommendations = st.sidebar.slider("Number of recommendations", 2, 20, 5)

# Auto-completion for book input
if book_input:
    book_options = book_name[book_name.str.contains(book_input, case=False, na=False)].tolist()
    if book_options:
        book_input = st.sidebar.selectbox("Select a book:", options=book_options)
    else:
        book_input = st.sidebar.text_input("Enter a book name:")

# Main section for displaying recommendations
if st.sidebar.button('Recommend'):
    st.subheader(f"Recommendations for: **{book_input}**")
    
    if book_input in book_pivot.index:
        recommendations = recommend_book(book_input, n_neighbors=num_recommendations)
                
        # Create a container for the book recommendations
        book_container = st.container()
        with book_container:
            cols = st.columns(3)  # Adjust the number of columns as needed
            for i, rec in enumerate(recommendations):
                with cols[i % 3]:  # Cycle through columns
                    st.markdown(f"<div class='book'><div class='book-title'>{rec}</div>", unsafe_allow_html=True)
                    # Display book image if available, or a placeholder
                    try:
                        image_url = final_ratings[final_ratings['title'] == rec]['image-url'].iloc[0]
                        st.image(image_url, width=120)
                    except:
                        st.markdown("<div class='placeholder-image'>No Image</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Book not found. Please check the name or try another title.")
else:
    st.sidebar.info("Enter a book title and hit 'Recommend' to get book suggestions.")

# Footer
st.markdown("""
<footer>
    <p>Powered by the Book Recommendation System Team | &copy; 2024</p>
</footer>
""", unsafe_allow_html=True)

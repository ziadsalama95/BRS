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
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=n_neighbors + 1)
    recommended_books = [book_pivot.index[book] for book in suggestion[0]]
    return recommended_books[1:]  # Exclude the first one as it is the input book

# Improved Streamlit UI
st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .book-title {
            font-weight: bold;
            margin-bottom: 15px;
        }
        footer {
            text-align: center;
            font-size: 12px;
            color: #777;
            margin-top: 20px;
        }
        .separator {
            border-top: 1px solid #ccc;
            margin: 0px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title('📚 Book Recommendation System')
st.markdown("""
Welcome to the **Book Recommendation System**! Enter a book title, and we'll suggest similar books. You can even see the book covers (if available).
""", unsafe_allow_html=True)

# Input section
st.sidebar.header("User Input")
book_input = st.sidebar.text_input("Enter a book name:")
num_recommendations = st.sidebar.slider("Number of recommendations", 2, 20, 5)

# Auto-completion for book input
if book_input:
    book_options = book_name[book_name.str.contains(book_input, case=False, na=False)].tolist()[:5]  # Limit to 5 suggestions
    if book_options:
        # Display suggestions below the input box
        for option in book_options:
            if st.sidebar.button(option, key=option):  # Create a button for each suggestion
                with st.spinner('Generating recommendations...'):
                    recommendations = recommend_book(option, n_neighbors=num_recommendations)  # Trigger recommendations
                
                st.subheader(f"Recommendations for: **{option}**")

                # Display book recommendations in a vertical list
                for rec in recommendations:
                    st.markdown(f"<div class='book'><div class='book-title'>{rec}</div>", unsafe_allow_html=True)
                    # Display book image if available
                    image_url = final_ratings[final_ratings['title'] == rec]['image-url'].iloc[0]
                    st.image(image_url, width=120)
                    
                    # Add a separator after each book
                    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
                    
    else:
        st.sidebar.warning("No matching books found. Please try another title.")
else:
    st.sidebar.info("Enter a book title to see suggestions.")

# Footer
st.markdown("""
<footer>
    <p>Powered by <a href="https://www.linkedin.com/in/ziadsalama/" target="_blank">Ziad Salama</a> | &copy; 2024</p>
</footer>
""", unsafe_allow_html=True)

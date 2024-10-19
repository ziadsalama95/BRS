
# Book Recommendation System 📚

This is a **Book Recommendation System** built using machine learning and deployed with **Streamlit**. It allows users to input a book title and provides similar book recommendations. Additionally, users can view book covers (if available).

## Project Overview

This system utilizes a pre-trained model and a set of book data to recommend books based on a user's input. The model works by finding the nearest neighbors of the given book in the feature space. The app is deployed and can be accessed [here](https://depi-brs.streamlit.app/).

## Features

- **Auto-completion**: Suggests book titles as you type.
- **Book Recommendations**: Returns a list of similar books.
- **Book Covers**: Displays the cover image of the recommended books (if available).
- **Customizable Recommendations**: Users can choose the number of book recommendations.
- **User-Friendly Interface**: Simple and interactive UI built with Streamlit.

## Tech Stack

- **Python**: Main programming language.
- **Streamlit**: Web framework used for deployment.
- **scikit-learn**: Machine learning library used to implement the recommendation model.
- **NumPy**: For numerical operations.
- **Pandas**: To manage and process the data.
- **PIL**: For handling book images.

## Model Details

- The system uses a **K-Nearest Neighbors (KNN)** algorithm for recommendations.
- Book titles and their corresponding features are stored in a **pivot table** format to enable efficient lookups and recommendations.
- The trained model and book data are stored in the `artifacts` folder and loaded using `pickle`.

## How to Run Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/ziadsalama95/book-recommendation-system.git
    ```

2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

4. Visit `http://localhost:8501` in your browser.

## Folder Structure

```
.
├── app.py              # Main Streamlit app
├── artifacts/
│   ├── model.pkl       # Trained recommendation model
│   ├── book_name.pkl   # Pickled list of book names
│   ├── book_pivot.pkl  # Pickled book pivot table for recommendation
│   └── final_ratings.pkl  # Dataset containing book titles and images
├── requirements.txt    # Required dependencies
└── README.md           # Project documentation
```

## Deployed App

The app is deployed and accessible at: [https://depi-brs.streamlit.app/](https://depi-brs.streamlit.app/).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

Feel free to explore and contribute!

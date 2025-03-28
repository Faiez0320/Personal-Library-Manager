import streamlit as st
import json

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    """Load the library from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    """Add a book to the library."""
    library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
    save_library(library)

def remove_book(library, title):
    """Remove a book from the library."""
    library[:] = [book for book in library if book["title"].lower() != title.lower()]
    save_library(library)

def search_books(library, keyword, search_by):
    """Search for books by title or author."""
    keyword = keyword.lower()
    return [book for book in library if keyword in book[search_by].lower()]

def display_statistics(library):
    """Display library statistics."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, read_percentage

# Streamlit UI
st.title("📚 Personal Library Manager")
library = load_library()

menu = st.sidebar.radio("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Statistics"])

if menu == "Add a Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        add_book(library, title, author, year, genre, read_status)
        st.success("Book added successfully!")

elif menu == "Remove a Book":
    st.subheader("Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        remove_book(library, title)
        st.success("Book removed successfully!")

elif menu == "Search for a Book":
    st.subheader("Search for a Book")
    search_by = st.radio("Search by", ["title", "author"])
    keyword = st.text_input("Enter search keyword")
    if st.button("Search"):
        results = search_books(library, keyword, search_by)
        if results:
            for book in results:
                st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

elif menu == "Display All Books":
    st.subheader("Your Library")
    if library:
        for book in library:
            st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("Your library is empty.")

elif menu == "Statistics":
    st.subheader("Library Statistics")
    total_books, read_percentage = display_statistics(library)
    st.write(f"📚 Total books: {total_books}")
    st.write(f"📖 Percentage read: {read_percentage:.2f}%")

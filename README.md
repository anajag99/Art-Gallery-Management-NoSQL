# Art Gallery Management System (NoSQL)

## Overview
The Art Gallery Management System is designed to streamline gallery operations by leveraging MongoDB (NoSQL) for flexible and scalable data management. The backend is built using Python and pymongo for seamless database interaction, while the frontend utilizes Kivy for an interactive user interface.

## Problem Statement
This project aims to build a robust, end-to-end solution for managing art gallery operations. By utilizing MongoDB, the system is designed to handle complex relationships between data entities such as artworks, exhibitions, loans, and sales transactions. The focus is on scalability, performance, and user experience.

## Key Features
- **CRUD Operations**: Full Create, Read, Update, and Delete support for managing artwork, exhibitions, loans, and sales transactions.
- **Search and Filtering**: Advanced search functionality to filter artworks based on partial keywords, making data retrieval efficient.
- **Exhibition and Loan Management**: Seamlessly manage exhibitions and artwork loans, including scheduling and tracking.
- **Sales and Transaction Monitoring**: Track sales transactions, including customer details, artwork involved, and payment methods.
- **User Authentication**: Secure user login system with credentials validation.

## Technologies Used
- **MongoDB**: A NoSQL database used for flexible and scalable data storage. It supports complex queries and fast retrieval of documents.
- **Python (pymongo)**: The backend is implemented in Python using the pymongo library for interacting with MongoDB. It handles CRUD operations, complex queries, and data formatting.
- **Kivy**: A Python-based framework for building the frontend GUI. Kivy allows the creation of interactive, cross-platform applications with a highly customizable interface.

## Database Architecture
The database is structured into multiple collections, each handling a different aspect of gallery management:
- **Artwork Collection**: Stores metadata about each artwork (e.g., title, artist, medium, price).
- **Exhibition Collection**: Manages exhibition details such as dates, venue, and participating artists.
- **Loan Collection**: Tracks artwork loans, including borrower information and loan terms.
- **Transaction Collection**: Records sales transactions, including customer, artwork, and payment details.
- **Conservation Collection**: Tracks conservation activities performed on artworks.

### Example MongoDB Collections:
```json
  {
    "Artwork": [
      {
        "title": "Starry Night",
        "artist": "Vincent van Gogh",
        "medium": "Oil on Canvas",
        "price": 1000000,
        "tags": ["impressionism", "night"]
      }
    ],
    "Exhibition": [
      {
        "name": "Impressionist Art",
        "venue": "Gallery A",
        "start_date": "2025-01-15",
        "end_date": "2025-02-15",
        "artists": ["Vincent van Gogh", "Claude Monet"]
      }
    ]
  }
```
## Backend Implementation
The backend is implemented in Python, using the pymongo library to interact with MongoDB. The following operations are supported:
- **Create**: Insert new documents into collections (e.g., adding new artwork).
- **Read**: Retrieve documents using queries (e.g., retrieving all artworks by a specific artist).
- **Update**: Modify existing documents based on specific criteria (e.g., updating artwork details).
- **Delete**: Remove documents from collections (e.g., deleting an artwork or transaction).
- **Search**: Perform case-insensitive searches on collections, allowing partial keyword matching.

### Example code for Frontend:
```python
  from kivy.app import App
  from kivy.uix.screenmanager import ScreenManager, Screen
  from kivy.uix.button import Button
  from kivy.uix.textinput import TextInput
  
  class LoginScreen(Screen):
      def authenticate(self, username, password):
          # Logic to authenticate against MongoDB
          pass
  
  class MainScreen(Screen):
      pass
  
  class ArtGalleryApp(App):
      def build(self):
          sm = ScreenManager()
          sm.add_widget(LoginScreen(name='login'))
          sm.add_widget(MainScreen(name='main'))
          return sm
  
  if __name__ == '__main__':
      ArtGalleryApp().run()
```
## Conclusion
This Art Gallery Management System offers a comprehensive solution for managing gallery operations using MongoDB, Python, and Kivy. It provides an intuitive and efficient way to handle artwork inventory, exhibitions, sales, loans, and conservation activities. The system's modular design ensures scalability and flexibility, making it suitable for small to large galleries.

## Future Enhancements
- Mobile App Integration: Extend the system for mobile platforms.
- Advanced User Management: Implement roles and permissions for gallery staff and users.
- Analytics and Reporting: Add features for generating reports on sales, exhibitions, and artwork performance.

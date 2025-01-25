# Flask Blog Application

This repository contains a Flask-based web application designed for blogging, user authentication, and interactive commenting. The app provides a user-friendly interface for managing posts and comments, along with a secure authentication system.

## Features
- User authentication system with sign-up, login, and logout functionality.
- Create, read, update, and delete (CRUD) operations for blog posts.
- Add and manage comments on posts.
- Secure image upload for blog posts, with file storage.
- Session-based user login.
- Flash messaging system for notifications.

## Technologies Used
- **Flask**: Framework for creating the web application.
- **SQLite**: Database for storing user, post, and comment data.
- **HTML, CSS**: Frontend for rendering templates.
- **Jinja2**: Template engine used in Flask.

## Installation and Setup
### Prerequisites
Make sure you have the following installed:
- Python (3.7+ recommended)
- Virtualenv (optional but recommended)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/flask-blog.git
   cd flask-blog
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```
   The application will start running on `http://127.0.0.1:5000`.

5. Open the URL in your browser to access the application.

## Folder Structure
```
flask-blog/
|-- static/           # Static files like CSS, JavaScript, and images
|-- templates/        # HTML templates for rendering views
|-- app.py            # Main application file
|-- requirements.txt  # Required Python dependencies
|-- MediaDb.db        # SQLite database file
```

## API Endpoints
| Endpoint                       | Method | Description                                   |
|--------------------------------|--------|-----------------------------------------------|
| `/` or `/login`                | GET/POST | Login page for user authentication            |
| `/signup`                      | GET/POST | Sign-up page for new users                   |
| `/home`                        | GET/POST | Home page displaying posts                   |
| `/postspage`                   | GET/POST | Page for managing posts and comments         |
| `/deletepost/<int:sno>`        | GET/POST | Delete a specific post                       |
| `/deletecomment/<int:sno>`     | GET/POST | Delete a specific comment                    |
| `/postcontent`                 | GET/POST | Add content and upload images for a post     |
| `/addcomment/<...>`            | GET/POST | Add a comment to a specific post             |
| `/logout`                      | GET     | Log out the current user                     |

## Database Models
### User
- `id`: Integer, Primary Key
- `name`: String
- `username`: String (Unique, Required)
- `email`: String
- `password`: String

### Post
- `sno`: Integer, Primary Key
- `username`: String (Author of the post)
- `content`: Text
- `imdata`: String (Filepath of the uploaded image)

### Comment
- `sno`: Integer, Primary Key
- `post_username`: String
- `comment_username`: String (Author of the comment)
- `post_sno`: Integer (Linked post ID)
- `comment`: Text

## Contribution
Contributions are welcome! Here’s how you can contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes and push them to your fork:
   ```bash
   git push origin feature/my-feature
   ```
4. Create a pull request describing your changes.

## License
This project is licensed under the [MIT License](LICENSE).


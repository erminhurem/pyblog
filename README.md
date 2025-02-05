# PyBlog - Modern Django Blog Platform

A feature-rich blogging platform built with Django and Tailwind CSS, featuring a modern, responsive design and a rich set of functionalities.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.0+-green.svg)
![Tailwind CSS](https://img.shields.io/badge/tailwindcss-3.0+-blue.svg)

## Features

- 🎨 Modern, responsive design with Tailwind CSS
- 👤 User authentication and registration
- ✍️ Rich text blog post creation and editing
- 🏷️ Tag-based post organization
- 💬 Interactive commenting system
- ❤️ Post likes with real-time updates
- 🔍 Full-text search functionality
- 🌓 Dark mode support
- 📱 Mobile-friendly interface
- 🔄 Similar posts suggestions
- 🔗 Social sharing capabilities
- 📊 User profiles with activity tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/erminhurem/pyblog.git
cd pyblog
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your configuration:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see your blog in action!

## Usage

### Creating Blog Posts

1. Log in to the admin interface at `/admin`
2. Navigate to "Posts" section
3. Click "Add Post"
4. Fill in the title, content, and other fields
5. Add tags for better organization
6. Set status to "Published" when ready
7. Save the post

### Managing Comments

- Comments can be added by authenticated users
- Users can edit and delete their own comments
- Administrators can moderate comments through the admin interface

### User Features

- Users can register and create profiles
- Like/unlike posts
- Comment on posts
- View their activity in their profile
- Share posts on social media

## Project Structure

```
pyblog/
├── core/                   # Project settings
├── djblog/                # Main blog application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py           # URL routing
│   └── templatetags/      # Custom template tags
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── djblog/           # Blog templates
│   └── includes/         # Reusable components
└── static/               # Static files (CSS, JS, images)
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Uses [django-taggit](https://github.com/jazzband/django-taggit) for tagging 

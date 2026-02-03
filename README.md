# RecipeShare

A full-stack recipe sharing platform built with Django where users can discover, create, and review recipes from a vibrant cooking community.

**Live Demo:** [https://recipe-share-aoq6.onrender.com](https://recipe-share-aoq6.onrender.com)  
**GitHub:** [https://github.com/Tathya-Dixit/recipe-share](https://github.com/Tathya-Dixit/recipe-share)

## Features

### User Management
- User registration and authentication
- Custom user profiles with bio and profile pictures
- Public and private profile views
- Edit profile functionality

### Recipe Management
- Create, read, update, and delete recipes
- Rich recipe details: title, image, description, prep time, ingredients, and step-by-step instructions
- Image upload with Cloudinary integration
- Recipe ownership and permissions

### Discovery & Search
- Browse all recipes with pagination (9 recipes per page)
- Search recipes by title or ingredients
- View recipes by specific authors
- Recipe ratings and review counts

### Reviews & Ratings
- Rate recipes from 1-5 stars
- Leave written reviews
- View average ratings
- Delete your own reviews
- One review per user per recipe
- Authors cannot review their own recipes

### UI/UX
- Responsive design with Tailwind CSS
- Font Awesome icons
- Toast notifications for user feedback
- Clean, modern interface with red and yellow theme

## Tech Stack

### Backend
- **Django** - Web framework
- **PostgreSQL** - Production database (via dj-database-url)
- **SQLite** - Development database
- **Whitenoise** - Static file serving

### Frontend
- **Tailwind CSS** - Styling via CDN
- **Font Awesome 4.7** - Icons
- **Django Templates** - Server-side rendering

### Cloud Services
- **Cloudinary** - Image hosting and management
- **Render** - Application deployment
- **PostgreSQL** - Production database

### Additional Libraries
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing
- `gunicorn` - WSGI HTTP server

## Installation

### Prerequisites
- Python 3.11+
- pip
- PostgreSQL (for production) or SQLite (for development)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/Tathya-Dixit/recipe-share.git
cd recipe-share
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development

# Cloudinary Configuration (optional for local dev)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to view the application.

## Project Structure

```
recipe-share/
├── accounts/              # User authentication and profiles
│   ├── models.py         # Custom User model
│   ├── views.py          # Auth and profile views
│   ├── forms.py          # Profile edit form
│   └── urls.py
├── recipes/               # Recipe management
│   ├── models.py         # Recipe and Review models
│   ├── views.py          # Recipe CRUD and search
│   ├── forms.py          # Recipe creation form
│   └── urls.py
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar
│   ├── accounts/         # Auth and profile templates
│   └── recipes/          # Recipe templates
├── static/                # Static files (CSS, JS, images)
├── recipeshare/           # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── build.sh              # Render deployment script
└── manage.py
```

## Key Models

### User (Custom)
```python
- username (unique)
- email
- password (hashed)
- bio (text, optional)
- profile_pic (image, optional)
- is_verified (boolean)
- created_at (datetime)
```

### Recipe
```python
- title (string, max 100 chars)
- image (image upload)
- small_description (text, max 500 chars)
- estimated_prep_time (string)
- ingredients_list (text, newline-separated)
- process (text, newline-separated steps)
- author (foreign key to User)
- created_at, updated_at (datetime)
```

### Review
```python
- review (text, max 500 chars)
- rating (integer, 1-5)
- recipe (foreign key to Recipe)
- reviewer (foreign key to User)
- created_at, updated_at (datetime)
- unique_together: (recipe, reviewer)
```

## Main URLs

### Authentication
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout

### Profiles
- `/profile/` - Current user's profile
- `/profile/edit/` - Edit profile
- `/user/<username>/` - Public profile view

### Recipes
- `/` - Home page (recipe feed)
- `/recipes/create/` - Create new recipe
- `/recipes/<id>/` - Recipe detail page
- `/recipes/<id>/edit/` - Edit recipe
- `/recipes/<id>/delete/` - Delete recipe (confirmation)
- `/recipes/<id>/review/` - Add review (POST)
- `/recipes/<id>/review/delete/` - Delete review (POST)

## Features in Detail

### Search Functionality
- Real-time search by recipe title or ingredients
- Search preserves across pagination
- Clear search option to view all recipes

### Pagination
- 9 recipes per page
- Previous/Next buttons
- Page numbers (on desktop)
- Search query persists across pages

### Image Handling
- Development: Local file storage
- Production: Cloudinary CDN
- Automatic image optimization
- Fallback placeholder images

### Security
- CSRF protection on all forms
- User authentication required for create/edit/delete
- Permission checks (users can only edit/delete their own content)
- Password hashing with Django's built-in authentication
- SSL redirect in production
- Secure cookies in production

### Permissions
- Anonymous users: Browse and search recipes
- Authenticated users: All above + create recipes, leave reviews
- Recipe authors: Edit and delete their own recipes
- Review authors: Delete their own reviews

## Deployment

### Production Environment Variables

```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=recipe-share-aoq6.onrender.com
DATABASE_URL=postgresql://user:password@host:port/database

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Render Deployment

The project includes a `build.sh` script for Render:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**Render Configuration:**
- Runtime: Python 3.11
- Build Command: `./build.sh`
- Start Command: `gunicorn recipeshare.wsgi:application`
- Add PostgreSQL database
- Set environment variables

## Development Notes

### Custom User Model
The project uses a custom User model extending `AbstractUser` with additional fields (bio, profile_pic, is_verified). This is defined in `accounts/models.py` and configured via `AUTH_USER_MODEL = 'accounts.User'` in settings.

### Image Storage
- **Development**: Django's default file storage (stored in `/media/`)
- **Production**: Cloudinary for CDN benefits and Render compatibility

### Static Files
- Whitenoise serves static files in production
- Tailwind CSS loaded via CDN (no build process required)

## Future Enhancements

Potential features to add:
- Recipe categories/tags
- Favorite/bookmark recipes
- Follow other users
- Recipe collections
- Email verification
- Password reset functionality
- Social media sharing
- Cooking timers
- Ingredient quantities calculator
- Print-friendly recipe view
- Advanced filters (dietary restrictions, cuisine type)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

Tathya Dixit

**Project Link:** [https://github.com/Tathya-Dixit/recipe-share](https://github.com/Tathya-Dixit/recipe-share)  
**Live Demo:** [https://recipe-share-aoq6.onrender.com](https://recipe-share-aoq6.onrender.com)

---

**Note:** This is a portfolio project built to demonstrate full-stack Django development skills including user authentication, CRUD operations, file uploads, database relationships, and cloud deployment.

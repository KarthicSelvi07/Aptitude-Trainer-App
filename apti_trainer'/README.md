# AptitudeTrainerApp

🔹 Steps to Set Up a Cloned Django Project
1. Install Prerequisites
1.1 Install Python
Django requires Python 3.8+. Check if Python is installed:
python --version
If not installed, download it from the Python Official Website.
1.2 Install Virtual Environment (Recommended)
A virtual environment keeps project dependencies isolated.
✅ Create a virtual environment
python -m venv myenv
✅ Activate the virtual environment
•	Windows: 
•	myenv\Scripts\activate
________________________________________
2. Clone the Django Project
Instead of creating a new project, clone the existing repository from GitHub:
git clone <repository_url>
Replace <repository_url> with your actual GitHub repository link.
Navigate into the project folder:
cd project_name
________________________________________
3. Install Django
pip install django
django-admin –version
________________________________________
4. Set Up the Database
Run migrations to apply database changes:
python manage.py migrate
________________________________________
5. Run the Development Server
Start the Django development server:
python manage.py runserver
This will start the server at:
🔗 http://127.0.0.1:8000/
________________________________________
6. Create a Superuser (Admin Panel Access)
Run the following command to create a superuser:
python manage.py createsuperuser
Provide a username, email, and password when prompted.
Run the server again:
python manage.py runserver
Log in at http://127.0.0.1:8000/admin/ using the superuser credentials.
________________________________________
7. Sync with Repository (For Updates)
If new changes are pushed by team members, update your local copy:
git pull origin main
________________________________________



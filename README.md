# Furni - E-commerce Platform #

Furni is a full-featured e-commerce website built using Python Django (backend). It provides seamless shopping experiences, secure authentication, and user-friendly interfaces.

* User Authentication: Signup, login, logout, and role-based access.

* Product Management: View products by category and detailed product pages.

* Shopping Cart: Add, remove, and update cart items.

* Secure Payments: Supports UPI payments.

* User Profile: Update profile details and manage orders.

* Order Management: Track orders and view order history.

* Review & Ratings: Users can submit reviews and rate products.

## Installation & Setup ##

### Clone the repository: ###
 git clone https://github.com/your-username/furni.git
 
 cd furni

Project Setup:
 ## Create virtual environment ##
 python -m venv venv
 source venv/bin/activate  # On Windows: venv\Scripts\activate

 ## Install dependencies ##
 pip install -r requirements.txt

 ## Apply migrations ##
 python manage.py migrate

 ## Create a superuser (for admin access) ##
 python manage.py createsuperuser

 ## Run the development server ##
 python manage.py runserver


## Environment Variables ##

Create a .env file in the root directory and configure:
 SECRET_KEY=your_django_secret_key
 
 DEBUG=True
 
 ALLOWED_HOSTS=*
 
 DATABASE_URL=your_postgresql_database_url

 ## Usage ##

1. Run the backend server (python manage.py runserver).

2. Start the frontend (npm start in the frontend folder).

3. Open the browser and navigate to http://localhost:3000.

4. Register/login and explore the platform.

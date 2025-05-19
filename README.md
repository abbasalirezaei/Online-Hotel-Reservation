````markdown
# 🏨 Django-React Hotel Booking App

This is a full-stack hotel booking application built with **Django (REST Framework)** on the backend and **React** on the frontend. Users can browse available hotels and rooms, filter based on preferences, and make reservations. Admins can manage hotels, rooms, and bookings through a dedicated panel.

---

## 📦 Tech Stack

- **Backend**: Django, Django REST Framework  
- **Frontend**: React, Axios  
- **Database**: SQLite (default), but easily switchable to PostgreSQL  
- **Styling**: CSS / Tailwind (if applicable)  
- **Authentication**: JWT Auth  

---

## 🎯 Features

- 🔍 Browse list of hotels  
- 🏨 View hotel details  
- 📅 Make reservations  
- 🔐 Login / Signup functionality  
- 📂 **Admin panel** for:  
  - Adding, editing, and deleting hotels & rooms  
  - Managing bookings and availability  
  - Viewing user information  
- 🛏️ **Room & Services Tab**:  
  - Display different types of rooms with images, capacity, and descriptions  
  - Display list of available hotel services (Wi‑Fi, Breakfast, Parking, etc.)  
- 🎛️ **Room Filter**:  
  - Filter rooms dynamically by:  
    - **Category** (Deluxe, Suite, etc.)  
    - **Price Range**  
    - **Availability** (dates and capacity)  
- 🔗 RESTful API integration  
- 📱 Responsive UI (mobile‑friendly)  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/abbasalirezaei/Django-React-Booking-Hotel.git
cd Django-React-Booking-Hotel
````

### 2. Backend Setup

```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

---

### 🐳 Running the Project with Docker

If you prefer to run the project with Docker containers, follow these steps:

#### 1. Build and Start Containers

```bash
docker-compose up --build
```

This command will build the Docker images and start both the backend and frontend containers.

#### 2. Apply Migrations

In a new terminal, run the following to apply database migrations:

```bash
docker-compose exec backend python manage.py migrate
```

#### 3. Create a Superuser (Admin)

To access the Django admin panel, create a superuser:

```bash
docker-compose exec backend python manage.py createsuperuser
```

Follow the prompts to set the username, email, and password.

#### 4. Access the Application

* **Backend API / Django Server**: [http://localhost:8000](http://localhost:8000)
* **Django Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **React Frontend**: [http://localhost:3000](http://localhost:3000)

#### 5. Stop the Containers

To stop and remove all running containers:

```bash
docker-compose down
```

---

## 🛠️ Admin Panel

* Go to: `http://localhost:8000/admin/`

* Create superuser:

  ```bash
  python manage.py createsuperuser
  ```

* Use the panel to manage hotels, rooms, and bookings.

---

## 📁 Folder Structure

```bash
Django-React-Booking-Hotel/
│
├── backend/
│   ├── hotel/              # Django app for hotel logic
│   ├── users/              # User auth and profile management
│   ├── db.sqlite3          # Default DB (can change to PostgreSQL)
│   └── ...
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   └── ...
```

---

## ✅ To-Do / Improvements

* [ ] Add payment gateway integration
* [ ] Add user reviews and ratings
* [ ] Email notifications for bookings
* [ ] Add calendar-based booking UI

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](./LICENSE)

---

## 🌟 Star if you like it!

If you found this project helpful or inspiring, consider giving it a ⭐️ on GitHub!

```
```

# Replacement

**Replacement** is a web application designed for efficient decision-making regarding device repair or replacement based on economic parameters. 
                It replaces manual calculations and provides quick and accurate results. The application is available only to registered users.

## 🌟 Key Features

- 📋 **Device Overview** – Each brand contains a list of devices.
- 🔄 **CRUD Operations** – Ability to add, edit, and delete devices.
- 📊 **Automated Calculation** – Based on input parameters, the application determines whether a repair is worthwhile or if a replacement is necessary.
- 🎨 **Simple UI** – Clean HTML + CSS templates for easy navigation.

## 🛠 Technologies Used

- **Django** (Python, backend)
- **HTML, CSS** (frontend)
- **SQLite** (database for default configuration parameters)

## 🚀 Installation

1. Clone the repository:
   ```
   git clone https://github.com/user/replacement.git
   cd replacement
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```
6. Open the application in your browser at `http://127.0.0.1:8000/`.

## 📖 Usage

1. After getting user info, you can log in to access the application.
2. Select which brand in menu and select "replacement".
3. Enter the repair price offer, manufacturing date, and previous repair costs.
4. The application calculates and displays the result:
   - **Repair is worthwhile** ✅
   - **Requires individual assessment** ⚠️
   - **Replacement is necessary** ❌

## 🎯 Future Enhancements

- 📈 Export results to PDF/Excel.
- 🔔 Ticket system.
- 🌐 Deployment on a custom domain.

## 📞 Contact
For any questions or suggestions, feel free to contact me at terri.hrabalova@gmail.com. 😊


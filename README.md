CapitalCompass

CapitalCompass is a web-based personal finance management application designed to help users effectively manage their finances through comprehensive budgeting tools. The app offers two primary budgeting methods: Zero-Based Budgeting and the Fifty-Thirty-Twenty Rule, each catering to different financial management strategies. CapitalCompass also integrates with the Plaid API, allowing users to link their bank accounts for automatic transaction tracking and real-time financial insights.

Key Features

- User Authentication:** Secure user registration and login.
- Budget Management:** Create, edit, and delete budgets using Zero-Based or Fifty-Thirty-Twenty Budgeting methods.
- Expense Tracking:** Add, edit, and delete expenses within budgets, ensuring accurate financial tracking.
- Financial Analysis:** Visualize spending patterns and compare monthly financial data with interactive charts.
- Bank Integration:** Link bank accounts via Plaid API for automatic transaction imports and account balance updates.
- Responsive Design:** Optimized for larger screens such as tablets and laptops for a detailed view of financial data.

Live Demo

You can try CapitalCompass online at: https://capitalcompass.pythonanywhere.com

Getting Started

To run CapitalCompass locally, follow these steps:


1. Clone the Repository:**

   bash
   git clone https://github.com/yourusername/capitalcompass.git
   cd capitalcompass
   `


2. Install Dependencies:

   Install the required Python packages using `requirements.txt`.

   bash
   pip install -r requirements.txt
   
3. Get Plaid API Keys from Plaid Sandbox

    To integrate the Plaid API with CapitalCompass, you'll need to obtain your API keys from the Plaid sandbox environment. Visit the plaid Api website, sign up to a developer account and get your PLAID_CLIENT_ID and PLAID_SECRET.

4. Set Up Environment Variables:

   Create a `.env` file in the root directory to store sensitive information like API keys. The file should include the following:

   env
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   PLAID_CLIENT_ID=your_plaid_client_id
   PLAID_SECRET=your_plaid_secret
   PLAID_ENVIRONMENT=sandbox 
   

5. Apply Migrations:

   Apply database migrations to set up your SQLite database.

   ```bash
   python manage.py migrate
   ```

6. Create a Superuser (Optional):

   If you want to access the Django admin panel, create a superuser.

   bash
   python manage.py createsuperuser
   

7. Run the Development Server:

   Start the Django development server.

   bash
   python manage.py runserver
   

8. Access the Application:

   Open your browser and go to `http://127.0.0.1:8000` to start using CapitalCompass locally.

Running Tests

To ensure everything is working correctly, you can run the automated tests:

python manage.py test

Deployment

For deploying CapitalCompass on a production server, ensure you:

- Set `DEBUG=False` in your environment variables.
- Use a production-grade database like PostgreSQL or MySQL.
- Set up a web server (like Gunicorn) and reverse proxy (like Nginx).
- Secure your environment with SSL/TLS.


## Acknowledgments

- Django: For providing a robust framework that simplifies web development.
- Plaid: For offering secure financial data APIs.
- Chart.js: For data visualization components.

For a live demo, visit https://capitalcompass.pythonanywhere.com. Thank you for using CapitalCompass!
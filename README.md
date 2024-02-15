# FinTracker Web Application

FinTracker is a web application designed to help users track their expenses and incomes conveniently. It offers functionalities to add, edit, and delete both expenses and incomes. Additionally, FinTracker provides visualizations of expenses and incomes through integration with Highcharts, using bar charts for expenses and pie charts for incomes.

## Features

- **Expense Management**: Users can add, edit, and delete expenses easily through the intuitive interface.
- **Income Management**: Similarly, users can manage their incomes by adding, editing, and deleting them as needed.
- **Highcharts Integration**: FinTracker utilizes Highcharts to provide visual representations of expenses and incomes, enhancing data comprehension.
- **Authentication and Authorization**: The application implements manual login, authentication, and registration processes to ensure secure access to user accounts.
- **Email Notifications**: FinTracker sends account activation emails and reset password emails to users, enhancing account security and usability.

## Technology Stack

- **Backend**: Developed using Python with the Django framework, ensuring robustness and scalability.
- **Frontend**: Utilizes HTML, CSS, and JavaScript for the user interface, providing a responsive and engaging experience.
- **Database**: Stores data using a relational database management system (PostgreSQL) for efficient data management.
- **Chart Visualization**: Integrates with Highcharts for dynamic and interactive visualization of expenses and incomes.

## Usage

To use FinTracker, follow these steps:

1. **Clone the Repository**: Clone the FinTracker repository to your local machine.
2. **Install Dependencies**: Install the necessary dependencies using `pip install -r requirements.txt`.
3. **Database Setup**: Set up the database according to the provided configuration in `settings.py`.
4. **Database Setup**: Configure your .env file 
5. **Run the Server**: Start the Django development server using `python manage.py runserver`.
6. **Access the Application**: Navigate to the provided URL in your web browser to access FinTracker.

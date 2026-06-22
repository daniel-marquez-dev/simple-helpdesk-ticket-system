# Simple Helpdesk Ticket System

Welcome to the **Simple Helpdesk Ticket System**! This is a web application designed to simplify the management, tracking, and resolution of technical support requests (tickets) within a corporate or customer service environment. The system centralizes communication, assigns priorities, and optimizes the support team's workflow.

---

## 🚀 Key Features

- **Ticket Management:** Create, edit, filter, and track support requests seamlessly.
- **Status Workflow:** Clear transitions from ticket opening (`Open`), to work in progress (`In Progress`), to final resolution (`Resolved` / `Closed`).
- **Priority Control:** Categorize tickets by urgency levels (Low, Medium, High, Critical).
- **Dashboard:** Quick visual metrics on current support status and overall workload.
- **Roles & Permissions:** Distinction between requesting users (customers/employees) and support agents handling the tasks.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript, React.js
- **Backend:** Node.js, Express.js
- **Database:** PostgreSQL / MySQL
- **Authentication:** JSON Web Tokens (JWT)

---

## 📦 Installation and Setup

Follow these steps to set up the local development environment:

### 1. Clone the repository
```bash
git clone [https://github.com/daniel-marquez-dev/simple-helpdesk-ticket-system.git](https://github.com/daniel-marquez-dev/simple-helpdesk-ticket-system.git)
cd simple-helpdesk-ticket-system
```

### 2. Configure Environment Variables
Create a .env file in the root directory following the .env.example structure, and define your credentials:
```
PORT=3000
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=helpdesk_db
JWT_SECRET=your_secret_key
```

### 3. Install Dependencies
Run the following command to install all the required packages:

```Bash
npm install
```

### 4. Run Migrations / Initialize Database
Set up your database tables by running the migration scripts:

```Bash
npm run migrate
```

### 5. Start the Application
To launch the server in development mode:
```npm run dev```

Open your browser and navigate to http://localhost:8000/register

### 💡 System Usage
Sign Up & Log In: Create an account as a regular user to report issues or log in with agent credentials to manage them.

Create a Ticket: Click on "New Ticket", fill in the title, description, category, and priority level.

Assignment & Resolution: Agents can pick up the ticket, change its status to "In Progress", add comments/technical notes, and finally mark it as "Resolved".

### 🛣️ Roadmap / Future Enhancements
Implement email notifications upon ticket status changes.

Support attachments (images or logs) inside tickets.

Weekly PDF report generation for analytics.

Two-factor authentication (2FA) for admin and agent accounts.

### 🤝 Contributing
Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project.

Create your Feature Branch (git checkout -b feature/AmazingFeature).

Commit your Changes (git commit -m 'Add some AmazingFeature').

Push to the Branch (git push origin feature/AmazingFeature).

Open a Pull Request.

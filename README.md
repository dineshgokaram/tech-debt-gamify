# Tech-Debt Gamify: A Gamified Technical Debt Management Platform

#Dashboard Screenshots 
<img width="1410" height="580" alt="Screenshot 2025-07-25 195058" src="https://github.com/user-attachments/assets/c9b96790-7b2a-4671-955a-819e0ce01a4b" />
<img width="1251" height="588" alt="Screenshot 2025-07-26 204034" src="https://github.com/user-attachments/assets/722ec1b2-3d86-4e6c-855c-1bcd784de24b" />

Technical debt is a constant challenge in software development, often lacking the visibility and motivation for teams to address it. **Tech-Debt Gamify** is a full-stack, containerized web application that tackles this problem head-on. It analyzes Python code from public Git repositories for code quality issues and transforms the cleanup process into an engaging and competitive game for developers, complete with points, achievement badges, and a live leaderboard.

This project was built from the ground up to demonstrate a wide range of modern software development skills, from backend API design and database management to frontend interactivity, data analysis, and real-world DevOps problem-solving.

## ✨ Key Features

*   **Secure User Authentication:** Full user registration and login system using password hashing (`bcrypt`) and **JWT (JSON Web Tokens)** for securing API endpoints.
*   **Dynamic Git Repository Analysis:** Analyzes any public Python repository on-the-fly using industry-standard tools like **Pylint** and **Flake8**.
*   **Core Gamification Engine:**
    *   Developers can "resolve" identified code issues via an API call.
    *   A flexible points system rewards developers based on the type of issue fixed.
    *   An achievement system awards persistent **badges** for hitting key milestones (e.g., "First Fix," "Bug Squasher").
*   **Live Leaderboard:** A real-time leaderboard ranks all users by their total accumulated points, fostering friendly competition.
*   **Interactive Frontend:** A clean, responsive single-page application built with vanilla **HTML, CSS, and JavaScript** that allows users to log in and view their dashboard.
*   **Data Reporting API:** A powerful data aggregation endpoint built with the **pandas** library, providing a historical summary of a project's health, ready for business intelligence tools.

## 🛠️ Tech Stack & Architecture

This project is built as a multi-container application orchestrated by **Docker Compose**, ensuring a consistent and reproducible environment.

| Category      | Technology                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| :------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend**   | ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)                                                                                                                                                                                                                                                  |
| **Database**  | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-DB4437?style=for-the-badge&logo=sqlalchemy&logoColor=white)                                                                                                                                                                                                                               |
| **Data Analysis** | ![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=for-the-badge&logo=pandas&logoColor=white)                                                                                                                                                                                                                                                                                                                                                             |
| **Frontend**  | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)                                                                                                                                                    |
| **DevOps**    | ![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)                                                                                                                                                        |

The architecture consists of two main services:
1.  **`api`**: A Docker container running the **FastAPI** backend, which handles all business logic, user authentication, and serves the static frontend.
2.  **`db`**: A Docker container running a **PostgreSQL** database for persistent data storage.

## 🚀 Getting Started

This project is fully containerized, making it incredibly simple to run on any machine with Docker Desktop installed.

**Prerequisites:**
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Instructions:**

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/tech-debt-gamify.git
    cd tech-debt-gamify
    ```

2.  **Run the application:**
    ```sh
    docker compose up --build
    ```
    The `--build` flag is only needed the first time to build the Docker images. For subsequent launches, you can simply use `docker compose up`.

3.  **Access the application:**
    *   The web interface is available at: **`http://127.0.0.1:8000/`**
    *   The interactive API documentation (Swagger UI) is at: **`http://127.0.0.1:8000/docs`**

The application will start, create the database tables, and seed the initial badge data automatically. You can then register a new user from the API docs and start analyzing projects!

## 💡 Key Learnings & Challenges Overcome

Building this project was a comprehensive journey through the entire lifecycle of a modern web application. Key takeaways include:

*   **Full-Stack Integration:** Designing a secure REST API contract and connecting it to a dynamic, client-side JavaScript frontend that consumes it.
*   **Advanced Docker & DevOps:** This project was a deep dive into real-world DevOps challenges. I learned to:
    *   Solve service startup **race conditions** between the API and database using Docker `healthcheck`s.
    *   Manage persistent data with Docker volumes and resolve **stale data conflicts** after schema changes.
    *   Debug container-specific dependency issues (e.g., installing `git` into a minimal Python image).
*   **Robust API & Database Design:** I designed a relational database schema with multiple one-to-many relationships and used SQLAlchemy to interact with it, learning to solve ORM-specific challenges like lazy vs. eager loading (`selectinload`).
*   **Real-World Debugging:** A significant portion of this project involved diagnosing and fixing complex bugs. A critical challenge was resolving a **circular import** error, which required a significant but necessary refactoring of the application's structure to enforce single-direction dependencies.

## 📈 Future Improvements

*   **Enhanced Frontend:**
    *   Integrate a modern framework like **React** to create a more dynamic user experience.
    *   Build a UI for analyzing new projects and resolving issues directly from the dashboard.
*   **CI/CD Pipeline:** Implement GitHub Actions to automatically run tests and linting on every push.
*   **More Analysis Tools:** Integrate other static analysis tools like `radon` (for complexity metrics) into the scoring system.

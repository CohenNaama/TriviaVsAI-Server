# Trivia VS AI: AI Trivia Master

## Current Development Status

**Note:** This application is currently in the early stages of development. As such, some functionalities and features are still under construction and may not be fully operational at this time. We are actively working to enhance and expand the application's capabilities, and we appreciate your understanding and patience as we continue to make improvements.

## Description

Trivia VS AI is an innovative trivia game powered by artificial intelligence, offering a dynamic and adaptive gameplay experience. Compete against AI, challenge your knowledge, and climb the leaderboards!

## Game Overview

**AI Trivia Master** is designed to provide a personalized trivia experience by generating questions in real-time, adapting to player knowledge levels, and offering detailed feedback.

### Key Features

- **Dynamic Question Generation:**
  - Leverage OpenAI to generate a diverse range of trivia questions across multiple categories.
  - Ensure questions are unique and continuously updated to keep the game fresh.

- **Real-Time Feedback:**
  - Use Claude to provide immediate feedback on answers, explaining both correct and incorrect responses.
  - Implement sentiment analysis to adjust difficulty and question types based on player engagement.

- **Adaptive Difficulty:**
  - Gemini technology adjusts question difficulty dynamically based on player performance and knowledge level.
  - Offer personalized question sets to maintain challenge and engagement.

- **Leaderboards and Social Features:**
  - Track player scores and display them on global leaderboards.
  - Enable social sharing and multiplayer modes for a competitive edge.

### Integration and Deployment

- **Backend:** Built with Flask to manage game state, player data, and a robust question database.
- **Deployment:** Dockerized for scalability and reliability, ensuring smooth performance under load.
- **User Interface:** Designed to be simple and engaging, providing a seamless gameplay experience.

## Technology Stack

- **Backend:** Python, Flask, SQLAlchemy, PostgreSQL
- **AI Integration:** OpenAI, Claude, Gemini
- **Frontend:** HTML, CSS, JavaScript (with plans to develop in React)
- **Authentication:** JWT (JSON Web Tokens)
- **Deployment:** Docker, Docker Compose
- **CI/CD Pipeline:** Planned for seamless integration and deployment

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Docker and Docker Compose

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/trivia-vs-ai.git
   cd trivia-vs-ai

2. **Set up a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies:**
```
pip install -r requirements.txt

```

4. **Configure the environment variables:**

   Create a .env file in the root directory and add the following:
```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost/dbname
```

5. **Initialize the database:**
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Run the application:**
```
flask run
```

   Access the application at http://127.0.0.1:5000.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

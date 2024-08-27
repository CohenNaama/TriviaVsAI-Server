# Trivia VS AI

## Table of Contents
- [Current Development Status](#current-development-status)
- [Description](#description)
- [Game Overview](#game-overview)
  - [Key Features](#key-features)
  - [Integration and Deployment](#integration-and-deployment)
- [AI Integration](#ai-integration)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [File Upload Limits](#file-upload-limits)
- [License](#license)

## Current Development Status

**Note:** This application is currently in the development stages, with several functionalities now fully operational, including AI-generated feedback and player level management. We are continuously working to enhance and expand the application's capabilities.

## Description

Trivia VS AI is an innovative trivia game powered by artificial intelligence, offering a dynamic and adaptive gameplay experience. Compete against AI, challenge your knowledge, and climb the leaderboards!

## Game Overview

**Trivia VS AI** is designed to provide a personalized trivia experience by generating questions in real-time, adapting to player knowledge levels, and offering detailed feedback.

### Key Features

- **Dynamic Question Generation:**
  - Leverage OpenAI to generate a diverse range of trivia questions across multiple categories.
  - Ensure questions are unique and continuously updated to keep the game fresh.

- **Real-Time AI Feedback:**
  - **Claude AI** generates immediate, personalized feedback on answers, explaining both correct and incorrect responses.
  - Feedback adapts dynamically to player performance, considering correct/incorrect answers and past performance in specific categories.

- **Adaptive Difficulty and Player Progression:**
  - **Gemini's technology** adjusts question difficulty dynamically based on player performance and knowledge level.
  - Player experience points and levels are tracked and updated, providing a personalized difficulty curve and rewarding progress.

- **Leaderboards and Social Features:**
  - Track player scores and display them on global leaderboards.
  - Enable social sharing and multiplayer modes for a competitive edge.
  
### Integration and Deployment

- **Backend:** Built with Flask to manage game state, player data, and a robust question database.
- **Deployment:** Dockerized for scalability and reliability, ensuring smooth performance under load.
- **User Interface:** Designed to be simple and engaging, providing a seamless gameplay experience.

### AI Integration

- **OpenAI**: Used to dynamically generate trivia questions. By leveraging GPT-3.5-turbo, the game provides an endless variety of unique and engaging questions that cover a broad range of topics, keeping the gameplay fresh and challenging.
  
- **Claude AI**: Integrated to deliver real-time, adaptive feedback based on player responses. Claude's insights help players learn from their mistakes, receive encouragement, and better understand the trivia content, creating a more engaging and educational experience.

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
   git clone https://github.com/CohenNaama/TriviaVsAI-Server.git
   cd TriviaVsAI-Server

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

To run the application, you need to configure some environment variables. Create a `.env` file in the root directory of your project and add the following:
```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost/triviadb
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_claude_api_key

POSTGRES_PASSWORD=your_postgres_password
PGADMIN_DEFAULT_EMAIL=your_pgadmin_email
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
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

### File Upload Limits

The application has a file upload limit set to 2MB. Ensure any files you upload comply with this restriction to avoid errors.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Tatami-Stop

![Icon](/doc/icon.svg)


>Tatami-Stop is an API for hostels providing essential functionalities like user management, room booking, and ordering room services.

## Features

- **User Management**: Create, read, update, and delete users.
- **Room Booking**: Book rooms and manage reservations.
- **Room Services**: Order various services to be delivered to rooms.

## Getting Started

These instructions will help you set up and run the Tatami-Stop API on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

## Technologies Used

- **FastAPI**: FastAPI is used as the web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: SQLAlchemy is utilized as the ORM (Object-Relational Mapping) tool to interact with the SQLite database.
- **SQLite**: SQLite is employed as the relational database management system for storing application data.
- **Ruff**: Ruff is used as a linter and formatter for maintaining code quality and style consistency.
- **Just**: Just is used as a task runner for automating common development tasks and workflows.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/OlegBW/tatami-stop.git
    cd tatami-stop
    ```

2. Build and start the Docker containers:
    ```bash
    docker-compose up -d
    ```

3. The API will be available at `http://localhost:5500`.

### Usage

The available endpoints and their descriptions can be accessed via the Swagger UI documentation at `http://localhost:5500/docs`.

- **Swagger UI**: `http://localhost:5500/docs`

### Environment Variables

The following environment variables can be set to configure the application:

- `SECRET_KEY`: Secret key for JWT authentication.
- `ALGORITHM`: Algorithm used for JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for access tokens in minutes.

### Contributing

We welcome contributions to improve Tatami-Stop. Please fork the repository and submit a pull request.

### License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Inspired by the need for efficient hostel management systems.


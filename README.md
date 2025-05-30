# PyVPNManager

A Python-based VPN management system with a Telegram bot for user requests, a FastAPI web service for admin control, and planned XTLS integration, all containerized with Docker Compose.

## Features
- Telegram bot for submitting VPN connection requests
- FastAPI admin panel for approving/rejecting requests
- Future support for XTLS service
- Dockerized for easy deployment and scalability

## Requirements
- Docker and Docker Compose
- Telegram bot token
- Python 3.8+ (handled via Docker)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Configure environment variables (e.g., bot token, admin credentials) in `.env` file.
3. Build and start services:
   ```bash
   docker-compose up --build
   ```
4. Start services (after initial build):
   ```bash
   docker-compose start
   ```

## Usage
- Users: Submit VPN connection requests via the Telegram bot.
- Admins: Access the FastAPI web interface to approve/reject requests.
- Monitor logs for service status and errors.

## Notes
- Project in active development; XTLS integration pending.
- Ensure `.env` is properly configured before starting.
- Refer to [FastAPI documentation](https://fastapi.tiangolo.com/) and [Docker Compose documentation](https://docs.docker.com/compose/) for setup details.

*Developed by a skilled Python developer building secure, user-friendly VPN management solutions.*

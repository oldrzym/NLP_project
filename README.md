

# Data Obfuscation System

This repository contains the code for a data obfuscation system designed to mask sensitive information (e.g., names, addresses, dates) in real-time chat applications. The system leverages **Pullenti** and **Natasha** for Named Entity Recognition (NER) alongside custom regular expressions and lemmatization-based masking for maximum accuracy.

## Features

- **Pullenti**: Used for recognizing personal names and addresses.
- **Natasha**: Handles broader named entity recognition (e.g., organizations, dates).
- **Custom Regex and Lemmatization**: Additional layer to mask account numbers, emails, and other sensitive entities.
- **Accuracy**: Achieves 97% obfuscation accuracy on the provided dataset.
  
## Project Structure

```
.
├── app/                 # Core application code
├── logs/                # Log files for debugging and monitoring
├── pullenti/            # Pullenti NER library for names and addresses
├── .dockerignore        # Files and directories to ignore in Docker context
├── .gitlab-ci.yml       # CI/CD pipeline configuration
├── Dockerfile           # Dockerfile to build the service
├── README.md            # Project description and instructions
├── REGEXES.ipynb        # Jupyter notebook with regex pattern experiments
├── ammo.txt             # Sample input text file for testing
├── build.sh             # Script for building the Docker container
├── load.yaml            # Configuration for loading data
├── main.py              # Main entry point of the application
├── post_data.txt        # Sample data for testing HTTP POST requests
├── requirements.txt     # Python dependencies for the project
├── tank_errors.log      # Log of errors during load testing
├── test_text.txt        # Sample text for testing obfuscation
```

## Setup

### Prerequisites

Make sure you have Docker installed on your machine. You can download Docker [here](https://www.docker.com/get-started).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/oldrzym/NLP_project.git
   cd NLP_project
   ```

2. Build the Docker image:
   ```bash
   docker build -t data-obfuscation-system .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 data-obfuscation-system
   ```

This will start the application on port 8000. You can now send requests to the service.

### API Usage

The system exposes a REST API for submitting text and receiving the obfuscated version.

- **POST** `/mask`:
  - **Input**: JSON payload with the field `text`, containing the message to be masked.
  - **Output**: The obfuscated text and a dictionary of masks.

Example request:
```bash
curl -X POST "http://localhost:8000/mask" -H "Content-Type: application/json" -d '{"text": "John Doe lives at 123 Main St."}'
```

### Performance

The system has been tested on a server with the following specifications:
- CPU: Intel i5-10400 (6 cores, 12 threads)
- RAM: 32GB DDR4
- GPU: NVIDIA RTX A4000

It can handle up to 10 concurrent requests with an average response time of 364 ms.

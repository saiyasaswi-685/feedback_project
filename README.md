
---

# Customer Feedback Sentiment Analysis System

## Overview

This project implements a scalable, event-driven microservice architecture designed to ingest customer feedback in real-time and process it asynchronously. By leveraging **Apache Kafka** as a message broker, the system decouples feedback ingestion from intensive processing tasks like sentiment analysis, ensuring high responsiveness and system resilience.

## Key Features

* **Asynchronous Processing**: Feedback is ingested via a REST API and offloaded to Kafka to prevent blocking calls.
* **Real-time Sentiment Analysis**: A dedicated worker service utilizes NLTK's VADER to categorize feedback as positive, negative, or neutral.
* **Persistent Storage**: Analyzed data is stored in a MySQL database with optimized schemas for retrieval.
* **Idempotency**: The worker service is designed to handle duplicate messages gracefully, preventing data duplication in the database.
* **Containerized Infrastructure**: Fully orchestrated using Docker Compose for consistent deployment.

---

## Tech Stack

* **Language**: Python 3.9
* **Framework**: Flask (API)
* **Message Broker**: Apache Kafka & Zookeeper
* **Database**: MySQL 8.0
* **Analysis Library**: NLTK (VADER Lexicon)
* **Orchestration**: Docker & Docker Compose

---

## Project Structure

```text
feedback_project/
├── api/                # Flask REST API service
├── worker/             # Kafka consumer & sentiment analyzer
├── db/                 # Database initialization scripts
├── docker-compose.yml  # Service orchestration
├── .env.example        # Environment variable template
└── README.md           # Documentation

```

---

## Setup & Installation

### Prerequisites

* Docker and Docker Compose installed.
* Postman or `curl` for API testing.

### Steps

1. **Clone the repository**:
```bash
git clone https://github.com/saiyasaswi-685/feedback_project
cd feedback_project

```


2. **Environment Configuration**:
Create a `.env` file based on `.env.example`.
3. **Launch the System**:
```bash
docker-compose up --build

```


Wait for the health checks to pass. The API will be available at `http://localhost:5000`.

---

## API Documentation

### 1. Submit Feedback

**Endpoint**: `POST /feedback`

**Description**: Accepts customer feedback and publishes an event to Kafka.

**Request Body**:

```json
{
  "customer_id": "C123",
  "feedback_text": "The service was excellent!",
  "timestamp": "2026-02-18T22:00:00Z"
}

```

**Response** (`202 Accepted`):

```json
{
  "id": "faef40e7-d35e-4f99-a189-493a1e152590",
  "message": "Success"
}

```

### 2. Retrieve All Feedback

**Endpoint**: `GET /feedback`

**Query Params**: `sentiment` (optional - positive|negative|neutral).

### 3. Retrieve by ID

**Endpoint**: `GET /feedback/<message_id>`

---

## Design Decisions

* **Why Kafka?**: Kafka provides a high-throughput, fault-tolerant backbone that allows the system to handle spikes in feedback volume without crashing the database.
* **Idempotency Logic**: Implemented `INSERT IGNORE` (or existence checks) in the worker service to ensure that even if a message is delivered twice by Kafka, the database remains consistent.
* **Health Checks**: Custom Docker health checks ensure that the API and Worker only start processing once Kafka and MySQL are fully operational.

---

## Testing

To run the automated tests:

```bash
# Execute within the specific service container
docker-compose exec api pytest

```

---


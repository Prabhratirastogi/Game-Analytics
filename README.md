# Game Analytics Web Service

## Overview

This project is a web service designed for a game analytics company where data analysts can upload CSV files and run various analyses on the data. The service supports filtering, aggregation, and basic authentication to secure API access. The solution is containerized using Docker and deployed on a free tier of a cloud provider.

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [API Endpoints](#api-endpoints)
4. [Setup and Deployment](#setup-and-deployment)
5. [Cost Estimate](#cost-estimate)
6. [License](#license)

## Project Description

The Game Analytics Web Service allows users to upload CSV files containing game data, query the data with various filters, and perform aggregations. It includes simple UI for data querying, supports string and date-based filters, and provides basic authentication for accessing the API.

## Features

- **CSV File Upload**: Endpoint to upload a CSV file containing game data.
- **Data Analysis**: Filter and query data based on various criteria.
- **Aggregations**: Perform max, min, and mean calculations on numerical columns.
- **String and Date Filters**: Support for substring matching in string fields and exact match or range queries for date fields.
- **Basic Authentication**: Simple user registration and login functionality.
- **Cost-Effective Deployment**: Deployed on a free-tier cloud provider to minimize costs.

## API Endpoints

### 1. Upload CSV Data

**Endpoint**: `POST /upload-csv/`  
**Description**: Upload a CSV file for processing. The CSV file should be accessible via a public link.

**Request**:

POST /upload-csv/

Request_Body:
{
    "csv_url": "http://localhost:8000/upload-csv/"
}

Response:
{
    "message": "CSV file processed successfully."
}

### 2. Register User

**Endpoint**: `POST /auth/register/`
**Description**: Register a new user for authentication.

**Request**:
POST /auth/register/

Request-Body:
{
    "username": "user",
    "email": "user email",
    "password": "password"
}

Response:
{
    "message": "User registered successfully."
}

### 3. Login User

**Endpoint**: `POST /auth/login/`
**Description**: Login a user to receive authentication tokens.

**Request**:
POST /auth/login/

Request_Body:
{
    "username": "user",
    "password": "password"
}

Response:
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}

### 4. Refresh Token

**Endpoint**: `POST /auth/token/refresh/`
**Description**: Refresh the authentication token.

**Request**:
POST /auth/token/refresh/

Request_Body:
{
    "refresh": "your_refresh_token"
}

Response:
{
    "access": "new_access_token"
}

### 5. Logout User
**Endpoint**: 'POST /auth/logout/'
**Description**: Logout a user by invalidating the current token.

**Request**:
POST /auth/logout/

Request_Body:
{
    "refresh": "your_refresh_token"
}

Response:
{
    "message": "Logged out successfully."
}

### 6. Query Data
**Endpoint**: 'GET /query_data/'
Example: /query_data/?name=TD
**Description**: Get records where the name field contains the substring "TD".

### 7. Get Max of Given Date

**Endpoint**: 'GET /query_data/'
Example: /query_data/?date_gt=2021-01-01
**Description**: Get records with date greater than the specified date.

### 7. Get Age by Value

**Endpoint**: 'GET /query_data/'
Example: /query_data/?required_age=17
**Description**: Get records where age is greater than or equal to 17.

### 8. Get Maximum Price

**Endpoint**: 'GET /query_data/'
Example: /query_data/?aggregate_max_price=true
**Description**: Get the maximum price from the price field.

### 9. Get Minimum Price

**Endpoint**: 'GET /query_data/'
Example: /query_data/?aggregate_min_price=true
**Description**: Get the minimum price from the price field.

### 10. Get Mean of Price

**Endpoint**: `GET /query_data/`
Example: /query_data/?aggregate_mean_price=true
**Description**: Get the mean price from the price field.

### 11. Filter by Release Date

**Endpoint**: `GET /query_data/`
Example: /query_data/?release_date=2021-09-07
**Description**: Get records with a specific release_date.

### 12. Filter by Release Price

**Endpoint**: `GET /query_data/`
Example: /query_data/?price=13.99
**Description**: Get records with a specific price.

### Setup and Deployment
Prerequisites
Docker
Docker Compose
Local Development
Clone the Repository


## git clone https://github.com/your-username/game-analytics-web-service.git

### Build the Docker Image
docker-compose build
Start the Services

docker-compose up
Access the Application

Open http://localhost:8000 in your browser.

### Deployment
Create a Docker Image

The Dockerfile and docker-compose.yml files are already configured for deployment.

docker-compose build
Deploy to a Free Cloud Tier

Choose a cloud provider with a free tier (e.g., Heroku, Railway, Vercel). Follow the cloud provider’s instructions for deploying Docker images.

### Deploy the Image
Push the Docker image to a container registry if required by your cloud provider. For example, with Docker Hub:

Set Up Environment Variables
Configure environment variables on the cloud provider’s dashboard to match the .env file settings.

Cost Estimate
Service	                                  Free Tier Limit	                                 Cost per Month (if exceeded)
Cloud Provider	                          Free Tier Plan	                                 Costs vary depending on usage
Database (SQLite)                       Included in free tier	                                      None
Database (ClickHouse)             Check free tier limits for your provider	                 Varies depending on resource usage
Compute Resources	              Free Tier Plan (e.g., 1 vCPU, 1GB RAM)	                     Varies based on usage


Estimated Cost Calculation:

Assumptions:
.. One CSV Upload per day.
.. 100 Queries per day.

Cost Estimate:
.. Cloud Storage: Free tier usually covers small amounts of storage.
.. Compute Resources: Check the free tier limits for the specific cloud provider.

Note: Ensure you stay within the free tier limits to avoid charges.

License
This project is licensed under the MIT License - see the LICENSE file for details.


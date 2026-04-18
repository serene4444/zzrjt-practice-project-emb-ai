# Sentiment Analyzer Web App

Fast, browser-based sentiment analysis with resilient fallback logic so users get useful results even when the upstream AI endpoint is slow or unavailable.

## Live Project Page

## Overview

This project solves a common product issue: sentiment features that feel unreliable because they depend on a single external API call.

The application is built for:
- Developers learning API-backed ML integrations
- Teams prototyping text intelligence features in web products
- Recruiters and reviewers evaluating backend reliability decisions

Why this approach is effective:
- It combines a remote model call with local fallback classification
- It handles blank input and network/API failures explicitly
- It keeps response time low using caching and connection reuse

## Key Features

- Web interface for entering free-text statements and viewing sentiment output
- Flask backend endpoint for analysis requests
- Remote-first inference using the hosted Watson sentiment model
- Rule-based fallback when the remote service is unavailable
- Fast repeated requests via in-memory memoization cache
- Cooldown window after remote failures to avoid repeated slow retries
- Dedicated blank-input message instead of generic invalid-text handling

## Tech Stack

### Frontend
- HTML
- Bootstrap 4 (CDN)
- Vanilla JavaScript (XMLHttpRequest)

### Backend
- Python 3
- Flask
- Requests

### Quality and Tooling
- Pylint for static analysis
- Python bytecode compile checks (py_compile)

## Architecture / How It Works

Request flow:
1. User enters text in the UI and clicks Run Sentiment Analysis.
2. Frontend sends a GET request to /sentimentAnalyzer with URL-encoded input.
3. Flask route validates input and handles blank text early.
4. sentiment_analyzer attempts remote inference first.
5. If remote call fails, times out, or returns unusable data, fallback logic returns a local sentiment estimate.
6. Backend returns a formatted response string for rendering in the UI.

Important design decisions:
- Remote-first + local fallback: keeps quality high while preserving availability.
- Request session reuse: reduces connection overhead for repeated API calls.
- Cooldown after failure: avoids repeatedly blocking on known-bad remote state.
- LRU cache: makes repeated user queries effectively instant.

## Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### Steps
1. Clone the repository.
2. Open a terminal in the project root.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Flask app:

```bash
python server.py
```

5. Open in browser:
- http://127.0.0.1:5000

## Usage

### Web Workflow
1. Open the app in your browser.
2. Enter a sentence in the input field.
3. Click Run Sentiment Analysis.
4. Read the returned label and confidence score.

### Example endpoint calls

```bash
curl "http://127.0.0.1:5000/sentimentAnalyzer?textToAnalyze=I%20love%20this%20new%20technology."
curl "http://127.0.0.1:5000/sentimentAnalyzer?textToAnalyze="
```

Expected behavior:
- Non-empty text returns sentiment output.
- Blank text returns a specific prompt to enter text.

## Static Code Analysis (Pylint)

Run static analysis on the sentiment module:

```bash
python -m pylint SentimentAnalysis/sentiment_analysis.py
```

To target a 10/10 score:
- Keep module and function docstrings complete and concise.
- Avoid unused imports and dead code.
- Keep naming and formatting consistent.
- Keep helper functions focused and testable.

## Challenges & Solutions

### 1. Slow response times from upstream service
Problem:
- Remote API calls could delay user responses, especially during service instability.

Solution:
- Added short remote timeouts, persistent HTTP session reuse, failure cooldown, and caching.

### 2. API dependency affecting reliability
Problem:
- A single external failure could degrade the user experience.

Solution:
- Implemented local keyword-based fallback sentiment logic to preserve response continuity.

### 3. Input handling edge cases
Problem:
- Blank input was previously treated like generic invalid text.

Solution:
- Added explicit blank-input handling in the route with a dedicated message.

## Future Improvements

- Replace rule-based fallback with a lightweight local ML model for better multilingual coverage.
- Add structured JSON API responses and keep formatting in the frontend.
- Introduce automated tests for edge cases and route behavior.
- Add production deployment config (WSGI server, env-based settings, observability).

## Screenshots / Demo

Add visuals here:
- UI screenshot of input and response panel
- Short GIF showing request flow and response updates
- Optional architecture diagram for backend logic

Suggested placement:
- docs/images/ui-home.png
- docs/images/ui-result.png
- docs/demo/sentiment-flow.gif

## Why This Project Stands Out

This project goes beyond a basic API wrapper by showing practical backend engineering decisions:
- Reliability under external dependency failures
- Performance tuning with measurable latency improvements
- Clear handling of user input edge cases

It reflects production-minded thinking while staying lightweight and readable.

## Author

Serene Plummer 
Software Engineering Student focused on AI and backend systems.

# Sentiment Analysis Full-stack Django Application

This project is a full-stack Django web application that allows users to upload customer reviews in CSV or XLSX format (for testing the web app please download the sample data file (i.e., `customer_reviews.xlsx`) from root directory of this repository) and performs sentiment analysis using an LLM via Groq API. The application processes the file, sends the reviews to the Groq API for sentiment analysis, and then displays the results (positive, negative, neutral) in a user-friendly format on the web.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Project Locally](#running-the-project-locally)
- [Usage](#usage)
- [Deploying on Render](#deploying-on-render)
- [Contributing](#contributing)
- [License](#license)

## Features

- **File Upload**: Users can upload `.csv` or `.xlsx` files containing customer reviews.
- **Sentiment Analysis**: The application uses Groq API for sentiment analysis, which returns a JSON response with sentiment scores.
- **Results Display**: Results are displayed on the web page in a clean, tabular format showing positive, negative, and neutral sentiment scores.
- **Error Handling**: The app handles errors such as invalid file formats, missing review columns, and issues with the sentiment analysis API.

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS (Basic styling)
- **API Integration**: Groq API for sentiment analysis
- **File Handling**: `pandas` for reading CSV and XLSX files
- **Environment Management**: `dotenv` for managing API keys securely

## Project Structure

```
project/
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── sentiment_analysis/
│   ├── __init__.py
│   ├── views.py         # Handles the sentiment analysis and file processing
│   ├── templates/       # Contains HTML templates
│   │   ├── analyze.html # Upload page template
│   │   ├── result.html  # Results page template
├── manage.py
├── .env                 # Contains the GROQ API key
├── .gitignore
├── Procfile               
├── README.md
└── requirements.txt
```

## Installation

### Prerequisites

- Python 3.10+
- Git

### Clone the Repository

```bash
git clone https://github.com/kumarshivesh/product-reviews-sentiment-analysis.git
cd project
```

### Create and Activate a Virtual Environment

```
python -m venv .venv
source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`
```

### Install Dependencies

```
pip install -r requirements.txt
```

## Environment Variables

Create a .env file in the root directory of the project and add the following variable(s):

```
GROQ_API_KEY=your_groq_api_key_here
```

## Running the Project Locally

#### 1. Apply database migrations:

```
python manage.py migrate
```

#### 2. Start the development server:
```
python manage.py runserver
```

#### 3. Open your web browser and go to 

http://127.0.0.1:8000/

## Usage

### 1. Upload a CSV or XLSX File:

Go to http://127.0.0.1:8000/ in your browser.
Click on the "Choose File" button and select a .csv or .xlsx file that contains customer reviews.

Example CSV format:

| **Review**                              |
|-----------------------------------------|
| "The product is amazing, very useful."  |
| "I am not satisfied with the quality."  |
| "It's okay, nothing special."           |


### 2. Analyze:

- Click the "Upload and Analyze" button to send the file for sentiment analysis.
- The results will be displayed on a new page in a table format, showing positive, negative, and neutral sentiment scores.

## Deploying on Render

This project is configured to deploy on `Render`. Follow these steps:

1. Sign in to Render and create a new Web Service connected to your GitHub repository.
2. Set the environment variables on Render as specified above.
3. Deploy the project using the provided Procfile.

### Build Command

Render will automatically install dependencies from requirements.txt.

### Start Command

The start command specified in Procfile is:

```
gunicorn project.wsgi --log-file -
```

Replace `project` with your Django project name if different.

## Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a feature branch (git checkout -b feature/my-feature)
3. Commit your changes (git commit -m 'Add new feature')
4. Push to the branch (git push origin feature/my-feature)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. 




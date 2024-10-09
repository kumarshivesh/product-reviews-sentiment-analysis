# sentiment_analysis/views.py
import os
import json
import re
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def analyze_sentiment(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'analyze.html', {'error': 'No file uploaded'})

        file = request.FILES['file']
        file_extension = file.name.split('.')[-1].lower()

        try:
            if file_extension == 'csv':
                df = pd.read_csv(file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file)
            else:
                return render(request, 'analyze.html', {'error': 'Invalid file format. Please upload CSV or XLSX file.'})
        except Exception as e:
            return render(request, 'analyze.html', {'error': f'Error reading file: {str(e)}'})

        if 'Review' not in df.columns:
            return render(request, 'analyze.html', {'error': 'The file does not contain a "review" column'})

        reviews = df['Review'].tolist()[:50]  # Limit to 50 reviews

        try:
            sentiment_scores = analyze_reviews(reviews)
            return render(request, 'result.html', {'sentiment_scores': sentiment_scores})
        except Exception as e:
            return render(request, 'analyze.html', {'error': f'Error during sentiment analysis: {str(e)}'})

    return render(request, 'analyze.html')


def analyze_reviews(reviews):
    prompt = f"""Analyze the sentiment of the following customer reviews. 
    Provide a score for positive, negative, and neutral sentiments. 
    The scores should add up to 1.0.
    Reviews: {json.dumps(reviews)}
    
    Return only a JSON object in the following format:
    {{
      "positive": score,
      "negative": score,
      "neutral": score
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=150
        )
        
        result = response.choices[0].message.content.strip()
        
        # Log the raw response for debugging
        #print(f"Raw Groq API response: {result}")
        
        # Try to parse the JSON response
        try:
            parsed_result = json.loads(result)
            
            # Validate the structure of the parsed result
            if not all(key in parsed_result for key in ['positive', 'negative', 'neutral']):
                raise ValueError("Missing required keys in the response")
            
            return parsed_result
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract the JSON part
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                try:
                    parsed_result = json.loads(json_match.group())
                    if not all(key in parsed_result for key in ['positive', 'negative', 'neutral']):
                        raise ValueError("Missing required keys in the response")
                    return parsed_result
                except:
                    pass
            
            raise ValueError(f"Failed to parse Groq API response: {result}")
        
    except Exception as e:
        raise Exception(f"Error in Groq API call: {str(e)}")


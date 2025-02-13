from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import csv
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    selector = request.form['selector']
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.select(selector)
        data = [el.get_text(strip=True) for el in elements]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/export', methods=['POST'])
def export():
    if not os.path.exists('scraped_data'):
        os.makedirs('scraped_data')
    data = request.json['data']
    format_type = request.json['format']
    if format_type == 'csv':
        filename = f"scraped_data/scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Scraped Data'])
            for row in data:
                writer.writerow([row])
        return jsonify({'success': True, 'file': filename})
    elif format_type == 'json':
        filename = f"scraped_data/scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return jsonify({'success': True, 'file': 'export.json'})
    return jsonify({'success': False, 'error': 'Invalid format'})

if __name__ == '__main__':
    app.run(debug=True)

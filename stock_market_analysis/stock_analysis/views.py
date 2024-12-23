import pandas as pd
import numpy as np
from io import StringIO
from django.shortcuts import render
from .forms import StockDataForm
from .models import StockData, StockAnalysis
from django.http import JsonResponse
from django.http import HttpResponse

# Function to plot stock data
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def plot_stock_data(symbol):
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    dates = [item.date for item in stock_data]
    prices = [item.close_price for item in stock_data]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, label=f'{symbol} Closing Prices')
    plt.title(f'{symbol} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to a BytesIO object and encode it to base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_str

def upload_stock_data(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        # Read the uploaded CSV file into a pandas DataFrame
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            return HttpResponse(f"Error reading the file: {e}", status=400)

        # Print the columns for debugging (optional, can be removed later)
        print("Columns in uploaded file:", df.columns)

        # Check for the presence of one of the expected columns ('symbol', 'symboltoken', or 'ticker')
        expected_columns = ['symbol', 'symboltoken', 'ticker']
        symbol_column = next((col for col in expected_columns if col in df.columns), None)

        if symbol_column is None:
            return HttpResponse("Error: None of the expected columns ('symbol', 'symboltoken', 'ticker') are present in the uploaded file.", status=400)

        # Access the symbol data using the first available column
        symbol_data = df[symbol_column]  # Use the first column that exists

        # Optional: Process the data, for example, display the first few rows
        print(symbol_data.head())  # Print the first few rows for debugging

        # Further processing (e.g., save data to the database or analyze it)
        # You can also process other columns in the DataFrame here as needed

        return HttpResponse("File uploaded and processed successfully!")

    return render(request, 'upload_stock_data.html')

# View for analyzing stock data
def analyze_stock_data(request):
    stocks = StockData.objects.all()
    analysis_results = []

    for stock in stocks:
        data = StockData.objects.filter(symbol=stock.symbol).order_by('date')[:10]
        close_prices = [item.close_price for item in data]
        moving_avg = np.mean(close_prices)
        volatility = np.std(close_prices)

        analysis = StockAnalysis.objects.create(
            stock=stock,
            moving_average=moving_avg,
            volatility=volatility
        )

        # Get the plot for the stock
        stock_img = plot_stock_data(stock.symbol)

        analysis_results.append({
            'analysis': analysis,
            'stock_img': stock_img
        })

    return render(request, 'analysis_report.html', {'analysis_results': analysis_results})


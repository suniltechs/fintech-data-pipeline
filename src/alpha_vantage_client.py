import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AlphaVantageClient:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = 'https://www.alphavantage.co/query'
        self.symbol = os.getenv('ALPHA_VANTAGE_SYMBOL', 'IBM')
    
    def get_daily_stock_data(self):
        """Fetch daily stock data for the configured symbol"""
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract the daily time series
            time_series = data.get('Time Series (Daily)', {})
            
            # Return the latest day's data
            if time_series:
                latest_date = list(time_series.keys())[0]
                latest_data = time_series[latest_date]
                
                return {
                    'date': latest_date,
                    'open': float(latest_data['1. open']),
                    'high': float(latest_data['2. high']),
                    'low': float(latest_data['3. low']),
                    'close': float(latest_data['4. close']),
                    'volume': int(latest_data['5. volume'])
                }
            else:
                print("No time series data found in response")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Alpha Vantage: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Error parsing data from Alpha Vantage: {e}")
            return None
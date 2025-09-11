import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from .database import init_database, insert_stock_data, get_yesterdays_data, insert_recommendation
from .alpha_vantage_client import AlphaVantageClient
from .openai_client import OpenAIClient


load_dotenv()

def run_pipeline():
    """Main pipeline function to fetch data, store it, and generate insights"""
    print("Starting pipeline execution...")
    
    # Initialize database
    init_database()
    
    # Fetch today's stock data
    av_client = AlphaVantageClient()
    stock_data = av_client.get_daily_stock_data()
    
    if stock_data:
        print(f"Fetched data for {stock_data['date']}")
        
        # Store data in database
        symbol = os.getenv('ALPHA_VANTAGE_SYMBOL', 'IBM')
        insert_stock_data(
            symbol, 
            stock_data['date'],
            stock_data['open'],
            stock_data['high'],
            stock_data['low'],
            stock_data['close'],
            stock_data['volume']
        )
        print("Data stored in database")
    else:
        print("Failed to fetch stock data")
        return
    
    # Get yesterday's data for analysis (we'll use today's data as we just stored it)
    # In a real scenario, we might want to wait until the next day to analyze today's data
    yesterday_data = get_yesterdays_data(symbol)
    
    if yesterday_data:
        print(f"Analyzing data for {yesterday_data['date']}")
        
        # Generate insights with OpenAI
        openai_client = OpenAIClient()
        summary, recommendations = openai_client.generate_insights(symbol, yesterday_data)
        
        if summary and recommendations:
            # Store recommendations
            insert_recommendation(
                yesterday_data['date'],
                symbol,
                summary,
                recommendations
            )
            print("Insights generated and stored")
            # 🔹 Debug print so you can see insights in terminal
            print("\n--- Generated Insights ---")
            print(f"Date: {yesterday_data['date']}")
            print(f"Symbol: {symbol}")
            print(f"Summary: {summary}")
            print("Recommendations:")
            print(recommendations)
            print("--------------------------\n")
        else:
            print("Failed to generate insights")
    else:
        print("No yesterday's data available for analysis")
    
    print("Pipeline execution completed")

if __name__ == "__main__":
    run_pipeline()
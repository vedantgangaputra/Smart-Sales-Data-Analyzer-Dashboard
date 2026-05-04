import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from datetime import datetime, timedelta
import random

class DataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_path)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            raise
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def preprocess(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        try:
            # Handle missing values
            self.data.dropna(inplace=True)
            # Convert date column if exists
            if 'Date' in self.data.columns:
                self.data['Date'] = pd.to_datetime(self.data['Date'])
            # Ensure numeric columns
            numeric_cols = ['Sales', 'Profit']
            for col in numeric_cols:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            self.data.dropna(inplace=True)
            print("Data preprocessed successfully.")
        except Exception as e:
            print(f"Error preprocessing data: {e}")
            raise

    def sales_by_product(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() and preprocess() first.")
        try:
            sales_by_product = self.data.groupby('Product')['Sales'].sum().sort_values(ascending=False)
            plt.figure(figsize=(10, 6))
            sales_by_product.plot(kind='bar', color='skyblue')
            plt.title('Total Sales by Product')
            plt.xlabel('Product')
            plt.ylabel('Total Sales')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error generating sales by product chart: {e}")

    def profit_by_region(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() and preprocess() first.")
        try:
            profit_by_region = self.data.groupby('Region')['Profit'].sum()
            plt.figure(figsize=(8, 8))
            profit_by_region.plot(kind='pie', autopct='%1.1f%%', startangle=140)
            plt.title('Profit Distribution by Region')
            plt.ylabel('')
            plt.show()
        except Exception as e:
            print(f"Error generating profit by region chart: {e}")

    def sales_trend(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() and preprocess() first.")
        try:
            if 'Date' not in self.data.columns:
                print("No Date column found for sales trend.")
                return
            sales_trend = self.data.groupby('Date')['Sales'].sum()
            plt.figure(figsize=(10, 6))
            sales_trend.plot(kind='line', marker='o', color='green')
            plt.title('Sales Trend Over Time')
            plt.xlabel('Date')
            plt.ylabel('Total Sales')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error generating sales trend chart: {e}")

    def heatmap(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() and preprocess() first.")
        try:
            numeric_data = self.data.select_dtypes(include=[float, int])
            if numeric_data.empty:
                print("No numeric data available for heatmap.")
                return
            plt.figure(figsize=(10, 8))
            sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Heatmap')
            plt.show()
        except Exception as e:
            print(f"Error generating heatmap: {e}")

def create_sample_data(file_path):
    if os.path.exists(file_path):
        return
    try:
        products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Printer', 'Tablet', 'Phone', 'Headphones']
        regions = ['North', 'South', 'East', 'West']
        start_date = datetime(2023, 1, 1)
        data = []
        for i in range(20):
            date = start_date + timedelta(days=random.randint(0, 365))
            product = random.choice(products)
            region = random.choice(regions)
            sales = random.randint(100, 1000)
            profit = sales * random.uniform(0.1, 0.3)
            data.append([date.strftime('%Y-%m-%d'), product, region, sales, round(profit, 2)])
        
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Product', 'Region', 'Sales', 'Profit'])
            writer.writerows(data)
        print(f"Sample data created in '{file_path}'.")
    except Exception as e:
        print(f"Error creating sample data: {e}")

def display_menu():
    print("\nData Analytics Menu:")
    print("1. Sales by Product (Bar Chart)")
    print("2. Profit by Region (Pie Chart)")
    print("3. Sales Trend (Line Graph)")
    print("4. Correlation Heatmap")
    print("5. Exit")

def get_user_choice():
    try:
        choice = int(input("Enter your choice (1-5): "))
        if choice < 1 or choice > 5:
            raise ValueError
        return choice
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        return None

if __name__ == "__main__":
    file_path = "sales_data.csv"
    
    # Auto-run: Create dataset if missing
    create_sample_data(file_path)
    
    # Initialize analyzer
    analyzer = DataAnalyzer(file_path)
    
    try:
        # Load and preprocess data
        analyzer.load_data()
        analyzer.preprocess()
        
        # Automatically display all graphs
        print("Displaying all graphs automatically...")
        analyzer.sales_by_product()
        analyzer.profit_by_region()
        analyzer.sales_trend()
        analyzer.heatmap()
        
        # Interactive menu
        while True:
            display_menu()
            choice = get_user_choice()
            if choice is None:
                continue
            elif choice == 1:
                analyzer.sales_by_product()
            elif choice == 2:
                analyzer.profit_by_region()
            elif choice == 3:
                analyzer.sales_trend()
            elif choice == 4:
                analyzer.heatmap()
            elif choice == 5:
                print("Exiting...")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
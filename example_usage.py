import pandas as pd
from logic.engine import analyze_coverage

def main():
    print("--- Product Portfolio Rationalisation Engine ---")
    
    # Load data
    try:
        df_customers = pd.read_csv('customers.csv')
        df_products = pd.read_csv('products.csv')
    except FileNotFoundError:
        print("Data files not found. Run generate_data.py first.")
        return

    # Run rationalization
    results = analyze_coverage(df_customers, df_products)
    
    lacks = results['lacks']
    excess = results['excess']
    
    print(f"\nAnalysis Summary:")
    print(f"- Total Customers: {len(df_customers)}")
    print(f"- Total Products:  {len(df_products)}")
    print(f"- Coverage Gaps:   {len(lacks)} (Customers unsatisfied)")
    print(f"- Portfolio Waste: {len(excess)} (Products with 0 users)")
    
    if len(excess) > 0:
        print("\nExcess Products candidate for removal:")
        print(excess[['ProductID', 'Cap_StaticPressure_Pa', 'Cap_SensiblePower_kW']])

if __name__ == "__main__":
    main()

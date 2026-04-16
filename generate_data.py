import pandas as pd
import numpy as np

def generate_sample_data():
    # Customer Segment Data (Requirements)
    # Range for static pressure: 0-60 Pa
    # Range for sensible power: 0.5-10 kW
    # Target Temperature: 21-25 C
    
    np.random.seed(42)
    num_customers = 50
    customer_data = {
        'CustomerID': [f'C{i:03d}' for i in range(num_customers)],
        'Req_StaticPressure_Pa': np.random.uniform(10, 55, num_customers),
        'Req_SensiblePower_kW': np.random.uniform(1, 9, num_customers),
        'Req_RoomTemp_C': np.random.uniform(21, 25, num_customers),
        'FluidType': ['Water'] * num_customers
    }
    df_customers = pd.DataFrame(customer_data)
    
    # Existing Product Portfolio (Variants)
    # Intentionally create some products that are outside customer ranges (Excess)
    # And leave some customer areas empty (Lacks)
    num_products = 15
    product_data = {
        'ProductID': [f'P{i:03d}' for i in range(num_products)],
        'Cap_StaticPressure_Pa': [20, 25, 30, 35, 40, 45, 10, 15, 80, 85, 90, 32, 33, 34, 100],
        'Cap_SensiblePower_kW':  [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 0.5, 1.0, 12, 13, 14, 3.1, 3.2, 3.3, 15],
        'Efficiency': np.random.uniform(0.7, 0.95, num_products),
        'UnitCost': np.random.uniform(200, 1000, num_products)
    }

    df_products = pd.DataFrame(product_data)
    
    # Save to CSV
    df_customers.to_csv('customers.csv', index=False)
    df_products.to_csv('products.csv', index=False)
    print("Sample data generated: customers.csv, products.csv")

if __name__ == "__main__":
    generate_sample_data()

import pandas as pd
import numpy as np

def generate_data_technical():
    # Customer Segment Data (Requirements)
    # Range for static pressure: 0-60 Pa
    # Range for sensible power: 0.5-10 kW
    # Target Temperature: 21-25 C
    
    np.random.seed(42)
    num_customers = 500
    customer_data = {
        'CustomerID': [f'C{i:03d}' for i in range(num_customers)],
        'Req_StaticPressure_Pa': np.random.uniform(5, 75, num_customers),
        'Req_SensiblePower_kW': np.random.uniform(0.5, 12, num_customers),
        'RoomVolume_m3': np.random.uniform(30, 300, num_customers),
        'TempDelta_C': np.random.choice([5, 8, 10, 12, 15], num_customers),
        'FluidType': ['Water'] * num_customers
    }
    df_customers = pd.DataFrame(customer_data)
    
    # Existing Product Portfolio (Variants) - Significant Increase
    num_products = 50
    product_data = {
        'ProductID': [f'P{i:03d}' for i in range(num_products)],
        # INTENTIONAL GAP: We only generate products for Pressure < 40 or Power < 6
        # This leaves a 'Lack' for customers needing High Pressure AND High Power
        'Cap_StaticPressure_Pa': np.random.uniform(0, 40, num_products),
        'Cap_SensiblePower_kW': np.random.uniform(0.1, 6, num_products),
        'Efficiency': np.random.uniform(0.65, 0.98, num_products),
        'UnitCost': np.random.uniform(150, 1500, num_products)
    }



    df_products = pd.DataFrame(product_data)
    
    # Save to CSV
    df_customers.to_csv('customers.csv', index=False)
    df_products.to_csv('products.csv', index=False)
    
    print("--- Digital Twin Initialization Complete ---")
    print(f"Generated {num_customers} customer profiles for segment [C].")
    print(f"Generated {num_products} product variants for portfolio [V].")
    print("Coordinates: Static Pressure (Pa), Sensible Power (kW)")

if __name__ == "__main__":
    generate_data_technical()


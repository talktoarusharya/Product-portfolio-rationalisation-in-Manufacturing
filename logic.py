import pandas as pd
import numpy as np

class Interaction:
    """
    Represents a relationship between attributes as defined in Algorithm 1.
    """
    def __init__(self, name, formula_fn, inputs, output):
        self.name = name
        self.formula_fn = formula_fn  # Lambda function for the math
        self.inputs = inputs          # List of attribute names
        self.output = output          # Output attribute name

class RationalizationEngine:
    def __init__(self):
        # Algorithm 1: Knowledge Base of Interactions
        # Based on the Fan-Coil case study in the paper (Section 7)
        self.interactions = [
            # Interaction 1: Power Required (Qs) = f(Room Volume, Temp Delta)
            # Simplified version of heat load calculation
            Interaction(
                "Heat Load Calculation",
                lambda vol, t_delta: vol * 0.04 * t_delta, # approx 40W per m3 per deg
                ['RoomVolume_m3', 'TempDelta_C'],
                'Req_SensiblePower_kW'
            ),
            # Interaction 2: Coil Power Capacity (Cap_Ps) = f(AirFlow, SurfaceArea)
            Interaction(
                "Coil Thermal Transfer",
                lambda flow, area: 0.1 * flow * area, # simplified heat exchange formula
                ['Cap_AirFlow_m3h', 'Cap_CoilArea_m2'],
                'Cap_SensiblePower_kW'
            )
        ]

    def algorithm_1_retrieve_tree(self, purpose):
        """
        Builds a tree of interactions starting from a purpose.
        Purpose: 'Room Air Cooling' -> Sensible Power
        """
        # For the demo, we assume the purpose leads to 'SensiblePower'
        # In a real KBS, this would be a graph traversal
        return self.interactions

    def algorithm_2_define_pl(self, customer_segment_ranges):
        """
        Defines the 'Right Product Variety' (V*) space.
        Calculates required system attributes for the given customer ranges.
        """
        # Segment defines ranges for effects and constraints
        # e.g., RoomVolume: [50, 200], TempDelta: [5, 15]
        v_min = customer_segment_ranges['RoomVolume_m3'][0]
        v_max = customer_segment_ranges['RoomVolume_m3'][1]
        t_min = customer_segment_ranges['TempDelta_C'][0]
        t_max = customer_segment_ranges['TempDelta_C'][1]
        
        # Calculate Required Power Range
        p_req_min = 0.04 * v_min * t_min
        p_req_max = 0.04 * v_max * t_max
        
        return {
            'Req_SensiblePower_kW': (p_req_min, p_req_max)
        }

    def algorithm_3_rationalize(self, df_customers, df_products):
        """
        Identifies Lacks, Excesses, and Redundancies.
        """
        # 1. Map Customers to Products (Coverage)
        coverage_map = {} # ProductID -> Count of customers served
        customer_status = [] # List of dicts
        
        for _, cust in df_customers.iterrows():
            # Find all products that satisfy the requirement
            # Requirement: Cap_SensiblePower >= Req_SensiblePower
            # AND: Cap_StaticPressure >= Req_StaticPressure
            
            matches = df_products[
                (df_products['Cap_SensiblePower_kW'] >= cust['Req_SensiblePower_kW']) &
                (df_products['Cap_StaticPressure_Pa'] >= cust['Req_StaticPressure_Pa'])
            ]
            
            matched_ids = matches['ProductID'].tolist()
            customer_status.append({
                'CustomerID': cust['CustomerID'],
                'IsSatisfied': len(matched_ids) > 0,
                'SatisfiedBy': matched_ids
            })
            
            for pid in matched_ids:
                coverage_map[pid] = coverage_map.get(pid, 0) + 1
        
        df_cust_results = pd.DataFrame(customer_status)
        
        # 2. Identify Lacks (Unsatisfied customers)
        customer_results = df_customers.merge(df_cust_results, on='CustomerID')
        lacks = customer_results[~customer_results['IsSatisfied']]
        
        # 3. Identify Excess (Products satisfying 0 customers)
        df_products['UsedCount'] = df_products['ProductID'].map(coverage_map).fillna(0)
        excess = df_products[df_products['UsedCount'] == 0]
        
        # 4. Identify Redundancy
        # Property (2) in paper: Ideally 1 product per customer.
        # If a customer is satisfied by > 3 products, those products are likely redundant.
        redundant_count = df_cust_results[df_cust_results['SatisfiedBy'].str.len() > 1]
        
        return {
            'lacks': lacks,
            'excess': excess,
            'redundant_scenarios': redundant_count,
            'customer_results': customer_results,
            'product_results': df_products
        }


# Global instance for use in app
engine = RationalizationEngine()

def analyze_coverage(df_customers, df_products):
    return engine.algorithm_3_rationalize(df_customers, df_products)

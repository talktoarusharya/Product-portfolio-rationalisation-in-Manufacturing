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
        Algorithm 1: Interactions Retrieval.
        Decomposes a 'Purpose' into a tree of technical requirements.
        """
        # The paper defines the tree starting from purpose -> Effects -> Req -> System Attributes
        # We model this as a multi-step knowledge retrieval
        tree = {
            'purpose': purpose,
            'root_effect': 'Room Temperature Consistency',
            'interactions': [
                {
                    'level': 1,
                    'name': 'Thermal Equilibrium (I1)',
                    'output': 'Required Sensible Power (kW)',
                    'inputs': ['Room Volume (m3)', 'Target Temp Delta (C)'],
                    'type': 'Environmental Constraint Translation'
                },
                {
                    'level': 2,
                    'name': 'Coil Capacity (I2)',
                    'output': 'Product Sensible Power (kW)',
                    'inputs': ['Air Flow rate (m3/h)', 'Coil Surface Area (m2)', 'Rows (N)'],
                    'type': 'Engineering System Attribute mapping'
                }
            ],
            'leaves': ['Req_SensiblePower_kW', 'Req_StaticPressure_Pa']
        }
        return tree


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
        Strictly implements Property (2) from the research:
        'Ideally 1 variant per customer. If multiple exist, choose the best based on economics/sustainability.'
        """
        customer_status = []
        best_variants_used = set()
        
        # Mapping each customer to their 'Best' match (Property 2)
        for _, cust in df_customers.iterrows():
            # Find all technically feasible matches
            matches = df_products[
                (df_products['Cap_SensiblePower_kW'] >= cust['Req_SensiblePower_kW']) &
                (df_products['Cap_StaticPressure_Pa'] >= cust['Req_StaticPressure_Pa'])
            ]
            
            if not matches.empty:
                # OPTIMIZATION: Choose the cheapest product (Economic Criterion)
                # If costs are equal, choose the most efficient (Sustainability Criterion)
                best_match = matches.sort_values(by=['UnitCost', 'Efficiency'], ascending=[True, False]).iloc[0]
                best_pid = best_match['ProductID']
                best_variants_used.add(best_pid)
                
                customer_status.append({
                    'CustomerID': cust['CustomerID'],
                    'IsSatisfied': True,
                    'BestProductID': best_pid,
                    'AvailableMatches': len(matches),
                    'OptimalCost': best_match['UnitCost']
                })
            else:
                customer_status.append({
                    'CustomerID': cust['CustomerID'],
                    'IsSatisfied': False,
                    'BestProductID': None,
                    'AvailableMatches': 0,
                    'OptimalCost': 0
                })
        
        df_cust_results = pd.DataFrame(customer_status)
        customer_results = df_customers.merge(df_cust_results, on='CustomerID')
        
        # Identify Lacks (Customers with 0 matches)
        lacks = customer_results[~customer_results['IsSatisfied']]
        
        # Identify Excess (Products not selected as the 'Best' for ANY customer)
        # This represents the set V \ V* (The wasteful variants)
        df_products['InOptimalSet'] = df_products['ProductID'].isin(best_variants_used)
        excess = df_products[~df_products['InOptimalSet']]
        
        # Identify Redundancy: Scenarios where a customer has > 1 choice
        redundant_scenarios = customer_results[customer_results['AvailableMatches'] > 1]
        
        return {
            'lacks': lacks,
            'excess': excess,
            'redundant_count': len(redundant_scenarios),
            'optimal_portfolio_size': len(best_variants_used),
            'customer_results': customer_results,
            'product_results': df_products
        }



# Global instance for use in app
engine = RationalizationEngine()

def analyze_coverage(df_customers, df_products):
    return engine.algorithm_3_rationalize(df_customers, df_products)

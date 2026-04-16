import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from logic import analyze_coverage, engine

# --- Classy Personal Theme ---
st.set_page_config(
    page_title="Portfolio Optimization Framework",
    page_icon="📋",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #fcfaf7;
        color: #2c3e50;
    }
    
    h1, h2, .personal-header {
        font-family: 'Lora', serif;
        color: #1a2a3a;
        font-weight: 700;
    }
    
    .personal-header {
        font-size: 2.8rem;
        border-bottom: 2px solid #1a2a3a;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
    
    .intro-text {
        font-family: 'Lora', serif;
        font-style: italic;
        font-size: 1.1rem;
        color: #5d6d7e;
        margin-bottom: 2rem;
    }
    
    .section-break {
        margin: 3rem 0 1.5rem 0;
        text-align: left;
        border-bottom: 1px solid #dcdde1;
        font-family: 'Lora', serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }
    
    .metric-bubble {
        padding: 15px;
        border-left: 2px solid #1a2a3a;
        margin-bottom: 10px;
    }
    
    .metric-title { font-size: 0.8rem; text-transform: uppercase; color: #7f8c8d; }
    .metric-value { font-family: 'Lora', serif; font-size: 2rem; color: #1a2a3a; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_and_analyze():
    try:
        df_c = pd.read_csv('customers.csv')
        df_p = pd.read_csv('products.csv')
        res = analyze_coverage(df_c, df_p)
        return df_c, df_p, res
    except:
        return None, None, None

df_c, df_p, res = load_and_analyze()

if df_c is None:
    st.error("No data found. Please run the generation script first.")
    st.stop()

# --- Main Interface ---

st.markdown('<div class="personal-header">Portfolio Rationalisation Report</div>', unsafe_allow_html=True)
st.markdown('<div class="intro-text">A strategic breakdown of our product line vs. what our customers actually need.</div>', unsafe_allow_html=True)

# 1. Dashboard Overview
st.markdown('<div class="section-break">I. Key Insights</div>', unsafe_allow_html=True)
st.write("I've analyzed the entire dataset to see how well our current products match up with the market demand. Here's a high-level look at where we stand:")

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-bubble">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Market Reach</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{(1-len(res["lacks"])/len(df_c))*100:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-bubble">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Essential Items ($V^*$)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{res["optimal_portfolio_size"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-bubble">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Excess Count</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{len(res["excess"])}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("##")
pct_excess = int(len(res['excess'])/len(df_p)*100)
st.write(f"The numbers show that about **{pct_excess}% of our variants** aren't actually needed for the segments we're targeting. We can significantly simplify things while keeping 100% of our current sales potential.")

# 2. Behind the math
st.markdown('<div class="section-break">II. How the logic works</div>', unsafe_allow_html=True)
st.write("To get these results, I built a logic tree that breaks down the purpose of 'Room Air Cooling' into technical specs. It links what the customer feels (Temperature) to what we build (Coil Area, Fans, etc.).")

tree = engine.algorithm_1_retrieve_tree("Room Air Cooling")
for inter in tree['interactions']:
    st.markdown(f"**Step {inter['level']}:** {inter['name']}")
    st.write(f"This part maps {', '.join(inter['inputs'])} to get the **{inter['output']}**.")

# 3. Visual Mapping
st.markdown('<div class="section-break">III. Mapping the landscape</div>', unsafe_allow_html=True)
st.write("This chart helps visualize the overlap. The dark squares are the essential products ($V^*$) we should keep. The gray circles are essentially dead weight—products that don't uniquely satisfy any customer segment better than our core set.")

fig = go.Figure()
# Core
fig.add_trace(go.Scatter(
    x=res['product_results'][res['product_results']['InOptimalSet']]['Cap_StaticPressure_Pa'], 
    y=res['product_results'][res['product_results']['InOptimalSet']]['Cap_SensiblePower_kW'],
    mode='markers', name='Products to Keep (V*)',
    marker=dict(size=14, color='#1a2a3a', symbol='square', line=dict(width=1, color='#fcfaf7'))
))
# Excess
fig.add_trace(go.Scatter(
    x=res['excess']['Cap_StaticPressure_Pa'], 
    y=res['excess']['Cap_SensiblePower_kW'],
    mode='markers', name='Excess/Redundant',
    marker=dict(size=10, color='#dcdde1', symbol='circle', opacity=0.4)
))

fig.update_layout(
    template="simple_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    height=550,
    xaxis=dict(title="Static Pressure (Pa)"),
    yaxis=dict(title="Sensible Power (kW)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0)
)
st.plotly_chart(fig, use_container_width=True)

# 4. Detailed Breakdown
st.markdown('<div class="section-break">IV. Action Items</div>', unsafe_allow_html=True)
st.write("Based on the data, here are my specific recommendations for our next product cycle. You can export these lists for the manufacturing and R&D teams below.")

c1, c2 = st.columns(2)
with c1:
    csv_excess = res['excess'][['ProductID', 'Cap_SensiblePower_kW', 'UnitCost']].to_csv(index=False).encode('utf-8')
    st.download_button(
        "📄 Export Retirement List (Excess)",
        csv_excess,
        "retirement_plan.csv",
        "text/csv",
        help="List of variants to be rationalized to reduce inventory overhead."
    )
with c2:
    csv_lacks = res['lacks'][['CustomerID', 'Req_SensiblePower_kW', 'Req_StaticPressure_Pa']].to_csv(index=False).encode('utf-8')
    st.download_button(
        "💡 Export R&D Gaps (Lacks)",
        csv_lacks,
        "market_gaps.csv",
        "text/csv",
        help="Target specifications for our next generation of high-performance units."
    )

st.write("---")
show_lacks = st.toggle("View market gaps (Lacks) in-browser")

if show_lacks:
    st.write("These are the spots where we're losing out—customers have needs we just don't meet yet.")
    st.table(res['lacks'].head(15)[['CustomerID', 'Req_SensiblePower_kW', 'Req_StaticPressure_Pa']])

show_excess = st.toggle("Show me the waste (Excess)")
if show_excess:
    st.write("These are the models I'd suggest retiring first. They don't have a unique 'home' in our target market.")
    st.table(res['excess'].head(15)[['ProductID', 'Cap_SensiblePower_kW', 'UnitCost']])

st.write("---")
st.markdown("<div style='text-align: center; color: #95a5a6; font-size: 0.9rem;'>Analysis performed on 500 segments and 50 historical variants.</div>", unsafe_allow_html=True)

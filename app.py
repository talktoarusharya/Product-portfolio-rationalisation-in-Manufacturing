import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
from logic.engine import analyze_coverage

# --- 🚀 Performance Optimization (Skill 6) ---
@st.cache_data
def get_analysis(df_cust, df_prod):
    return analyze_coverage(df_cust, df_prod)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --- 🧠 UI/UX Architecture (Skill 1) ---
st.set_page_config(
    page_title="Portfolio Wellness Pro",
    page_icon="🏭",
    layout="wide",
)

# --- 🎨 Advanced Styling (Skill 2) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(30, 27, 75) 100%);
        color: #f8fafc;
    }
    
    /* 🧊 Glossy Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 24px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .glass-card:hover {
        border: 1px solid rgba(99, 102, 241, 0.5);
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 40px -15px rgba(0,0,0,0.6);
    }
    
    /* 🌈 Typography */
    .hero-text {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin-bottom: 1rem;
    }
    
    .kpi-val {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to bottom, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* 🔘 Interactive Elements */
    .stButton>button {
        border-radius: 12px;
        padding: 0.6rem 2rem;
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- 🔄 Stateful Application Design (Skill 4) ---
if 'data_initialized' not in st.session_state:
    st.session_state.data_initialized = False

# --- 🖼️ Header Section ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown('<div class="hero-text">Intelligent <br>Portfolio Rationalizer</div>', unsafe_allow_html=True)
    st.markdown("#### *Engineering the perfect match between customer demand and product variety.*")
with header_col2:
    lottie_fac = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_z9ed2jna.json")
    if lottie_fac:
        st_lottie(lottie_fac, height=250)

# --- 📂 Data Management (Skill 8) ---
def check_data_exists():
    import os
    return os.path.exists('customers.csv') and os.path.exists('products.csv')

if not check_data_exists() and not st.session_state.data_initialized:
    st.markdown("""
    <div class="glass-card">
        <h3>🔍 System Readiness Check</h3>
        <p>No manufacturing data detected in the workspace. Initialize the Digital Twin to proceed.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Initialize Portfolio Digital Twin", type="primary"):
        import generate_data
        generate_data.generate_sample_data()
        st.session_state.data_initialized = True
        st.rerun()
else:
    # --- 📊 Dashboard Content ---
    df_cust = pd.read_csv('customers.csv')
    df_prod = pd.read_csv('products.csv')
    
    results = get_analysis(df_cust, df_prod)
    lacks = results['lacks']
    excess = results['excess']
    
    # --- 📈 Metrics Row (Skill 5) ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Market Coverage</div><div class="kpi-val">{100 - (len(lacks)/len(df_cust)*100):.1f}%</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Portfolio Leaness</div><div class="kpi-val">{len(df_prod)-len(excess)}/{len(df_prod)}</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Supply Gaps</div><div class="kpi-val">{len(lacks)}</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Optimization Win</div><div class="kpi-val">${len(excess)*450}k</div></div>', unsafe_allow_html=True)

    # --- 🧩 Interactive Tabs (Skill 3) ---
    tabs = st.tabs(["🚀 Market Intelligence", "🛠️ Rationalization Hub", "🎭 Scenario Simulation", "📖 Science & Methods"])
    
    with tabs[0]:
        st.markdown("### 🗺️ Visualizing the Opportunity Space")
        fig = go.Figure()
        
        # Add Heatmap area for "Ideal" coverage if possible, or just scatter
        fig.add_trace(go.Scatter(
            x=df_cust['Req_StaticPressure_Pa'], y=df_cust['Req_SensiblePower_kW'],
            mode='markers', name='Target Demand',
            marker=dict(size=12, color='#818cf8', opacity=0.3, line=dict(width=1, color='white')),
            text=df_cust['CustomerID']
        ))
        
        fig.add_trace(go.Scatter(
            x=df_prod['Cap_StaticPressure_Pa'], y=df_prod['Cap_SensiblePower_kW'],
            mode='markers', name='Installed Portfolio',
            marker=dict(size=16, color='#fb7185', symbol='diamond', line=dict(width=2, color='white')),
            text=df_prod['ProductID']
        ))
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Static Pressure (Pa)", gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Sensible Power (kW)", gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(l=0, r=0, t=20, b=0),
            height=600
        )
        st.plotly_chart(fig, width="stretch")

    with tabs[1]:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("""
            <div class="glass-card" style="border-left: 5px solid #fb7185;">
                <h4>📉 Wasteful Excess (Candidate for Retirement)</h4>
                <p>These models satisfy zero current customers. Retiring them reduces inventory overhead.</p>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(excess[['ProductID', 'Cap_StaticPressure_Pa', 'Cap_SensiblePower_kW', 'UnitCost']], width="stretch")
            
        with col_r:
            st.markdown("""
            <div class="glass-card" style="border-left: 5px solid #818cf8;">
                <h4>📈 Supply Lacks (Opportunity for Innovation)</h4>
                <p>These requirements are currently ignored. New product development should target these coordinates.</p>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(lacks[['CustomerID', 'Req_StaticPressure_Pa', 'Req_SensiblePower_kW']], width="stretch")

    with tabs[2]:
        st.markdown("### 🔮 Portfolio Evolution Lab")
        st.write("Simulate the impact of adding a new variant to your manufacturing lineage.")
        
        with st.container():
            c1, c2, c3 = st.columns([1,1,1])
            with c1:
                s_p = st.number_input("Target Pressure (Pa)", 0, 100, 50)
            with c2:
                s_w = st.number_input("Target Power (kW)", 0.0, 20.0, 5.0)
            with c3:
                st.write("###")
                if st.button("⚡ Simulate ROI"):
                    new_item = pd.DataFrame([{
                        'ProductID': 'SIM-PRO-1', 'Cap_StaticPressure_Pa': s_p,
                        'Cap_SensiblePower_kW': s_w, 'Efficiency': 0.9, 'UnitCost': 550
                    }])
                    new_prod_df = pd.concat([df_prod, new_item], ignore_index=True)
                    sim_results = analyze_coverage(df_cust, new_prod_df)
                    improv = len(lacks) - len(sim_results['lacks'])
                    
                    if improv > 0:
                        st.balloons()
                        st.success(f"**Impact Detected!** This addition captures **{improv}** additional customers ({improv/len(df_cust)*100:.1f}% market growth).")
                    else:
                        st.error("**Inefficient Addition:** This variant provides no new coverage. Current products already serve this segment.")

    with tabs[3]:
        st.markdown("## 🧠 Scientific Methodology")
        st.markdown("""
        This platform implements the **Product Variety Rationalisation** approach by *Giovannini et al. (2014)*.
        
        #### 🏗️ The 3 Pillar Algorithm:
        1. **Interaction Trees**: Decomposing high-level customer purposes into leaf-level engineering variables.
        2. **V* Space Definition**: Mathematically defining the smallest subset of variety that preserves 100% customer satisfaction.
        3. **Rationalization Audit**: Continuous auditing of 'Excess' vs 'Lacks' using digital twin synchronization.
        """)
        st.image("https://img.icons8.com/wired/512/FFFFFF/factory.png", width=100) # Placeholder for more cool visuals

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b;'>Built with Advanced Streamlit Frontend Engineering skill-set.</div>", unsafe_allow_html=True)

# Portfolio Rationalization Framework (Manufacturing)

### "The right level of customisation isn't about how much we *can* build, but how much we *should* build."

This project is a technical implementation of a product-line rationalization system. It bridges the gap between customer needs (Marketing) and technical specifications (Engineering) to find the "Just Right" balance of variety.

## 🧠 The Core Idea
In manufacturing, variety is expensive. Every extra variant adds complexity to the shop floor, the warehouse, and the supply chain. This tool helps identify:
1.  **Gaps (Lacks)**: Market opportunities we're currently missing.
2.  **Waste (Excess)**: Product variants that don't satisfy any unique customer segment and should be retired.
3.  **Core Variety ($V^*$)**: The absolute minimum number of products needed to satisfy 100% of the possible demand.

## 🚀 Getting Started
I've designed this to be straightforward to set up.

```bash
# Clone the repository
git clone https://github.com/talktoarusharya/Product-portfolio-rationalisation-in-Manufacturing
cd Product-portfolio-rationalisation-in-Manufacturing

# Install the necessary libraries
pip install -r requirements.txt

# Reset/Prepare the data twin
python generate_data.py

# Launch my analysis dashboard
streamlit run app.py
```

## 📐 Implementation Logic
I based this on the research from *Giovannini et al.*, focusing on three specific algorithms:
-   **Structure**: Building an interaction tree that maps "What the customer wants" to "What we build."
-   **Definition**: Calculating the ideal product space ($V^*$) to bound our portfolio.
-   **Rationalization**: A spatial audit that flags overlaps and redundancies using economic and sustainability criteria.

## 📊 Outputs
The dashboard provides a detailed executive report with **Action Items**, allowing you to export specific retirement lists for manufacturing and R&D gap plans for product development.

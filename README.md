# Product Portfolio Rationalisation in Manufacturing

This project implements the methodology proposed by *Giovannini et al. (2014)* regarding the rationalisation of product lines in mass customisation manufacturing.

## Overview

The core objective is to link each product variant to the specific customer profile that needs it, avoiding:
- **Lacks**: Customers whose needs are not met by any variant.
- **Redundancies**: Multiple variants proposed for the same customer need.
- **Excesses**: Variants not related to any customer segment.

## Features

- **Market Analysis Dashboard**: Visualises customer needs vs product capabilities.
- **Rationalisation Engine**: Identifies coverage gaps and wasteful excess in the portfolio.
- **Scenario Simulator**: Allows "What-if" analysis for introducing new products or removing old ones.
- **Premium UI**: Dark-themed, interactive Streamlit dashboard.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate sample data (optional):
   ```bash
   python generate_data.py
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Case Study: Fan-Coil Units
The application includes a demonstration based on industrial fan-coil units, focusing on parameters like static pressure and sensible cooling power.

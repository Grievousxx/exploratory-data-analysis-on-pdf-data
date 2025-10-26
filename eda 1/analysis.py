# === Step 1: Import Required Libraries ===
import plotly.io as pio
pio.renderers.default = 'browser'
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# === Step 2: Load the CSV File ===
file = "dummy_financial_report.csv"

if not os.path.exists(file):
    print(f"❌ File not found: {file}")
    exit()

df = pd.read_csv(file)

# === Step 3: Clean Column Names ===
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

# === Step 4: Convert Data Types ===
numeric_cols = ['revenue_(million_usd)', 'expenses_(million_usd)', 'profit_(million_usd)']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

df['year'] = pd.to_datetime(df['year'], format='%Y')

# === Step 5: Create Derived Metrics ===
df['revenue_growth_%'] = df['revenue_(million_usd)'].pct_change() * 100
df['profit_margin_%'] = (df['profit_(million_usd)'] / df['revenue_(million_usd)']) * 100

# === Step 6: Visualizations ===

# Revenue vs Profit Over Time
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['year'], y=df['revenue_(million_usd)'], mode='lines+markers', name='Revenue'))
fig1.add_trace(go.Scatter(x=df['year'], y=df['profit_(million_usd)'], mode='lines+markers', name='Profit'))
fig1.update_layout(title='Revenue vs Profit Over Time', xaxis_title='Year', yaxis_title='Million USD')
fig1.show()

# Profit Margin Over Time
fig2 = px.bar(df, x='year', y='profit_margin_%', title='Profit Margin Over Time',
              text_auto=True, color='profit_margin_%', color_continuous_scale='Viridis')
fig2.update_layout(yaxis_title='Profit Margin (%)')
fig2.show()

# Revenue Growth Over Time
fig3 = px.bar(df, x='year', y='revenue_growth_%', title='Year-over-Year Revenue Growth (%)',
              text_auto=True, color='revenue_growth_%', color_continuous_scale='RdBu')
fig3.add_hline(y=0, line_dash='dash', line_color='black')
fig3.update_layout(yaxis_title='Growth Rate (%)')
fig3.show()

# === Step 7: Summary Observations ===
observations = []

# Max Revenue Growth
max_growth_year = df.loc[df['revenue_growth_%'].idxmax()]['year'].year
max_growth_value = df['revenue_growth_%'].max()
observations.append(f"1. Highest revenue growth: {max_growth_year} with {max_growth_value:.2f}%.")

# Min Profit Margin
min_margin_year = df.loc[df['profit_margin_%'].idxmin()]['year'].year
min_margin_value = df['profit_margin_%'].min()
observations.append(f"2. Lowest profit margin: {min_margin_year} at {min_margin_value:.2f}%.")

# Profit Trend
start_profit = df['profit_(million_usd)'].iloc[0]
end_profit = df['profit_(million_usd)'].iloc[-1]
if end_profit > start_profit:
    observations.append(f"3. Net profit increased from {start_profit}M to {end_profit}M.")
else:
    observations.append("3. Profit did not show an overall increase.")

# Print Observations
print("\nSummary Observations:")
for obs in observations:
    print(obs)



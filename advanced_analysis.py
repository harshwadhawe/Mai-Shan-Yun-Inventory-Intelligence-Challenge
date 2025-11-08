#!/usr/bin/env python3
"""
Advanced Analysis for MSY Inventory Intelligence Challenge
- Seasonal patterns
- Anomaly detection
- Forecasting preparation
- Inventory optimization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# Get directories
base_dir = Path(__file__).parent
processed_dir = base_dir / "processed_data"
output_dir = base_dir / "eda_output"
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("ADVANCED ANALYSIS")
print("=" * 80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1/6] Loading data...")
print("-" * 80)

consumption_monthly = pd.read_csv(processed_dir / "ingredient_consumption_monthly.csv")
ingredient_summary = pd.read_csv(processed_dir / "ingredient_summary.csv")
consumption_with_shipments = pd.read_csv(processed_dir / "ingredient_consumption_with_shipments.csv")
monthly_sales_item = pd.read_csv(base_dir / "cleaned_data" / "monthly_sales_item.csv")

month_order = ['May', 'June', 'July', 'August', 'September', 'October']
print(f"✓ Loaded data for analysis")

# ============================================================================
# 2. SEASONAL PATTERN ANALYSIS
# ============================================================================
print("\n[2/6] Seasonal pattern analysis...")
print("-" * 80)

# Calculate month-over-month growth
consumption_pivot = consumption_monthly.pivot(index='month', columns='ingredient', values='total_consumption')
consumption_pivot = consumption_pivot.reindex(month_order)

# Calculate growth rates
growth_rates = {}
for ingredient in consumption_pivot.columns:
    values = consumption_pivot[ingredient].values
    if len(values) > 1 and values[0] > 0:
        growth = ((values[-1] - values[0]) / values[0]) * 100
        growth_rates[ingredient] = growth

# Find ingredients with significant growth/decline
significant_growth = {k: v for k, v in growth_rates.items() if abs(v) > 20}
print(f"\nIngredients with >20% change:")
for ingredient, growth in sorted(significant_growth.items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {ingredient}: {growth:+.1f}%")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Top growing ingredients
if significant_growth:
    top_growing = sorted(significant_growth.items(), key=lambda x: x[1], reverse=True)[:5]
    ingredients = [x[0] for x in top_growing]
    growths = [x[1] for x in top_growing]
    
    colors = ['green' if g > 0 else 'red' for g in growths]
    axes[0, 0].barh(range(len(ingredients)), growths, color=colors, alpha=0.7)
    axes[0, 0].set_yticks(range(len(ingredients)))
    axes[0, 0].set_yticklabels(ingredients)
    axes[0, 0].set_title('Top 5 Ingredients - Growth Rate (May to Oct)', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Growth Rate (%)')
    axes[0, 0].axvline(x=0, color='black', linestyle='--', linewidth=1)
    axes[0, 0].grid(True, alpha=0.3, axis='x')

# Consumption volatility (coefficient of variation)
volatility = consumption_monthly.groupby('ingredient')['total_consumption'].agg(['std', 'mean'])
volatility['cv'] = volatility['std'] / volatility['mean']
volatility = volatility.sort_values('cv', ascending=False).head(10)

axes[0, 1].barh(range(len(volatility)), volatility['cv'], color=sns.color_palette("Reds", len(volatility)))
axes[0, 1].set_yticks(range(len(volatility)))
axes[0, 1].set_yticklabels(volatility.index)
axes[0, 1].set_title('Top 10 Most Volatile Ingredients (CV)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Coefficient of Variation')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# Monthly consumption heatmap
top_10_ingredients = ingredient_summary.nlargest(10, 'total_consumption_6months')['ingredient'].values
heatmap_data = consumption_pivot[top_10_ingredients].T
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[1, 0], 
            cbar_kws={'label': 'Consumption'})
axes[1, 0].set_title('Top 10 Ingredients - Monthly Consumption Heatmap', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Ingredient')

# Revenue trend by month
monthly_revenue = monthly_sales_item.groupby('month')['Amount'].sum().reindex(month_order)
axes[1, 1].plot(monthly_revenue.index, monthly_revenue.values, marker='o', linewidth=3, 
                markersize=10, color='#2E86AB', label='Revenue')
axes[1, 1].fill_between(monthly_revenue.index, monthly_revenue.values, alpha=0.3, color='#2E86AB')
axes[1, 1].set_title('Monthly Revenue Trend with Growth Annotations', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Revenue ($)')
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].tick_params(axis='x', rotation=45)

# Add growth annotations
for i in range(1, len(monthly_revenue)):
    prev_val = monthly_revenue.iloc[i-1]
    curr_val = monthly_revenue.iloc[i]
    growth = ((curr_val - prev_val) / prev_val) * 100
    axes[1, 1].annotate(f'{growth:+.1f}%', 
                        (monthly_revenue.index[i], curr_val),
                        textcoords="offset points", xytext=(0,10), ha='center',
                        fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig(output_dir / "advanced_analysis_seasonal.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: advanced_analysis_seasonal.png")
plt.close()

# ============================================================================
# 3. ANOMALY DETECTION
# ============================================================================
print("\n[3/6] Anomaly detection...")
print("-" * 80)

# Detect anomalies using Z-score method
anomalies = []

for ingredient in consumption_pivot.columns:
    values = consumption_pivot[ingredient].dropna()
    if len(values) > 2:
        mean = values.mean()
        std = values.std()
        if std > 0:
            z_scores = np.abs((values - mean) / std)
            anomaly_mask = z_scores > 2  # Threshold: 2 standard deviations
            
            if anomaly_mask.any():
                for month in values[anomaly_mask].index:
                    z_score = z_scores[month]
                    anomalies.append({
                        'ingredient': ingredient,
                        'month': month,
                        'consumption': values[month],
                        'z_score': z_score,
                        'deviation': (values[month] - mean) / mean * 100
                    })

if anomalies:
    anomalies_df = pd.DataFrame(anomalies)
    print(f"\nDetected {len(anomalies)} anomalies:")
    for _, row in anomalies_df.nlargest(10, 'z_score').iterrows():
        print(f"  {row['ingredient']} in {row['month']}: Z-score={row['z_score']:.2f}, "
              f"Deviation={row['deviation']:+.1f}%")
    
    anomalies_df.to_csv(output_dir / "detected_anomalies.csv", index=False)
    print(f"✓ Saved: detected_anomalies.csv")
else:
    print("  No significant anomalies detected")

# ============================================================================
# 4. INVENTORY OPTIMIZATION ANALYSIS
# ============================================================================
print("\n[4/6] Inventory optimization analysis...")
print("-" * 80)

# Calculate reorder points and safety stock
inventory_analysis = []

for _, row in ingredient_summary.iterrows():
    ingredient = row['ingredient']
    avg_monthly = row['avg_monthly_consumption']
    
    # Get monthly consumption for this ingredient
    ingredient_consumption = consumption_monthly[consumption_monthly['ingredient'] == ingredient]
    
    if len(ingredient_consumption) > 0:
        std_monthly = ingredient_consumption['total_consumption'].std()
        max_monthly = ingredient_consumption['total_consumption'].max()
        min_monthly = ingredient_consumption['total_consumption'].min()
        
        # Calculate safety stock (assuming 1 month lead time, 95% service level)
        safety_stock = 1.65 * std_monthly if std_monthly > 0 else avg_monthly * 0.2
        
        # Reorder point = average consumption + safety stock
        reorder_point = avg_monthly + safety_stock
        
        # Get shipment info if available
        shipment_info = consumption_with_shipments[
            consumption_with_shipments['ingredient'] == ingredient
        ].iloc[0] if len(consumption_with_shipments[
            consumption_with_shipments['ingredient'] == ingredient
        ]) > 0 else None
        
        inventory_analysis.append({
            'ingredient': ingredient,
            'avg_monthly_consumption': avg_monthly,
            'std_monthly_consumption': std_monthly,
            'max_monthly_consumption': max_monthly,
            'min_monthly_consumption': min_monthly,
            'safety_stock': safety_stock,
            'reorder_point': reorder_point,
            'has_shipment_data': row['has_shipment_data'],
            'frequency': shipment_info['frequency'] if shipment_info is not None and pd.notna(shipment_info['frequency']) else None,
            'quantity_per_shipment': shipment_info['quantity_per_shipment'] if shipment_info is not None and pd.notna(shipment_info['quantity_per_shipment']) else None
        })

inventory_df = pd.DataFrame(inventory_analysis)

# Identify ingredients at risk
inventory_df['risk_level'] = inventory_df.apply(lambda row: 
    'HIGH' if row['std_monthly_consumption'] > row['avg_monthly_consumption'] * 0.5 
    else 'MEDIUM' if row['std_monthly_consumption'] > row['avg_monthly_consumption'] * 0.3
    else 'LOW', axis=1)

print(f"\nInventory Risk Levels:")
risk_counts = inventory_df['risk_level'].value_counts()
for level, count in risk_counts.items():
    print(f"  {level}: {count} ingredients")

high_risk = inventory_df[inventory_df['risk_level'] == 'HIGH']
if len(high_risk) > 0:
    print(f"\nHigh Risk Ingredients (high volatility):")
    for _, row in high_risk.iterrows():
        print(f"  {row['ingredient']}: CV={row['std_monthly_consumption']/row['avg_monthly_consumption']:.2f}")

inventory_df.to_csv(output_dir / "inventory_optimization.csv", index=False)
print(f"✓ Saved: inventory_optimization.csv")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Risk level distribution
risk_colors = {'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'green'}
risk_counts.plot(kind='bar', ax=axes[0], color=[risk_colors.get(level, 'gray') for level in risk_counts.index])
axes[0].set_title('Ingredient Risk Level Distribution', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Risk Level')
axes[0].set_ylabel('Number of Ingredients')
axes[0].grid(True, alpha=0.3, axis='y')
axes[0].tick_params(axis='x', rotation=0)

# Reorder points for top ingredients
top_10_reorder = inventory_df.nlargest(10, 'reorder_point')
axes[1].barh(range(len(top_10_reorder)), top_10_reorder['reorder_point'], 
             color=sns.color_palette("viridis", len(top_10_reorder)))
axes[1].set_yticks(range(len(top_10_reorder)))
axes[1].set_yticklabels(top_10_reorder['ingredient'])
axes[1].set_title('Top 10 Ingredients - Recommended Reorder Points', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Reorder Point (Monthly Consumption + Safety Stock)')
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(output_dir / "advanced_analysis_inventory.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: advanced_analysis_inventory.png")
plt.close()

# ============================================================================
# 5. FORECASTING PREPARATION
# ============================================================================
print("\n[5/6] Forecasting preparation...")
print("-" * 80)

# Prepare time series data for forecasting
forecast_data = []

for ingredient in consumption_pivot.columns:
    values = consumption_pivot[ingredient].dropna()
    if len(values) >= 4:  # Need at least 4 data points
        # Calculate trend
        x = np.arange(len(values))
        trend_coef = np.polyfit(x, values, 1)[0]
        
        # Calculate seasonality (if we had more data)
        # For now, calculate month-over-month change
        if len(values) > 1:
            avg_change = np.mean(np.diff(values))
        else:
            avg_change = 0
        
        forecast_data.append({
            'ingredient': ingredient,
            'trend_slope': trend_coef,
            'avg_monthly_change': avg_change,
            'last_value': values.iloc[-1],
            'forecast_next_month': values.iloc[-1] + avg_change,
            'volatility': values.std() / values.mean() if values.mean() > 0 else 0
        })

forecast_df = pd.DataFrame(forecast_data)
forecast_df = forecast_df.sort_values('forecast_next_month', ascending=False)

print(f"\nTop 5 Ingredients - Next Month Forecast:")
for _, row in forecast_df.head(5).iterrows():
    print(f"  {row['ingredient']}: {row['forecast_next_month']:,.0f} "
          f"(trend: {row['trend_slope']:+.0f}/month)")

forecast_df.to_csv(output_dir / "forecasting_data.csv", index=False)
print(f"✓ Saved: forecasting_data.csv")

# ============================================================================
# 6. COST EFFICIENCY ANALYSIS
# ============================================================================
print("\n[6/6] Cost efficiency analysis...")
print("-" * 80)

# Calculate revenue per unit of consumption
efficiency_analysis = consumption_monthly.groupby('ingredient').agg({
    'total_consumption': 'sum',
    'revenue': 'sum'
})

efficiency_analysis['revenue_per_unit'] = efficiency_analysis['revenue'] / efficiency_analysis['total_consumption']
efficiency_analysis = efficiency_analysis.sort_values('revenue_per_unit', ascending=False)

print(f"\nTop 5 Most Cost-Efficient Ingredients (Revenue per Unit):")
for ingredient, row in efficiency_analysis.head(5).iterrows():
    print(f"  {ingredient}: ${row['revenue_per_unit']:.4f} per unit")

efficiency_analysis.to_csv(output_dir / "cost_efficiency.csv", index=False)
print(f"✓ Saved: cost_efficiency.csv")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Revenue per unit
top_10_efficiency = efficiency_analysis.head(10)
axes[0].barh(range(len(top_10_efficiency)), top_10_efficiency['revenue_per_unit'], 
             color=sns.color_palette("coolwarm", len(top_10_efficiency)))
axes[0].set_yticks(range(len(top_10_efficiency)))
axes[0].set_yticklabels(top_10_efficiency.index)
axes[0].set_title('Top 10 Ingredients - Revenue per Unit of Consumption', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Revenue per Unit ($)')
axes[0].grid(True, alpha=0.3, axis='x')

# Total revenue vs consumption
axes[1].scatter(efficiency_analysis['total_consumption'], efficiency_analysis['revenue'], 
                s=100, alpha=0.6, c=efficiency_analysis['revenue_per_unit'], 
                cmap='viridis', edgecolors='black', linewidth=1)
axes[1].set_xlabel('Total Consumption')
axes[1].set_ylabel('Total Revenue ($)')
axes[1].set_title('Consumption vs Revenue (Color = Efficiency)', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)
cbar = plt.colorbar(axes[1].collections[0], ax=axes[1])
cbar.set_label('Revenue per Unit ($)')

plt.tight_layout()
plt.savefig(output_dir / "advanced_analysis_efficiency.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: advanced_analysis_efficiency.png")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("ADVANCED ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\nAll outputs saved to: {output_dir}")
print("\nGenerated Files:")
print("  1. advanced_analysis_seasonal.png - Seasonal patterns and growth")
print("  2. advanced_analysis_inventory.png - Inventory optimization")
print("  3. advanced_analysis_efficiency.png - Cost efficiency analysis")
print("  4. detected_anomalies.csv - Anomaly detection results")
print("  5. inventory_optimization.csv - Reorder points and safety stock")
print("  6. forecasting_data.csv - Forecasting preparation")
print("  7. cost_efficiency.csv - Revenue efficiency metrics")
print("\n" + "=" * 80)


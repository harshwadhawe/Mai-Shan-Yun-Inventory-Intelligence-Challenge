#!/usr/bin/env python3
"""
Exploratory Data Analysis (EDA) for MSY Inventory Intelligence Challenge
Comprehensive analysis of sales, consumption, and inventory patterns
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
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Get directories
base_dir = Path(__file__).parent
cleaned_dir = base_dir / "cleaned_data"
processed_dir = base_dir / "processed_data"
output_dir = base_dir / "eda_output"
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1/8] Loading data...")
print("-" * 80)

# Load processed data
consumption_monthly = pd.read_csv(processed_dir / "ingredient_consumption_monthly.csv")
consumption_detailed = pd.read_csv(processed_dir / "ingredient_consumption_detailed.csv")
ingredient_summary = pd.read_csv(processed_dir / "ingredient_summary.csv")
consumption_with_shipments = pd.read_csv(processed_dir / "ingredient_consumption_with_shipments.csv")
item_sales = pd.read_csv(processed_dir / "item_sales_with_ingredients.csv")
monthly_sales_item = pd.read_csv(cleaned_dir / "monthly_sales_item.csv")

print(f"✓ Loaded {len(consumption_monthly)} monthly consumption records")
print(f"✓ Loaded {len(ingredient_summary)} ingredients")
print(f"✓ Loaded {len(item_sales)} item sales records")

# ============================================================================
# 2. BASIC STATISTICS
# ============================================================================
print("\n[2/8] Calculating basic statistics...")
print("-" * 80)

# Month order
month_order = ['May', 'June', 'July', 'August', 'September', 'October']

# Overall statistics
stats = {
    'total_revenue': monthly_sales_item['Amount'].sum(),
    'total_items_sold': monthly_sales_item['Count'].sum(),
    'unique_items': monthly_sales_item['level_name'].nunique(),
    'unique_ingredients': len(ingredient_summary),
    'months_analyzed': monthly_sales_item['month'].nunique(),
    'avg_monthly_revenue': monthly_sales_item.groupby('month')['Amount'].sum().mean(),
    'avg_monthly_items': monthly_sales_item.groupby('month')['Count'].sum().mean(),
}

print("\nOverall Statistics:")
for key, value in stats.items():
    if isinstance(value, float):
        print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}" if 'revenue' in key else f"  {key.replace('_', ' ').title()}: {value:,.0f}")
    else:
        print(f"  {key.replace('_', ' ').title()}: {value}")

# ============================================================================
# 3. TIME SERIES ANALYSIS
# ============================================================================
print("\n[3/8] Time series analysis...")
print("-" * 80)

# Monthly revenue trend
monthly_revenue = monthly_sales_item.groupby('month')['Amount'].sum().reindex(month_order)
monthly_items = monthly_sales_item.groupby('month')['Count'].sum().reindex(month_order)

print("\nMonthly Revenue Trend:")
for month, revenue in monthly_revenue.items():
    print(f"  {month}: ${revenue:,.2f}")

print("\nMonthly Items Sold Trend:")
for month, count in monthly_items.items():
    print(f"  {month}: {count:,} items")

# Revenue trend visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Revenue over time
axes[0].plot(monthly_revenue.index, monthly_revenue.values, marker='o', linewidth=2, markersize=8, color='#2E86AB')
axes[0].fill_between(monthly_revenue.index, monthly_revenue.values, alpha=0.3, color='#2E86AB')
axes[0].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Revenue ($)')
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Items sold over time
axes[1].plot(monthly_items.index, monthly_items.values, marker='s', linewidth=2, markersize=8, color='#A23B72')
axes[1].fill_between(monthly_items.index, monthly_items.values, alpha=0.3, color='#A23B72')
axes[1].set_title('Monthly Items Sold Trend', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Items Sold')
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(output_dir / "monthly_trends.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: monthly_trends.png")
plt.close()

# ============================================================================
# 4. INGREDIENT CONSUMPTION ANALYSIS
# ============================================================================
print("\n[4/8] Ingredient consumption analysis...")
print("-" * 80)

# Top ingredients by total consumption
top_ingredients = ingredient_summary.nlargest(10, 'total_consumption_6months')

print("\nTop 10 Ingredients by Total Consumption:")
for idx, row in top_ingredients.iterrows():
    print(f"  {row['ingredient']}: {row['total_consumption_6months']:,.0f} (avg: {row['avg_monthly_consumption']:,.0f}/month)")

# Consumption trend by ingredient
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Top 5 ingredients consumption over time
top_5_ingredients = top_ingredients.head(5)['ingredient'].values
consumption_pivot = consumption_monthly.pivot(index='month', columns='ingredient', values='total_consumption')
consumption_pivot = consumption_pivot.reindex(month_order)

for ingredient in top_5_ingredients:
    if ingredient in consumption_pivot.columns:
        axes[0, 0].plot(consumption_pivot.index, consumption_pivot[ingredient], 
                        marker='o', label=ingredient, linewidth=2)

axes[0, 0].set_title('Top 5 Ingredients - Consumption Over Time', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Consumption')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# Total consumption by ingredient (bar chart)
top_10_consumption = top_ingredients.head(10)
axes[0, 1].barh(range(len(top_10_consumption)), top_10_consumption['total_consumption_6months'], 
                color=sns.color_palette("viridis", len(top_10_consumption)))
axes[0, 1].set_yticks(range(len(top_10_consumption)))
axes[0, 1].set_yticklabels(top_10_consumption['ingredient'])
axes[0, 1].set_title('Top 10 Ingredients - Total Consumption (6 Months)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Total Consumption')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# Average monthly consumption
axes[1, 0].barh(range(len(top_10_consumption)), top_10_consumption['avg_monthly_consumption'], 
                color=sns.color_palette("plasma", len(top_10_consumption)))
axes[1, 0].set_yticks(range(len(top_10_consumption)))
axes[1, 0].set_yticklabels(top_10_consumption['ingredient'])
axes[1, 0].set_title('Top 10 Ingredients - Average Monthly Consumption', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Average Monthly Consumption')
axes[1, 0].grid(True, alpha=0.3, axis='x')

# Consumption vs Revenue correlation
ingredient_revenue = consumption_monthly.groupby('ingredient')['revenue'].sum().sort_values(ascending=False).head(10)
axes[1, 1].barh(range(len(ingredient_revenue)), ingredient_revenue.values, 
                color=sns.color_palette("coolwarm", len(ingredient_revenue)))
axes[1, 1].set_yticks(range(len(ingredient_revenue)))
axes[1, 1].set_yticklabels(ingredient_revenue.index)
axes[1, 1].set_title('Top 10 Ingredients - Total Revenue Contribution', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Total Revenue ($)')
axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(output_dir / "ingredient_analysis.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: ingredient_analysis.png")
plt.close()

# ============================================================================
# 5. TOP ITEMS ANALYSIS
# ============================================================================
print("\n[5/8] Top items analysis...")
print("-" * 80)

# Top items by revenue
top_items_revenue = monthly_sales_item.groupby('level_name').agg({
    'Amount': 'sum',
    'Count': 'sum'
}).sort_values('Amount', ascending=False).head(15)

print("\nTop 15 Items by Total Revenue:")
for item, row in top_items_revenue.iterrows():
    print(f"  {item}: ${row['Amount']:,.2f} ({row['Count']:,} sold)")

# Top items by quantity
top_items_count = monthly_sales_item.groupby('level_name')['Count'].sum().sort_values(ascending=False).head(15)

# Visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 12))

# Top items by revenue
top_15_revenue = top_items_revenue.head(15)
axes[0].barh(range(len(top_15_revenue)), top_15_revenue['Amount'], 
             color=sns.color_palette("mako", len(top_15_revenue)))
axes[0].set_yticks(range(len(top_15_revenue)))
axes[0].set_yticklabels([name[:40] + '...' if len(name) > 40 else name for name in top_15_revenue.index])
axes[0].set_title('Top 15 Items by Total Revenue', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Total Revenue ($)')
axes[0].grid(True, alpha=0.3, axis='x')

# Top items by quantity
top_15_count = top_items_count.head(15)
axes[1].barh(range(len(top_15_count)), top_15_count.values, 
             color=sns.color_palette("rocket", len(top_15_count)))
axes[1].set_yticks(range(len(top_15_count)))
axes[1].set_yticklabels([name[:40] + '...' if len(name) > 40 else name for name in top_15_count.index])
axes[1].set_title('Top 15 Items by Total Quantity Sold', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Total Quantity Sold')
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(output_dir / "top_items_analysis.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: top_items_analysis.png")
plt.close()

# ============================================================================
# 6. INVENTORY & SHIPMENT ANALYSIS
# ============================================================================
print("\n[6/8] Inventory & shipment analysis...")
print("-" * 80)

# Ingredients with shipment data
ingredients_with_shipments = ingredient_summary[ingredient_summary['has_shipment_data'] == True]
print(f"\nIngredients with shipment data: {len(ingredients_with_shipments)}")

# Calculate consumption vs shipment frequency
shipment_analysis = consumption_with_shipments[consumption_with_shipments['frequency'].notna()].copy()

if len(shipment_analysis) > 0:
    # Group by ingredient and frequency
    freq_analysis = shipment_analysis.groupby(['ingredient', 'frequency']).agg({
        'total_consumption': 'mean',
        'estimated_shipments_needed': 'mean'
    }).reset_index()
    
    print("\nAverage Monthly Consumption by Shipment Frequency:")
    for freq in ['weekly', 'biweekly', 'monthly']:
        freq_data = freq_analysis[freq_analysis['frequency'] == freq]
        if len(freq_data) > 0:
            avg_consumption = freq_data['total_consumption'].mean()
            print(f"  {freq}: {avg_consumption:,.0f} (avg across {len(freq_data)} ingredients)")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Ingredients with vs without shipment data
shipment_status = ingredient_summary['has_shipment_data'].value_counts()
axes[0].pie(shipment_status.values, labels=['With Shipment Data', 'Without Shipment Data'], 
            autopct='%1.1f%%', startangle=90, colors=['#2E86AB', '#A23B72'])
axes[0].set_title('Ingredients: Shipment Data Availability', fontsize=12, fontweight='bold')

# Shipment frequency distribution
if len(ingredients_with_shipments) > 0:
    freq_dist = ingredients_with_shipments['frequency'].value_counts()
    axes[1].bar(freq_dist.index, freq_dist.values, color=sns.color_palette("Set2", len(freq_dist)))
    axes[1].set_title('Shipment Frequency Distribution', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Frequency')
    axes[1].set_ylabel('Number of Ingredients')
    axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / "inventory_analysis.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: inventory_analysis.png")
plt.close()

# ============================================================================
# 7. CORRELATION ANALYSIS
# ============================================================================
print("\n[7/8] Correlation analysis...")
print("-" * 80)

# Consumption vs Revenue correlation
consumption_revenue_corr = consumption_monthly.groupby('ingredient').agg({
    'total_consumption': 'sum',
    'revenue': 'sum'
}).corr().iloc[0, 1]

print(f"\nConsumption vs Revenue Correlation: {consumption_revenue_corr:.3f}")

# Monthly correlation
monthly_corr = consumption_monthly.groupby('month').agg({
    'total_consumption': 'sum',
    'revenue': 'sum'
}).corr().iloc[0, 1]

print(f"Monthly Consumption vs Revenue Correlation: {monthly_corr:.3f}")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Consumption vs Revenue scatter
ingredient_totals = consumption_monthly.groupby('ingredient').agg({
    'total_consumption': 'sum',
    'revenue': 'sum'
})

axes[0].scatter(ingredient_totals['total_consumption'], ingredient_totals['revenue'], 
                s=100, alpha=0.6, color='#2E86AB')
axes[0].set_xlabel('Total Consumption')
axes[0].set_ylabel('Total Revenue ($)')
axes[0].set_title('Ingredient Consumption vs Revenue', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(ingredient_totals['total_consumption'], ingredient_totals['revenue'], 1)
p = np.poly1d(z)
axes[0].plot(ingredient_totals['total_consumption'], p(ingredient_totals['total_consumption']), 
              "r--", alpha=0.8, linewidth=2, label=f'Trend (r={consumption_revenue_corr:.3f})')
axes[0].legend()

# Monthly consumption vs revenue
monthly_totals = consumption_monthly.groupby('month').agg({
    'total_consumption': 'sum',
    'revenue': 'sum'
}).reindex(month_order)

axes[1].scatter(monthly_totals['total_consumption'], monthly_totals['revenue'], 
                s=200, alpha=0.7, color='#A23B72', marker='s')
for month in monthly_totals.index:
    axes[1].annotate(month, (monthly_totals.loc[month, 'total_consumption'], 
                             monthly_totals.loc[month, 'revenue']), 
                     fontsize=9, ha='center')
axes[1].set_xlabel('Total Consumption')
axes[1].set_ylabel('Total Revenue ($)')
axes[1].set_title('Monthly Consumption vs Revenue', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "correlation_analysis.png", dpi=300, bbox_inches='tight')
print(f"✓ Saved: correlation_analysis.png")
plt.close()

# ============================================================================
# 8. KEY INSIGHTS & SUMMARY
# ============================================================================
print("\n[8/8] Generating insights and summary...")
print("-" * 80)

# Calculate growth rates
revenue_growth = ((monthly_revenue.iloc[-1] - monthly_revenue.iloc[0]) / monthly_revenue.iloc[0]) * 100
items_growth = ((monthly_items.iloc[-1] - monthly_items.iloc[0]) / monthly_items.iloc[0]) * 100

# Find most volatile ingredients
ingredient_volatility = consumption_monthly.groupby('ingredient')['total_consumption'].std() / \
                       consumption_monthly.groupby('ingredient')['total_consumption'].mean()
most_volatile = ingredient_volatility.nlargest(5)

# Generate insights report
insights = f"""
================================================================================
EDA KEY INSIGHTS & SUMMARY
================================================================================

OVERALL PERFORMANCE:
  • Total Revenue (6 months): ${stats['total_revenue']:,.2f}
  • Total Items Sold: {stats['total_items_sold']:,.0f}
  • Average Monthly Revenue: ${stats['avg_monthly_revenue']:,.2f}
  • Average Monthly Items: {stats['avg_monthly_items']:,.0f}

GROWTH TRENDS:
  • Revenue Growth (May to October): {revenue_growth:.1f}%
  • Items Sold Growth (May to October): {items_growth:.1f}%

TOP PERFORMERS:
  • Highest Revenue Item: {top_items_revenue.index[0]} (${top_items_revenue.iloc[0]['Amount']:,.2f})
  • Most Sold Item: {top_items_count.index[0]} ({top_items_count.iloc[0]:,.0f} units)
  • Highest Consumption Ingredient: {top_ingredients.iloc[0]['ingredient']} ({top_ingredients.iloc[0]['total_consumption_6months']:,.0f})

INGREDIENT INSIGHTS:
  • Ingredients with shipment data: {len(ingredients_with_shipments)}/{len(ingredient_summary)}
  • Most volatile ingredient: {most_volatile.index[0]} (CV: {most_volatile.iloc[0]:.2f})
  • Consumption-Revenue Correlation: {consumption_revenue_corr:.3f}

INVENTORY MANAGEMENT:
  • Ingredients needing attention (no shipment data): {len(ingredient_summary) - len(ingredients_with_shipments)}
  • Weekly shipments: {len(ingredients_with_shipments[ingredients_with_shipments['frequency'] == 'weekly'])} ingredients
  • Biweekly shipments: {len(ingredients_with_shipments[ingredients_with_shipments['frequency'] == 'biweekly'])} ingredients
  • Monthly shipments: {len(ingredients_with_shipments[ingredients_with_shipments['frequency'] == 'monthly'])} ingredients

RECOMMENDATIONS:
  1. Monitor {most_volatile.index[0]} closely due to high consumption volatility
  2. Consider adding shipment tracking for ingredients without data
  3. Focus inventory optimization on top 5 consuming ingredients
  4. Analyze seasonal patterns for better forecasting

================================================================================
"""

print(insights)

# Save insights to file
with open(output_dir / "eda_insights.txt", 'w') as f:
    f.write(insights)

# Save summary statistics
summary_stats = pd.DataFrame([stats])
summary_stats.to_csv(output_dir / "summary_statistics.csv", index=False)

print(f"✓ Saved: eda_insights.txt")
print(f"✓ Saved: summary_statistics.csv")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("EDA COMPLETE!")
print("=" * 80)
print(f"\nAll outputs saved to: {output_dir}")
print("\nGenerated Files:")
print("  1. monthly_trends.png - Revenue and items sold trends")
print("  2. ingredient_analysis.png - Ingredient consumption analysis")
print("  3. top_items_analysis.png - Top performing items")
print("  4. inventory_analysis.png - Inventory and shipment analysis")
print("  5. correlation_analysis.png - Correlation visualizations")
print("  6. eda_insights.txt - Key insights and recommendations")
print("  7. summary_statistics.csv - Summary statistics")
print("\n" + "=" * 80)


#!/usr/bin/env python3
"""
Intermediate Processing Script for MSY Inventory Intelligence Challenge
This script combines all cleaned data into unified datasets for dashboard use.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Get directories
base_dir = Path(__file__).parent
cleaned_dir = base_dir / "cleaned_data"
output_dir = base_dir / "processed_data"
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("INTERMEDIATE DATA PROCESSING")
print("=" * 80)

# ============================================================================
# 1. LOAD CLEANED DATA
# ============================================================================
print("\n[1/5] Loading cleaned data...")
print("-" * 80)

ingredient_usage = pd.read_csv(cleaned_dir / "ingredient_usage_cleaned.csv")
monthly_sales_item = pd.read_csv(cleaned_dir / "monthly_sales_item.csv")
shipment_data = pd.read_csv(cleaned_dir / "shipment_data_cleaned.csv")

print(f"✓ Loaded ingredient usage: {ingredient_usage.shape}")
print(f"✓ Loaded monthly sales (item-level): {monthly_sales_item.shape}")
print(f"✓ Loaded shipment data: {shipment_data.shape}")

# ============================================================================
# 2. CREATE INGREDIENT CONSUMPTION BY MONTH
# ============================================================================
print("\n[2/5] Calculating ingredient consumption by month...")
print("-" * 80)

# Merge sales with ingredient usage
# Note: Need to match item names - some may not match exactly
sales_ingredients = monthly_sales_item.merge(
    ingredient_usage,
    left_on='level_name',
    right_on='item_name',
    how='left'
)

# Get all ingredient columns (excluding item_name)
ingredient_cols = [col for col in ingredient_usage.columns if col != 'item_name']

# Calculate consumption for each ingredient: sales_count * ingredient_per_item
consumption_data = []

for _, row in sales_ingredients.iterrows():
    if pd.isna(row['item_name']):
        # Item not found in ingredient usage - skip or handle separately
        continue
    
    month = row['month']
    sales_count = row['Count']
    
    for ingredient_col in ingredient_cols:
        ingredient_per_item = row[ingredient_col]
        if pd.notna(ingredient_per_item) and ingredient_per_item > 0:
            total_consumption = sales_count * ingredient_per_item
            
            consumption_data.append({
                'month': month,
                'item_name': row['item_name'],
                'sales_count': sales_count,
                'ingredient': ingredient_col,
                'consumption_per_item': ingredient_per_item,
                'total_consumption': total_consumption,
                'revenue': row['Amount']
            })

consumption_df = pd.DataFrame(consumption_data)

# Aggregate consumption by month and ingredient
monthly_consumption = consumption_df.groupby(['month', 'ingredient']).agg({
    'total_consumption': 'sum',
    'sales_count': 'sum',
    'revenue': 'sum'
}).reset_index()

# Add month order for sorting
month_order = ['May', 'June', 'July', 'August', 'September', 'October']
monthly_consumption['month_order'] = monthly_consumption['month'].map(
    {month: idx for idx, month in enumerate(month_order)}
)
monthly_consumption = monthly_consumption.sort_values(['month_order', 'ingredient']).drop('month_order', axis=1)

print(f"✓ Created consumption data: {consumption_df.shape}")
print(f"✓ Aggregated monthly consumption: {monthly_consumption.shape}")

# ============================================================================
# 3. CREATE INGREDIENT SUMMARY WITH SHIPMENT INFO
# ============================================================================
print("\n[3/5] Creating ingredient summary with shipment information...")
print("-" * 80)

# Get unique ingredients from consumption
all_ingredients = monthly_consumption['ingredient'].unique()

# Create ingredient summary
ingredient_summary = []

for ingredient in all_ingredients:
    # Get consumption stats
    ingredient_consumption = monthly_consumption[monthly_consumption['ingredient'] == ingredient]
    total_consumption = ingredient_consumption['total_consumption'].sum()
    avg_monthly_consumption = ingredient_consumption['total_consumption'].mean()
    months_active = len(ingredient_consumption)
    
    # Find matching shipment data
    shipment_match = shipment_data[shipment_data['ingredient_usage_column'] == ingredient]
    
    summary_row = {
        'ingredient': ingredient,
        'total_consumption_6months': total_consumption,
        'avg_monthly_consumption': avg_monthly_consumption,
        'months_active': months_active,
        'has_shipment_data': len(shipment_match) > 0
    }
    
    if len(shipment_match) > 0:
        shipment_row = shipment_match.iloc[0]
        summary_row.update({
            'shipment_ingredient_name': shipment_row['ingredient'],
            'quantity_per_shipment': shipment_row['quantity_per_shipment'],
            'unit': shipment_row['unit'],
            'num_shipments': shipment_row['num_shipments'],
            'frequency': shipment_row['frequency']
        })
    else:
        summary_row.update({
            'shipment_ingredient_name': None,
            'quantity_per_shipment': None,
            'unit': None,
            'num_shipments': None,
            'frequency': None
        })
    
    ingredient_summary.append(summary_row)

ingredient_summary_df = pd.DataFrame(ingredient_summary)

print(f"✓ Created ingredient summary: {ingredient_summary_df.shape}")

# ============================================================================
# 4. CREATE MONTHLY INGREDIENT CONSUMPTION WITH SHIPMENT DATA
# ============================================================================
print("\n[4/5] Merging consumption with shipment data...")
print("-" * 80)

# Merge monthly consumption with shipment data
monthly_consumption_with_shipment = monthly_consumption.merge(
    shipment_data[['ingredient_usage_column', 'quantity_per_shipment', 'unit', 'frequency', 'num_shipments']],
    left_on='ingredient',
    right_on='ingredient_usage_column',
    how='left'
)

# Calculate estimated shipments needed based on consumption
def calculate_shipments_needed(row):
    if pd.isna(row['quantity_per_shipment']) or row['quantity_per_shipment'] == 0:
        return None
    
    # Convert consumption to same unit (simplified - would need unit conversion in real scenario)
    consumption = row['total_consumption']
    quantity_per_shipment = row['quantity_per_shipment']
    
    # Estimate shipments needed (assuming same units for now)
    shipments_needed = consumption / quantity_per_shipment if quantity_per_shipment > 0 else None
    return shipments_needed

monthly_consumption_with_shipment['estimated_shipments_needed'] = monthly_consumption_with_shipment.apply(
    calculate_shipments_needed, axis=1
)

# Rename for clarity
monthly_consumption_with_shipment.rename(columns={
    'ingredient_usage_column': 'shipment_ingredient_name'
}, inplace=True)

print(f"✓ Merged consumption with shipment data: {monthly_consumption_with_shipment.shape}")

# ============================================================================
# 5. CREATE ITEM-LEVEL SALES WITH INGREDIENT USAGE
# ============================================================================
print("\n[5/5] Creating item-level sales with ingredient usage...")
print("-" * 80)

# Merge sales with ingredient usage for detailed analysis
item_sales_with_ingredients = monthly_sales_item.merge(
    ingredient_usage,
    left_on='level_name',
    right_on='item_name',
    how='left'
)

# Add flag for items with ingredient data
item_sales_with_ingredients['has_ingredient_data'] = item_sales_with_ingredients['item_name'].notna()

print(f"✓ Created item sales with ingredients: {item_sales_with_ingredients.shape}")

# ============================================================================
# 6. SAVE ALL PROCESSED DATA
# ============================================================================
print("\n[6/6] Saving processed data...")
print("-" * 80)

# Save detailed consumption data
consumption_df.to_csv(output_dir / "ingredient_consumption_detailed.csv", index=False)
print(f"✓ Saved: ingredient_consumption_detailed.csv ({consumption_df.shape})")

# Save monthly aggregated consumption
monthly_consumption.to_csv(output_dir / "ingredient_consumption_monthly.csv", index=False)
print(f"✓ Saved: ingredient_consumption_monthly.csv ({monthly_consumption.shape})")

# Save monthly consumption with shipment data
monthly_consumption_with_shipment.to_csv(
    output_dir / "ingredient_consumption_with_shipments.csv", 
    index=False
)
print(f"✓ Saved: ingredient_consumption_with_shipments.csv ({monthly_consumption_with_shipment.shape})")

# Save ingredient summary
ingredient_summary_df.to_csv(output_dir / "ingredient_summary.csv", index=False)
print(f"✓ Saved: ingredient_summary.csv ({ingredient_summary_df.shape})")

# Save item sales with ingredients
item_sales_with_ingredients.to_csv(output_dir / "item_sales_with_ingredients.csv", index=False)
print(f"✓ Saved: item_sales_with_ingredients.csv ({item_sales_with_ingredients.shape})")

# Create a comprehensive unified dataset
unified_data = {
    'consumption_detailed': consumption_df,
    'consumption_monthly': monthly_consumption,
    'consumption_with_shipments': monthly_consumption_with_shipment,
    'ingredient_summary': ingredient_summary_df,
    'item_sales': item_sales_with_ingredients
}

# Save as pickle for easy loading
import pickle
with open(output_dir / "unified_data.pkl", 'wb') as f:
    pickle.dump(unified_data, f)
print(f"✓ Saved: unified_data.pkl (all datasets combined)")

# ============================================================================
# PRINT SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("INTERMEDIATE PROCESSING COMPLETE!")
print("=" * 80)
print(f"\nProcessed data files saved to: {output_dir}")
print("\nFiles created:")
print("  1. ingredient_consumption_detailed.csv - Item-level consumption details")
print("  2. ingredient_consumption_monthly.csv - Monthly aggregated consumption")
print("  3. ingredient_consumption_with_shipments.csv - Consumption + shipment info")
print("  4. ingredient_summary.csv - Summary stats for each ingredient")
print("  5. item_sales_with_ingredients.csv - Sales data with ingredient usage")
print("  6. unified_data.pkl - All datasets in one pickle file")
print("\n" + "=" * 80)

# Print some statistics
print("\nKey Statistics:")
print(f"  • Total unique ingredients tracked: {len(all_ingredients)}")
print(f"  • Total items with sales data: {monthly_sales_item['level_name'].nunique()}")
print(f"  • Items matched with ingredient data: {item_sales_with_ingredients['has_ingredient_data'].sum()}")
print(f"  • Months of data: {monthly_sales_item['month'].nunique()}")
print(f"  • Total consumption records: {len(consumption_df)}")
print("\n" + "=" * 80)


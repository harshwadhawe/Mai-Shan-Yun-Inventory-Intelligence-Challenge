#!/usr/bin/env python3
"""
Comprehensive Data Cleaning Script for MSY Inventory Intelligence Challenge
This script cleans and standardizes all data files for the dashboard.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from datetime import datetime

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Get the base directory
base_dir = Path(__file__).parent
output_dir = base_dir / "cleaned_data"
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("MSY DATA CLEANING PROCESS")
print("=" * 80)

# ============================================================================
# 1. CLEAN INGREDIENT CSV
# ============================================================================
print("\n[1/4] Cleaning Ingredient Data...")
print("-" * 80)

ingredient_df = pd.read_csv(base_dir / "MSY Data - Ingredient.csv")

# Standardize column names (remove spaces, lowercase, consistent naming)
ingredient_df.columns = ingredient_df.columns.str.strip()
ingredient_df.rename(columns={
    'Item name': 'item_name',
    'braised beef used (g)': 'braised_beef_g',
    'Braised Chicken(g)': 'braised_chicken_g',
    'Braised Pork(g)': 'braised_pork_g',
    'Egg(count)': 'egg_count',
    'Rice(g)': 'rice_g',
    'Ramen (count)': 'ramen_count',
    'Rice Noodles(g)': 'rice_noodles_g',
    'chicken thigh (pcs)': 'chicken_thigh_pcs',
    'Chicken Wings (pcs)': 'chicken_wings_pcs',
    'flour (g)': 'flour_g',
    'Pickle Cabbage': 'pickle_cabbage',
    'Green Onion': 'green_onion',
    'Cilantro': 'cilantro',
    'White onion': 'white_onion',
    'Peas(g)': 'peas_g',
    'Carrot(g)': 'carrot_g',
    'Boychoy(g)': 'bokchoy_g',  # Fix typo
    'Tapioca Starch': 'tapioca_starch'
}, inplace=True)

# Replace NaN with 0 for ingredient quantities (missing means not used)
ingredient_df = ingredient_df.fillna(0)

# Ensure numeric columns are numeric
numeric_cols = ingredient_df.columns[1:]  # All except item_name
for col in numeric_cols:
    ingredient_df[col] = pd.to_numeric(ingredient_df[col], errors='coerce').fillna(0)

# Save cleaned ingredient data
ingredient_df.to_csv(output_dir / "ingredient_usage_cleaned.csv", index=False)
print(f"✓ Cleaned ingredient data: {ingredient_df.shape}")
print(f"  Saved to: {output_dir / 'ingredient_usage_cleaned.csv'}")

# ============================================================================
# 2. CLEAN SHIPMENT CSV
# ============================================================================
print("\n[2/4] Cleaning Shipment Data...")
print("-" * 80)

shipment_df = pd.read_csv(base_dir / "MSY Data - Shipment.csv")

# Standardize column names
shipment_df.columns = shipment_df.columns.str.strip()
shipment_df.rename(columns={
    'Ingredient': 'ingredient',
    'Quantity per shipment': 'quantity_per_shipment',
    'Unit of shipment': 'unit',
    'Number of shipments': 'num_shipments',
    'frequency': 'frequency'
}, inplace=True)

# Standardize frequency values (case-insensitive)
shipment_df['frequency'] = shipment_df['frequency'].str.strip().str.lower()
frequency_mapping = {
    'weekly': 'weekly',
    'biweekly': 'biweekly',
    'monthly': 'monthly'
}
shipment_df['frequency'] = shipment_df['frequency'].map(frequency_mapping).fillna(shipment_df['frequency'])

# Standardize ingredient names to match ingredient usage data
# Map shipment ingredients to ingredient usage columns
ingredient_mapping = {
    'Beef': 'braised_beef_g',
    'Chicken': 'braised_chicken_g',
    'Ramen': 'ramen_count',
    'Rice Noodles': 'rice_noodles_g',
    'Flour': 'flour_g',
    'Tapioca Starch': 'tapioca_starch',
    'Rice': 'rice_g',
    'Green Onion': 'green_onion',
    'White Onion': 'white_onion',
    'Cilantro': 'cilantro',
    'Egg': 'egg_count',
    'Peas + Carrot': 'peas_g',  # Note: This is combined in shipment but separate in usage
    'Bokchoy': 'bokchoy_g',
    'Chicken Wings': 'chicken_wings_pcs'
}

shipment_df['ingredient_usage_column'] = shipment_df['ingredient'].map(ingredient_mapping)

# Save cleaned shipment data
shipment_df.to_csv(output_dir / "shipment_data_cleaned.csv", index=False)
print(f"✓ Cleaned shipment data: {shipment_df.shape}")
print(f"  Saved to: {output_dir / 'shipment_data_cleaned.csv'}")

# ============================================================================
# 3. CLEAN MONTHLY SALES DATA (EXCEL FILES)
# ============================================================================
print("\n[3/4] Cleaning Monthly Sales Data...")
print("-" * 80)

monthly_files = {
    'May': 'May_Data_Matrix (1).xlsx',
    'June': 'June_Data_Matrix.xlsx',
    'July': 'July_Data_Matrix (1).xlsx',
    'August': 'August_Data_Matrix (1).xlsx',
    'September': 'September_Data_Matrix.xlsx',
    'October': 'October_Data_Matrix_20251103_214000.xlsx'
}

def clean_amount(amount_str):
    """Convert amount string like '$1,234.56' to float"""
    if pd.isna(amount_str):
        return 0.0
    if isinstance(amount_str, (int, float)):
        return float(amount_str)
    # Remove $ and commas, convert to float
    cleaned = str(amount_str).replace('$', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except:
        return 0.0

def clean_count(count_val):
    """Convert count string with commas to int"""
    if pd.isna(count_val):
        return 0
    if isinstance(count_val, (int, float)):
        return int(count_val)
    # Remove commas
    cleaned = str(count_val).replace(',', '').strip()
    try:
        return int(float(cleaned))
    except:
        return 0

all_monthly_data = []

for month, filename in monthly_files.items():
    file_path = base_dir / filename
    if not file_path.exists():
        print(f"  ⚠ Warning: {filename} not found, skipping...")
        continue
    
    print(f"  Processing {month}...")
    
    # Read all sheets
    excel_data = pd.read_excel(file_path, sheet_name=None)
    
    # Process each sheet
    for sheet_name, df in excel_data.items():
        # Standardize column names
        df.columns = df.columns.str.strip()
        
        # Clean Amount column
        if 'Amount' in df.columns:
            df['Amount'] = df['Amount'].apply(clean_amount)
        
        # Clean Count column
        if 'Count' in df.columns:
            df['Count'] = df['Count'].apply(clean_count)
        
        # Determine data level based on column names
        data_level = None
        level_column = None
        
        if 'Group' in df.columns:
            data_level = 'group'
            level_column = 'Group'
        elif 'Category' in df.columns:
            data_level = 'category'
            level_column = 'Category'
        elif 'Item Name' in df.columns:
            data_level = 'item'
            level_column = 'Item Name'
        
        # Standardize level column name
        if level_column:
            df.rename(columns={level_column: 'level_name'}, inplace=True)
        
        # Add metadata
        df['month'] = month
        df['data_level'] = data_level
        df['source_file'] = filename
        df['sheet_name'] = sheet_name
        
        # Select and reorder columns
        cols = ['month', 'data_level', 'level_name', 'Count', 'Amount', 'source_file', 'sheet_name']
        if 'source_page' in df.columns:
            cols.insert(-2, 'source_page')
        if 'source_table' in df.columns:
            cols.insert(-2, 'source_table')
        
        df = df[[c for c in cols if c in df.columns]]
        
        all_monthly_data.append(df)

# Combine all monthly data
if all_monthly_data:
    combined_monthly = pd.concat(all_monthly_data, ignore_index=True)
    
    # Save combined monthly data
    combined_monthly.to_csv(output_dir / "monthly_sales_combined.csv", index=False)
    print(f"✓ Combined monthly sales data: {combined_monthly.shape}")
    print(f"  Saved to: {output_dir / 'monthly_sales_combined.csv'}")
    
    # Also save separate files by data level
    for level in ['group', 'category', 'item']:
        level_data = combined_monthly[combined_monthly['data_level'] == level].copy()
        if not level_data.empty:
            level_data.to_csv(output_dir / f"monthly_sales_{level}.csv", index=False)
            print(f"  ✓ {level.capitalize()} level data: {level_data.shape}")

# ============================================================================
# 4. CREATE SUMMARY STATISTICS
# ============================================================================
print("\n[4/4] Generating Summary Statistics...")
print("-" * 80)

summary = {
    'ingredient_data': {
        'total_menu_items': len(ingredient_df),
        'total_ingredients': len(ingredient_df.columns) - 1,
        'ingredient_columns': list(ingredient_df.columns[1:])
    },
    'shipment_data': {
        'total_ingredients': len(shipment_df),
        'unique_frequencies': shipment_df['frequency'].unique().tolist()
    },
    'monthly_sales_data': {
        'months_processed': len(monthly_files),
        'total_records': len(combined_monthly) if all_monthly_data else 0,
        'date_range': f"{min(monthly_files.keys())} - {max(monthly_files.keys())}"
    }
}

# Save summary
import json
with open(output_dir / "data_summary.json", 'w') as f:
    json.dump(summary, f, indent=2)

print(f"✓ Summary statistics saved to: {output_dir / 'data_summary.json'}")

# ============================================================================
# PRINT FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("DATA CLEANING COMPLETE!")
print("=" * 80)
print(f"\nCleaned data files saved to: {output_dir}")
print("\nFiles created:")
print("  - ingredient_usage_cleaned.csv")
print("  - shipment_data_cleaned.csv")
print("  - monthly_sales_combined.csv")
print("  - monthly_sales_group.csv")
print("  - monthly_sales_category.csv")
print("  - monthly_sales_item.csv")
print("  - data_summary.json")
print("\n" + "=" * 80)


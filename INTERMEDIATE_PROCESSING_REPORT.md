# Intermediate Processing Report

## Overview
This report documents the intermediate processing step that combines all cleaned data into unified, analysis-ready datasets for the dashboard.

## Processing Pipeline

```
Cleaned Data → Intermediate Processing → Processed Data
     ↓                    ↓                      ↓
- ingredient_usage    - Merge sales with      - Unified datasets
- monthly_sales       - ingredient usage       - Ready for dashboard
- shipment_data       - Calculate consumption  - Analysis-ready
                      - Add shipment info
```

## Input Files (from `cleaned_data/`)

1. **ingredient_usage_cleaned.csv**: Menu items and their ingredient requirements
2. **monthly_sales_item.csv**: Item-level sales data by month
3. **shipment_data_cleaned.csv**: Shipment information for ingredients

## Processing Steps

### Step 1: Calculate Ingredient Consumption
- Merged sales data with ingredient usage data
- Calculated total consumption = sales_count × ingredient_per_item
- Created detailed consumption records for each item-ingredient combination

### Step 2: Aggregate Monthly Consumption
- Grouped consumption by month and ingredient
- Calculated total consumption, total sales, and total revenue per ingredient per month
- Created time series data for trend analysis

### Step 3: Merge with Shipment Data
- Joined consumption data with shipment information
- Added shipment frequency, quantity per shipment, and units
- Calculated estimated shipments needed based on consumption

### Step 4: Create Ingredient Summary
- Aggregated statistics for each ingredient:
  - Total consumption over 6 months
  - Average monthly consumption
  - Number of months with activity
  - Shipment information (if available)

### Step 5: Item Sales with Ingredients
- Merged sales data with ingredient usage
- Added flag for items with ingredient data
- Ready for item-level analysis

## Output Files (in `processed_data/`)

### 1. `ingredient_consumption_detailed.csv`
**Purpose**: Detailed item-level consumption records

**Columns**:
- `month`: Month of consumption
- `item_name`: Menu item name
- `sales_count`: Number of items sold
- `ingredient`: Ingredient column name
- `consumption_per_item`: Amount of ingredient per item
- `total_consumption`: Total consumption (sales_count × consumption_per_item)
- `revenue`: Revenue from sales

**Use Cases**:
- Item-level ingredient analysis
- Identifying which items drive ingredient consumption
- Cost analysis per item

**Shape**: 486 rows × 7 columns

---

### 2. `ingredient_consumption_monthly.csv`
**Purpose**: Monthly aggregated consumption by ingredient

**Columns**:
- `month`: Month
- `ingredient`: Ingredient column name
- `total_consumption`: Total consumption for the month
- `sales_count`: Total items sold (that use this ingredient)
- `revenue`: Total revenue from items using this ingredient

**Use Cases**:
- Time series analysis
- Trend identification
- Monthly consumption patterns
- Forecasting future needs

**Shape**: 84 rows × 5 columns (14 ingredients × 6 months)

---

### 3. `ingredient_consumption_with_shipments.csv`
**Purpose**: Monthly consumption merged with shipment information

**Columns**:
- All columns from `ingredient_consumption_monthly.csv`
- `shipment_ingredient_name`: Name from shipment data
- `quantity_per_shipment`: Quantity per shipment
- `unit`: Unit of measurement
- `frequency`: Shipment frequency (weekly/biweekly/monthly)
- `num_shipments`: Number of shipments
- `estimated_shipments_needed`: Calculated shipments needed based on consumption

**Use Cases**:
- Inventory management
- Reorder point analysis
- Shipment planning
- Comparing consumption vs. shipments

**Shape**: 84 rows × 11 columns

---

### 4. `ingredient_summary.csv`
**Purpose**: Summary statistics for each ingredient

**Columns**:
- `ingredient`: Ingredient column name
- `total_consumption_6months`: Total consumption over 6 months
- `avg_monthly_consumption`: Average monthly consumption
- `months_active`: Number of months with consumption
- `has_shipment_data`: Boolean indicating if shipment data exists
- `shipment_ingredient_name`: Name from shipment data (if available)
- `quantity_per_shipment`: Quantity per shipment (if available)
- `unit`: Unit of measurement (if available)
- `num_shipments`: Number of shipments (if available)
- `frequency`: Shipment frequency (if available)

**Use Cases**:
- Quick overview of ingredient usage
- Identifying high/low consumption ingredients
- Planning inventory levels
- Dashboard summary views

**Shape**: 14 rows × 10 columns

---

### 5. `item_sales_with_ingredients.csv`
**Purpose**: Sales data merged with ingredient usage

**Columns**:
- All columns from `monthly_sales_item.csv`
- All ingredient columns from `ingredient_usage_cleaned.csv`
- `has_ingredient_data`: Boolean flag for items with ingredient data

**Use Cases**:
- Item-level analysis
- Understanding which items use which ingredients
- Menu optimization
- Ingredient cost analysis per item

**Shape**: 667 rows × 29 columns

---

### 6. `unified_data.pkl`
**Purpose**: All datasets combined in a Python pickle file

**Contents**:
- Dictionary with keys:
  - `consumption_detailed`: Detailed consumption DataFrame
  - `consumption_monthly`: Monthly aggregated consumption DataFrame
  - `consumption_with_shipments`: Consumption with shipment data DataFrame
  - `ingredient_summary`: Ingredient summary DataFrame
  - `item_sales`: Item sales with ingredients DataFrame

**Use Cases**:
- Quick loading in Python scripts
- Dashboard data loading
- Analysis scripts

---

## Key Statistics

- **Total unique ingredients tracked**: 14
- **Total items with sales data**: 162
- **Items matched with ingredient data**: 78 (48%)
- **Months of data**: 6 (May - October)
- **Total consumption records**: 486

## Data Quality Notes

1. **Item Matching**: Not all items in sales data have matching ingredient usage data (78 out of 162 items matched). This is expected as some items may be:
   - New items not yet in ingredient database
   - Special items or combos
   - Items with different naming conventions

2. **Unit Conversion**: The `estimated_shipments_needed` calculation assumes same units between consumption and shipments. In a production system, proper unit conversion would be needed (e.g., grams to pounds).

3. **Missing Shipment Data**: Some ingredients have consumption data but no shipment data (e.g., braised_pork_g, carrot_g). These may need manual tracking or different data sources.

## Usage Examples

### Loading Processed Data in Python

```python
import pandas as pd
from pathlib import Path

# Load individual files
consumption = pd.read_csv('processed_data/ingredient_consumption_monthly.csv')
summary = pd.read_csv('processed_data/ingredient_summary.csv')

# Or load unified data
import pickle
with open('processed_data/unified_data.pkl', 'rb') as f:
    data = pickle.load(f)
    consumption = data['consumption_monthly']
    summary = data['ingredient_summary']
```

### Example Queries

**Top 5 ingredients by consumption:**
```python
top_ingredients = summary.nlargest(5, 'total_consumption_6months')
```

**Monthly trend for a specific ingredient:**
```python
beef_trend = consumption[consumption['ingredient'] == 'braised_beef_g']
```

**Items using a specific ingredient:**
```python
beef_items = item_sales[item_sales['braised_beef_g'] > 0]
```

## Next Steps

The processed data is now ready for:
1. **Dashboard Development**: All data is in dashboard-ready format
2. **Visualization**: Time series, trends, comparisons
3. **Predictive Analytics**: Forecasting future consumption
4. **Inventory Management**: Reorder point calculations
5. **Cost Analysis**: Ingredient cost per item

## Regenerating Processed Data

To regenerate all processed data files, run:
```bash
python3 intermediate_processing.py
```

This will recreate all files in the `processed_data/` directory.


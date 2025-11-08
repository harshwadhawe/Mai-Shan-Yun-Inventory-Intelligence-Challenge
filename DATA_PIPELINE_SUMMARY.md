# MSY Data Pipeline Summary

## Overview
This document provides a complete overview of the data processing pipeline for the Mai Shan Yun Inventory Intelligence Challenge.

## Pipeline Architecture

```
Raw Data → Data Cleaning → Intermediate Processing → Processed Data
   ↓            ↓                    ↓                    ↓
.xlsx      cleaned_data/      processed_data/      Dashboard Ready
.csv       - Standardized     - Unified datasets    - Analysis-ready
           - Cleaned          - Consumption calc    - Visualizations
           - Validated        - Shipment merged     - Forecasting
```

## Directory Structure

```
mai-shen-yun/
├── Raw Data Files
│   ├── *.xlsx (Monthly sales data)
│   ├── MSY Data - Ingredient.csv
│   └── MSY Data - Shipment.csv
│
├── cleaned_data/          # Step 1: Data Cleaning Output
│   ├── ingredient_usage_cleaned.csv
│   ├── shipment_data_cleaned.csv
│   ├── monthly_sales_combined.csv
│   ├── monthly_sales_group.csv
│   ├── monthly_sales_category.csv
│   ├── monthly_sales_item.csv
│   └── data_summary.json
│
└── processed_data/        # Step 2: Intermediate Processing Output
    ├── ingredient_consumption_detailed.csv
    ├── ingredient_consumption_monthly.csv
    ├── ingredient_consumption_with_shipments.csv
    ├── ingredient_summary.csv
    ├── item_sales_with_ingredients.csv
    └── unified_data.pkl
```

## Processing Steps

### Step 1: Data Cleaning (`data_cleaning.py`)

**Input**: Raw Excel and CSV files  
**Output**: `cleaned_data/` directory

**Actions**:
- Standardized column names (snake_case)
- Converted string numbers to proper numeric types
- Handled missing values
- Fixed data inconsistencies
- Combined monthly sales data

**Key Files Created**:
- `ingredient_usage_cleaned.csv`: 17 menu items × 18 ingredients
- `shipment_data_cleaned.csv`: 14 ingredients with shipment info
- `monthly_sales_combined.csv`: 795 records across 6 months

### Step 2: Intermediate Processing (`intermediate_processing.py`)

**Input**: Cleaned data from `cleaned_data/`  
**Output**: `processed_data/` directory

**Actions**:
- Merged sales with ingredient usage
- Calculated ingredient consumption (sales × usage)
- Aggregated consumption by month and ingredient
- Merged consumption with shipment data
- Created summary statistics

**Key Files Created**:
- `ingredient_consumption_monthly.csv`: 84 records (14 ingredients × 6 months)
- `ingredient_summary.csv`: 14 ingredients with summary stats
- `ingredient_consumption_with_shipments.csv`: Consumption + shipment planning
- `unified_data.pkl`: All datasets in one file

## Data Flow

### Ingredient Consumption Calculation

```
Sales Data (item, count) 
    × 
Ingredient Usage (item, ingredient, amount)
    =
Consumption (month, ingredient, total_consumption)
```

**Example**:
- Beef Tossed Ramen sold: 468 units in May
- Each uses: 140g braised beef
- Total consumption: 468 × 140 = 65,520g braised beef in May

### Shipment Integration

```
Consumption (month, ingredient, total)
    +
Shipment Data (ingredient, quantity_per_shipment, frequency)
    =
Planning Data (month, ingredient, consumption, shipments_needed)
```

## Key Metrics

### Data Volume
- **Menu Items**: 17 items with ingredient data
- **Ingredients Tracked**: 14 active ingredients
- **Sales Items**: 162 unique items in sales data
- **Matched Items**: 78 items (48% match rate)
- **Time Period**: 6 months (May - October)
- **Total Records**: 
  - Sales: 667 item-level records
  - Consumption: 486 detailed records
  - Monthly aggregation: 84 records

### Consumption Statistics
- **Highest Consumption**: braised_beef_g (609,540g over 6 months)
- **Most Active**: All 14 ingredients active in all 6 months
- **Average Monthly**: Varies by ingredient (983 - 101,590g)

## Usage Guide

### For Dashboard Development

**Recommended Files**:
1. `ingredient_consumption_monthly.csv` - For time series charts
2. `ingredient_summary.csv` - For summary cards/KPIs
3. `ingredient_consumption_with_shipments.csv` - For inventory alerts
4. `item_sales_with_ingredients.csv` - For item-level analysis

### For Analysis

**Python Example**:
```python
import pandas as pd

# Load processed data
consumption = pd.read_csv('processed_data/ingredient_consumption_monthly.csv')
summary = pd.read_csv('processed_data/ingredient_summary.csv')

# Time series analysis
beef_trend = consumption[consumption['ingredient'] == 'braised_beef_g']

# Top ingredients
top_5 = summary.nlargest(5, 'total_consumption_6months')
```

### For Forecasting

**Recommended Approach**:
1. Use `ingredient_consumption_monthly.csv` as time series input
2. Group by ingredient for individual forecasts
3. Consider seasonality (6 months of data)
4. Use shipment frequency for validation

## Running the Pipeline

### Complete Pipeline
```bash
# Step 1: Clean data
python3 data_cleaning.py

# Step 2: Process data
python3 intermediate_processing.py
```

### Individual Steps
```bash
# Explore raw data
python3 explore_data.py

# Clean only
python3 data_cleaning.py

# Process only (requires cleaned_data/)
python3 intermediate_processing.py
```

## Output Files Quick Reference

| File | Rows | Columns | Primary Use |
|------|------|---------|-------------|
| `ingredient_usage_cleaned.csv` | 17 | 19 | Menu item recipes |
| `shipment_data_cleaned.csv` | 14 | 6 | Shipment planning |
| `monthly_sales_item.csv` | 667 | 9 | Sales analysis |
| `ingredient_consumption_monthly.csv` | 84 | 5 | Time series, trends |
| `ingredient_summary.csv` | 14 | 10 | Summary stats, KPIs |
| `ingredient_consumption_with_shipments.csv` | 84 | 11 | Inventory management |
| `item_sales_with_ingredients.csv` | 667 | 29 | Item-level analysis |

## Next Steps

The processed data is ready for:

1. **Dashboard Development**
   - Interactive visualizations
   - Real-time inventory tracking
   - Trend analysis

2. **Predictive Analytics**
   - Forecast ingredient demand
   - Predict reorder dates
   - Seasonal pattern detection

3. **Inventory Optimization**
   - Identify overstocked items
   - Detect shortage risks
   - Optimize reorder points

4. **Cost Analysis**
   - Ingredient cost per item
   - Revenue per ingredient
   - Profitability analysis

## Documentation

- **Data Cleaning**: See `DATA_CLEANING_REPORT.md`
- **Intermediate Processing**: See `INTERMEDIATE_PROCESSING_REPORT.md`
- **This Summary**: Overview of entire pipeline

## Notes

- All data is cleaned and validated
- Missing values handled appropriately
- Units may need conversion for production use
- Some items don't have ingredient data (expected)
- Shipment data available for 10 out of 14 ingredients


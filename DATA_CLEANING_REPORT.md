# MSY Data Cleaning Report

## Overview
This report documents the data cleaning process for the Mai Shan Yun Inventory Intelligence Challenge dataset.

## Files Processed

### 1. CSV Files
- **MSY Data - Ingredient.csv**: Menu items and their ingredient usage
- **MSY Data - Shipment.csv**: Shipment information for ingredients

### 2. Excel Files (Monthly Sales Data)
- May_Data_Matrix (1).xlsx
- June_Data_Matrix.xlsx
- July_Data_Matrix (1).xlsx
- August_Data_Matrix (1).xlsx
- September_Data_Matrix.xlsx
- October_Data_Matrix_20251103_214000.xlsx

## Cleaning Steps Performed

### 1. Ingredient Usage Data (`ingredient_usage_cleaned.csv`)
**Original Issues:**
- Inconsistent column naming (mixed case, spaces, parentheses)
- Missing values (NaN) representing ingredients not used in menu items
- Typo: "Boychoy" should be "Bokchoy"

**Cleaning Actions:**
- Standardized all column names to snake_case format
- Replaced all NaN values with 0 (indicating ingredient not used)
- Fixed typo: "Boychoy" → "bokchoy_g"
- Ensured all numeric columns are properly typed as float64
- Renamed "Item name" to "item_name" for consistency

**Result:**
- 17 menu items
- 18 ingredient columns
- All missing values handled (0 = not used)

### 2. Shipment Data (`shipment_data_cleaned.csv`)
**Original Issues:**
- Inconsistent frequency values (e.g., "Biweekly" vs "biweekly")
- Need to map ingredients to ingredient usage columns

**Cleaning Actions:**
- Standardized column names to snake_case
- Normalized frequency values to lowercase
- Created mapping between shipment ingredients and ingredient usage columns
- Added `ingredient_usage_column` field for easy joining

**Result:**
- 14 ingredients with shipment information
- Standardized frequency values: weekly, biweekly, monthly
- Ready for joining with ingredient usage data

### 3. Monthly Sales Data (`monthly_sales_combined.csv`)
**Original Issues:**
- Amount values stored as strings with "$" and commas (e.g., "$1,234.56")
- Count values stored as strings with commas (e.g., "1,234")
- Inconsistent sheet structures across months
- October file has different sheet order (Category, Item, Group vs Group, Category, Item)

**Cleaning Actions:**
- Converted Amount strings to float (removed "$" and commas)
- Converted Count strings to integers (removed commas)
- Standardized column names across all files
- Identified data level (group, category, item) automatically
- Renamed level columns to "level_name" for consistency
- Added metadata columns: month, data_level, source_file, sheet_name
- Combined all monthly data into unified format

**Result:**
- 795 total records across 6 months
- 22 group-level records
- 106 category-level records
- 667 item-level records
- All numeric values properly converted

## Output Files

All cleaned data is saved in the `cleaned_data/` directory:

1. **ingredient_usage_cleaned.csv**: Cleaned menu item ingredient usage
2. **shipment_data_cleaned.csv**: Cleaned shipment information
3. **monthly_sales_combined.csv**: All monthly sales data combined
4. **monthly_sales_group.csv**: Group-level sales only
5. **monthly_sales_category.csv**: Category-level sales only
6. **monthly_sales_item.csv**: Item-level sales only
7. **data_summary.json**: Summary statistics and metadata

## Data Quality Improvements

### Before Cleaning:
- ❌ Inconsistent naming conventions
- ❌ String-formatted numbers
- ❌ Missing values as NaN
- ❌ Different structures across months
- ❌ No unified format

### After Cleaning:
- ✅ Consistent snake_case naming
- ✅ Proper numeric data types
- ✅ Missing values handled (0 for unused ingredients)
- ✅ Unified structure across all months
- ✅ Ready for analysis and visualization

## Next Steps

The cleaned data is now ready for:
1. **Dashboard Development**: All data is in a consistent, analysis-ready format
2. **Data Integration**: Easy to join ingredient usage with sales data
3. **Predictive Analytics**: Time series data ready for forecasting
4. **Visualization**: Clean numeric data for charts and graphs

## Usage

To regenerate cleaned data, run:
```bash
python3 data_cleaning.py
```

All cleaned files will be saved to the `cleaned_data/` directory.


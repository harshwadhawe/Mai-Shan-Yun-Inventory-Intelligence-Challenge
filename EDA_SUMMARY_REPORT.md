# Exploratory Data Analysis (EDA) Summary Report

## Overview
This report summarizes the comprehensive exploratory data analysis performed on the Mai Shan Yun restaurant data, covering sales trends, ingredient consumption, inventory management, and predictive insights.

## Analysis Components

### 1. Basic Statistics & Performance Metrics

**Overall Performance (6 months: May - October 2024):**
- **Total Revenue**: $367,367.58
- **Total Items Sold**: 47,916 items
- **Average Monthly Revenue**: $61,227.93
- **Average Monthly Items Sold**: 7,986 items
- **Unique Menu Items**: 162 items
- **Tracked Ingredients**: 14 active ingredients

**Growth Trends:**
- **Revenue Growth**: +12.5% (May to October)
- **Items Sold Growth**: +8.6% (May to October)
- Positive growth trajectory indicates healthy business expansion

### 2. Time Series Analysis

**Monthly Revenue Trend:**
- May: $65,083.90
- June: $42,527.32 (-34.7% decline)
- July: $46,095.19 (+8.4% recovery)
- August: $65,217.20 (+41.5% growth)
- September: $75,236.62 (+15.4% growth)
- October: $73,207.35 (-2.7% slight decline)

**Key Observations:**
- Significant dip in June (likely seasonal or operational)
- Strong recovery and growth in August-September
- Overall positive trend despite June setback
- Monthly revenue correlation with consumption: 0.991 (very strong)

### 3. Top Performers

**Top Revenue-Generating Items:**
1. Beef Ramen: $28,199.52 (1,854 sold)
2. Lunch Special: $24,783.14 (1,776 sold)
3. Beef Tossed Ramen: $24,316.12 (1,647 sold)
4. Chicken Ramen: $15,451.16 (1,056 sold)
5. Beef Tossed Rice Noodle: $14,058.42 (875 sold)

**Most Consumed Ingredients (6 months):**
1. Rice Noodles: 760,500 units
2. Braised Beef: 609,540 units
3. Braised Chicken: 520,860 units
4. Rice: 375,200 units
5. Braised Pork: 328,080 units

### 4. Ingredient Consumption Analysis

**Consumption Patterns:**
- **Highest Consumption**: Rice noodles lead with 126,750 units/month average
- **Most Volatile**: Carrot, Peas, Rice, White Onion (CV: 0.56) - require close monitoring
- **Stable Ingredients**: Most ingredients show consistent consumption patterns

**Growth Trends (May to October):**
- **Significant Growth (>20%):**
  - Carrot: +149.6%
  - Peas: +149.6%
  - Rice: +149.6%
  - White Onion: +149.6%

- **Significant Decline (>20%):**
  - Pickle Cabbage: -54.1%
  - Rice Noodles: -31.2%
  - Braised Beef: -27.8%
  - Bokchoy: -27.7%
  - Cilantro: -27.5%

### 5. Inventory & Shipment Analysis

**Shipment Data Coverage:**
- 11 out of 14 ingredients have shipment tracking data (78.6% coverage)
- **Missing shipment data for**: Braised Pork, Carrot, Pickle Cabbage

**Shipment Frequency Distribution:**
- **Weekly**: 8 ingredients (most common)
- **Biweekly**: 2 ingredients (Ramen, Rice)
- **Monthly**: 1 ingredient (Rice Noodles)

**Average Monthly Consumption by Frequency:**
- Weekly shipments: 38,682 units (avg)
- Biweekly shipments: 31,860 units (avg)
- Monthly shipments: 126,750 units (avg)

### 6. Inventory Risk Assessment

**Risk Level Distribution:**
- **LOW Risk**: 9 ingredients (stable consumption)
- **MEDIUM Risk**: 1 ingredient
- **HIGH Risk**: 4 ingredients (high volatility)
  - Carrot (CV: 0.56)
  - Peas (CV: 0.56)
  - Rice (CV: 0.56)
  - White Onion (CV: 0.56)

**Recommendations:**
- Implement tighter monitoring for high-risk ingredients
- Increase safety stock for volatile ingredients
- Review reorder points for ingredients with high CV

### 7. Cost Efficiency Analysis

**Most Cost-Efficient Ingredients (Revenue per Unit):**
1. Egg: $26.18 per unit
2. Ramen: $14.52 per unit
3. Carrot: $1.29 per unit
4. Peas: $1.29 per unit
5. Cilantro: $0.73 per unit

**Insights:**
- Eggs and ramen generate highest revenue per unit consumed
- Focus on items using these high-efficiency ingredients
- Consider menu optimization based on efficiency metrics

### 8. Forecasting Insights

**Next Month Forecast (November 2024):**
- **Rice**: 122,290 units (trend: +16,140/month) - **INCREASING**
- **Rice Noodles**: 106,920 units (trend: -4,209/month) - **DECREASING**
- **Braised Beef**: 90,928 units (trend: -3,604/month) - **DECREASING**
- **Braised Chicken**: 84,060 units (trend: -1,229/month) - **DECREASING**
- **Braised Pork**: 65,248 units (trend: +3,269/month) - **INCREASING**

**Key Forecasting Observations:**
- Rice consumption showing strong upward trend
- Rice noodles and beef showing declining trends
- Pork consumption increasing
- Use these trends for inventory planning

### 9. Correlation Analysis

**Key Correlations:**
- **Monthly Consumption vs Revenue**: 0.991 (very strong positive correlation)
- **Ingredient-level Consumption vs Revenue**: -0.159 (weak negative correlation)

**Interpretation:**
- Overall monthly consumption strongly predicts revenue
- Individual ingredient consumption doesn't directly correlate with revenue (menu mix effect)

### 10. Anomaly Detection

**Results:**
- No significant anomalies detected using Z-score method (threshold: 2σ)
- Data appears consistent across months
- No unusual spikes or drops requiring investigation

## Key Insights & Recommendations

### Business Insights

1. **Strong Growth Trajectory**
   - 12.5% revenue growth over 6 months
   - Business is expanding successfully
   - June dip was temporary, strong recovery

2. **Menu Performance**
   - Beef Ramen is top revenue generator
   - Ramen and noodle dishes dominate sales
   - Focus marketing on top performers

3. **Seasonal Patterns**
   - June shows significant decline (investigate cause)
   - August-September show peak performance
   - Plan inventory for seasonal variations

### Inventory Management Recommendations

1. **High-Priority Actions:**
   - Add shipment tracking for 3 missing ingredients (Braised Pork, Carrot, Pickle Cabbage)
   - Increase safety stock for 4 high-risk ingredients (Carrot, Peas, Rice, White Onion)
   - Monitor rice consumption closely (strong upward trend)

2. **Optimization Opportunities:**
   - Review reorder points for volatile ingredients
   - Adjust shipment frequencies based on consumption trends
   - Implement automated alerts for high-risk ingredients

3. **Forecasting Priorities:**
   - Focus on rice (increasing trend) - ensure adequate supply
   - Monitor rice noodles and beef (declining trends) - adjust ordering
   - Track pork consumption (increasing trend)

### Data Quality Observations

1. **Strengths:**
   - Comprehensive sales data across 6 months
   - Good ingredient usage mapping (78 items matched)
   - Strong shipment data coverage (78.6%)

2. **Areas for Improvement:**
   - 48% item match rate (some items lack ingredient data)
   - Missing shipment data for 3 ingredients
   - Need more historical data for better forecasting

## Visualizations Generated

1. **monthly_trends.png** - Revenue and items sold trends over time
2. **ingredient_analysis.png** - Ingredient consumption patterns and rankings
3. **top_items_analysis.png** - Top performing menu items
4. **inventory_analysis.png** - Shipment data and frequency distribution
5. **correlation_analysis.png** - Consumption vs revenue correlations
6. **advanced_analysis_seasonal.png** - Seasonal patterns and growth rates
7. **advanced_analysis_inventory.png** - Inventory risk levels and reorder points
8. **advanced_analysis_efficiency.png** - Cost efficiency metrics

## Data Files Generated

1. **summary_statistics.csv** - Overall performance metrics
2. **eda_insights.txt** - Key insights summary
3. **inventory_optimization.csv** - Reorder points and safety stock calculations
4. **forecasting_data.csv** - Next month forecasts and trends
5. **cost_efficiency.csv** - Revenue efficiency by ingredient
6. **detected_anomalies.csv** - Anomaly detection results (none found)

## Next Steps

1. **Dashboard Development**
   - Use processed data for interactive visualizations
   - Implement real-time inventory tracking
   - Create alert system for high-risk ingredients

2. **Predictive Analytics**
   - Build forecasting models using time series data
   - Implement demand prediction for next 3-6 months
   - Create reorder point optimization algorithm

3. **Inventory Optimization**
   - Implement automated reorder alerts
   - Optimize safety stock levels
   - Reduce waste through better forecasting

4. **Data Enhancement**
   - Add ingredient cost data for profitability analysis
   - Include supplier lead times for better planning
   - Track actual inventory levels for validation

## Conclusion

The EDA reveals a healthy, growing restaurant business with strong revenue trends. Key opportunities exist in inventory optimization, particularly for high-volatility ingredients. The data is well-structured and ready for advanced analytics and dashboard development.

**Overall Assessment**: Data quality is good, business performance is strong, and there are clear opportunities for inventory optimization and cost efficiency improvements.


# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Process Data (if not already done)
```bash
python3 data_cleaning.py
python3 intermediate_processing.py
python3 eda_analysis.py
python3 advanced_analysis.py
```

### Step 3: Run Dashboard
```bash
streamlit run dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 📊 Dashboard Sections

1. **📈 Overview** - Key metrics and trends
2. **🥘 Ingredient Insights** - Detailed ingredient analysis
3. **📦 Inventory Management** - Reorder alerts and optimization
4. **🔮 Predictive Analytics** - Forecasting and predictions
5. **💰 Cost Optimization** - Spending analysis
6. **📊 Sales Analysis** - Sales trends and impact

## 🎯 Key Features

- ✅ Interactive visualizations (hover, zoom, pan)
- ✅ Real-time inventory alerts
- ✅ Next month forecasting
- ✅ Cost efficiency analysis
- ✅ Sales impact tracking

## 📝 Notes

- All data is pre-processed and cached for fast performance
- Dashboard uses processed data from `processed_data/` and `eda_output/` directories
- Make sure all data processing scripts have been run before starting the dashboard


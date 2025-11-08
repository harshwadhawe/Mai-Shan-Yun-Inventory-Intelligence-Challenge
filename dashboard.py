#!/usr/bin/env python3
"""
MSY Inventory Intelligence Dashboard
Interactive dashboard for restaurant inventory management
Built with Streamlit for the Mai Shan Yun Challenge
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="MSY Inventory Intelligence Dashboard",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .alert-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load all processed data"""
    base_dir = Path(__file__).parent
    processed_dir = base_dir / "processed_data"
    cleaned_dir = base_dir / "cleaned_data"
    eda_dir = base_dir / "eda_output"
    
    data = {
        'consumption_monthly': pd.read_csv(processed_dir / "ingredient_consumption_monthly.csv"),
        'ingredient_summary': pd.read_csv(processed_dir / "ingredient_summary.csv"),
        'consumption_with_shipments': pd.read_csv(processed_dir / "ingredient_consumption_with_shipments.csv"),
        'item_sales': pd.read_csv(processed_dir / "item_sales_with_ingredients.csv"),
        'monthly_sales': pd.read_csv(cleaned_dir / "monthly_sales_item.csv"),
        'inventory_optimization': pd.read_csv(eda_dir / "inventory_optimization.csv"),
        'forecasting_data': pd.read_csv(eda_dir / "forecasting_data.csv"),
        'cost_efficiency': pd.read_csv(eda_dir / "cost_efficiency.csv")
    }
    return data

# Load data
data = load_data()

# Month order
month_order = ['May', 'June', 'July', 'August', 'September', 'October']

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<h1 class="main-header">🍜 MSY Inventory Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SIDEBAR - Navigation
# ============================================================================
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Dashboard Section",
    ["📈 Overview", "🥘 Ingredient Insights", "📦 Inventory Management", 
     "🔮 Predictive Analytics", "💰 Cost Optimization", "📊 Sales Analysis"]
)

# ============================================================================
# OVERVIEW PAGE
# ============================================================================
if page == "📈 Overview":
    st.header("📈 Dashboard Overview")
    
    # Key Metrics
    total_revenue = data['monthly_sales']['Amount'].sum()
    total_items = data['monthly_sales']['Count'].sum()
    avg_monthly_revenue = data['monthly_sales'].groupby('month')['Amount'].sum().mean()
    unique_ingredients = len(data['ingredient_summary'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue (6 months)", f"${total_revenue:,.2f}")
    with col2:
        st.metric("Total Items Sold", f"{total_items:,.0f}")
    with col3:
        st.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.2f}")
    with col4:
        st.metric("Tracked Ingredients", f"{unique_ingredients}")
    
    st.markdown("---")
    
    # Revenue Trend
    monthly_revenue = data['monthly_sales'].groupby('month')['Amount'].sum().reindex(month_order)
    monthly_items = data['monthly_sales'].groupby('month')['Count'].sum().reindex(month_order)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Monthly Revenue Trend', 'Monthly Items Sold Trend'),
        vertical_spacing=0.15
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_revenue.index, y=monthly_revenue.values,
                   mode='lines+markers', name='Revenue',
                   line=dict(color='#1f77b4', width=3),
                   marker=dict(size=10)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_items.index, y=monthly_items.values,
                   mode='lines+markers', name='Items Sold',
                   line=dict(color='#ff7f0e', width=3),
                   marker=dict(size=10)),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Month", row=2, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="Items Sold", row=2, col=1)
    fig.update_layout(height=600, showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Ingredients
    st.subheader("Top 10 Ingredients by Consumption")
    top_ingredients = data['ingredient_summary'].nlargest(10, 'total_consumption_6months')
    
    fig = px.bar(
        top_ingredients,
        x='total_consumption_6months',
        y='ingredient',
        orientation='h',
        labels={'total_consumption_6months': 'Total Consumption (6 months)', 'ingredient': 'Ingredient'},
        color='total_consumption_6months',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INGREDIENT INSIGHTS PAGE
# ============================================================================
elif page == "🥘 Ingredient Insights":
    st.header("🥘 Ingredient Insights")
    
    # Ingredient selector
    ingredients = data['ingredient_summary']['ingredient'].tolist()
    selected_ingredient = st.selectbox("Select Ingredient", ingredients)
    
    # Get data for selected ingredient
    ingredient_data = data['consumption_monthly'][data['consumption_monthly']['ingredient'] == selected_ingredient]
    ingredient_summary = data['ingredient_summary'][data['ingredient_summary']['ingredient'] == selected_ingredient].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Consumption (6 months)", f"{ingredient_summary['total_consumption_6months']:,.0f}")
    with col2:
        st.metric("Avg Monthly Consumption", f"{ingredient_summary['avg_monthly_consumption']:,.0f}")
    with col3:
        st.metric("Months Active", f"{ingredient_summary['months_active']}")
    with col4:
        has_shipment = "✅ Yes" if ingredient_summary['has_shipment_data'] else "❌ No"
        st.metric("Shipment Data", has_shipment)
    
    st.markdown("---")
    
    # Consumption over time
    ingredient_data_ordered = ingredient_data.set_index('month').reindex(month_order).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ingredient_data_ordered['month'],
        y=ingredient_data_ordered['total_consumption'],
        mode='lines+markers',
        name='Consumption',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10)
    ))
    fig.update_layout(
        title=f'{selected_ingredient} - Consumption Over Time',
        xaxis_title='Month',
        yaxis_title='Consumption',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top and least used ingredients
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 5 Most Used Ingredients")
        top_5 = data['ingredient_summary'].nlargest(5, 'total_consumption_6months')
        fig = px.bar(
            top_5,
            x='ingredient',
            y='total_consumption_6months',
            labels={'total_consumption_6months': 'Total Consumption', 'ingredient': 'Ingredient'},
            color='total_consumption_6months',
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top 5 Least Used Ingredients")
        bottom_5 = data['ingredient_summary'].nsmallest(5, 'total_consumption_6months')
        fig = px.bar(
            bottom_5,
            x='ingredient',
            y='total_consumption_6months',
            labels={'total_consumption_6months': 'Total Consumption', 'ingredient': 'Ingredient'},
            color='total_consumption_6months',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INVENTORY MANAGEMENT PAGE
# ============================================================================
elif page == "📦 Inventory Management":
    st.header("📦 Inventory Management & Reorder Alerts")
    
    # Inventory status
    st.subheader("🔔 Inventory Status & Alerts")
    
    # Calculate current inventory status (simulated - would come from actual inventory)
    inventory_status = []
    for _, row in data['inventory_optimization'].iterrows():
        ingredient = row['ingredient']
        reorder_point = row['reorder_point']
        avg_consumption = row['avg_monthly_consumption']
        
        # Simulate current inventory (using forecast as proxy)
        forecast_data = data['forecasting_data'][data['forecasting_data']['ingredient'] == ingredient]
        if len(forecast_data) > 0:
            forecasted_consumption = forecast_data.iloc[0]['forecast_next_month']
            # Simulate current inventory as 80% of reorder point
            current_inventory = reorder_point * 0.8
            
            status = "🟢 Good" if current_inventory > reorder_point else "🟡 Low" if current_inventory > reorder_point * 0.5 else "🔴 Critical"
            
            inventory_status.append({
                'ingredient': ingredient,
                'current_inventory': current_inventory,
                'reorder_point': reorder_point,
                'status': status,
                'forecasted_consumption': forecasted_consumption
            })
    
    inventory_df = pd.DataFrame(inventory_status)
    
    # Display alerts
    critical = inventory_df[inventory_df['status'] == '🔴 Critical']
    low = inventory_df[inventory_df['status'] == '🟡 Low']
    
    if len(critical) > 0:
        st.markdown('<div class="alert-box alert-danger">', unsafe_allow_html=True)
        st.error(f"🚨 **CRITICAL ALERT**: {len(critical)} ingredients need immediate reorder!")
        for _, row in critical.iterrows():
            st.write(f"- **{row['ingredient']}**: Current: {row['current_inventory']:,.0f}, Reorder Point: {row['reorder_point']:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if len(low) > 0:
        st.markdown('<div class="alert-box alert-warning">', unsafe_allow_html=True)
        st.warning(f"⚠️ **LOW STOCK ALERT**: {len(low)} ingredients approaching reorder point")
        for _, row in low.iterrows():
            st.write(f"- **{row['ingredient']}**: Current: {row['current_inventory']:,.0f}, Reorder Point: {row['reorder_point']:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if len(critical) == 0 and len(low) == 0:
        st.markdown('<div class="alert-box alert-success">', unsafe_allow_html=True)
        st.success("✅ All ingredients are at healthy inventory levels")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Inventory optimization table
    st.subheader("📊 Inventory Optimization Data")
    
    display_cols = ['ingredient', 'avg_monthly_consumption', 'reorder_point', 'safety_stock', 'risk_level']
    inventory_display = data['inventory_optimization'][display_cols].copy()
    inventory_display.columns = ['Ingredient', 'Avg Monthly Consumption', 'Reorder Point', 'Safety Stock', 'Risk Level']
    
    st.dataframe(inventory_display, use_container_width=True, height=400)
    
    # Risk level distribution
    risk_counts = data['inventory_optimization']['risk_level'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Level Distribution",
            color_discrete_map={'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Reorder points visualization
        top_reorder = data['inventory_optimization'].nlargest(10, 'reorder_point')
        fig = px.bar(
            top_reorder,
            x='reorder_point',
            y='ingredient',
            orientation='h',
            labels={'reorder_point': 'Reorder Point', 'ingredient': 'Ingredient'},
            title="Top 10 Ingredients - Reorder Points",
            color='risk_level',
            color_discrete_map={'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipment tracking
    st.subheader("🚚 Shipment Tracking")
    shipment_data = data['consumption_with_shipments'][
        data['consumption_with_shipments']['frequency'].notna()
    ].copy()
    
    if len(shipment_data) > 0:
        freq_dist = shipment_data['frequency'].value_counts()
        fig = px.bar(
            x=freq_dist.index,
            y=freq_dist.values,
            labels={'x': 'Shipment Frequency', 'y': 'Number of Ingredients'},
            title="Shipment Frequency Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PREDICTIVE ANALYTICS PAGE
# ============================================================================
elif page == "🔮 Predictive Analytics":
    st.header("🔮 Predictive Analytics & Forecasting")
    
    st.info("📊 **Forecasting Model**: Uses historical consumption patterns to predict future ingredient needs")
    
    # Forecast summary
    st.subheader("📈 Next Month Forecast (November 2024)")
    
    forecast_display = data['forecasting_data'][['ingredient', 'forecast_next_month', 'trend_slope', 'volatility']].copy()
    forecast_display.columns = ['Ingredient', 'Forecasted Consumption', 'Trend (per month)', 'Volatility (CV)']
    forecast_display = forecast_display.sort_values('Forecasted Consumption', ascending=False)
    
    st.dataframe(forecast_display, use_container_width=True, height=400)
    
    # Top forecasted ingredients
    top_forecast = data['forecasting_data'].nlargest(10, 'forecast_next_month')
    
    fig = px.bar(
        top_forecast,
        x='forecast_next_month',
        y='ingredient',
        orientation='h',
        labels={'forecast_next_month': 'Forecasted Consumption', 'ingredient': 'Ingredient'},
        title="Top 10 Ingredients - Next Month Forecast",
        color='trend_slope',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend analysis
    st.subheader("📊 Trend Analysis")
    
    ingredient_selector = st.selectbox("Select Ingredient for Trend Analysis", data['forecasting_data']['ingredient'].tolist())
    
    ingredient_consumption = data['consumption_monthly'][
        data['consumption_monthly']['ingredient'] == ingredient_selector
    ].set_index('month').reindex(month_order).reset_index()
    
    forecast_row = data['forecasting_data'][data['forecasting_data']['ingredient'] == ingredient_selector].iloc[0]
    
    # Create forecast line
    months_extended = month_order + ['November (Forecast)']
    consumption_values = ingredient_consumption['total_consumption'].tolist()
    forecast_value = forecast_row['forecast_next_month']
    consumption_values.append(forecast_value)
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=month_order,
        y=consumption_values[:-1],
        mode='lines+markers',
        name='Historical Consumption',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=['October', 'November (Forecast)'],
        y=[consumption_values[-2], forecast_value],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(size=10, symbol='diamond')
    ))
    
    fig.update_layout(
        title=f'{ingredient_selector} - Consumption Trend & Forecast',
        xaxis_title='Month',
        yaxis_title='Consumption',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        trend_direction = "📈 Increasing" if forecast_row['trend_slope'] > 0 else "📉 Decreasing"
        st.metric("Trend Direction", trend_direction)
    with col2:
        st.metric("Trend Slope", f"{forecast_row['trend_slope']:+.0f}/month")
    with col3:
        st.metric("Volatility (CV)", f"{forecast_row['volatility']:.2f}")

# ============================================================================
# COST OPTIMIZATION PAGE
# ============================================================================
elif page == "💰 Cost Optimization":
    st.header("💰 Cost Optimization & Spending Analysis")
    
    # Cost efficiency
    st.subheader("💵 Revenue per Unit of Consumption")
    
    top_efficiency = data['cost_efficiency'].nlargest(10, 'revenue_per_unit')
    
    fig = px.bar(
        top_efficiency,
        x='revenue_per_unit',
        y='ingredient',
        orientation='h',
        labels={'revenue_per_unit': 'Revenue per Unit ($)', 'ingredient': 'Ingredient'},
        title="Top 10 Most Cost-Efficient Ingredients",
        color='revenue_per_unit',
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Total spending by ingredient
    st.subheader("💸 Total Revenue Contribution by Ingredient")
    
    ingredient_revenue = data['consumption_monthly'].groupby('ingredient')['revenue'].sum().sort_values(ascending=False)
    
    fig = px.bar(
        x=ingredient_revenue.index,
        y=ingredient_revenue.values,
        labels={'x': 'Ingredient', 'y': 'Total Revenue ($)'},
        title="Total Revenue Contribution by Ingredient"
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Consumption vs Revenue scatter
    st.subheader("📊 Consumption vs Revenue Analysis")
    
    consumption_revenue = data['consumption_monthly'].groupby('ingredient').agg({
        'total_consumption': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    fig = px.scatter(
        consumption_revenue,
        x='total_consumption',
        y='revenue',
        size='revenue',
        color='revenue',
        hover_name='ingredient',
        labels={'total_consumption': 'Total Consumption', 'revenue': 'Total Revenue ($)'},
        title="Consumption vs Revenue Relationship",
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top spending items
    st.subheader("🍜 Top Revenue-Generating Menu Items")
    
    top_items = data['monthly_sales'].groupby('level_name').agg({
        'Amount': 'sum',
        'Count': 'sum'
    }).sort_values('Amount', ascending=False).head(15)
    
    fig = px.bar(
        top_items.reset_index(),
        x='Amount',
        y='level_name',
        orientation='h',
        labels={'Amount': 'Total Revenue ($)', 'level_name': 'Menu Item'},
        title="Top 15 Revenue-Generating Items",
        color='Amount',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SALES ANALYSIS PAGE
# ============================================================================
elif page == "📊 Sales Analysis":
    st.header("📊 Sales Analysis & Trends")
    
    # Monthly sales breakdown
    st.subheader("📅 Monthly Sales Breakdown")
    
    monthly_sales_summary = data['monthly_sales'].groupby('month').agg({
        'Amount': 'sum',
        'Count': 'sum'
    }).reindex(month_order).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Monthly Revenue', 'Monthly Items Sold')
    )
    
    fig.add_trace(
        go.Bar(x=monthly_sales_summary['month'], y=monthly_sales_summary['Amount'],
               name='Revenue', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=monthly_sales_summary['month'], y=monthly_sales_summary['Count'],
               name='Items Sold', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=2)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="Items Sold", row=1, col=2)
    fig.update_layout(height=400, showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top items
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Items by Revenue")
        top_revenue = data['monthly_sales'].groupby('level_name')['Amount'].sum().nlargest(10)
        fig = px.bar(
            x=top_revenue.values,
            y=top_revenue.index,
            orientation='h',
            labels={'x': 'Revenue ($)', 'y': 'Menu Item'},
            color=top_revenue.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Items by Quantity")
        top_quantity = data['monthly_sales'].groupby('level_name')['Count'].sum().nlargest(10)
        fig = px.bar(
            x=top_quantity.values,
            y=top_quantity.index,
            orientation='h',
            labels={'x': 'Quantity Sold', 'y': 'Menu Item'},
            color=top_quantity.values,
            color_continuous_scale='Oranges'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Sales impact on ingredients
    st.subheader("🍜 Menu Item Sales Impact on Ingredient Consumption")
    
    # Select item
    items_with_data = data['item_sales'][data['item_sales']['has_ingredient_data'] == True]['level_name'].unique()
    selected_item = st.selectbox("Select Menu Item", items_with_data)
    
    item_data = data['item_sales'][data['item_sales']['level_name'] == selected_item].iloc[0]
    
    # Get ingredient usage for this item
    ingredient_cols = [col for col in data['item_sales'].columns if col not in 
                       ['month', 'data_level', 'level_name', 'Count', 'Amount', 
                        'source_page', 'source_table', 'source_file', 'sheet_name', 'item_name', 'has_ingredient_data']]
    
    item_ingredients = []
    for col in ingredient_cols:
        if pd.notna(item_data[col]) and item_data[col] > 0:
            item_ingredients.append({
                'ingredient': col,
                'amount_per_item': item_data[col]
            })
    
    if item_ingredients:
        ingredients_df = pd.DataFrame(item_ingredients)
        ingredients_df = ingredients_df.sort_values('amount_per_item', ascending=False)
        
        fig = px.bar(
            ingredients_df,
            x='ingredient',
            y='amount_per_item',
            labels={'ingredient': 'Ingredient', 'amount_per_item': 'Amount per Item'},
            title=f"Ingredient Usage for {selected_item}",
            color='amount_per_item',
            color_continuous_scale='Purples'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate total consumption impact
        total_sold = data['monthly_sales'][data['monthly_sales']['level_name'] == selected_item]['Count'].sum()
        st.info(f"**Total Impact**: {selected_item} has been sold {total_sold:,} times, contributing to ingredient consumption across all months.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>MSY Inventory Intelligence Dashboard | Built for Mai Shan Yun Challenge</p>
        <p>Data Analytics | Predictive Insights | Inventory Optimization</p>
    </div>
""", unsafe_allow_html=True)


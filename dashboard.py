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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main Theme - Works with both light and dark modes */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    
    /* Consistent typography */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.6rem !important;
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        padding: 0.5rem 0;
    }
    
    [data-testid="stSidebar"] label {
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 0 !important;
    }
    
    /* Metric cards */
    .metric-card {
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }
    
    /* Alert boxes */
    .alert-box {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .alert-warning {
        border-left: 4px solid #ffb74d;
    }
    
    .alert-danger {
        border-left: 4px solid #ef5350;
    }
    
    .alert-success {
        border-left: 4px solid #66bb6a;
    }
    
    /* Consistent spacing */
    .stMarkdown {
        line-height: 1.6;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 0.95rem;
    }
    
    /* Selectbox and input improvements */
    .stSelectbox label, .stSlider label {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Info boxes */
    .stInfo {
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Consistent button styling */
    button {
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        padding: 2rem 0;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load processed data files"""
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
        'monthly_sales_category': pd.read_csv(cleaned_dir / "monthly_sales_category.csv"),
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
st.markdown('<h1 class="main-header">MSY Inventory Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SIDEBAR - Navigation
# ============================================================================
st.sidebar.markdown("## Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Select Dashboard Section",
    ["Overview", "Ingredient Insights", "Inventory Management", 
     "Predictive Analytics", "Cost Optimization", "Sales Analysis"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

# Month Filter - Available on all pages
st.sidebar.markdown("### Month Filter")
view_mode = st.sidebar.radio(
    "View Mode",
    ["All Months", "Single Month", "Compare Months"],
    key="view_mode"
)

selected_months = []
if view_mode == "Single Month":
    selected_month = st.sidebar.selectbox("Select Month", month_order, key="single_month")
    selected_months = [selected_month]
elif view_mode == "Compare Months":
    selected_months = st.sidebar.multiselect(
        "Select Months to Compare",
        month_order,
        default=month_order[-2:] if len(month_order) >= 2 else month_order,
        key="compare_months"
    )
else:
    selected_months = month_order

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
**MSY Inventory Intelligence Dashboard**

Transform raw restaurant data into actionable insights for inventory management, cost optimization, and predictive analytics.
""")

# ============================================================================
# OVERVIEW PAGE
# ============================================================================
if page == "Overview":
    st.header("Dashboard Overview")
    
    # Key Metrics
    total_revenue = data['monthly_sales']['Amount'].sum()
    avg_monthly_revenue = data['monthly_sales'].groupby('month')['Amount'].sum().mean()
    monthly_revenue = data['monthly_sales'].groupby('month')['Amount'].sum().reindex(month_order)
    revenue_growth = ((monthly_revenue.iloc[-1] - monthly_revenue.iloc[0]) / monthly_revenue.iloc[0]) * 100
    
    # Calculate inventory health metrics
    inventory_status = []
    for _, row in data['inventory_optimization'].iterrows():
        ingredient = row['ingredient']
        reorder_point = row['reorder_point']
        forecast_data = data['forecasting_data'][data['forecasting_data']['ingredient'] == ingredient]
        if len(forecast_data) > 0:
            forecasted_consumption = forecast_data.iloc[0]['forecast_next_month']
            current_inventory = reorder_point * 0.8
            daily_consumption = forecasted_consumption / 30
            days_of_supply = current_inventory / daily_consumption if daily_consumption > 0 else 999
            status = "Good" if current_inventory > reorder_point else "Low" if current_inventory > reorder_point * 0.5 else "Critical"
            inventory_status.append({'status': status, 'days_of_supply': days_of_supply})
    
    if inventory_status:
        inv_df = pd.DataFrame(inventory_status)
        critical_count = len(inv_df[inv_df['status'] == 'Critical'])
        avg_days_supply = inv_df['days_of_supply'].mean()
        # Calculate health score (0-100)
        health_score = max(0, 100 - (critical_count * 20) - (len(inv_df[inv_df['status'] == 'Low']) * 10))
    else:
        critical_count = 0
        avg_days_supply = 0
        health_score = 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue (6 months)", f"${total_revenue:,.2f}")
    with col2:
        st.metric("Revenue Growth", f"{revenue_growth:+.1f}%", 
                 delta=f"{revenue_growth:+.1f}%" if revenue_growth > 0 else None)
    with col3:
        st.metric("Inventory Health Score", f"{health_score:.0f}/100",
                 delta="Healthy" if health_score >= 80 else "Needs Attention")
    with col4:
        st.metric("Critical Alerts", f"{critical_count}", 
                 delta="Action Required" if critical_count > 0 else None)
    
    st.markdown("---")
    
    # Month-wise Revenue Analysis
    if view_mode == "Single Month" and selected_months:
        # Show single month details
        month_data = monthly_revenue[monthly_revenue.index == selected_months[0]]
        if len(month_data) > 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{selected_months[0]} Revenue", f"${month_data.iloc[0]:,.2f}")
            with col2:
                # Calculate month-over-month change
                month_idx = month_order.index(selected_months[0])
                if month_idx > 0:
                    prev_month = month_order[month_idx - 1]
                    prev_revenue = monthly_revenue[prev_month]
                    change = ((month_data.iloc[0] - prev_revenue) / prev_revenue) * 100
                    st.metric("Month-over-Month Change", f"{change:+.1f}%")
                else:
                    st.metric("Month-over-Month Change", "N/A")
            with col3:
                # Items sold for this month
                month_items = data['monthly_sales'][data['monthly_sales']['month'] == selected_months[0]]['Count'].sum()
                st.metric(f"{selected_months[0]} Items Sold", f"{month_items:,.0f}")
        
        # Show ingredient consumption for this month
        st.subheader(f"Top 5 Ingredients - {selected_months[0]} Consumption")
        month_consumption = data['consumption_monthly'][data['consumption_monthly']['month'] == selected_months[0]]
        top_month_ingredients = month_consumption.nlargest(5, 'total_consumption')
        
        fig = px.bar(
            top_month_ingredients,
            x='total_consumption',
            y='ingredient',
            orientation='h',
            labels={'total_consumption': 'Consumption', 'ingredient': 'Ingredient'},
            color='total_consumption',
            color_continuous_scale='Blues',
            title=f"Top 5 Ingredients - {selected_months[0]}"
        )
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif view_mode == "Compare Months" and len(selected_months) >= 2:
        # Compare selected months
        st.subheader(f"Month Comparison: {', '.join(selected_months)}")
        
        # Revenue comparison
        compare_revenue = monthly_revenue[monthly_revenue.index.isin(selected_months)]
        
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=compare_revenue.index,
                y=compare_revenue.values,
                marker_color='#667eea',
                text=compare_revenue.values,
                texttemplate='$%{text:,.0f}',
                textposition='outside'
            ))
            fig.update_layout(
                title='Revenue Comparison',
                xaxis_title='Month',
                yaxis_title='Revenue ($)',
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Ingredient consumption comparison
            compare_consumption = data['consumption_monthly'][
                data['consumption_monthly']['month'].isin(selected_months)
            ]
            top_ingredients_compare = compare_consumption.groupby('ingredient')['total_consumption'].sum().nlargest(5)
            
            fig = px.bar(
                x=top_ingredients_compare.values,
                y=top_ingredients_compare.index,
                orientation='h',
                labels={'x': 'Total Consumption', 'y': 'Ingredient'},
                title="Top 5 Ingredients (Selected Months)",
                color=top_ingredients_compare.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed comparison table
        st.subheader("Detailed Month Comparison")
        comparison_data = []
        for month in selected_months:
            month_sales = data['monthly_sales'][data['monthly_sales']['month'] == month]
            comparison_data.append({
                'Month': month,
                'Revenue': month_sales['Amount'].sum(),
                'Items Sold': month_sales['Count'].sum(),
                'Avg Item Price': (month_sales['Amount'].sum() / month_sales['Count'].sum()) if month_sales['Count'].sum() > 0 else 0
            })
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, height=150)
        
    else:
        # All months view (default)
        # Single Revenue Trend Chart
        filtered_revenue = monthly_revenue[monthly_revenue.index.isin(selected_months)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered_revenue.index,
            y=filtered_revenue.values,
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#667eea'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        fig.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top 5 Ingredients - filtered by selected months
        st.subheader("Top 5 Ingredients by Consumption")
        filtered_consumption = data['consumption_monthly'][data['consumption_monthly']['month'].isin(selected_months)]
        top_ingredients = filtered_consumption.groupby('ingredient')['total_consumption'].sum().nlargest(5).reset_index()
        top_ingredients.columns = ['ingredient', 'total_consumption']
        
        fig = px.bar(
            top_ingredients,
            x='total_consumption',
            y='ingredient',
            orientation='h',
            labels={'total_consumption': 'Total Consumption', 'ingredient': 'Ingredient'},
            color='total_consumption',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INGREDIENT INSIGHTS PAGE
# ============================================================================
elif page == "Ingredient Insights":
    st.header("Ingredient Insights")
    
    # Ingredient selector
    ingredients = data['ingredient_summary']['ingredient'].tolist()
    selected_ingredient = st.selectbox("Select Ingredient", ingredients)
    
    # Get data for selected ingredient
    ingredient_data = data['consumption_monthly'][data['consumption_monthly']['ingredient'] == selected_ingredient]
    ingredient_summary = data['ingredient_summary'][data['ingredient_summary']['ingredient'] == selected_ingredient].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Consumption (6 months)", f"{ingredient_summary['total_consumption_6months']:,.0f}")
    with col2:
        st.metric("Avg Monthly Consumption", f"{ingredient_summary['avg_monthly_consumption']:,.0f}")
    with col3:
        has_shipment = "Yes" if ingredient_summary['has_shipment_data'] else "No"
        st.metric("Shipment Data", has_shipment)
    
    st.markdown("---")
    
    # Month-wise consumption analysis
    if view_mode == "Single Month" and selected_months:
        # Show single month consumption
        month_consumption = ingredient_data[ingredient_data['month'] == selected_months[0]]
        if len(month_consumption) > 0:
            st.subheader(f"{selected_ingredient} - {selected_months[0]}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Consumption", f"{month_consumption.iloc[0]['total_consumption']:,.0f}")
            with col2:
                st.metric("Items Sold", f"{month_consumption.iloc[0]['sales_count']:,.0f}")
            with col3:
                st.metric("Revenue", f"${month_consumption.iloc[0]['revenue']:,.2f}")
    elif view_mode == "Compare Months" and len(selected_months) >= 2:
        # Compare consumption across months
        st.subheader(f"{selected_ingredient} - Month Comparison")
        compare_data = ingredient_data[ingredient_data['month'].isin(selected_months)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=compare_data['month'],
            y=compare_data['total_consumption'],
            marker_color='#667eea',
            text=compare_data['total_consumption'],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        ))
        fig.update_layout(
            title=f'{selected_ingredient} - Consumption by Month',
            xaxis_title='Month',
            yaxis_title='Consumption',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # All months trend
        st.subheader("Consumption Trend")
        ingredient_data_filtered = ingredient_data[ingredient_data['month'].isin(selected_months)]
        ingredient_data_ordered = ingredient_data_filtered.set_index('month').reindex(
            [m for m in month_order if m in selected_months]
        ).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ingredient_data_ordered['month'],
            y=ingredient_data_ordered['total_consumption'],
            mode='lines+markers',
            name='Consumption',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#667eea'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        fig.update_layout(
            title=f'{selected_ingredient} - Consumption Over Time',
            xaxis_title='Month',
            yaxis_title='Consumption',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INVENTORY MANAGEMENT PAGE
# ============================================================================
elif page == "Inventory Management":
    st.header("Inventory Management & Reorder Alerts")
    
    # Inventory status
    st.subheader("Inventory Status & Alerts")
    
    # Calculate current inventory status
    inventory_status = []
    for _, row in data['inventory_optimization'].iterrows():
        ingredient = row['ingredient']
        reorder_point = row['reorder_point']
        avg_consumption = row['avg_monthly_consumption']
        safety_stock = row['safety_stock']
        
        # Simulate current inventory (using forecast as proxy)
        forecast_data = data['forecasting_data'][data['forecasting_data']['ingredient'] == ingredient]
        if len(forecast_data) > 0:
            forecasted_consumption = forecast_data.iloc[0]['forecast_next_month']
            # Simulate current inventory as 80% of reorder point
            current_inventory = reorder_point * 0.8
            
            # Calculate days of supply
            daily_consumption = forecasted_consumption / 30  # Average daily consumption
            days_of_supply = current_inventory / daily_consumption if daily_consumption > 0 else 999
            
            # Calculate recommended order quantity
            recommended_order = max(0, reorder_point - current_inventory + safety_stock)
            
            # Calculate days until reorder needed
            days_until_reorder = (current_inventory - reorder_point) / daily_consumption if daily_consumption > 0 else 999
            if days_until_reorder < 0:
                days_until_reorder = 0  # Already below reorder point
            
            status = "Good" if current_inventory > reorder_point else "Low" if current_inventory > reorder_point * 0.5 else "Critical"
            
            # Check for overstock (inventory > 150% of monthly consumption)
            is_overstocked = current_inventory > (forecasted_consumption * 1.5)
            
            inventory_status.append({
                'ingredient': ingredient,
                'current_inventory': current_inventory,
                'reorder_point': reorder_point,
                'status': status,
                'forecasted_consumption': forecasted_consumption,
                'days_of_supply': days_of_supply,
                'recommended_order_qty': recommended_order,
                'days_until_reorder': days_until_reorder,
                'is_overstocked': is_overstocked
            })
    
    inventory_df = pd.DataFrame(inventory_status)
    
    # Inventory alerts
    critical = inventory_df[inventory_df['status'] == 'Critical']
    low = inventory_df[inventory_df['status'] == 'Low']
    overstocked = inventory_df[inventory_df['is_overstocked'] == True]
    
    # Summary metrics at top
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Critical", len(critical), delta="Action Required" if len(critical) > 0 else None)
    with col2:
        st.metric("Low Stock", len(low))
    with col3:
        st.metric("Overstocked", len(overstocked))
    with col4:
        healthy_count = len(inventory_df) - len(critical) - len(low) - len(overstocked)
        st.metric("Healthy", healthy_count)
    
    st.markdown("---")
    
    # Critical Alerts - Visual Cards
    if len(critical) > 0:
        st.subheader(f"Critical Alerts ({len(critical)} ingredients need immediate attention)")
        
        # Create visual cards for each critical item
        for idx, (_, row) in enumerate(critical.iterrows()):
            with st.expander(f"{row['ingredient']} - URGENT ACTION REQUIRED", expanded=(idx == 0)):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Current Status**")
                    st.metric("Current Inventory", f"{row['current_inventory']:,.0f}", 
                             delta=f"{row['current_inventory'] - row['reorder_point']:,.0f} below reorder point",
                             delta_color="inverse")
                    st.metric("Reorder Point", f"{row['reorder_point']:,.0f}")
                
                with col2:
                    st.markdown("**Timeline**")
                    st.metric("Days of Supply", f"{row['days_of_supply']:.1f} days",
                             delta="Stockout imminent" if row['days_of_supply'] < 7 else "Low stock",
                             delta_color="inverse")
                    st.metric("Forecasted Next Month", f"{row['forecasted_consumption']:,.0f}")
                
                with col3:
                    st.markdown("**Recommended Action**")
                    st.markdown(f"""
                    <div style="background-color: #ffebee; padding: 1rem; border-radius: 8px; border-left: 4px solid #ef5350;">
                        <h4 style="color: #c62828; margin: 0 0 0.5rem 0;">Immediate Action</h4>
                        <p style="margin: 0.5rem 0;"><strong>Order Quantity:</strong> {row['recommended_order_qty']:,.0f} units</p>
                        <p style="margin: 0.5rem 0;"><strong>Order By:</strong> Today</p>
                        <p style="margin: 0.5rem 0;"><strong>Priority:</strong> HIGH</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Visual gauge for inventory level
                inventory_percent = (row['current_inventory'] / row['reorder_point']) * 100 if row['reorder_point'] > 0 else 0
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = inventory_percent,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': f"Inventory Level (%)"},
                    delta = {'reference': 100, 'position': "top"},
                    gauge = {
                        'axis': {'range': [None, 150]},
                        'bar': {'color': "red"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 100], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 100
                        }
                    }
                ))
                fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)
    
    # Low Stock Alerts
    if len(low) > 0:
        st.subheader(f"Low Stock Alerts ({len(low)} ingredients approaching reorder point)")
        
        # Create compact table with action buttons
        low_display = low[['ingredient', 'current_inventory', 'reorder_point', 'days_of_supply', 'recommended_order_qty', 'days_until_reorder']].copy()
        low_display.columns = ['Ingredient', 'Current Inventory', 'Reorder Point', 'Days of Supply', 'Order Qty', 'Days Until Reorder']
        low_display = low_display.sort_values('Days of Supply', ascending=True)
        
        st.dataframe(
            low_display.style.format({
                'Current Inventory': '{:,.0f}',
                'Reorder Point': '{:,.0f}',
                'Days of Supply': '{:.1f}',
                'Order Qty': '{:,.0f}',
                'Days Until Reorder': '{:.0f}'
            }).applymap(
                lambda x: 'background-color: #fff3cd' if isinstance(x, (int, float)) and x < 10 else '',
                subset=['Days of Supply']
            ),
            use_container_width=True,
            height=min(400, len(low) * 50 + 50)
        )
        
        st.info(f"**Action Required**: Order the recommended quantities within the specified days to prevent stockouts.")
    
    # Overstock Alerts
    if len(overstocked) > 0:
        st.subheader(f"Overstock Alerts ({len(overstocked)} ingredients may be overstocked)")
        
        overstock_display = []
        for _, row in overstocked.iterrows():
            excess = row['current_inventory'] - (row['forecasted_consumption'] * 1.2)
            excess_percent = (excess / row['current_inventory'] * 100) if row['current_inventory'] > 0 else 0
            overstock_display.append({
                'Ingredient': row['ingredient'],
                'Current Inventory': row['current_inventory'],
                'Expected Monthly Need': row['forecasted_consumption'] * 1.2,
                'Excess Units': excess,
                'Excess %': excess_percent,
                'Recommendation': f"Reduce next order by {excess * 0.5:,.0f} units"
            })
        
        overstock_df = pd.DataFrame(overstock_display)
        st.dataframe(
            overstock_df.style.format({
                'Current Inventory': '{:,.0f}',
                'Expected Monthly Need': '{:,.0f}',
                'Excess Units': '{:,.0f}',
                'Excess %': '{:.1f}%'
            }),
            use_container_width=True,
            height=min(300, len(overstocked) * 50 + 50)
        )
        
        st.warning(f"**Waste Prevention**: Consider reducing order quantities for these ingredients to minimize waste and storage costs.")
    
    # All Good Status
    if len(critical) == 0 and len(low) == 0 and len(overstocked) == 0:
        st.success("**All Clear!** All ingredients are at healthy inventory levels with no immediate action required.")
    
    st.markdown("---")
    
    # Inventory Health Dashboard
    st.subheader("Inventory Health Dashboard")
    
    # Calculate summary metrics
    total_ingredients = len(inventory_df)
    avg_days_supply = inventory_df['days_of_supply'].mean()
    critical_count = len(inventory_df[inventory_df['status'] == 'Critical'])
    low_count = len(inventory_df[inventory_df['status'] == 'Low'])
    overstock_count = len(inventory_df[inventory_df['is_overstocked'] == True])
    healthy_count = total_ingredients - critical_count - low_count - overstock_count
    
    # Overall health score
    health_score = max(0, 100 - (critical_count * 25) - (low_count * 10) - (overstock_count * 5))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Health score gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = health_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Inventory Health Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Key Metrics")
        st.metric("Total Ingredients", total_ingredients)
        st.metric("Avg Days of Supply", f"{avg_days_supply:.1f} days")
        st.metric("Health Score", f"{health_score:.0f}/100",
                 delta="Excellent" if health_score >= 80 else "Good" if health_score >= 60 else "Needs Attention",
                 delta_color="normal" if health_score >= 80 else "off")
    
    st.markdown("---")
    
    # Inventory Status Summary
    st.subheader("Inventory Status Summary")
    status_counts = {
        'Critical': critical_count,
        'Low Stock': low_count,
        'Healthy': healthy_count,
        'Overstocked': overstock_count
    }
    
    status_df = pd.DataFrame({
        'Status': list(status_counts.keys()),
        'Count': list(status_counts.values())
    })
    fig = px.bar(
        status_df,
        x='Status',
        y='Count',
        title="Inventory Status Distribution",
        color='Status',
        color_discrete_map={
            'Critical': '#ef5350',
            'Low Stock': '#ffb74d',
            'Healthy': '#66bb6a',
            'Overstocked': '#ffa726'
        }
    )
    fig.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Shipment vs Usage - Key comparison
    shipment_data = data['consumption_with_shipments'][
        data['consumption_with_shipments']['frequency'].notna()
    ].copy()
    
    # Shipment Tracking
    if len(shipment_data) > 0:
        st.subheader("Shipment Tracking")
        
        # Calculate coverage issues
        shipment_summary = []
        for _, row in shipment_data.iterrows():
            if pd.notna(row['quantity_per_shipment']) and pd.notna(row['estimated_shipments_needed']):
                frequency = row['frequency']
                quantity_per_shipment = row['quantity_per_shipment']
                
                if frequency == 'weekly':
                    shipments_per_month = 4
                elif frequency == 'biweekly':
                    shipments_per_month = 2
                elif frequency == 'monthly':
                    shipments_per_month = 1
                else:
                    shipments_per_month = 1
                
                total_shipment_quantity = quantity_per_shipment * shipments_per_month
                estimated_usage = row['total_consumption']
                coverage_ratio = (total_shipment_quantity / estimated_usage * 100) if estimated_usage > 0 else 0
                
                shipment_summary.append({
                    'ingredient': row['ingredient'],
                    'frequency': frequency,
                    'coverage_ratio': coverage_ratio,
                    'estimated_usage': estimated_usage,
                    'shipment_quantity': total_shipment_quantity
                })
        
        if shipment_summary:
            shipment_df = pd.DataFrame(shipment_summary)
            coverage_issues = shipment_df[(shipment_df['coverage_ratio'] < 90) | (shipment_df['coverage_ratio'] > 110)]
            
            if len(coverage_issues) > 0:
                st.warning(f"**{len(coverage_issues)} ingredients have shipment coverage issues**")
                issues_display = coverage_issues[['ingredient', 'frequency', 'coverage_ratio']].copy()
                issues_display.columns = ['Ingredient', 'Shipment Frequency', 'Coverage Ratio (%)']
                issues_display = issues_display.sort_values('Coverage Ratio (%)')
                st.dataframe(issues_display, use_container_width=True, height=200)
                st.info("**Action**: Adjust shipment frequency or quantity to match consumption patterns.")
            else:
                st.success("All ingredients have appropriate shipment coverage.")

# ============================================================================
# PREDICTIVE ANALYTICS PAGE
# ============================================================================
elif page == "Predictive Analytics":
    st.header("Predictive Analytics & Forecasting")
    
    st.info("**Forecasting Model**: Uses historical consumption patterns to predict future ingredient needs")
    
    # Forecast summary - Top 10
    st.subheader("Next Month Forecast (November 2024)")
    
    top_forecast = data['forecasting_data'].nlargest(10, 'forecast_next_month')
    
    fig = px.bar(
        top_forecast,
        x='forecast_next_month',
        y='ingredient',
        orientation='h',
        labels={'forecast_next_month': 'Forecasted Consumption', 'ingredient': 'Ingredient'},
        title="Top 10 Ingredients - Next Month Forecast",
        color='trend_slope',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend analysis - Single ingredient
    st.subheader("Detailed Trend Analysis")
    ingredient_selector = st.selectbox("Select Ingredient", data['forecasting_data']['ingredient'].tolist())
    
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
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#667eea'),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=['October', 'November (Forecast)'],
        y=[consumption_values[-2], forecast_value],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#f093fb', width=3, dash='dash'),
        marker=dict(size=10, symbol='diamond', color='#f093fb')
    ))
    
    fig.update_layout(
        title=f'{ingredient_selector} - Consumption Trend & Forecast',
        xaxis_title='Month',
        yaxis_title='Consumption',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        trend_direction = "Increasing" if forecast_row['trend_slope'] > 0 else "Decreasing"
        st.metric("Trend Direction", trend_direction)
    with col2:
        st.metric("Trend Slope", f"{forecast_row['trend_slope']:+.0f}/month")
    with col3:
        st.metric("Volatility (CV)", f"{forecast_row['volatility']:.2f}")

# ============================================================================
# COST OPTIMIZATION PAGE
# ============================================================================
elif page == "Cost Optimization":
    st.header("Cost Optimization & Spending Analysis")
    
    # Estimated Ingredient Usage Cost
    st.subheader("Estimated Ingredient Usage Cost")
    
    # Calculate estimated cost for selected months
    monthly_cost_data = []
    for month in selected_months:
        month_consumption = data['consumption_monthly'][data['consumption_monthly']['month'] == month]
        month_revenue = month_consumption['revenue'].sum()
        estimated_cost = month_revenue * 0.30  # 30% food cost ratio
        
        monthly_cost_data.append({
            'month': month,
            'revenue': month_revenue,
            'estimated_cost': estimated_cost
        })
    
    cost_df = pd.DataFrame(monthly_cost_data)
    monthly_total_cost = cost_df.set_index('month').reindex(selected_months)['estimated_cost']
    monthly_total_revenue = cost_df.set_index('month').reindex(selected_months)['revenue']
    
    if view_mode == "Single Month" and selected_months:
        # Single month cost breakdown
        month_cost = monthly_total_cost.iloc[0] if len(monthly_total_cost) > 0 else 0
        month_rev = monthly_total_revenue.iloc[0] if len(monthly_total_revenue) > 0 else 0
        cost_ratio = (month_cost / month_rev * 100) if month_rev > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{selected_months[0]} Revenue", f"${month_rev:,.2f}")
        with col2:
            st.metric(f"{selected_months[0]} Estimated Cost", f"${month_cost:,.2f}")
        with col3:
            st.metric("Cost Ratio", f"{cost_ratio:.1f}%")
    else:
        # Multi-month cost vs revenue chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=monthly_total_cost.index, y=monthly_total_cost.values,
                   name='Estimated Cost', marker_color='#9e9e9e', opacity=0.7),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=monthly_total_revenue.index, y=monthly_total_revenue.values,
                       mode='lines+markers', name='Revenue',
                       line=dict(color='#667eea', width=3),
                       marker=dict(size=10)),
            secondary_y=True
        )
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Estimated Cost ($)", secondary_y=False)
        fig.update_yaxes(title_text="Revenue ($)", secondary_y=True)
        fig.update_layout(
            title='Monthly Estimated Cost vs Revenue',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(x=0.7, y=0.95)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Note**: Estimated costs are calculated as 30% of revenue (typical food cost ratio).")
    st.markdown("---")
    
    # Top 5 cost-efficient ingredients
    st.subheader("Top 5 Most Cost-Efficient Ingredients")
    top_efficiency = data['cost_efficiency'].nlargest(5, 'revenue_per_unit').reset_index()
    top_efficiency = top_efficiency.rename(columns={'index': 'ingredient'})
    
    fig = px.bar(
        top_efficiency,
        x='revenue_per_unit',
        y='ingredient',
        orientation='h',
        labels={'revenue_per_unit': 'Revenue per Unit ($)', 'ingredient': 'Ingredient'},
        color='revenue_per_unit',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SALES ANALYSIS PAGE
# ============================================================================
elif page == "Sales Analysis":
    st.header("Sales Analysis & Trends")
    
    # Monthly sales breakdown
    st.subheader("Monthly Sales Breakdown")
    
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
               name='Revenue', marker_color='#667eea'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=monthly_sales_summary['month'], y=monthly_sales_summary['Count'],
               name='Items Sold', marker_color='#f093fb'),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=2)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="Items Sold", row=1, col=2)
    fig.update_layout(
        height=400, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Month-wise Sales Analysis
    if view_mode == "Single Month" and selected_months:
        st.subheader(f"{selected_months[0]} Sales Analysis")
        
        # Category sales for selected month
        month_category_sales = data['monthly_sales_category'][
            (data['monthly_sales_category']['month'] == selected_months[0]) &
            (data['monthly_sales_category']['level_name'] != 'Combo Items Donot Delete')
        ]
        top_categories_month = month_category_sales.nlargest(5, 'Amount')
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                top_categories_month,
                x='Amount',
                y='level_name',
                orientation='h',
                labels={'Amount': 'Revenue ($)', 'level_name': 'Category'},
                title=f"Top 5 Categories - {selected_months[0]}",
                color='Amount',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top items for this month
            month_items = data['monthly_sales'][data['monthly_sales']['month'] == selected_months[0]]
            top_items_month = month_items.nlargest(5, 'Amount')
            fig = px.bar(
                top_items_month,
                x='Amount',
                y='level_name',
                orientation='h',
                labels={'Amount': 'Revenue ($)', 'level_name': 'Menu Item'},
                title=f"Top 5 Items - {selected_months[0]}",
                color='Amount',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
    elif view_mode == "Compare Months" and len(selected_months) >= 2:
        st.subheader(f"Month Comparison: {', '.join(selected_months)}")
        
        # Category comparison
        compare_category = data['monthly_sales_category'][
            (data['monthly_sales_category']['month'].isin(selected_months)) &
            (data['monthly_sales_category']['level_name'] != 'Combo Items Donot Delete')
        ]
        top_categories = compare_category.groupby('level_name')['Amount'].sum().nlargest(5).index.tolist()
        category_pivot = compare_category[compare_category['level_name'].isin(top_categories)].pivot_table(
            index='month',
            columns='level_name',
            values='Amount',
            aggfunc='sum'
        ).reindex(selected_months).fillna(0)
        
        fig = go.Figure()
        for category in category_pivot.columns:
            fig.add_trace(go.Bar(
                name=category,
                x=category_pivot.index,
                y=category_pivot[category],
                hovertemplate=f'<b>{category}</b><br>Month: %{{x}}<br>Revenue: $%{{y:,.2f}}<extra></extra>'
            ))
        fig.update_layout(
            barmode='group',
            title='Top 5 Categories - Month Comparison',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # All months - Monthly Sales by Category
        st.subheader("Monthly Sales by Category")
        
        category_sales = data['monthly_sales_category'].copy()
        category_sales = category_sales[
            (category_sales['level_name'] != 'Combo Items Donot Delete') &
            (category_sales['month'].isin(selected_months))
        ]
        
        # Top 5 categories only
        top_categories = category_sales.groupby('level_name')['Amount'].sum().nlargest(5).index.tolist()
        category_pivot = category_sales[category_sales['level_name'].isin(top_categories)].pivot_table(
            index='month',
            columns='level_name',
            values='Amount',
            aggfunc='sum'
        ).reindex([m for m in month_order if m in selected_months]).fillna(0)
        
        fig = go.Figure()
        for category in category_pivot.columns:
            fig.add_trace(go.Bar(
                name=category,
                x=category_pivot.index,
                y=category_pivot[category],
                hovertemplate=f'<b>{category}</b><br>Month: %{{x}}<br>Revenue: $%{{y:,.2f}}<extra></extra>'
            ))
        fig.update_layout(
            barmode='stack',
            title='Top 5 Categories - Monthly Sales',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top 5 items by revenue - filtered by selected months
        st.subheader("Top 5 Revenue-Generating Items")
        filtered_sales = data['monthly_sales'][data['monthly_sales']['month'].isin(selected_months)]
        top_revenue = filtered_sales.groupby('level_name')['Amount'].sum().nlargest(5).reset_index()
        top_revenue.columns = ['item', 'revenue']
        fig = px.bar(
            top_revenue,
            x='revenue',
            y='item',
            orientation='h',
            labels={'revenue': 'Revenue ($)', 'item': 'Menu Item'},
            color='revenue',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
    <div class="footer-text">
        <p><strong>MSY Inventory Intelligence Dashboard</strong></p>
        <p>Built for Mai Shan Yun Challenge</p>
    </div>
""", unsafe_allow_html=True)


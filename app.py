import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------------------------------------
# 1. SETUP PAGE CONFIG & PALETTE
# -------------------------------------------------------------
st.set_page_config(page_title="Amazon Executive Analytics Dashboard", layout="wide")
st.title("Amazon Executive Product Analytics Dashboard")
st.markdown("Marketplace Strategy & Sales Growth Command Center")

# -------------------------------------------------------------
# 2. DATA ENGINEERING PIPELINE (Loading & Auto-Cleaning)
# -------------------------------------------------------------
@st.cache_data
def load_and_clean_amazon_data():
    df = pd.read_csv("amazon.csv")
    
    # Clean pricing attributes
    for col in ['discounted_price', 'actual_price']:
        df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Clean discount metrics
    df['discount_percentage'] = df['discount_percentage'].astype(str).str.replace('%', '')
    df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce') / 100

    # Clean consumer feedback numbers
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_count'] = df['rating_count'].astype(str).str.replace(',', '')
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce').fillna(0).astype(int)

    # Engineer analytic proxies
    df['revenue_proxy'] = df['discounted_price'] * df['rating_count']
    
    # Clean category string paths safely
    def extract_root(cat_str):
        if pd.isna(cat_str):
            return "Uncategorized"
        parts = str(cat_str).split('|')
        return parts[0].strip() if len(parts) > 0 else str(cat_str)

    df['root_category'] = df['category'].apply(extract_root)
    return df

# Initialize dataframe
df = load_and_clean_amazon_data()

# -------------------------------------------------------------
# 3. SIDEBAR CATEGORY FILTERING MODULE
# -------------------------------------------------------------
st.sidebar.header("Dashboard Controls")
available_categories = sorted(df['root_category'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    label="Filter by Product Category",
    options=available_categories,
    default=available_categories
)

# Apply filter mask to dataframe
filtered_df = df[df['root_category'].isin(selected_categories)]

# -------------------------------------------------------------
# 4. ADVANCED REVENUE MAXIMIZATION KPI ENGINE
# -------------------------------------------------------------
st.subheader("Actionable Sales Growth Analytics")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

median_engagement = filtered_df['rating_count'].median() if not filtered_df.empty else 0
undiscovered_gems = filtered_df[(filtered_df['rating'] >= 4.3) & (filtered_df['rating_count'] < median_engagement)]
underperforming_items = filtered_df[(filtered_df['discount_percentage'] > 0.5) & (filtered_df['rating'] < 3.5)]
optimal_deals = filtered_df[(filtered_df['discount_percentage'] >= 0.2) & (filtered_df['discount_percentage'] <= 0.4) & (filtered_df['rating'] >= 4.0)]

with kpi1:
    st.metric(
        label="Catalog GMV Proxy", 
        value=f"${filtered_df['revenue_proxy'].sum():,.0f}" if not filtered_df.empty else "$0"
    )
with kpi2:
    st.metric(
        label="Undiscovered High-Value Gems", 
        value=f"{len(undiscovered_gems)} Products"
    )
with kpi3:
    st.metric(
        label="High-Discount Value Burners", 
        value=f"{len(underperforming_items)} Products"
    )
with kpi4:
    st.metric(
        label="Optimal Promotional Matches", 
        value=f"{len(optimal_deals)} Skus"
    )

# -------------------------------------------------------------
# 5. PRE-CALCULATE PLOT DATA & CHARTS SCRIPT
# -------------------------------------------------------------
if not filtered_df.empty:
    # Elasticity Processing
    filtered_df['discount_bucket'] = pd.cut(filtered_df['discount_percentage'], bins=10, labels=[f"{int(i*10)}%-{int((i+1)*10)}%" for i in range(10)])
    elasticity_df = filtered_df.groupby('discount_bucket', observed=False).agg(
        avg_revenue=('revenue_proxy', 'mean')
    ).reset_index().fillna(0)
    
    # Identify dynamic peak ranges
    peak_discount = elasticity_df.loc[elasticity_df['avg_revenue'].idxmax(), 'discount_bucket'] if not elasticity_df.empty else "N/A"
    
    # Calculate top revenue category
    revenue_by_cat = filtered_df.groupby('root_category')['revenue_proxy'].sum().reset_index().sort_values(by='revenue_proxy', ascending=False)
    top_rev_cat = revenue_by_cat.iloc[0]['root_category'] if not revenue_by_cat.empty else "N/A"

    # Line Chart
    fig_elasticity = px.line(
        elasticity_df, x='discount_bucket', y='avg_revenue', markers=True,
        labels={'discount_bucket': 'Applied Discount Range', 'avg_revenue': 'Avg Revenue Velocity per Item ($)'},
        template='plotly_white'
    )
    fig_elasticity.update_traces(line_color='#FF9900', line_width=4)

    # Leaderboard Bar Chart
    top_products_df = filtered_df.sort_values(by='revenue_proxy', ascending=False).head(10).copy()
    top_products_df['Short_Name'] = top_products_df['product_name'].str.slice(0, 30) + "..."
    fig_products_sales = px.bar(
        top_products_df, x='revenue_proxy', y='Short_Name', orientation='h',
        color='revenue_proxy', color_continuous_scale='Blues',
        labels={'revenue_proxy': 'Estimated Sales Volume ($)', 'Short_Name': 'Product Title'},
        template='plotly_white'
    )
    fig_products_sales.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)

    # Heatmap Chart
    fig_heatmap = px.density_heatmap(
        filtered_df, x='rating', y='discount_percentage', z='revenue_proxy', histfunc='sum',
        nbinsx=6, nbinsy=6,
        labels={'rating': 'Customer Rating (1-5)', 'discount_percentage': 'Applied Discount Rate', 'revenue_proxy': 'Total Estimated Sales ($)'},
        template='plotly_white', color_continuous_scale='Viridis'
    )

    # -------------------------------------------------------------
    # 6. REVENUE MAXIMIZATION STRATEGY PREVIEW (PLAIN ENGLISH)
    # -------------------------------------------------------------
    st.markdown("---")
    st.subheader("Strategic Action Plan for Amazon Managers")

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### Where to Focus Ad Spend")
        st.markdown(f"""
        * **The Discount Sweet Spot**: Our data shows that items with a **{peak_discount} discount** trigger the highest customer sales velocity. Avoid pushing discounts past 50%, as revenue returns flatten out significantly.
        * **Top Performing Category**: **{top_rev_cat}** is currently driving your highest overall transaction volume. Funnel a larger share of your marketing budget here to maximize returns.
        """)
        
    with col_right:
        st.markdown("### Immediate Inventory Action Items")
        st.markdown(f"""
        * **Launch Lightning Deals**: We identified **{len(undiscovered_gems)} products** that have near-perfect 5-star customer ratings but very low visibility. Move them to front-page promotions immediately.
        * **Stop Margin Bleeding**: We found **{len(underperforming_items)} products** with heavy discounts over 50% that are still trapped with sub-3.5 star ratings. Reduce these discounts immediately to protect profit margins.
        """)

    # -------------------------------------------------------------
    # 7. DRILL-DOWN DATA VIEWS (ORGANIZED IN CLEAN TABS)
    # -------------------------------------------------------------
    st.markdown("---")
    st.subheader("Granular Data Exploration")

    tab_table, tab_charts = st.tabs(["View Targeted Product Action List", "View Visual Analytical Charts"])

    with tab_table:
        st.markdown("### Inventory Action List: Ready for Promotional Campaign Deployment")
        if not undiscovered_gems.empty:
            action_list = undiscovered_gems[['product_name', 'root_category', 'discounted_price', 'rating', 'rating_count']].sort_values(by='rating', ascending=False).head(15)
            action_list.columns = ['Product Name', 'Category', 'Current Price', 'Rating Score', 'Review Counts']
            st.dataframe(action_list, use_container_width=True, hide_index=True)
            
            st.download_button(
                label="Export Marketing Target List to CSV",
                data=action_list.to_csv(index=False).encode('utf-8'),
                file_name="amazon_marketing_targets.csv",
                mime="text/csv",
                help="Click here to download this list for ad campaigns."
            )
        else:
            st.info("No products match the specific criteria.")

    with tab_charts:
        st.markdown("### Advanced Technical Chart Matrices")
        col_row1_left, col_row1_right = st.columns(2)
        with col_row1_left:
            st.markdown("#### Pricing Elasticity Sweet-Spot Locator")
            st.plotly_chart(fig_elasticity, use_container_width=True)
        with col_row1_right:
            st.markdown("#### Top 10 Products by Estimated Sales Volume")
            st.plotly_chart(fig_products_sales, use_container_width=True)
            
        st.markdown("#### High-Conversion Promotion Strategy Blueprint (Heatmap Matrix)")
        st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.warning("Please select at least one product category in the sidebar to populate dashboard metrics.")

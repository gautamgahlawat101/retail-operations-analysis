import html

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Design tokens ──────────────────────────────────────────────────────────────
PRIMARY = "#3B82F6"
TEAL = "#2DD4BF"
ORANGE = "#FB923C"
GRAY = "#64748B"
MUTED = "#94A3B8"
BEST = "#22C55E"
WORST = "#EF4444"
BG = "#0F172A"
SURFACE = "#1E293B"
TEXT = "#F8FAFC"
MUTED = "#CBD5E1"
COLORWAY = [PRIMARY, TEAL, ORANGE, GRAY, MUTED]

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    colorway=COLORWAY,
    font=dict(color=TEXT, family="Inter, Arial, sans-serif", size=13),
    margin=dict(l=48, r=24, t=16, b=48),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
    yaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
)


def apply_chart_style(fig):
    fig.update_layout(**CHART_LAYOUT)
    return fig


def format_currency(value):
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.2f}"


def chart_spacer():
    return


def section_header(title):
    st.header(title)


def subchart(title):
    st.subheader(title)


def format_kpi_value(value, format_name, prefix="", suffix=""):
    if format_name == "currency":
        if value >= 1_000_000:
            return f"{prefix}{value / 1_000_000:.2f}M"
        if value >= 1_000:
            return f"{prefix}{value / 1_000:.1f}K"
        return f"{prefix}{value:,.0f}"
    if format_name == "decimal":
        return f"{prefix}{value:.2f}{suffix}"
    return f"{prefix}{int(round(value)):,}{suffix}"


def render_animated_metrics(cards):
    """Render KPI cards using native Streamlit metric widgets."""
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            st.metric(
                label=card["label"],
                value=format_kpi_value(
                    card["target"],
                    card["format"],
                    card.get("prefix", ""),
                    card.get("suffix", ""),
                ),
            )


def inject_dark_theme():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {BG};
                color: {TEXT} !important;
            }}
            .stMarkdownContainer, .stDataFrame, .stTabs, .stDataFrame div {{
                color: {TEXT} !important;
            }}
            [data-testid="stHeader"] {{
                background: rgba(15, 23, 42, 0.85);
            }}
            .block-container {{
                padding-top: 1rem !important;
                padding-bottom: 2rem !important;
            }}
            h1 {{
                color: {TEXT} !important;
                font-weight: 700 !important;
                margin-top: 0 !important;
                margin-bottom: 0 !important;
            }}
            h2, h3 {{
                color: {TEXT} !important;
            }}
            [data-testid="stMetricContainer"] {{
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid rgba(56, 189, 248, 0.28);
                border-radius: 16px;
                padding: 0.9rem 1rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            }}
            [data-testid="stMetricLabel"] {{
                color: {TEXT} !important;
                font-weight: 600 !important;
            }}
            [data-testid="stMetricValue"] {{
                font-size: 1.5rem;
                color: #F8FAFC !important;
            }}
            [data-testid="stSelectbox"] label,
            [data-testid="stMultiSelect"] label,
            [data-testid="stForm"] label,
            [data-testid="stSelectbox"] span,
            [data-testid="stMultiSelect"] span,
            [data-testid="stSelectbox"] div[role="combobox"],
            [data-testid="stMultiSelect"] div[role="combobox"] {{
                color: #F8FAFC !important;
                font-weight: 600 !important;
            }}
            [data-testid="stSelectbox"] > div,
            [data-testid="stMultiSelect"] > div {{
                min-height: 2.2rem !important;
            }}
            [data-testid="stSelectbox"] [data-baseweb="select"],
            [data-testid="stMultiSelect"] [data-baseweb="select"] {{
                min-height: 2.2rem !important;
                background: rgba(15, 23, 42, 0.98) !important;
            }}
            [data-testid="stSelectbox"] > div > div > div,
            [data-testid="stMultiSelect"] > div > div > div {{
                padding-top: 0.2rem !important;
                padding-bottom: 0.2rem !important;
                background: rgba(15, 23, 42, 0.98) !important;
                color: #F8FAFC !important;
            }}
            [data-testid="stSelectbox"] input,
            [data-testid="stMultiSelect"] input,
            [data-testid="stMultiSelect"] [data-baseweb="tag"] span,
            [data-testid="stMultiSelect"] [data-baseweb="tag"] {{
                color: #F8FAFC !important;
            }}
            [data-testid="stMultiSelect"] [data-baseweb="tag"] {{
                background: rgba(59, 130, 246, 0.32) !important;
                border: 1px solid rgba(59, 130, 246, 0.55) !important;
            }}
            [data-baseweb="popover"],
            [data-baseweb="menu"] {{
                background: {BG} !important;
                color: #F8FAFC !important;
            }}
            [data-baseweb="popover"] *,
            [data-baseweb="menu"] *,
            [role="option"],
            [role="listbox"] * {{
                color: #F8FAFC !important;
                background: transparent !important;
            }}
            [data-baseweb="menu"] [aria-selected="true"] {{
                background: rgba(59, 130, 246, 0.35) !important;
                color: #F8FAFC !important;
            }}
            [data-baseweb="menu"] [aria-selected="true"] * {{
                color: #F8FAFC !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def period_mask(dates, ref_date, period):
    if period == "mtd":
        return (
            (dates.dt.year == ref_date.year)
            & (dates.dt.month == ref_date.month)
            & (dates <= ref_date)
        )
    if period == "qtd":
        q_start = ((ref_date.month - 1) // 3) * 3 + 1
        return (
            (dates.dt.year == ref_date.year)
            & (dates.dt.month >= q_start)
            & (dates.dt.month <= ref_date.month)
            & (dates <= ref_date)
        )
    if period == "ytd":
        return (dates.dt.year == ref_date.year) & (dates <= ref_date)
    raise ValueError(f"Unknown period: {period}")


def cumulative_daily_revenue(df_exp, ref_date, period):
    mask = period_mask(df_exp["Date"], ref_date, period)
    subset = df_exp.loc[mask]
    daily = (
        subset.groupby(subset["Date"].dt.date)["Total_Cost"]
        .sum()
        .sort_index()
        .cumsum()
        .reset_index()
    )
    daily.columns = ["Date", "Cumulative_Revenue"]
    daily["Date"] = pd.to_datetime(daily["Date"])
    return daily


def build_sankey_from_flows(flows):
    """Build a 3-level Sankey: Customer_Category → Store_Type → Payment_Method."""
    categories = sorted(flows["Customer_Category"].unique())
    stores = sorted(flows["Store_Type"].unique())
    payments = sorted(flows["Payment_Method"].unique())

    cat_idx = {c: i for i, c in enumerate(categories)}
    store_idx = {s: i + len(categories) for i, s in enumerate(stores)}
    pay_idx = {p: i + len(categories) + len(stores) for i, p in enumerate(payments)}

    labels = categories + stores + payments
    node_colors = (
        [PRIMARY] * len(categories)
        + [TEAL] * len(stores)
        + [ORANGE] * len(payments)
    )

    cs = flows.groupby(["Customer_Category", "Store_Type"])["value"].sum().reset_index()
    sp = flows.groupby(["Store_Type", "Payment_Method"])["value"].sum().reset_index()

    sources, targets, values = [], [], []
    for _, row in cs.iterrows():
        sources.append(cat_idx[row["Customer_Category"]])
        targets.append(store_idx[row["Store_Type"]])
        values.append(row["value"])
    for _, row in sp.iterrows():
        sources.append(store_idx[row["Store_Type"]])
        targets.append(pay_idx[row["Payment_Method"]])
        values.append(row["value"])

    link_colors = []
    for s in sources:
        if s < len(categories):
            link_colors.append("rgba(59,130,246,0.35)")
        else:
            link_colors.append("rgba(45,212,191,0.35)")

    fig = go.Figure(
        go.Sankey(
            node=dict(pad=18, thickness=18, line=dict(color="#334155", width=0.5),
                      label=labels, color=node_colors),
            link=dict(source=sources, target=targets, value=values, color=link_colors),
        )
    )
    return apply_chart_style(fig)


def build_sankey_count(df_txn):
    flows = (
        df_txn.groupby(["Customer_Category", "Store_Type", "Payment_Method"])["Transaction_ID"]
        .nunique()
        .reset_index(name="value")
    )
    return build_sankey_from_flows(flows)


@st.cache_data
def load_data():
    clean_cols = [
        "Transaction_ID",
        "Date",
        "Customer_Name",
        "Product",
        "Total_Items",
        "Total_Cost",
        "Payment_Method",
        "City",
        "Store_Type",
        "Discount_Applied",
        "Customer_Category",
        "Season",
    ]
    exploded_cols = [
        "Transaction_ID",
        "Date",
        "Customer_Name",
        "Product",
        "Payment_Method",
        "City",
        "Store_Type",
        "Customer_Category",
        "Season",
        "Day_Of_Week",
        "Total_Cost",
    ]

    df = pd.read_csv(
        "data/df_cleaned.csv",
        usecols=clean_cols,
        parse_dates=["Date"],
        low_memory=False,
    )

    df_exploded = pd.read_csv(
        "data/df_exploded_priced.csv",
        usecols=exploded_cols,
        parse_dates=["Date"],
        low_memory=False,
    )

    return df, df_exploded


# ── Page setup ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_dark_theme()

st.markdown("# Retail Analytics Dashboard")

df, df_exploded = load_data()

cities = sorted(df["City"].unique())
store_types = sorted(df["Store_Type"].unique())

with st.form("dashboard_filters"):
    filt_col1, filt_col2, filt_col3 = st.columns([1.5, 1.5, 0.7])
    with filt_col1:
        selected_cities = st.multiselect("City", options=cities, default=cities)
    with filt_col2:
        selected_store_types = st.multiselect("Store Type", options=store_types, default=store_types)
    with filt_col3:
        st.markdown("<div style='height: 1.9rem;'></div>", unsafe_allow_html=True)
        apply_filters = st.form_submit_button("Apply", type="primary", use_container_width=True)

if apply_filters:
    df_f = df[df["City"].isin(selected_cities) & df["Store_Type"].isin(selected_store_types)]
    df_exp = df_exploded[
        df_exploded["City"].isin(selected_cities) & df_exploded["Store_Type"].isin(selected_store_types)
    ]
else:
    df_f = df[df["City"].isin(cities) & df["Store_Type"].isin(store_types)]
    df_exp = df_exploded[
        df_exploded["City"].isin(cities) & df_exploded["Store_Type"].isin(store_types)
    ]

if df_f.empty or df_exp.empty:
    st.warning("No records match the selected city/store type combination.")
    st.stop()

ref_date = df_exp["Date"].max()
latest_year = int(ref_date.year)

# ── Core KPI calculations ──────────────────────────────────────────────────────
total_revenue = df_exp["Total_Cost"].sum()
total_transactions = df_f["Transaction_ID"].nunique()
avg_order_value = total_revenue / total_transactions if total_transactions else 0
total_customers = df_f["Customer_Name"].nunique()
clv = total_revenue / total_customers if total_customers else 0

mtd_revenue = df_exp.loc[period_mask(df_exp["Date"], ref_date, "mtd"), "Total_Cost"].sum()
qtd_revenue = df_exp.loc[period_mask(df_exp["Date"], ref_date, "qtd"), "Total_Cost"].sum()
ytd_revenue = df_exp.loc[period_mask(df_exp["Date"], ref_date, "ytd"), "Total_Cost"].sum()

avg_items = df_f["Total_Items"].mean()
discount_rate = df_f["Discount_Applied"].mean() * 100

first_txn = df_f.groupby("Customer_Name")["Date"].min()
customers_latest = df_f.loc[df_f["Date"].dt.year == latest_year, "Customer_Name"].unique()
new_customers = sum(first_txn[c].year == latest_year for c in customers_latest)
repeat_customers = len(customers_latest) - new_customers

# ── Section 1: Overview KPIs ───────────────────────────────────────────────────
section_header("Overview")

render_animated_metrics([
    {"label": "Total Revenue", "target": total_revenue, "format": "currency", "prefix": "$"},
    {"label": "Total Transactions", "target": total_transactions, "format": "int"},
    {"label": "Average Order Value", "target": avg_order_value, "format": "currency", "prefix": "$"},
    {"label": "Unique Customers", "target": total_customers, "format": "int"},
])

render_animated_metrics([
    {"label": "Customer Lifetime Value", "target": clv, "format": "currency", "prefix": "$"},
    {"label": f"Revenue MTD ({ref_date.strftime('%b %Y')})", "target": mtd_revenue, "format": "currency", "prefix": "$"},
    {"label": f"Revenue QTD (Q{(ref_date.month - 1) // 3 + 1} {latest_year})", "target": qtd_revenue, "format": "currency", "prefix": "$"},
    {"label": f"Revenue YTD ({latest_year})", "target": ytd_revenue, "format": "currency", "prefix": "$"},
])

render_animated_metrics([
    {"label": "Avg Items per Transaction", "target": avg_items, "format": "decimal", "suffix": ""},
    {"label": "Discount Rate", "target": discount_rate, "format": "decimal", "suffix": "%"},
    {"label": f"New Customers ({latest_year})", "target": new_customers, "format": "int"},
    {"label": f"Repeat Customers ({latest_year})", "target": repeat_customers, "format": "int"},
])

st.divider()

# ── Section 2: Time-based trends ───────────────────────────────────────────────
section_header("Revenue Over Time")

col_t1, col_t2 = st.columns(2)

with col_t1:
    subchart("Monthly Revenue Trend")
    monthly = (
        df_exp.groupby(df_exp["Date"].dt.to_period("M"))["Total_Cost"]
        .sum()
        .reset_index()
    )
    monthly["Date"] = monthly["Date"].dt.to_timestamp()
    fig = px.line(
        monthly, x="Date", y="Total_Cost",
        labels={"Total_Cost": "Revenue ($)", "Date": ""},
    )
    fig.update_traces(line=dict(color=PRIMARY, width=2.5))
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_t2:
    subchart("Revenue by Season")
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    revenue_by_season = (
        df_exp.groupby("Season")["Total_Cost"].sum().reindex(season_order).reset_index()
    )
    fig = px.bar(
        revenue_by_season, x="Season", y="Total_Cost",
        labels={"Total_Cost": "Revenue ($)", "Season": ""},
    )
    fig.update_traces(marker_color=PRIMARY)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

subchart("Cumulative Revenue — Month / Quarter / Year to Date")
col_t3, col_t4, col_t5 = st.columns(3)

period_labels = {
    "mtd": f"MTD ({ref_date.strftime('%b %Y')})",
    "qtd": f"QTD (Q{(ref_date.month - 1) // 3 + 1})",
    "ytd": f"YTD ({latest_year})",
}

for col, period in zip([col_t3, col_t4, col_t5], ["mtd", "qtd", "ytd"]):
    cum = cumulative_daily_revenue(df_exp, ref_date, period)
    with col:
        fig = px.line(
            cum, x="Date", y="Cumulative_Revenue",
            labels={"Cumulative_Revenue": "Revenue ($)", "Date": ""},
            title=period_labels[period],
        )
        fig.update_traces(line=dict(color=TEAL, width=2))
        fig.update_layout(
            showlegend=False,
            title=dict(font=dict(size=13, color=MUTED), x=0, xanchor="left"),
            margin=dict(l=40, r=16, t=36, b=40),
        )
        st.plotly_chart(apply_chart_style(fig), width="stretch")

st.divider()

# ── Section 3: Store Performance ─────────────────────────────────────────────────
section_header("Store Performance")

col_a, col_b = st.columns(2)

with col_a:
    subchart("Revenue by Store Type")
    revenue_by_store = (
        df_exp.groupby("Store_Type")["Total_Cost"].sum().reset_index().sort_values("Total_Cost")
    )
    fig = px.bar(
        revenue_by_store, x="Total_Cost", y="Store_Type", orientation="h",
        labels={"Total_Cost": "Revenue ($)", "Store_Type": ""},
    )
    fig.update_traces(marker_color=PRIMARY)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_b:
    subchart("Transaction Count by Store Type")
    txn_by_store = (
        df_f.groupby("Store_Type")["Transaction_ID"]
        .nunique()
        .reset_index(name="Transaction_Count")
        .sort_values("Transaction_Count")
    )
    fig = px.bar(
        txn_by_store, x="Transaction_Count", y="Store_Type", orientation="h",
        labels={"Transaction_Count": "Transactions", "Store_Type": ""},
    )
    fig.update_traces(marker_color=TEAL)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

revenue_pivot = df_exp.pivot_table(
    values="Total_Cost", index="Store_Type", columns="City", aggfunc="sum", fill_value=0
)
txn_pivot = df_f.pivot_table(
    values="Transaction_ID", index="Store_Type", columns="City", aggfunc="nunique", fill_value=0
)
combo_df = (
    (revenue_pivot / txn_pivot.replace(0, float("nan")))
    .stack()
    .reset_index(name="Avg_Revenue_Per_Transaction")
    .dropna(subset=["Avg_Revenue_Per_Transaction"])
)
combo_df["Combo"] = combo_df["Store_Type"] + " × " + combo_df["City"]

col_c, col_d = st.columns(2)

with col_c:
    subchart("Best Store × City Combos")
    best_5 = combo_df.nlargest(5, "Avg_Revenue_Per_Transaction")
    fig = px.bar(
        best_5, x="Avg_Revenue_Per_Transaction", y="Combo", orientation="h",
        labels={"Avg_Revenue_Per_Transaction": "Avg Revenue / Txn ($)", "Combo": ""},
    )
    fig.update_traces(marker_color=BEST)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_d:
    subchart("Worst Store × City Combos")
    worst_5 = combo_df.nsmallest(5, "Avg_Revenue_Per_Transaction")
    fig = px.bar(
        worst_5, x="Avg_Revenue_Per_Transaction", y="Combo", orientation="h",
        labels={"Avg_Revenue_Per_Transaction": "Avg Revenue / Txn ($)", "Combo": ""},
    )
    fig.update_traces(marker_color=WORST)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

st.divider()

# ── Section 4: Geographic Breakdown ──────────────────────────────────────────────
section_header("Geographic Breakdown")

col_e, col_f = st.columns([2, 1])

with col_e:
    subchart("Revenue by City")
    revenue_by_city = (
        df_exp.groupby("City")["Total_Cost"].sum().reset_index().sort_values("Total_Cost")
    )
    fig = px.bar(
        revenue_by_city, x="Total_Cost", y="City", orientation="h",
        labels={"Total_Cost": "Revenue ($)", "City": ""},
    )
    fig.update_traces(marker_color=PRIMARY)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_f:
    subchart("Top Cities")
    top_cities = (
        df_exp.groupby("City")["Total_Cost"].sum().sort_values(ascending=False).reset_index()
    )
    top_cities.columns = ["City", "Revenue"]
    top_cities["Revenue"] = top_cities["Revenue"].apply(format_currency)
    st.dataframe(top_cities, hide_index=True, width="stretch")

st.divider()

# ── Section 5: Customer Insights ───────────────────────────────────────────────
section_header("Customer Insights")

col_g, col_h = st.columns(2)

with col_g:
    subchart("Customer Category Distribution")
    category_counts = df_f["Customer_Category"].value_counts().reset_index()
    category_counts.columns = ["Customer_Category", "Count"]
    fig = px.bar(
        category_counts.sort_values("Count"),
        x="Count", y="Customer_Category", orientation="h",
        labels={"Count": "Transactions", "Customer_Category": ""},
    )
    fig.update_traces(marker_color=PRIMARY)
    fig.update_layout(showlegend=False)
    st.caption("Uniform ~12.5% per category — bar chart highlights the even split more clearly than a pie.")
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_h:
    subchart("Repeat vs One-time Customers")
    customer_txn_counts = df_f["Customer_Name"].value_counts()
    repeat_split = pd.DataFrame(
        {
            "Segment": ["One-time (1 txn)", "Repeat (2+ txns)"],
            "Count": [(customer_txn_counts == 1).sum(), (customer_txn_counts >= 2).sum()],
        }
    )
    fig = px.bar(
        repeat_split, x="Segment", y="Count",
        labels={"Count": "Customers", "Segment": ""},
        color="Segment",
        color_discrete_map={"One-time (1 txn)": ORANGE, "Repeat (2+ txns)": TEAL},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

col_g2, col_g3 = st.columns(2)

with col_g2:
    subchart(f"New vs Repeat Customers in {latest_year}")
    yr_split = pd.DataFrame(
        {"Segment": ["New", "Repeat"], "Count": [new_customers, repeat_customers]}
    )
    fig = px.bar(
        yr_split, x="Segment", y="Count",
        labels={"Count": "Customers", "Segment": ""},
        color="Segment",
        color_discrete_map={"New": PRIMARY, "Repeat": TEAL},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_g3:
    subchart("Weekday vs Weekend Revenue")
    weekend_days = {"Saturday", "Sunday"}
    df_exp_copy = df_exp.copy()
    df_exp_copy["Period"] = df_exp_copy["Day_Of_Week"].apply(
        lambda d: "Weekend" if d in weekend_days else "Weekday"
    )
    wd_we = df_exp_copy.groupby("Period")["Total_Cost"].sum().reset_index()
    fig = px.bar(
        wd_we, x="Period", y="Total_Cost",
        labels={"Total_Cost": "Revenue ($)", "Period": ""},
        color="Period",
        color_discrete_map={"Weekday": PRIMARY, "Weekend": ORANGE},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

subchart("Customer Journey — Category → Store → Payment")
sankey_rev = (
    df_exp.groupby(["Customer_Category", "Store_Type", "Payment_Method"])["Total_Cost"]
    .sum()
    .reset_index(name="value")
)
sankey_tabs = st.tabs(["By Transaction Count", "By Revenue"])
with sankey_tabs[0]:
    st.plotly_chart(build_sankey_count(df_f), width="stretch")
with sankey_tabs[1]:
    st.plotly_chart(build_sankey_from_flows(sankey_rev), width="stretch")

col_p1, col_p2 = st.columns(2)

with col_p1:
    subchart("Pareto — Customer Revenue Concentration")
    cust_rev = (
        df_exp.groupby("Customer_Name")["Total_Cost"].sum().sort_values(ascending=False).reset_index()
    )
    cust_rev["Cumulative_Pct"] = cust_rev["Total_Cost"].cumsum() / cust_rev["Total_Cost"].sum() * 100
    cust_rev["Customer_Pct"] = (cust_rev.index + 1) / len(cust_rev) * 100
    fig = px.line(
        cust_rev, x="Customer_Pct", y="Cumulative_Pct",
        labels={"Customer_Pct": "% of Customers (ranked)", "Cumulative_Pct": "% of Total Revenue"},
    )
    fig.update_traces(line=dict(color=PRIMARY, width=2.5))
    fig.add_hline(y=80, line_dash="dash", line_color=GRAY, annotation_text="80%")
    fig.update_layout(showlegend=False)
    top20_share = cust_rev.loc[cust_rev["Customer_Pct"] <= 20, "Cumulative_Pct"].max()
    st.caption(f"Top 20% of customers generate ~{top20_share:.0f}% of revenue.")
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_p2:
    subchart("Customer Category × Store Type")
    heatmap_data = pd.crosstab(df_f["Customer_Category"], df_f["Store_Type"])
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Store Type", y="Customer Category", color="Transactions"),
        color_continuous_scale=[[0, SURFACE], [0.5, PRIMARY], [1, TEAL]],
        aspect="auto",
    )
    fig.update_layout(coloraxis_colorbar=dict(title="Txns"))
    st.plotly_chart(apply_chart_style(fig), width="stretch")

subchart("Top 10 Most Frequent Customers")
top10_customers = df_f["Customer_Name"].value_counts().head(10).reset_index()
top10_customers.columns = ["Customer_Name", "Transaction_Count"]
fig = px.bar(
    top10_customers, x="Transaction_Count", y="Customer_Name", orientation="h",
    labels={"Transaction_Count": "Transactions", "Customer_Name": ""},
)
fig.update_traces(marker_color=TEAL)
fig.update_layout(showlegend=False)
st.plotly_chart(apply_chart_style(fig), width="stretch")

st.divider()

# ── Section 6: Product Analysis ────────────────────────────────────────────────
section_header("Product Analysis")

col_i, col_j = st.columns(2)

with col_i:
    subchart("Top 10 Products by Revenue")
    top10_revenue = (
        df_exp.groupby("Product")["Total_Cost"].sum().sort_values(ascending=False).head(10).reset_index()
    )
    fig = px.bar(
        top10_revenue, x="Total_Cost", y="Product", orientation="h",
        labels={"Total_Cost": "Revenue ($)", "Product": ""},
    )
    fig.update_traces(marker_color=PRIMARY)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

with col_j:
    subchart("Top 10 Products by Purchase Count")
    top10_count = df_exp["Product"].value_counts().head(10).reset_index()
    top10_count.columns = ["Product", "Purchase_Count"]
    fig = px.bar(
        top10_count, x="Purchase_Count", y="Product", orientation="h",
        labels={"Purchase_Count": "Purchases", "Product": ""},
    )
    fig.update_traces(marker_color=TEAL)
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_style(fig), width="stretch")

st.divider()

# ── Section 7: Payment Methods ───────────────────────────────────────────────────
section_header("Payment Methods")

subchart("Payment Method Distribution")
payment_counts = df_f["Payment_Method"].value_counts().reset_index()
payment_counts.columns = ["Payment_Method", "Count"]
fig = px.pie(
    payment_counts,
    names="Payment_Method",
    values="Count",
    hole=0.45,
    color_discrete_sequence=[TEAL, PRIMARY, ORANGE, MUTED],
)
fig.update_traces(
    textinfo="percent+label",
    textfont=dict(color=TEXT, size=13),
    hovertemplate="%{label}: %{value} transactions<extra></extra>",
)
fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        font=dict(color=TEXT, size=12),
    ),
)
st.plotly_chart(apply_chart_style(fig), width="stretch")


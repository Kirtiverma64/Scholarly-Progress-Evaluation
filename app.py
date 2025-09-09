import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel("Student Performance Analysis sheet.xlsx", sheet_name="Marks")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

st.title("📊 Student Performance Dashboard")

# Show dataset preview
with st.expander("🔍 View Dataset"):
    st.dataframe(df.head())

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filters")

# Automatically detect categorical columns
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

for col in cat_cols:
    options = st.sidebar.multiselect(f"Filter {col.capitalize()}:", options=df[col].unique())
    if options:
        df = df[df[col].isin(options)]

# --- Display filtered dataset ---
st.subheader("Filtered Data")
st.dataframe(df)

# --- Visualization Section ---
st.subheader("📈 Visualizations")

# Ensure numeric columns are correctly typed
df = df.apply(pd.to_numeric, errors="ignore")
num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

# Scatter plot
if len(num_cols) >= 2:
    x_axis = st.selectbox("Select X-axis:", num_cols, index=0)
    y_axis = st.selectbox("Select Y-axis:", num_cols, index=1)

    fig, ax = plt.subplots()
    ax.scatter(df[x_axis], df[y_axis], alpha=0.6, c="blue")
    ax.set_xlabel(x_axis.capitalize())
    ax.set_ylabel(y_axis.capitalize())
    st.pyplot(fig)
else:
    st.warning("⚠️ Not enough numeric columns for scatter plot. Check your dataset.")

# Grouped bar chart
if cat_cols and num_cols:
    cat_col = st.selectbox("Select Categorical Column (for group analysis):", cat_cols)
    num_col = st.selectbox("Select Numeric Column (to average):", num_cols)

    avg_vals = df.groupby(cat_col)[num_col].mean().sort_values()

    fig, ax = plt.subplots(figsize=(7, 5))
    avg_vals.plot(kind="barh", ax=ax, color="teal")  # horizontal bar chart
    ax.set_xlabel(f"Average {num_col.capitalize()}")
    ax.set_ylabel(cat_col.capitalize())
    plt.tight_layout()
    st.pyplot(fig)

st.success("✅ Interactive dashboard ready!")

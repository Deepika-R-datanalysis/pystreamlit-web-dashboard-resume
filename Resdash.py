import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load or create the applicants DataFrame
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Applicants.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Category', 'Resume'])
    return df

# Function to save the applicants DataFrame


def save_data(df):
    df.to_csv('Applicants.csv', index=False)

    # Main function to run the ATS

def main():
    st.title('Applicant Resume Dashboard')

    # Load or create the DataFrame
    df = load_data()

    # sidebar

    st.sidebar.header("Please Filter Here:")
    category = st.sidebar.multiselect(
        "Select the Category:",
        options=df["Category"].unique(),
        default=df["Category"].unique()

    )

    df_selection = df.query("Category == @category")

    st.dataframe(df_selection)

    # Count by Category [BAR CHART]
    count_by_category = df_selection.groupby(by=["Category"])[["Resume"]].count().sort_values(by="Category")
    fig_count_category = px.bar(
        count_by_category,
        x="Resume",
        y=count_by_category.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#0083B8"] * len(count_by_category),
        template="plotly_white",
    )
    fig_count_category.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_count_category, use_container_width=True)

    # Check if the dataframe is empty:
    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()  # This will halt the app from further execution.

    # Display the DataFrame
    # print(df)
    # Main content
    # st.subheader('View Applicants')
    # st.write(df)


if __name__ == '__main__':
    main()

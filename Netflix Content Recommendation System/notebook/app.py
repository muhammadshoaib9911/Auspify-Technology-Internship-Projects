import streamlit as st
from recommender import recommend, df


st.set_page_config(
    page_title="Netflix Recommendation System",
    page_icon="🎬",
    layout="wide"
)


st.title("🎬 Netflix Recommendation System")

st.write(
    "Discover movies and TV shows similar to your favorite titles."
)


# Title selection
selected_title = st.selectbox(
    "Select a Netflix title:",
    sorted(df["title"].unique())
)


# Number of recommendations
num_recommendations = st.slider(
    "Number of recommendations",
    min_value=5,
    max_value=10,
    value=5
)


if st.button("🎯 Recommend"):

    recommendations = recommend(
        selected_title,
        num_recommendations
    )

    st.subheader(
        f"Recommended titles similar to '{selected_title}'"
    )

    for _, row in recommendations.iterrows():

        st.markdown(
            f"""
            ### 🎬 {row['title']}

            **Type:** {row['type']}  
            **Genre:** {row['listed_in']}  
            **Rating:** {row['rating']}  
            **Similarity:** {row['similarity_score']}%
            """
        )

        st.divider()
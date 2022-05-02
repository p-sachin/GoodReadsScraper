import streamlit as st
from PIL import Image  # Required to show images
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

img1 = Image.open("img/goodreads.png")
st.image(img1)
# Text/Title
st.title("Best Books of the Decade: 2000s")


# Header/Subheader
st.header("""
**Objectives:**""")

st.markdown("""
> 1. Scraping the required data of the analysis of 6399 books.

> 2. Creating own dataset for 5596 best books using pandas.

> 3. Preprocessing the data for better analysis, by transforming the data with normalization.

> 4. Visualizing the data using matplotlib and seaborn.

> 5. Publishing the results using streamlit with the help of plotly.

""")


# Actual work begins here

df = pd.read_csv("data/goodread_final_5596.csv")


df['url'] = df["url"].astype(str)
df['title'] = df["title"].astype(str)
df['author'] = df['author'].astype(str)
df['num_reviews'] = df['num_reviews'].astype(int)
df['num_ratings'] = df['num_ratings'].astype(int)
df['avg_rating'] = df['avg_rating'].astype(float)
df['num_pages'] = df['num_pages'].astype(int)
df['original_publish_year'] = df['original_publish_year'].astype(int)

# df["awards"] = df["awards"].apply(eval).str.len()
df["genres"] = df["genres"].apply(eval)
df["places"] = df["places"].apply(eval)

# apply the min-max scaling in Pandas using the .min() and .max() methods


def min_max_normalization(df):
    # copy the dataframe
    df_norm = df.copy()
    # apply min-max scaling
    df_norm["minmax_norm_ratings"] = 1 + ((df_norm['avg_rating'] - df_norm['avg_rating'].min()) / (
        df_norm['avg_rating'].max() - df_norm['avg_rating'].min())) * 9
    return df_norm


# call the min_max_scaling function
df = min_max_normalization(df)

# call the min_max_scaling function
df = min_max_normalization(df)


# apply the min-max scaling in Pandas using the .min() and .max() methods
def mean_normalization(df):
    # copy the dataframe
    df_norm = df.copy()
    # apply mean scaling
    df_norm["mean_norm_ratings"] = 1 + ((df_norm['avg_rating'] - df_norm['avg_rating'].mean()) / (
        df_norm['avg_rating'].max() - df_norm['avg_rating'].min())) * 9
    return df_norm


# call the min_max_scaling function
df = mean_normalization(df)

st.header('Data Analysis & Key Findings')
st.subheader("""Visualizations (Matplotlib & Plotly)""")
st.text(' ')
st.text(' ')

# 1st Graph Pie Chart
original_title5 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Pie Chart representing the top 10 Genres</p>'
st.markdown(original_title5, unsafe_allow_html=True)

df_pie = pd.read_csv("data/pie_chart.csv")
#fig_piechart = px.pie(df_pie, values='Value', names='Genre', title='Genre of the Books')
# fig_piechart.show()
# st.plotly_chart(fig_piechart.show())

labels = df_pie['Genre']
sizes = df_pie['Value']


fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('equal')

explode = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
ax.pie(sizes, labels=labels, autopct='%1.0f%%', explode=explode)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(plt.show())
st.markdown("""

                   - *The **fiction books** were released the **most** in a decade of 2000s.*
                   - *Similarly, the **science fiction** was **least** released.*
""")
st.text(' ')
st.text(' ')

# 2nd Graph (box & Whisker Plot)
# Median of 325, 1/4th quartile = 250, 3/4th quartile = 416
original_title3 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Box Plot Diagram of Number of Pages in a Book</p>'
st.markdown(original_title3, unsafe_allow_html=True)

img3 = Image.open("img/boxplot.png")
st.image(img3, caption="Box Plot Diagram")
st.markdown("""
                - *Median = 325 Pages*
                - *Maximum = 710 Pages*
                - *Minimum = 5 Pages*
""")
st.text(' ')
st.text(' ')

# 3rd Graph

original_title8 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Number of Books published according to Years</p>'
st.markdown(original_title8, unsafe_allow_html=True)
df_bookaccyears = pd.read_csv("data/booksaccordingtoyears.csv")
fig_booksyears = px.bar(df_bookaccyears, x="Published Years", y="Number of Books",
                        color="Number of Books", color_discrete_sequence=px.colors.qualitative.Dark24)
fig_booksyears.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=2000,
        dtick=1
    ))
st.plotly_chart(fig_booksyears)
st.markdown("""

                   - *In the first 4 years, there was a **slight rise** in the rate of books published each year.*
                   - *From 2004 till 2009, there was a **linear** change in rate of books published each year.*
""")
st.text(' ')
st.text(' ')

# 4th Graph
original_title6 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Relationship of Number of Reviews over published Years</p>'
st.markdown(original_title6, unsafe_allow_html=True)
df_reviewsyears = pd.read_csv("data/reviews_years.csv")
fig_reviewsyears = px.bar(df_reviewsyears, x="Published Years", y="Total Number of Reviews",
                          color="Total Number of Reviews", color_discrete_sequence=px.colors.qualitative.Prism)
fig_reviewsyears.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=2000,
        dtick=1
    ))
st.plotly_chart(fig_reviewsyears)
st.markdown("""

                   - *In the first 4 years, there was a **steady** rate of change in number of reviews.*
                   - *From 2004 till 2009, there was a **major** change in rate of reviews exceeding 1M.*
""")
st.text(' ')
st.text(' ')

# 5th graph
original_title1 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Normalised Average Ratings for a Decade</p>'
st.markdown(original_title1, unsafe_allow_html=True)

df_normalised = pd.read_csv("data/normalised_average.csv")
fig_normalised = px.line(
    df_normalised, x="Published Years", y="Normalised Average Ratings")
fig_normalised.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=2000,
        dtick=1
    ))
fig_normalised.update_layout(
    title_font_family="Times New Roman",
    title_font_color="blue"
)
st.plotly_chart(fig_normalised)

st.markdown("""

                   - *The **highest peak** in 2003 showing an average rating of 8.11.*
                   - *The **lowest peak** in 2007 showing an average rating of 8.05.*
""")
st.text(' ')
st.text(' ')

# 6th Graph
original_title2 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Number of Books published by the Authors (Top 20)</p>'
st.markdown(original_title2, unsafe_allow_html=True)

df_author20 = pd.read_csv("data/top20_author.csv")
#slider_1 = st.slider("Select Awards", min_value=0, max_value=22, value = 22)
fig_authorbooks = px.bar(df_author20, x="Books", y="Author",
                         color='Author', color_discrete_sequence=px.colors.qualitative.Vivid)


st.plotly_chart(fig_authorbooks)
st.markdown("""

                   - *Authors **Meg Cabot** and **Hiromu Arakawa** published **22** books in total during the decade 2000s.*
                   - *There were **5** Authors published **11** books during the between 2000-2009.*
""")
st.text(' ')
st.text(' ')

# 7th Graph
original_title4 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Total Reviews obtained by the Authors (Top 20)</p>'
st.markdown(original_title4, unsafe_allow_html=True)
df_authorreviewed20 = pd.read_csv("data/top20_reviewedauthor.csv")
#slider_1 = st.slider("Select me", min_value=0, max_value=20)
fig_authorreviewed = px.bar(df_authorreviewed20, x="Author",
                            y="Total Aggregated Reviews", color="Total Aggregated Reviews")

st.plotly_chart(fig_authorreviewed)
st.markdown("""

                   - *The **highest** number of total reviews is to be seen with the Author Stephanie Meyer, she published 9 books in the 2000s decade and showing that she had more than 0.3M readers.*
                   - *The **lowest** number of total reviews is to be seen with Author Sara Gruen, she published only one book and gathered around 60k reviews showing that the readers were exceeding 60k.*
""")
st.text(' ')
st.text(' ')

# 8th Graph
original_title9 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Number of Awards given to the Authors (Top 20)</p>'
st.markdown(original_title9, unsafe_allow_html=True)

df_authorawards1 = pd.read_csv("data/authors_awards.csv")
#slider_1 = st.slider("Select Awards", min_value=0, max_value=22, value = 22)
fig_authorawards1 = px.bar(df_authorawards1, x="Awards", y="Author",
                           color='Author', color_discrete_sequence=px.colors.qualitative.Alphabet)


st.plotly_chart(fig_authorawards1)
st.markdown("""

                   - *Author **Neil Gaimann** received **60** Awards.*
                   - *Author **Mo Willems** received **11** Awards.*
""")
st.text(' ')
st.text(' ')


st.header("Conclusion")

st.text(' ')

# 9th Graph
original_title7 = '<p style="font-family:Times New Roman; color:Blue; font-size: 18px;">Correlation Coefficient Heat Map</p>'
st.markdown(original_title7, unsafe_allow_html=True)

img4 = Image.open("img/cr.png")
st.image(img4, caption="Correlation Coefficient Heat Map")
st.markdown("""
                - *A **strong uphill** (positive linear) relationship can be seen between the **number of ratings & number of reviews**.*
                - *A **moderate uphill** (positive linear) relationship is being observed between **number of reviews & awards** and **number of ratings & awards**.*
                - *No linear relationship can be observed between the **series released & the number of ratings**.*
""")
st.text(' ')
st.text(' ')

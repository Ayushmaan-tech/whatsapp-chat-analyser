import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)



    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words,num_media_messages,num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2 ,col3,col4= st.columns(4)  # Only two columns now, each with even width

        with col1:
            st.header("Total Messages")
            st.subheader(f"{num_messages}")  # Use subheader to keep text smaller if needed for alignment

        with col2:
            st.header("Total Words")
            st.subheader(f"{words}")  # Use subheader here as well to match sizes
        with col3:
            st.header("Media Shared")
            st.subheader(f"{num_media_messages}")
        with col4:
            st.header("Links Shared")
            st.subheader(f"{num_links}")

    #monthly timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # daily timeline
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='blue')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # activity map
    st.title('Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        st.header("Most busy day")

        busy_day = helper.week_activity_map(selected_user, df)
        busy_day.index = pd.CategoricalIndex(busy_day.index, categories=day_order, ordered=True)
        busy_day = busy_day.sort_index()

        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        busy_month.index = pd.CategoricalIndex(busy_month.index, categories=month_order, ordered=True)
        busy_month=busy_month.sort_index()

        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    # finding the busiest user in group
    if selected_user=='Overall':
        st.title("Most Busy User")
        x,new_df=helper.most_busy_users(df)
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)

        with col1:
            ax.bar(x.index,x.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

     # WordCloud
    st.title("Wordcloud")
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # most common words
    most_common_df = helper.most_common_words(selected_user,df)

    fig,ax = plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')

    st.title('Most commmon words')
    st.pyplot(fig)

    # emoji analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)
    if emoji_df is not None and not emoji_df.empty:
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)


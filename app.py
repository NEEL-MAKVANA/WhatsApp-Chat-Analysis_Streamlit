import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

st.set_page_config(
    page_title="Whats app chat analyser",
    # page_icon="nk.png",  # Provide the path to your logo file
)

st.sidebar.title("Welcome to chat analysis app")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.title("All the chats from file")
    st.dataframe(df)

    # fetch unique users
    user_list = df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user, df
        )
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        # st.title("Monthly Timeline")
        # timeline = helper.monthly_timeline(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.plot(timeline["time"], timeline["message"], color="green")
        # plt.xticks(rotation="vertical")
        # st.pyplot(fig)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(
            selected_user, df
        )  # Assuming selected_user and df are defined elsewhere
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"], color="green")
        ax.set_xlabel("Monthly Time")  # Adding label to the x-axis
        ax.set_ylabel("Message Count")  # Adding label to the y-axis
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["message"], color="black")
        ax.set_xlabel("Daily Time")  # Adding label to the x-axis
        ax.set_ylabel("Message Count")  # Adding label to the y-axis
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color="purple")
            ax.set_xlabel("Days")  # Adding label to the x-axis
            ax.set_ylabel("Message Count")  # Adding label to the y-axis
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            ax.set_xlabel("Months")  # Adding label to the x-axis
            ax.set_ylabel("Message Count")  # Adding label to the y-axis
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        ax.set_xlabel("Time slot of 1 hour")  # Adding label to the x-axis
        ax.set_ylabel("Days name")  # Adding label to the y-axis

        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation="vertical")
                ax.set_xlabel("Person name")  # Adding label to the x-axis
                ax.set_ylabel("Message Count")  # Adding label to the y-axis
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation="vertical")

        st.title("Most commmon words")
        st.pyplot(fig)

        # sentiment added

        # Sentiment Analysis Results
        st.title("Sentiment Analysis")

        if selected_user == "Overall":
            st.write("Sentiment distribution across all users:")
            sentiment_counts = df["sentiment"].value_counts()
            st.bar_chart(sentiment_counts)
        else:
            st.write(f"Sentiment distribution for user: {selected_user}")
            df = df[df["user"] == selected_user]
            sentiment_counts = df["sentiment"].value_counts()
            st.bar_chart(sentiment_counts)

        # Sentiment Distribution by User
        if selected_user == "Overall":
            st.write("Sentiment distribution for each user:")
            sentiment_by_user = (
                df.groupby("user")["sentiment"].value_counts().unstack().fillna(0)
            )
            st.write(sentiment_by_user)

        # # emoji analysis
        # emoji_df = helper.emoji_helper(selected_user, df)
        # st.title("Emoji Analysis")

        # col1, col2 = st.columns(2)

        # with col1:
        #     st.dataframe(emoji_df)
        # with col2:
        #     fig, ax = plt.subplots()
        #     ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        #     st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        emoji_df = emoji_df[
            emoji_df[0] != "group_notification"
        ]  # Remove 'group_notification'
        st.title("Emoji Analysis")
        st.write("Emoji analysis by count")

        # Display emoji list
        # with st.expander("Emoji List"):
        st.dataframe(emoji_df)

        # Aggregate emojis by category or frequency
        aggregated_data = (
            emoji_df.groupby(0)[1].sum().nlargest(5)
        )  # Example: Top 10 most frequent emojis

        # Plot aggregated data using Plotly
        fig = go.Figure(
            data=[go.Bar(x=aggregated_data.index, y=aggregated_data.values)]
        )
        fig.update_layout(xaxis_title="Emoji", yaxis_title="Frequency")
        st.write("Emoji analysis by chart")
        st.plotly_chart(fig)

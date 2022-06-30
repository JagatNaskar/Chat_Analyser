import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
#seaborn heatmap is used to create heatmap
import seaborn as sns


st.sidebar.title("Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Select a file")  # To upload and read file
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # to convert bytecode to string
    # st.text(data)   # to show the data in the screen
    df = preprocessor.preprocess(data)  # calling the "preprocessor function" to change the data format
    st.dataframe(df)  # display data frame

    # data analysis starts from here

    # create dropdown and fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall Analysis")

    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)  # selected by user
    if st.sidebar.button("Analize wrt"):  # button to start analysis
        num_messages, words, num_of_media, num_of_links = helper.fetch_stats(selected_user, df)  # importing from helper file

        st.title("Statistics From Your Chat")
        col1, col2, col3, col4 = st.columns(4)  # creating 4 columns

        with col1:  # visualizing col1, col2, col3, col4
            st.header("Total Messages ")
            st.title(num_messages)

        with col2:
            st.header("Total Words ")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_of_media)
        with col4:
            st.header("Link Shared")
            st.title(num_of_links)

    #timeline
        #monthly timeline
        st.title("Monthly Analysis")
        timeline = helper.monthly_Timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Analysis")
        daily_timeline = helper.dailyTimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Date_Only'], daily_timeline['message'], color='black')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Busiest Day")
            busy_Day = helper.week_activity_Map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_Day.index, busy_Day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Busiest Month")
            busy_Month = helper.month_activity_Map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_Month.index, busy_Month.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #creating "HEATMAP"
        user_heatmap = helper.heatmap(selected_user, df)
        st.title("Heat Map - weekly activity")
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #finding the busiest user
        if selected_user == 'Overall Analysis':
            st.title('Most Busy Users')
            x, new_df = helper.MostBusyUser(df)
            fig, axis = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                axis.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.title('Percentage')
                st.dataframe(new_df)

                #wordCloud
        st.title("Word Cloud....")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)    # to show the image
        st.pyplot(fig)

         # most common words
        #st.title("Most Common words")
        st.title("Most Common words")
        col1, col2 = st.columns(2)
        most_common_df = helper.most_common_words(selected_user, df)
        with col1:
            st.subheader("20 Most Common words in table")
            st.dataframe(most_common_df)  # print the most common words in the form of table
        with col2:
            st.subheader("20 Most Common words in GRAPH")
            fig, ax = plt.subplots()  # for ploting the table in the form of BAR graph
            ax.barh(most_common_df[0], most_common_df[1])   #barh for horizontal bar chart
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


    #emoji analysis
        st.title("Most common emojis")
        emojji_df = helper.emoji_function(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emojji_df)
        with col2:
            fig, ax = plt.subplots()
            #head() top 5 emoji //    autopct="%0.2f for showing % inside pie chart
            ax.pie(emojji_df[1].head(), labels = emojji_df[0].head(),autopct="%0.2f")  #x axis consists of emojis, y = number of emoji
            st.pyplot(fig)



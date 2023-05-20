import streamlit as st
import Preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Upload a File")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=Preprocessor.preprocess(data)
    # st.title('Data Frame Sample')
    # st.dataframe(df.head(20))

    # Fetching unique users:
    user_list=df['User'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Select a User for Analysis",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,num_words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline for the Data:
        st.title('Monthly Timeline')
        m_timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(m_timeline['Time'],m_timeline['Message'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline for the Data:
        st.title('Daily Timeline')
        d_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(d_timeline['Only Date'], d_timeline['Message'], color='yellow')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Weekly/Monthly Activity:
        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day=helper.week_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_month=helper.month_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Building a HeatMap:
        st.title('Weekly Activity Heat Map')
        h_map=helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(h_map)
        st.pyplot(fig)

        # Getting Busiest Users in the Group:
        if selected_user=='Overall':
            st.title('Most Busiest Users')
            x,new_df=helper.fetch_busiest_user(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            # Displaying a Bar Graph for most busiest users:
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            # Displaying a Data Frame for most busiest users:
            with col2:
                st.dataframe(new_df)

        # Display Most Common Words using Bar Graph:
        most_common_df=helper.most_common_words(selected_user,df)
        st.title('Most Common Words')
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)

        # Emoji Analysis:
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            l={0,1,2,3,4}
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=l,autopct="%0.2f")
            st.pyplot(fig)
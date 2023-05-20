from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji




# For Displaying Chat Stats:
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['User'] == selected_user]

    # No. of Messages:
    num_messages = df.shape[0]

    # No. of words:
    words = []
    for messages in df['Message']:
        words.extend(messages.split())

    # No. of Media Messages:
    num_media_messages=df[df['Message']=='<Media omitted>\n'].shape[0]

    # No. of Links:
    extract = URLExtract()
    links=[]
    for messages in df['Message']:
        links.extend(extract.find_urls(messages))

    return num_messages,len(words),num_media_messages,len(links)

def fetch_busiest_user(df):
    x=df['User'].value_counts().head(5)
    new_df=round( (df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'Percentage'})
    return x,new_df

def most_common_words(selected_user,df):
    f=open('venv/Stop_Words','r')
    stop_words=f.read()
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp=df[df['User']!='group_notifications']
    temp=temp[temp['Message']!='<Media omitted>\n']
    words=[]
    for messages in temp['Message']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for messages in df['Message']:
        emojis.extend([c for c in messages if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    timeline=df.groupby(['Year','Month Number','Month']).count()['Message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i]+"-"+str(timeline['Year'][i]))
    timeline['Time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    timeline=df.groupby('Only Date').count()['Message'].reset_index()
    return  timeline

def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Day Name'].value_counts()

def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    hmap=df.pivot_table(index='Day Name',columns='Period',values='Message',aggfunc='count').fillna(0)
    return hmap
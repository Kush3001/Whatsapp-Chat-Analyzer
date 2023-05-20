import re
import pandas as pd
def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages=re.split(pattern,data)[1:]
    dates =re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date':'Date'},inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notifications')
            messages.append(entry[0])

    df['User']=users
    df['Message']=messages
    df.drop(columns=['user_message'],inplace=True)
    # Finding out Year:
    df['Year']=df['Date'].dt.year
    # Finding Month Number:
    df['Month Number']=df['Date'].dt.month
    # Finding out Month Names:
    df['Month']=df['Date'].dt.month_name()
    # Finding out only Date:
    df['Only Date']=df['Date'].dt.date
    # Finding Day:
    df['Day']=df['Date'].dt.day
    # Extracting Day Name:
    df['Day Name']=df['Date'].dt.day_name()
    # Extracting Hours and Minutes:
    df['Hour']=df['Date'].dt.hour
    df['Minute']=df['Date'].dt.minute
    # Extracting Period:
    period=[]
    for hour in df[['Day Name','Hour']]['Hour']:
        if hour==23:
            period.append(str(hour)+'-'+str('00'))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['Period']=period
    return df
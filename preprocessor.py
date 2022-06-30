import re
import datetime
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # separate message and user name
    users = []
    messages = []
    for message in df['user_message']:  # loop in user_message
        entry = re.split('([\w\W]+?):\s', message)  # divided in 2 parts(after : and before :)
        if (entry[1:]):  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')  # if group notificaiton, then add to users
            messages.append(entry[0])  # if messages add to messages

    df['user'] = users  # new column user
    df['message'] = messages  # new column message
    df.drop(columns=['user_message'], inplace=True)

    # breaking date to get year
    df['year'] = df['date'].dt.year
    # breaking date to get months
    df['month'] = df['date'].dt.month_name()
    # extracting month from date and storing in month_num varible
    df['month_num'] = df['date'].dt.month
    # breaking date to get day
    df['day'] = df['date'].dt.day

    df['day_name'] = df['date'].dt.day_name()   #gives day name
    # breaking date to get minutes
    df['minute'] = df['date'].dt.minute
    # breaking date to get hour
    df['hour'] = df['date'].dt.hour

    #HEATMAP
    # creating new column 'period(hour-(hour+1))' from 'hour'
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(hour) + "-" + str(hour + 1))  # hour 9 will look line 9-10 in period column
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period  # storing all the period value in period[]

    return df

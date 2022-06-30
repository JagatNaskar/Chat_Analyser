from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter #to count the frequency of each word
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]         # for spesific user 'total messages in the group'
    words = []
    for message in df['message']:      # for spesific user 'total words in the group'
        words.extend(message.split())

    #return num_messages, len(words)

    # number media used
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]   #since all the media is omited, '<Media omitted>/n' is present in message

    #number of links used

    links = []
    for message in df['message']:
        links.extend(URLExtract().find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


    #Most busy user function
def MostBusyUser(df):
    x = df['user'].value_counts().head(5)  #top five texter

    #no. of message per user in percentage
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'Percentage'})  # df.shape[0] is total number of message
    return x,df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user

    #for filtering few words out
    f = open('stopwords.txt', 'r')  # importing stopwords file
    stop_words = f.read();  # readinfg all the words
    temp = df[df['user'] != 'group_notification']  # removing group notification
    temp = temp[temp['message'] != 'omitted']
    temp = temp[temp['message'] != '<Media omitted>\n']  # removing media ommited
    temp = temp[temp['message'] != 'This message was deleted\n']  # removing deleted message
    temp = temp[temp['message'] != '.\n']

    #function to remove the stop words
    def remove_Stopwords(message):
        arr=[]
        for word in message.lower().split():
            if word not in stop_words:
                arr.append(word)
        return " ".join(arr)    #again forming sentence and returning

    wc = WordCloud(width=400, height=400, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_Stopwords)    #calling remove_stop word function
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))   #generate function create wordCloud, predefined
    return df_wc


def most_common_words(selected_user, df):
    f = open('stopwords.txt', 'r')  # importing stopwords file
    stop_words = f.read();  # readinfg all the words

    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user


    # removing group_notification
    # removing .
    # removing deleted message

    temp = df[df['user'] != 'group_notification']  # removing group notification
    temp = temp[temp['message'] != '<Media omitted>\n']  # removing media ommited
    temp = temp[temp['message'] != 'This message was deleted\n']  # removing deleted message
    temp = temp[temp['message'] != '.\n']

    # Find the frequency of each cleaned word
    words = []
    for message in temp['message']:  # temp dataframe is used, cleaned dataset
        for word in message.lower().split():  # converting all messages to lowercase
            if word not in stop_words:  # without split(), only character would have stored # removing stop words
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))  #20 highest frequency words
    return most_common_df


#emoji analysis
def emoji_function(selected_user, df):
    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user

    emojii=[]
    for message in df['message']:
        emojii.extend([c for c in message if c in emoji.UNICODE_EMOJI_ENGLISH])

    emoji_df = pd.DataFrame(Counter(emojii).most_common(len(Counter(emojii))))
    return emoji_df

#timeline
#monthly timeline
def monthly_Timeline(selected_user, df):
    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time  # inserting time in timeline dataframe
    return timeline

#daily timeline
def dailyTimeline(selected_user, df):
    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user
    df['Date_Only'] = df['date'].dt.date  # creating only date in df
    daily_timeline = df.groupby('Date_Only').count()['message'].reset_index()  # reset_index() to set title
    return daily_timeline

#week activity map
def week_activity_Map(selected_user, df):
    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user
    return df['day_name'].value_counts()  # .value_counts() gives the most active day

#month activity map
def month_activity_Map(selected_user, df):
    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user
    return df['month'].value_counts()  # .value_counts() gives the most active month


def heatmap(selected_user, df):
    if selected_user != 'Overall Analysis':   #df will remain same if selected_user == overall_analysis
        df = df[df['user'] == selected_user]    #for particular user, df will change to selected user

    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heatmap
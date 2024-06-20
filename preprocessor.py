import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s\w+\s-\s'

    messages = re.split(pattern , data)[1:]
    dates = re.findall(pattern , data)


    date = []
    time = []

    for i in dates:
        date.append(i.split(", ")[0])
        time.append(i.split(", ")[1])


    df = pd.DataFrame({
    
    'user_message':messages, 
    'date': date , 
    'time':time
    
    })


    user_name = []
    user_msg=[]





 
    for i in messages:
        x=re.split( '([\w\W]+?):\s',i)


        if x[1:]:
            user_name.append(x[1])
            user_msg.append(x[2])

        else:
            user_name.append('Group Notification')
            user_msg.append(x[0])


    df['user']=user_name
    df['message'] = user_msg

    df.drop(columns=['user_message'],inplace=True)


    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()


    return df
from wordcloud  import WordCloud

def show_stats(selected_user,df):
    if selected_user != "overall":
       df =  df[df['user']== selected_user]

    num_msg = df.shape[0]

    words=[]

    for msg in df['message']:
        words.extend(msg.split())

    num_words = len(words)


    num_media = df[df['message']=='<Media omitted>\n'].shape[0]

    return num_msg,num_words,num_media,df




def word_cloud_generate(selected_user,df):
    if selected_user != "overall":
       df =  df[df['user']== selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    # df_wc = wc.generate(df['message'].str.cat(seo=" "))
    df_wc = wc.generate(" ".join(df['message'].tolist()))

    return df_wc
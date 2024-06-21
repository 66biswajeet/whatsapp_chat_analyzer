import streamlit as st
import streamlit_shadcn_ui as ui
import preprocessor
import helper
import matplotlib.pyplot as plt
import pandas as pd
import emoji

st.sidebar.title("whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.title("All Messages Table")
    st.dataframe(df)
    

    #fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0,'overall')

    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    num_msg , num_words , num_media, df = helper.show_stats(selected_user,df)

    if st.sidebar.button("Show Analysis"):
        

        st.title("Summary")
        col1,col2,col3 = st.columns(3,gap='small')




        with col1:
            
            

            # font_size = "20px"

            # header_text = f"Total Messages by: {selected_user}"

            # st.markdown(f"<h1 style='font-size:{font_size}'> {header_text} </h1>", unsafe_allow_html=True)

            # st.title(num_msg)

            ui.metric_card(title="Total Messages ", content=num_msg, description="Total messages by the user", key="card1")


        with col2:
            
            ui.metric_card(title="Total Words ", content=num_words, description="Total words on the messages", key="card2")

           

        with col3:
            
            
            ui.metric_card(title="Total Media ", content=num_media, description="Total media shared", key="card3")
           

        if selected_user != "overall":
            st.title(f"Messages by {selected_user}")
            with st.container(border=True ):
                st.write(df)

            
            


        if selected_user == "overall":
            st.title("Most Active Users") 

            col1 ,col2 = st.columns(2,gap="large")
               

            with col1:
        
                    
                            top5 = df['user'].value_counts().head(10)

                            fig , ax = plt.subplots()

                            ax.bar(top5.index,top5.values , color='black')
                            plt.xticks(rotation='vertical')
                            plt.xlabel('Names Of person',color='red')
                            plt.ylabel('No of Messages',color='blue')
                            st.pyplot(fig)
                            plt.show()   
            
            with col2:

                
                
                percent_df =  round((df['user'].value_counts()/df.shape[0])*100,2)

                ui.metric_card(title="Most Contribution :", content=f" {percent_df.index[0]}", description=f"Highest messages of {percent_df[0]} %", key="card6")
                st.dataframe(percent_df,height=170)



                
        

        st.title(" Common Words" ) 

        col1 ,col2 = st.columns(2,gap="large")

        with col1:
                 
                df_wc = helper.word_cloud_generate(selected_user,df)
                fig,ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

        # busy months

        st.title("Busy Months" )
        col1 ,col2 = st.columns(2,gap="large")

        with col1:
            
            df['new_month'] = df['month']
            df['new_month'] = pd.to_datetime(df['month'], format='%B').dt.month 
            new_df =(df['new_month'].value_counts().sort_index())
            # st.dataframe(new_df)

            fig , ax = plt.subplots()

            ax.bar(new_df.index,new_df.values , color='black')

            
            # plt.xticks(rotation='vertical')
            plt.xlabel('Months',color='red')
            plt.ylabel('No of Messages',color='blue')
            st.pyplot(fig)
            plt.show()           

            new_df2 =(df['month'].value_counts())
            ui.metric_card(title="Longest Conversation Month is  ", content = f"{new_df2.index[0]}", description=f"{new_df2.values[0]} messages has transfered", key="card4")



        with col2:
             
             new_df2 =(df['month'].value_counts())
             st.dataframe(new_df2,height=400)
             
                 
      
        
        # for longest conversation days 

        st.title("Logest Conversation Days")
        col1 , col2  =st.columns(2)


       
        

       


        with col2:

             


            long_days = df['date'].value_counts().sort_values(ascending=False)
            st.dataframe(long_days , height=500)




        with col1:

            
            date_only = long_days.index[0].strftime("%d-%m-%y")
             
            ui.metric_card(title="Longest Conversation Day is  ", content = f"{date_only}", description=f"{long_days.values[0]} messages has transfered", key="card5")

            

            fig , ax = plt.subplots()

            ax.bar(long_days.index,long_days.values , color='black')

            plt.xticks(rotation='vertical')
            plt.xlabel('Months',color='red')
            plt.ylabel('No of Messages',color='blue')
            st.line_chart(long_days)
            plt.show() 




        emojis=[]
        for message in df['message']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

        emoji_df = pd.DataFrame(emojis).value_counts()
        emoji_df_pie = pd.DataFrame(emojis).value_counts().head(10)


        st.title("Common Emojis Used")
        col1 , col2 = st.columns(2)

        with col2:

            st.dataframe(emoji_df, height=300)

        # fig , ax = plt.subplots()

        # ax.pie(emoji_df.index,emoji_df.values)

        # plt.xticks(rotation='vertical')
        # plt.xlabel('Emojis',color='red')
        # plt.ylabel('using frequecy',color='blue')
        # st.pyplot(fig)
        # plt.show() 
        
        with col1:
             

            emoji_names = emoji_df_pie.index.tolist()
            emoji_counts = emoji_df_pie.values.tolist()

            fig, ax = plt.subplots()
            ax.pie(emoji_counts, labels=emoji_names , autopct = "%0.2f")

            plt.xticks(rotation='vertical')
            
            st.pyplot(fig)
            plt.show()
        
      

footer_html = """
<div style="text-align: center; padding: 10px; background-color: "black";">
  <p>© 2024 Biswajeet Jena - Developed with ❤️ using Streamlit</p>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
st.markdown("--- \n © 2024 Biswajeet Jena | @jeetcode")


                
            

       
       
          
            
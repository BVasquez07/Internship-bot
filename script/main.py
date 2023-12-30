import streamlit as st

def save_webhook(url):
    with open('webhooks.txt', 'a+') as f: 
        f.write(url + ",")  

st.title('Discord Webhook Saver')
st.write('Please enter your Discord webhook URL and submit to save it.')

webhook_url = st.text_input('Webhook URL')

if st.button('Submit'):
    if webhook_url:  
        save_webhook(webhook_url)
        st.success('Webhook URL saved successfully!')
    else:
        st.error('Please enter a valid webhook URL.')

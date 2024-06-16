import streamlit as st
import google.generativeai as gen_ai

# Configure Streamlit page settings
st.set_page_config(
    page_title="R&D Auto Repair Chat",
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = st.secrets["API_KEY"]

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
info = '''
At R&D Auto Repair, we use cutting-edge technology and industry best practices to provide high-quality services to our customers.
Established in 2014, R&D Auto Repair has been a family-owned and operated business for over 5 years. 
We offer complete auto repairs on most car models. We offer repair services that keep your vehicle running as it should, no matter what condition you bring it in.
Rey, R&D's repair expert, has over 10 years of experience working with various cars. He's extremely knowledgeable and is quick with his work.
The best part is that his prices are incredibly fair, and he's willing to work with your budget!
4.9 Rating on Yelp for reliable and efficient repairs.

Services:
Auto Diagnosis or Inspection
Auto Maintenance
Auto Mirror Replacement
Auto Noise Diagnosis
Auto Repairs
Check Engine Light
Oil Changes
Tire Pressure Monitoring System Diagnosis
Auto Electronics Installation
Auto Window Replacement
Window Tinting
Auto General Diagnosis
Auto Mirror Repair
Auto No-Start Diagnosis
Auto Pre-Purchase Inspection
Auto Vibration Diagnosis
Engine Oil Light Diagnosis
Routine Automotive Maintenance
Transmission Leak Inspection
Auto Window Repair
Auto Windshield Replacement

Hours: 
Saturday	8:30 AM - 5:30 PM
Sunday	Closed
Monday	9 AM - 7 PM
Tuesday	9 AM - 7 PM
Wednesday	9 AM - 7 PM
Thursday	9 AM - 7 PM
Friday  9 AM - 7 PM

Adress: 1567 Laurelwood Rd, Santa Clara, CA
Phone: 408-728-5517
'''

initial_instruction = f'''
You are a chatbot named Rey.AI that handles questions for a business called R&D Auto Repair.
Always use a friendly tone and answer questions as accurately as possible.
Do not make up fake information or answer unrelated questions. 
If you do not know an answer to a question, tell the user you don't know and ask them to contact this phone number: (408-728-5517)
Here is information regarding the business: {info}
Now respond to the user input: '''


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("R&D Auto Repair Chat Bot")
st.subheader('This is Rey.AI, a chatbot that can answer questions about R&D Auto Repair. How can I help?')

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        markdown_filtered = message.parts[0].text
        if initial_instruction in markdown_filtered:
            markdown_filtered = markdown_filtered[len(initial_instruction)::]
        st.markdown(markdown_filtered)

# Input field for user's message
user_prompt = st.chat_input("Ask about R&D Auto Repair!")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(initial_instruction+user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

# streamlit run streambot2.py

import streamlit as st
import pandas as pd
import os

# File to store the questionnaire responses
RESPONSES_FILE = 'responses.csv'

# Function to load or create a CSV file for responses
def load_responses():
    if os.path.exists(RESPONSES_FILE):
        return pd.read_csv(RESPONSES_FILE)
    else:
        return pd.DataFrame(columns=['user_id', 'category', 'video', 'safety', 'movement', 'comfort', 'completed'])

# Function to save responses to CSV
def save_responses(df):
    df.to_csv(RESPONSES_FILE, index=False)

# Initialize session state
if 'responses_df' not in st.session_state:
    st.session_state.responses_df = load_responses()
if 'is_csv_created' not in st.session_state:
    st.session_state.is_csv_created = True

# Define categories and YouTube video URLs
categories = {
    'Category 1': [
        'https://youtube.com/watch?v=4Dp3pLaz97s',  # Replace with your actual video URLs
        'https://www.youtube.com/watch?v=FNYBb24sHCc',
        'https://youtube.com/watch?v=UYUgk-ooBnA',
        'https://youtube.com/watch?v=w5obWdSBipA'
    ],
    'Category 2': [
        'https://youtube.com/watch?v=mYEjeRn8Rak',
        'https://youtube.com/watch?v=15U5i23WNL0',
        'https://youtube.com/watch?v=j_H5po52nhk',
        'https://youtube.com/watch?v=fGwT5oFEdPE'
    ],
    'Category 3': [
        'https://youtube.com/watch?v=Ej0dMMtWkqQ',
        'https://youtube.com/watch?v=7yjyLhShPME',
        'https://youtube.com/watch?v=fIzRZabPORk',
        'https://youtube.com/watch?v=Y20Cp9ZS10s'
    ],
    'Category 4': [
        'https://youtube.com/watch?v=p1RGj_hBaOM',
        'https://youtube.com/watch?v=sbsvW54xaKo',
        'https://youtube.com/watch?v=mihRVObGGls',
        'https://youtube.com/watch?v=v2b3EyqONdU'
    ]
}

# Streamlit App
st.title("Video App with Questionnaire")

# User ID input
user_id = st.text_input("Enter your User Mail:")

if user_id:
    st.write(f"Welcome, User: {user_id}")

    # Show available categories
    selected_category = st.selectbox("Choose a category:", list(categories.keys()))

    if selected_category:
        # Show available videos in the selected category
        video_urls = categories[selected_category]
        video_titles = [f"Video {i+1}" for i in range(len(video_urls))]
        selected_video_index = st.selectbox("Choose a video:", video_titles)

        # Determine the video URL and number
        video_number = int(selected_video_index.split()[1]) - 1
        selected_video_url = video_urls[video_number]

        # Show the YouTube video
        if selected_video_url:
            st.video(selected_video_url)

            # Questionnaire after video
            st.write("Please rate the following aspects of the robot:")

            # Question 1: Robot's safety regarding objects/people
            safety = st.select_slider(
                "Rate robot's safety regarding walls/objects/people:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "Not Safe" if x == 1 else ("Safe" if x == 5 else "")
            )

            # Question 2: Robot's movement
            movement = st.select_slider(
                "Rate how natural/expected the robot navigation is:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "Not Expected" if x == 1 else ("Expected" if x == 5 else "")
            )

            # Question 3: Comfort level with the robot
            comfort = st.select_slider(
                "Imagine you are walking alongside the robot. Rate your comfort level with the robot:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "Not Comfortable" if x == 1 else ("Comfortable" if x == 5 else "")
            )

            if st.button("Submit"):
                # Check if response already exists
                if st.session_state.responses_df[(st.session_state.responses_df['user_id'] == user_id) &
                                                (st.session_state.responses_df['category'] == selected_category) &
                                                (st.session_state.responses_df['video'] == video_number)].empty:
                    # Save the response
                    new_entry = pd.DataFrame([[user_id, selected_category, video_number, safety, movement, comfort, True]],
                                             columns=['user_id', 'category', 'video', 'safety', 'movement', 'comfort', 'completed'])
                    st.session_state.responses_df = pd.concat([st.session_state.responses_df, new_entry], ignore_index=True)
                    save_responses(st.session_state.responses_df)
                    st.session_state.is_csv_created = True
                    st.success("Your response has been recorded!")
                else:
                    st.warning("You have already submitted a response for this video.")

    # Show completed videos
    if selected_category:
        completed_videos = st.session_state.responses_df[(st.session_state.responses_df['user_id'] == user_id) &
                                                        (st.session_state.responses_df['category'] == selected_category) &
                                                        (st.session_state.responses_df['completed'] == True)]['video'].tolist()

        st.write([f"Video {i+1}" for i in completed_videos])

        # Check if all videos are completed in the selected category
        if len(completed_videos) == len(categories[selected_category]):
            st.markdown("<h3 style='color: black;'>You have completed all videos in this category! Pass to the next one.</h3>", unsafe_allow_html=True)

    # Provide download link for user's responses at any time
    if user_id:
        total_completed_videos = st.session_state.responses_df[(st.session_state.responses_df['user_id'] == user_id) &
                                                        (st.session_state.responses_df['completed'] == True)]['video'].tolist()
        completed_categories = []
        for category, videos in categories.items():
            completed_videos = st.session_state.responses_df[(st.session_state.responses_df['user_id'] == user_id) &
                                                            (st.session_state.responses_df['category'] == category) &
                                                            (st.session_state.responses_df['completed'] == True)]['video'].tolist()
            if len(completed_videos) == len(videos):
                completed_categories.append(category)
        
        st.write("You have completed the following categories:")
        st.write(completed_categories)
        
        if(len(total_completed_videos)) == 16:
            st.markdown("<h3 style='color: blue;'>You have completed all the videos! Download responses and send them to: eliasgol@post.bgu.ac.il.</h3>", unsafe_allow_html=True)
            
        user_responses = st.session_state.responses_df[st.session_state.responses_df['user_id'] == user_id]
        if not user_responses.empty:
            csv = user_responses.to_csv(index=False)
            st.download_button(
                label="Download your responses",
                data=csv,
                file_name=f"user_{user_id}_responses.csv",
                mime='text/csv'
            )

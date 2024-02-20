#---------------------------------------------------
#          LIBRARY AND MODULE IMPORTS
#---------------------------------------------------
import streamlit as st
import cv2
import tempfile
import time

import instructions
import regarding_spotify_interact
import about_us

#---------------------------------------------------
#          PAGE CONFIGURATIONS ETC.
#---------------------------------------------------
# Page title and icon
st.set_page_config(page_title="<Music Selector Name>", page_icon=":musical_note:", layout="wide")

#---------------------------------------------------
#             FUNCTIONS
#---------------------------------------------------

moods = {
    "Happy": ["song 1", "song 2", "song 3", "song 4", "song 5"],
    "Sad": ["song 1", "song 2", "song 3", "song 4", "song 5"],
    "Excited": ["song 1", "song 2", "song 3", "song 4", "song 5"],
    "Relaxed": ["song 1", "song 2", "song 3", "song 4", "song 5"]
}
#a dummy dictionary for text-based input (back-up)


def dummy_text_function():
    #This dummy function takes the text as input and returns the playlist
    st.subheader(f"Here's a {mood.lower()} playlist for you!")
    for playlist in moods[mood]:
        return st.write(playlist)



def dummy_img_and_vid_function():
    #This dummy function takes the either image or video files as input and returns the playlist
    st.subheader(f"Here's a <identified emotion> playlist for you!")
    st.write("imagine this is a list of songs")


def process_file(file):
    #This function takes one required argument which is either an image or a video file from the file_uploader forms
    #and process the corresponding file type after user input.
    if file.type.startswith('image'):
        # process image
        st.image(file)
        return file
    elif file.type.startswith('video'):
        # process video
        st.video(file)
        return file
    else:
        st.write("Unsupported file type")
        return None
        #default if the file submitted is not among the required file types


def save_video(frames, fps):
    # Function to save the recorded video
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for frame in frames:
        out.write(frame)

    out.release()


def start_stop_recording():
    # Function to start/stop recording
    global recording, frames

    if record:
        recording = not recording

        if recording:
            st.write('Recording...')
        else:
            st.write('Stopped')
            save_video(frames, 20)  # Save the recorded video with 20 fps
            frames = []  # Clear the frames list

#------------------------------------
#      HEADER AND DESCRIPTION
#------------------------------------

st.title("<Music Selector Project>") #official name still hasn't been decided
st.write(" ")

col3, col4 = st.columns([1.5,3])
col3.title(" ")
with col3:
    st.subheader("Tune in your Emotions, Transform out your Playlist!")
    st.subheader(" ")
    col3_1, col3_2, col3_3 = col3.columns([0.5,1,0.5])
    col3_2.image("interface/images/inst_flow1_hd.png")


col3.title(" ")
col3.caption("Application Accuracy: <80.56%>")
col4.image("interface/images/Playlist-amico (1).png")
#image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>
st.subheader(" ")

#----------------------------------
#       SIDEBAR
#----------------------------------

with st.sidebar:
    st.title("About <Music Selector>") #change to official name
    st.image("interface/images/Music-cuate.png")
    #attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

    st.subheader("For questions about application usage:")
    page = st.selectbox("choose a query", ["How to generate your playlist?",
                                                  "How to add playlist to your Spotify library?",
                                                 ])
    #drop down option for Q&As

    if page == "How to generate your playlist?":
        instructions.instructions_page()
    if page == "How to add playlist to your Spotify library?":
        regarding_spotify_interact.spotify_page()
    #link selectbox to indiv .py file (==individual page)

    st.subheader("Know more about the creators:")
    about_us_page = st.button("About Us")
    #link page button to the individual .py file (==individual page)
    if about_us_page:
        about_us.about_us()


#--------------------------------------------
#configure page layout
col1, col2,  col3 = st.columns([3.5, 0.5, 4])

#-------------------------------------------

with col1:
    st.write(" ")
    st.subheader("Take a selfie or a video capture!")
    st.write("Take a picture or a short video recording of your face showing how your current emotion.")

    container = st.container(border=True)
    col_form = st.form("collective_input")

    row1_col1, row1_col2 = st.columns(2)
    row_2 = st.columns(1)

    with row1_col1:
    #--------------Camera Image---------------#
        image_captured = st.camera_input("click on \"Take Photo\" ")
        # camera widget; will return a jpeg file once image is taken.
        st.session_state["image_captured"] = None
        # Initialized camera state variable

    with row1_col2:
    #------------Camera Recoding-------------#
        run = st.checkbox('Run Webcam')
        FRAME_WINDOW = st.image([])
        webcam = cv2.VideoCapture(0)

        #Button to start/stop recording
        record = st.button('Start Recording')
        # Variables to manage recording
        recording = False
        frames = []

        camera_rec = st.cv2.VideoCapture(0)
        #main camera for recording

        while run:
            _, frame = camera_rec.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)

            if recording:
                frames.append(frame)

            start_stop_recording()

    with row1_col2:
        uploaded_file = st.file_uploader("or upload an image or a video", type=["image/jpeg", "image/png", "video/mp4"])
        st.session_state["uploaded_file"] = None
        if uploaded_file is not None:
            input_file = process_file(uploaded_file)

    submit_button = col_form.form_submit_button("Extract Emotion from File", args=[image_captured])
    if submit_button:
        if input_file:
            st.session_state["uploaded_file"] = input_file
            if input_file.type.startswith('image'):
                st.write("Reading emotion from image file...")
            elif input_file.type.startswith('video'):
                st.write("Reading emotion from video file...")

with col1:
    # text input form
    st.subheader("Select a mood!")
    with st.form("text_input"):
        mood = st.selectbox("Choose an emotion:", list(moods.keys()))
        st.session_state["mood"] = None
        submit_button= st.form_submit_button("Submit Emotion")
        if submit_button:
            st.write("Emotion selected")
            st.session_state["mood"] = mood

# Display generated playlist based on input
with col3:
    st.write(" ")
    if st.session_state.get("uploaded_image"):
        uploaded_image = st.session_state["uploaded_image"]
        st.write("Image input detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_img_and_vid_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    elif st.session_state.get("image_captured"):
        uploaded_image = st.session_state["image_captured"]
        st.write("Camera Image detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_img_and_vid_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    elif st.session_state.get("uploaded_video"):
        uploaded_video = st.session_state["uploaded_video"]
        st.write("Video input detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_img_and_vid_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    elif st.session_state.get("mood"):
        mood = st.session_state["mood"]
        st.write(f"Selected emotion: {mood}")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_text_function()

        #embeded link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    else:
        st.subheader(" ")
        st.caption("                 Please Choose your preferred input type to generate the playlist.")

# #video stuff
# st.title("Play Uploaded File")

# uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
# temporary_location = False

# if uploaded_file is not None:
#     temporary_location = write_to_disk(uploaded_file)

# if temporary_location:
#     video_stream = cv2.VideoCapture(temporary_location)
#     # Check if camera opened successfully
#     if (video_stream.isOpened() == False):
#         print("Error opening video  file")
#     else:
#         # Read until video is completed
#         while (video_stream.isOpened()):
#             # Capture frame-by-frame
#             ret, image = video_stream.read()
#             if ret:
#                 # Display the resulting frame
#                 st.image(image, channels="BGR", use_column_width=True)
#             else:
#                 break
#         video_stream.release()
#         cv2.destroyAllWindows()

# def write_to_disk(uploaded_file):
#     """Writes an uploaded video file to disk and returns the file path."""
#     with tempfile.NamedTemporaryFile(delete=False) as out:
#         out.write(uploaded_file.read())
#         return out.name

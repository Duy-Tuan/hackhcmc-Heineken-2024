from cfg import st, get_yolo, os, Image
import google.generativeai as genai
from cfg import SAVE_FOLDER

st.set_page_config(
    page_title='Streamlit cheat sheet',
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
    body {
        opacity:1;
        background-color: #3A3B3C; /* Màu nền trắng */
    }
    
    .custom-container {
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.9); /* Màu nền cho container */
        border-radius: 10px; /* Bo tròn góc */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Đổ bóng */
    }
    .custom-title {
        text-align: center;
        font-size: 70px;
        font-weight: bold;
        margin-bottom: 10px;
        margin-top: -5px;
        color: #00E8E4; /* Màu chữ xanh dương */
        background-color: #3A3B3C;
        border: 0px solid white;
        border-radius: 10px;
        opacity: 1;
        height: 100px
        box-shadow: 0 0 100px rgba(0, 226, 234, 0.01); /* Đổ bóng */
        
    }
    .custom-subtitle {
        text-align: center;
        font-size: 20px;
        font-weight: normal;
        margin-top: -50px;
        margin-bottom: 20px;
        color: #E4E6EB; 
    }
    .custom-image {
        max-height: 200px;
        width: auto;
    }
    .button-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 100%;
    }
    .button-container button {
        height: 100%;
        width: 100%;
        font-size: 20px;
        padding: 10px;
    }
    .prev-button {
        grid-column: span 2;
    }
    .next-button {
        grid-column: span 2;
    }
    .stApp {
        margin-bottom: 20px; /* Khoảng cách từ top xuống */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="custom-title">Heineken Digital Empowerment Demo</h1>',
            unsafe_allow_html=True)

if 'current_image_index' not in st.session_state:
    st.session_state.current_image_index = 0

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

if "gemini" not in st.session_state:
    st.session_state.gemini = genai.GenerativeModel(
        model_name="gemini-1.5-flash")

if 'overlay' not in st.session_state:
    st.session_state.overlay = False

if 'image_files' not in st.session_state:
    st.session_state.image_files = []

if "response" not in st.session_state:
    st.session_state.response = None


def show_image_info(image_path):
    result = get_yolo.scan(image_path)

    # st.write(f"Results: {response.text}")
    return result


st.logo("logo.png")

col1, col2, col3, col4, col5 = st.columns([5, 5, 0.7, 0.5, 0.7])

with col3:
    if st.button('Previous'):
        if st.session_state.current_image_index == 0:
            st.session_state.current_image_index = len(
                st.session_state.image_files)
        else:
            st.session_state.current_image_index -= 1
        st.session_state.response = None
        st.session_state.overlay = False

with col4:
    if st.button('Next\t'):
        if st.session_state.current_image_index == len(st.session_state.image_files):
            st.session_state.current_image_index = 0
        else:
            st.session_state.current_image_index += 1
        st.session_state.response = None
        st.session_state.overlay = False

with col1:
    folder_path_2 = st.text_input("Fill Folder Path")
    placeholder = st.empty()
    if folder_path_2:
        if os.path.isdir(folder_path_2):
            st.session_state.image_files = [f for f in os.listdir(folder_path_2) if f.lower().endswith(
                ('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
            current_image_path = os.path.join(
                folder_path_2, st.session_state.image_files[st.session_state.current_image_index])
            image = Image.open(current_image_path)
            placeholder.image(image, caption=os.path.basename(
                current_image_path), use_column_width=True)
        else:

            print("")

with col5:
    if st.button('Show Overlay'):

        if not st.session_state.overlay:
            image = Image.open(
                f"{SAVE_FOLDER}temp.jpg")
            placeholder.image(image, caption=os.path.basename(
                current_image_path), use_column_width=True, width=300)
            st.session_state.overlay = True
        else:
            image = Image.open(current_image_path)
            placeholder.image(image, caption=os.path.basename(
                current_image_path), use_column_width=True, width=300)
            st.session_state.overlay = False

with col2:
    if (len(st.session_state.image_files) > 0):
        current_image_path = os.path.join(
            folder_path_2, st.session_state.image_files[st.session_state.current_image_index])
        result = show_image_info(current_image_path)

    if st.button("Analysis"):
        img = Image.open(current_image_path)
        prompt = f"""Based on the object detection result: {result}, please provide a detailed and accurate description of the image by listing the following information in bullet points. Ensure that all descriptions are based solely on the visible and identified elements in the image. Do not infer or assume details that are not explicitly detected.

Before listing the information, start the response with the sentence: 'Here is the result after analysis:'.
Beer Brands: Identify and list the names of all beer brands visible in the image. Only include brands that are clearly identifiable.
Brand Presence: Compare the visibility and presence of each beer brand (e.g., posters, beer cans, logos, etc.). Highlight which brand appears more prominently based on observable evidence and suggest why it might be considered more dominant. Do not make assumptions about market share or popularity outside of the visible context.
People and Attitudes: Count and describe the number of people or customers in the image. Note their actions, expressions, and attitudes based solely on visible cues. Avoid speculating on their thoughts or feelings.
Setting Details: Describe the setting of the image, including observable details about the weather, location, and time of day (if discernible). Only include details that can be explicitly seen or inferred from the context, and do not add assumptions or unrelated information.
        """
        with st.spinner("Analyzing..."):
            if st.session_state.response == None:
                st.session_state.response = st.session_state.gemini.generate_content(
                    [prompt, img])
                # st.write(st.session_state.response.text)

    if st.session_state.response:
        st.subheader("Statistics")

        for class_name, list_bounding_box in result.items():
            st.write(f"{class_name}: {len(list_bounding_box)}")
        st.divider()

        st.subheader("Competitor")

        for class_name, list_bounding_box in result.items():
            if "Logo" in class_name and "Heineken" not in class_name:
                name = class_name.replace("Logo", "")
                st.write(f"Competitor: {name}")

        st.divider()
        st.subheader("Description")
        st.write(st.session_state.response.text)

import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
import requests

def load_lottie_animation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Set up the page configuration
st.set_page_config(page_title="ChatGPT-like UI", layout="wide")


# Custom styles for enhanced layout
st.markdown("""
    <style>
    .sidebar-content {
        overflow-y: auto;
        max-height: 90vh;
    }

    .clickable-topic {
        cursor: pointer;
        color: blue;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Sidebar header
    st.selectbox("Select Model", ["Model A", "Model B", "Model C"], key="model_select")
    st.markdown("---")
    st.text_input("🔍 Search", placeholder="")
    st.markdown("---")
    st.header("History")
    st.markdown("---")

    # Simulate history items with share, rename, and delete options
    for i in range(10):  # Example history items
        with st.container():
            # Create clickable topic links
            if st.button(f"Topic {i + 1}", key=f"topic_{i}"):
                st.session_state["selected_topic"] = f"Topic {i + 1}"
            col1, col2, col3 = st.columns(3)
            col1.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🔗&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;", key=f"share_{i}")
            col2.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✏️&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key=f"rename_{i}")
            col3.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🗑️&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key=f"delete_{i}")
            st.markdown("---")


cat_animation_url = "https://lottie.host/fbaf127e-e6d0-41a0-8942-76e8216236d1/jtqrNoFPYx.json"
cat_animation = load_lottie_animation(cat_animation_url)

cols1, cols2, cols3 = st.columns([6,1,1])
with cols1:
    st.markdown("")
with cols2:
    if st.button("📝 New Post"):
        st.rerun()
with cols3:
    if st.button("🤖 Account"):
        st.success("Logged out successfully!")

if cat_animation:
    st_lottie(cat_animation, height=150, width=150, loop=True, quality="high")
    st.title("KUKI AI")
else:
    st.error("Failed to load animation. Please check the URL.")

# Set the background image
bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1650738962968-1cda273212eb?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
background-size: cover;
background-repeat: no-repeat;
background-attachment: local;
}
</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)

# Main content area
st.title("ChatGPT UI")
if "selected_topic" in st.session_state:
    st.subheader(f"Selected: {st.session_state['selected_topic']}")

# bg_animation_url = "https://lottie.host/20e599e0-af9e-49b0-9db1-3ab3c537a5f4/zYhXlRtFUi.json"
# bg_animation = load_lottie_animation(bg_animation_url)
# if bg_animation:
#     st_lottie(bg_animation, height=1500, width=1500, loop=True)
# else:
#     st.error("Failed to load animation. Please check the URL.")

import streamlit as st
from streamlit_lottie import st_lottie
from few_shot import FewShotPosts
from post_generator import generate_post
import requests
import pycountry

# Options for length
length_options = ["Short", "Medium", "Long"]

# Function to get all languages using pycountry
def get_all_languages():
    return sorted(
        [(language.name, language.alpha_2) for language in pycountry.languages if hasattr(language, "alpha_2")],
        key=lambda x: x[0]  # Sort by display name
    )

# Function to load Lottie animation from URL or file
def load_lottie_animation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Main app layout
def main():
    st.subheader("LinkedIn Post Generator")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()

    # Fetch all languages
    all_languages = get_all_languages()
    language_names = [lang[0] for lang in all_languages]
    language_codes = {lang[0]: lang[1] for lang in all_languages}

    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_names)

    # Generate Button
    if st.button("Generate"):
        language_code = language_codes[selected_language]
        post = generate_post(selected_length, language_code, selected_tag)
        st.write(post)

    # Load and display Lottie animation
    st.markdown("---")  # Separator line
    st.subheader("Enjoy this cute cat animation!")
    cat_animation_url = "https://lottie.host/c39564c8-927a-4efa-9542-24b438af4027/exUCllbPKa.json"  # Replace with your animation URL
    cat_animation = load_lottie_animation(cat_animation_url)

    if cat_animation:
        st_lottie(cat_animation, height=300, width=500, loop=True)
    else:
        st.error("Failed to load animation. Please check the URL.")


# Run the app
if __name__ == "__main__":
    main()

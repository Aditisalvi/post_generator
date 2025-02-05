import urllib
import streamlit as st
from streamlit_lottie import st_lottie
from utils.lottie_loader import load_lottie_animation
from utils.language_utils import get_all_languages
from utils.file_utils import download_file
from few_shot import FewShotPosts
from post_generator import generate_post
from utils.share_utils import share_via_email, share_on_linkedin, share_on_x, copy_to_clipboard
import requests
import pycountry
import base64
from io import BytesIO
from fpdf import FPDF
import webbrowser
import urllib.parse
from backend import MongoDBBackend  # Importing backend methods

# Options for length
length_options = ["Short", "Medium", "Long"]

# Function to generate a unique and relevant title
def generate_title(topic, length, language):
    length_descriptions = {
        "Short": "A concise",
        "Medium": "An insightful",
        "Long": "An in-depth"
    }
    return f"{length_descriptions[length]} post about {topic} in {language}"


# Function to create a PDF file with Unicode font
def create_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicode', fname='Arial Unicode MS.ttf', uni=True)
    pdf.set_font("ArialUnicode", size=14)
    pdf.multi_cell(0, 15, title)
    pdf.ln(10)  # Add spacing
    pdf.multi_cell(0, 10, content)
    pdf_output = BytesIO()
    pdf.output(pdf_output, dest="F")  # Output PDF as binary stream
    pdf_output.seek(0)  # Reset stream position
    return pdf_output

# Initialize backend instance
backend = MongoDBBackend(
    username="aditisalvi013",
    password="INE3fxSRrDfSxOP4",
    db_name="posts",
    collection_name="my_posts"
)

st.set_page_config(page_title="KUKI AI", layout="wide")

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
    
    footer {
        font-size: 20px;
        text-align: center;
        padding: 10px;
        margin-top: 20px;
        color: #4BFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Sidebar header
    st.selectbox("Select Model",
                 ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama-guard-3-8b", "llama3-70b-8192",
                  "llama3-8b-8192", "mixtral-8x7b-32768"], key="model_select")
    st.markdown("---")

    st.text_input("🔍 Search", placeholder="")
    st.markdown("---")
    st.header("History")
    st.markdown("---")

    # Fetch all post titles from the database
    posts = backend.get_all_posts()  # Fetch all posts from MongoDB
    if posts:
        for post in posts:
            title = post.get('title', 'Untitled')  # Safely handle missing title
            post_id = str(post.get('_id', 'unknown'))  # Safely handle missing _id

            # Skip posts without a valid _id
            if post_id == 'unknown':
                st.warning(f"Skipping post with missing ID: {title}")
                continue

            # Display post title with rename and delete options
            with st.container():
                # st.button(f"**{title}**", key=f"topic_{post_id}")  # Display the title
                if st.button(f"**{title}**", key=f"topic_{post_id}"):
                    st.session_state["selected_topic"] = title
                    st.session_state["selected_post_content"] = post['content']  # Store content for display

                col2, col3 = st.columns(2)


                if col2.button("✏️ Rename", key=f"rename_{post_id}"):
                    new_title = st.text_input("Enter new title", value=title, key=f"new_title_{post_id}")
                    if st.button("Save", key=f"save_rename_{post_id}"):
                        print(f"Attempting to update post: {post_id}, New Title: {new_title}")
                        if backend.update_post_title(post_id, new_title):
                            # Update the title in session state after backend update
                            for p in st.session_state.posts:
                                if p["_id"] == post_id:
                                    p["title"] = new_title
                            st.success(f"Post '{title}' updated to '{new_title}'!")
                        else:
                            st.error(f"Failed to update post '{title}'.")

                # Delete Button
                if col3.button("🗑️ Delete", key=f"delete_{post_id}"):
                    backend.delete_post(post_id)  # Backend method to delete
                    st.success(f"Post '{title}' deleted successfully!")
                    st.rerun()  # Reload to reflect changes
            st.markdown("---")
    else:
        st.info("No saved posts found.")
        st.markdown("---")

cat_animation_url = "https://lottie.host/fbaf127e-e6d0-41a0-8942-76e8216236d1/jtqrNoFPYx.json"
cat_animation = load_lottie_animation(cat_animation_url)

cols1, cols2, cols3 = st.columns([6, 1, 1])
with cols1:
    st.markdown("")
with cols2:
    if st.button("📝 New Post"):
        st.rerun()
with cols3:
    if st.button("🤖 Account"):
        st.success("Logged out successfully!")

co1, co2, co3 = st.columns([3, 1.5, 3])
with co1:
    st.markdown("")
with co2:
    if cat_animation:
        st_lottie(cat_animation, height=150, width=190, loop=True, quality="high")
        st.title("&nbsp;&nbsp;&nbsp;KUKI AI")
    else:
        st.error("Failed to load animation. Please check the URL.")
with co3:
    st.markdown("")

# Set the background image
bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1498116069452-debf99cb30f0?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
background-size: cover;
background-repeat: no-repeat;
background-attachment: local;
}

</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)

# Display selected post if a topic is selected
if "selected_topic" in st.session_state:
    st.subheader(f"Selected Topic: {st.session_state['selected_topic']}")
    selected_title = st.session_state['selected_topic']
    selected_post = st.session_state.get("selected_post_content", "No content available")
    st.write(st.session_state.get("selected_post_content", "No content available"))
    st.markdown("---")

    st.subheader("Share Post")
    share_options = st.selectbox(
        "Choose sharing option:",
        ["Select", "Text File", "PDF File", "HTML File", "MD File", "Copy to Clipboard", "Share via Email",
         "Share on LinkedIn", "Share on X"], key={selected_title}
    )

    if share_options == "Text File":
        download_file(f"{selected_title}\n\n{selected_post}", f"{selected_title}_post.txt")
    elif share_options == "PDF File":
        pdf_content = create_pdf(selected_title, selected_post)
        st.download_button(
            label="Download PDF",
            data=pdf_content,
            file_name=f"{selected_title}_post.pdf",
            mime="application/pdf"
        )
    elif share_options == "HTML File":
        html_content = f"<html><body><h2>{selected_title}</h2><p>{selected_post}</p></body></html>"
        download_file(html_content, f"{selected_title}_post.html")
    elif share_options == "MD File":
        markdown_content = f"# {selected_title}\n\n{selected_post}"
        download_file(markdown_content, f"{selected_title}_post.md")
    elif share_options == "Copy to Clipboard":
        copy_to_clipboard(f"{selected_title}\n\n{selected_post}")
    elif share_options == "Share via Email":
        share_via_email(f"{selected_title}\n\n{selected_post}", selected_title)
    elif share_options == "Share on LinkedIn":
        share_on_linkedin(selected_post, selected_title)
    elif share_options == "Share on X":
        share_on_x(selected_post, selected_title)

    st.markdown("---")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")

# Main app layout
def main():
    if "post_title" not in st.session_state:
        st.session_state.post_title = ""
    if "generated_post" not in st.session_state:
        st.session_state.generated_post = ""

    st.title("Post Generator")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()

    # Fetch all languages
    all_languages = get_all_languages()
    language_names = [lang[0] for lang in all_languages]
    language_codes = {lang[0]: lang[1] for lang in all_languages}

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_names)

    # Generate Button
    if st.button("Generate"):
        language_code = language_codes[selected_language]
        generated_post = generate_post(selected_length, language_code, selected_tag)

        # Create title for the post
        title = generate_title(selected_tag, selected_length, selected_language)

        # Store generated post and title in session state
        st.session_state.generated_post = generated_post
        st.session_state.post_title = title

        # Save to MongoDB
        backend.save_post(title, generated_post, [selected_tag], selected_length, selected_language)  # Tags passed as a list
        st.success("Post generated and saved successfully!")

    # Display generated post if it exists in session state
    if "generated_post" in st.session_state:
        post = st.session_state.generated_post
        title = st.session_state.post_title

        st.markdown(f"<h2 style='text-align: center; font-weight: bold;'>{title}</h2>", unsafe_allow_html=True)
        st.write(post)
        st.markdown("---")  # Separator line

        # Persist share options
        st.subheader("Share Post")
        share_option = st.selectbox(
            "Choose sharing option:",
            ["Select", "Text File", "PDF File", "HTML File", "MD File", "Copy to Clipboard", "Share via Email",
             "Share on LinkedIn", "Share on X"], key=title
        )

        if share_option == "Text File":
            download_file(f"{title}\n\n{post}", f"{selected_tag}_post.txt")
        elif share_option == "PDF File":
            pdf_content = create_pdf(title, post)
            st.download_button(
                label="Download PDF",
                data=pdf_content,
                file_name=f"{selected_tag}_post.pdf",
                mime="application/pdf"
            )
        elif share_option == "HTML File":
            html_content = f"<html><body><h2>{title}</h2><p>{post}</p></body></html>"
            download_file(html_content, f"{selected_tag}_post.html")
        elif share_option == "MD File":
            markdown_content = f"# {title}\n\n{post}"
            download_file(markdown_content, f"{selected_tag}_post.md")
        elif share_option == "Copy to Clipboard":
            copy_to_clipboard(f"{title}\n\n{post}")
        elif share_option == "Share via Email":
            share_via_email(f"{title}\n\n{post}", title)
        elif share_option == "Share on LinkedIn":
            share_on_linkedin(post, title)
        elif share_option == "Share on X":
            share_on_x(post, title)

    # List saved posts
    # st.markdown("---")
    # st.subheader("View Saved Posts")
    # if st.button("Load Saved Posts"):
    #     posts = backend.get_all_posts()
    #     if posts:
    #         for post in posts:
    #             st.markdown(f"### {post['title']}")
    #             st.markdown(post['content'])
    #             st.markdown(
    #                 f"**Tags:** {post['tags']} | **Length:** {post['length']} | **Language:** {post['language']}")
    #             st.markdown("---")
    #     else:
    #         st.info("No saved posts found.")
    #
    # st.markdown("---")

    # st.subheader("Delete Post")
    # delete_title = st.text_input("Enter the title of the post to delete")
    # if st.button("Delete Post"):
    #     if delete_title:
    #         deleted_count = backend.delete_post(delete_title)
    #         if deleted_count > 0:
    #             st.success(f"Post '{delete_title}' deleted successfully!")
    #         else:
    #             st.error(f"No post found with the title '{delete_title}'.")
    #     else:
    #         st.error("Please enter a title.")

    # Footer
    st.markdown("""
        <footer>
            Built with ❤️ by Aditi Salvi
        </footer>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()

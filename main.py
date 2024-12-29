import urllib
import streamlit as st
from streamlit_lottie import st_lottie
from few_shot import FewShotPosts
from post_generator import generate_post
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

# Function to download content as a file
def download_file(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)

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

# Function to copy content to clipboard
def copy_to_clipboard(content):
    st.code(content)
    st.success("Copied to clipboard!")

# Function to share via email (opens Gmail with prefilled content)
def share_via_email(content, title):
    subject = title
    body = content
    mailto_link = f"https://mail.google.com/mail/?view=cm&fs=1&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    webbrowser.open(mailto_link)

# Function to share on LinkedIn (prefills title and content)
def share_on_linkedin(content, title):
    linkedin_url = "https://www.linkedin.com/shareArticle"
    params = {
        "mini": "true",
        "url": "http://example.com",  # Replace with your app's URL
        "title": title,
        "summary": content
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{linkedin_url}?{query_string}"
    webbrowser.open(full_url)

# Function to share on X (Twitter)
def share_on_x(content, title):
    x_url = "https://twitter.com/intent/tweet"
    params = {
        "text": f"{title}\n{content}"
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{x_url}?{query_string}"
    webbrowser.open(full_url)

# Initialize backend instance
backend = MongoDBBackend(
    username="aditisalvi013",
    password="INE3fxSRrDfSxOP4",
    db_name="posts",
    collection_name="my_posts"
)

# Main app layout
def main():
    if "post_title" not in st.session_state:
        st.session_state.post_title = ""
    if "generated_post" not in st.session_state:
        st.session_state.generated_post = ""

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
        title = f"An Insightful Post on {selected_tag}"

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
             "Share on LinkedIn", "Share on X"]
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
    st.markdown("---")
    st.subheader("View Saved Posts")
    if st.button("Load Saved Posts"):
        posts = backend.get_all_posts()
        if posts:
            for post in posts:
                st.markdown(f"### {post['title']}")
                st.markdown(post['content'])
                st.markdown(
                    f"**Tags:** {post['tags']} | **Length:** {post['length']} | **Language:** {post['language']}")
                st.markdown("---")
        else:
            st.info("No saved posts found.")

    st.markdown("---")

    st.subheader("Delete Post")
    delete_title = st.text_input("Enter the title of the post to delete")
    if st.button("Delete Post"):
        if delete_title:
            deleted_count = backend.delete_post(delete_title)
            if deleted_count > 0:
                st.success(f"Post '{delete_title}' deleted successfully!")
            else:
                st.error(f"No post found with the title '{delete_title}'.")
        else:
            st.error("Please enter a title.")

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

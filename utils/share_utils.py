import webbrowser
import urllib.parse
import streamlit as st

def copy_to_clipboard(content):
    st.code(content)
    st.success("Copied to clipboard!")

def share_via_email(content, title):
    subject = title
    body = content
    mailto_link = f"https://mail.google.com/mail/?view=cm&fs=1&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    webbrowser.open(mailto_link)

def share_on_linkedin(content, title):
    # linkedin_url = "https://www.linkedin.com/shareArticle"
    # params = {"mini": "true", "title": title, "summary": content}
    # webbrowser.open(f"{linkedin_url}?{urllib.parse.urlencode(params)}")
    linkedin_url = "https://www.linkedin.com/shareArticle"
    params = {
        "url": f"{content}.com",  # Replace with your app's URL
        "title": f"{title}",
        "summary": content
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{linkedin_url}?{query_string}"
    webbrowser.open(full_url)


def share_on_x(content, title):
    x_url = "https://twitter.com/intent/tweet"
    params = {"text": f"{title}\n{content}"}
    webbrowser.open(f"{x_url}?{urllib.parse.urlencode(params)}")


from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "8 to 12 lines"
    if length == "Medium":
        return "15 to 20 lines"
    if length == "Long":
        return "21 to 25 lines"


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    generated_content = response.content.strip()

    # Add tags at the end
    return f"{generated_content}"


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. Include emojis relevant to the topic and distribute them naturally across sentences. Add a section at the end with relevant tags.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    Write the post entirely in the selected language, ensuring it remains professional and engaging.
    '''

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\n4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\nExample {i + 1}: \n\n{post_text}'

        if i == 1:  # Use max two samples
            break

    prompt += f"\n\n5) Use relevant emojis and end the post with a line for tags related to '{tag}'."
    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "Japanese", "Mental Health"))

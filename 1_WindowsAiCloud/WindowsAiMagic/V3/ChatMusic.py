import openai

gpt_api = "YOUR_OPENAI_API_KEY"


def get_openai_response(temp_input_text):
    openai.api_key = gpt_api
    openai.base_url = "https://api.gpt.ge/v1/"
    openai.default_headers = {"x-foo": "true"}
    completion = openai.chat.completions.create(
        model="suno-v3.5",
        messages=[
            {
                "role": "user",
                "content": temp_input_text
            },
        ],
        # temperature=0.3,  # 温度越低越稳定，推荐0.3，默认为1
        # n=1,
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    input_text = "高雅的女声，清脆的声音，让人感到舒适"
    raw_output = get_openai_response(input_text)
    print(raw_output)

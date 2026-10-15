import openai


def calculate_cost(completion, prompt_cost_per_1000=0.00015, completion_cost_per_1000=0.0006):
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    total_tokens = prompt_tokens + completion_tokens
    total_cost = (prompt_tokens / 1000) * prompt_cost_per_1000 + (completion_tokens / 1000) * completion_cost_per_1000
    return total_tokens, total_cost


def get_openai_response():
    openai.api_key = "YOUR_OPENAI_API_KEY"
    openai.base_url = "https://api.gpt.ge/v1/"
    openai.default_headers = {"x-foo": "true"}

    messages = []

    while True:
        user_input = input("用户输入：")
        messages.append({"role": "user", "content": user_input})
        # 调用 API
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,  # 温度越低越稳定，推荐0.3
            n=1,
        )
        assistant_message = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        print(assistant_message)

        total_tokens, total_cost = calculate_cost(completion)
        print(f"总 token 数: {total_tokens}")
        print(f"总费用: ${total_cost:.6f}")

        '''
        提示 $0.00015 / 1K tokens
        补全 $0.0006 / 1K tokens
        '''


# 调用函数
get_openai_response()

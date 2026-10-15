import json
import re

import openai


def start_gpt_api(DateFilepath):
    with open(DateFilepath, 'r', encoding='utf-8') as f:
        data = f.read()

    class MinimalGPTChat:
        def __init__(self, api_key, base_url=None, persona="", model="gpt-4o-mini"):
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
            self.model = model
            self.messages = [{"role": "system", "content": persona}]

        def chat(self, user_input):
            self.messages.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": ai_response})
            return ai_response

    bot = MinimalGPTChat(
        api_key='YOUR_OPENAI_API_KEY',
        base_url='https://api.gpt.ge/v1',
    )

    text_list = [
        "你是一个互联网从业者，男性，姓陈，前鹅厂管理层，22年被裁，目前38"
        "岁，经营一家创业公司，技术出身，喜欢批判说明社会现状，并以骂醒人的语气讲述故事，你的面向对象是企图改变自己认知的青年、中年人。"
        "下面我会发一个别人的文字稿，请你将这个文字稿以自己的语气重新梳理一遍，换个角度说明，但主题观点应该一致，这个很重要，"
        "需要自行发挥一部分，如新增故事或修改数字、案例，不要缩减，而应该适当补充，字数要多于这个文字稿，注意不要过多暴露自己的信息，"
        "而应该是处理文字稿。不要有层次结构如首先、其次等，而应该连续说明，就像一个人在面对面给你讲。记得字数要多于原文。不要带地名，"
        "人名等敏感信息。目标用户不一定只有年轻人，注意用语。例子要修改为我的朋友的经历，不要写我的。尽量与原文语气一致，"
        "可以使用较为尖锐的文字，同时引起讨论，可以极端一点，但要能过审。如果出现时间内容则改为今天的时间。\n"
        + data
        ,
        '总结生成的文字稿的视频标题，直接输出一个即可，不需要带引号。'
        '20字以内，不要太多。'
        '要让大家能看懂，不要太专业，符合我的目标画像，'
        '精准涵盖内容点，同时要吸引人，20字以内。最好能带点对立，极端，让大家讨论。'
        ,
        '总结生成的文字稿的视频标签，生成五个，要求常见，热度高，贴合内容，流量总和最大，注意按流量排序，我要发布在B站、小红书、'
        '百家号、抖音等平台，写成一横排，按热度排序，用空格分开。'
        '注意我的内容多为社会和商业内容，请避免出现无关标签。'
    ]

    index = 0

    gpt_generate_text = ''
    gpt_generate_title = ''
    gpt_generate_tags = []

    while True:
        try:
            if index >= len(text_list):
                break
            user_input = text_list[index]
            index += 1
            response = bot.chat(user_input)
            if index == 1:
                gpt_generate_text = response
            elif index == 2:
                def check_punctuation(string):
                    # 使用正则表达式匹配句号、感叹号、问号
                    matches = re.findall(r'[.?!:，。：！？]', string)
                    # print('matchesaaaaaa', matches)
                    # 如果匹配的标点符号超过两个，则返回True
                    return len(matches) > 2

                if check_punctuation(response):
                    index = 1
                    continue
                gpt_generate_title = response
            elif index == 3:
                gpt_generate_tags = response.split(' ')
            if index == 3:
                # 保存文件路径
                output_filename = r'/7_WindowsAiLocal_SWBZ/临时制作/middle.json'

                # 准备要保存的数据
                data_to_save = {
                    "text": gpt_generate_text.replace('“', '').replace('”', ''),  # 去掉引号
                    # "title": gpt_generate_title.replace(',','\n').replace('，','\n'),
                    "title": gpt_generate_title,
                    "tags": gpt_generate_tags
                }

                # 保存为JSON文件
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

                print(f"数据已成功保存到: {output_filename}")

        except Exception as e:
            print(f"发生错误: {e}")
            break


if __name__ == '__main__':
    start_gpt_api(r'/7_WindowsAiLocal_SWBZ/原文文字稿/05/2025_5_17.txt')

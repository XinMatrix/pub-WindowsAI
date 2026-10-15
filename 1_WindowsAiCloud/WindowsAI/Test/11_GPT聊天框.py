from tkinter import *

from Function.GPT.ChatModel import chat
from Dir_Old.Function.Install.function_install_old import Install

# 创建主界面
root = Tk()
root.title("Chat Box")
root.geometry("400x500")

# 创建聊天框
chat_frame = Frame(root)
chat_frame.pack(pady=10)

chat_scroll = Scrollbar(chat_frame)
chat_scroll.pack(side=RIGHT, fill=Y)

chat_list = Listbox(chat_frame, width=50, height=20, yscrollcommand=chat_scroll.set)
chat_list.pack(side=LEFT, fill=BOTH)
chat_scroll.config(command=chat_list.yview)

chat_list.insert(END, '有什么可以帮您？')

# 创建输入框
entry_frame = Frame(root)
entry_frame.pack(pady=10)

entry_box = Entry(entry_frame, width=40)
entry_box.pack(side=LEFT)

send_button = Button(entry_frame, text="Send")
send_button.pack(side=LEFT)


# 发送消息函数
def send_message():
    message = entry_box.get()
    if message:
        chat_list.insert(END, "You: " + message)
        # results = str(chat(input()))[1:].split(' ')
        results = str(chat(message))[1:].split(' ')
        if len(results) > 1:
            if results[1].startswith('Install_'):
                target = results[1].split('_')[1]
                Install(target)
                print(f'{target} 安装成功!')
                chat_list.insert(END, "WindowsAI: " + results[0])
        else:
            chat_list.insert(END, "WindowsAI: " + '功能正在开发中...')
            # print('功能正在开发中...')
        entry_box.delete(0, END)


send_button.configure(command=send_message)

root.mainloop()

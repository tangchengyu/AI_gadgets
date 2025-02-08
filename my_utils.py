"""
用途：和AI大模型交互的代码（网站关键的后端逻辑）
作者:tangchengyu
日期:2025年02月07日
"""
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

# 对"生成脚本"请求进行封装
def generate_script(subject, video_length, creativity, api_key):
    # 1.调用维基百科的API获得相关信息
    search = WikipediaAPIWrapper(lang="zh") #lang是用来指定搜索语言的，不指定的时候默认是英文zh就表示是中文
    search_result = search.run(subject)  # 获得搜索结果的摘要,参数传入:搜索词字符串

    # 2.获得视频的标题
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human","请为{subject}这个主题的视频想一个吸引人的标题")
        ]
    )

    # 3.获得视频的脚本内容
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )

    # 4.定义OpenAI模型
    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)

    # 5.把获得视频标题以及脚本的链组装起来
    title_chain = title_template | model
    script_chain = script_template | model
    # 6.嵌入初值得到链结果————视频标题和脚本内容
    title = title_chain.invoke({"subject": subject}).content # 等价于： title = title_chain.render(subject=subject)
    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content # 等价于：script = script_chain.render(title=title, duration=video_length, wikipedia_search=search_result)

    return search_result, title, script

#测试代码
# print(generate_script("sora模型", 1, 0.7, os.getenv("OPENAI_API_KEY")))
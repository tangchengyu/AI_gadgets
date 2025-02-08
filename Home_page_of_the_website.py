"""
用途：基于Streamlit的网站前端技术栈
作者:tangchengyu
日期:2025年02月07日
"""
import streamlit as st
from my_utils import generate_script

st.title("🎬 视频脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)") #streamlit的markdown网页链接语法

subject = st.text_input("💡 请输入视频的主题") #文字输入框
video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1) #数字输入框
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                    max_value=1.0, value=0.2, step=0.1)
submit = st.button("生成脚本")

if submit and not openai_api_key:
    st.info("请输入你的OpenAI API密钥") #用于显示信息性消息，通常以蓝色框的形式呈现。
    st.stop() #执行到这里后，后续代码不再被执行
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("视频长度需要大于或等于0.1")
    st.stop()
if submit:
    with st.spinner("AI正在思考中，请稍等..."):
    # st.spinner用于创建一个旋转的加载指示器，表示程序正在忙碌。"AI正在思考中，请稍等...": 这是与加载指示器一起显示的消息，告知用户需要稍等。
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
    # 实现效果：with缩进内部的代码还没有运行完，网页上就会一直有一个加载的效果
    st.success("视频脚本已生成！") #success: 这是 Streamlit 提供的一个函数，用于显示成功消息，通常以绿色框的形式呈现。
    st.subheader("🔥 标题：") #subheader: 这是 Streamlit 提供的一个函数，用于创建子标题，通常用于分隔不同的内容部分。
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)
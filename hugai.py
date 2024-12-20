"""
户改描述生成器
v1.3
作者：程超乾
"""
import streamlit as st

# 词汇表
vocabulary = {
    "动作": [
        "拆除", "新建", "安装", "合并到", "改造为", "合并为", "上移", "下移","左移","右移", "增大","减小","分隔出","改为","封闭门洞"
    ],
    "房间": [
        "阳台", "厨房", "客厅", "卧室", "开放厨房", "门厅", "储物间", "卫生间", "过道", "书房", "起居间", "衣帽间",
        "餐厅", "洗手间", "储物间", "此房间未拍摄"
    ],
    "对象": [
        "墙体", "垭口", "推拉门", "单开门", "双开门", "普通窗", "落地窗", "门", "门洞", "横向栅栏", "竖向栅栏", "横向墙体", "竖向墙体",
        "横向短墙","竖向短墙"
    ],
    "方位": [
        "上墙体", "下墙体", "左墙体", "右墙体", "中间", "上方", "下方", "左侧", "右侧", "左上方", "左下方", "右上方", "右下方","上侧","下侧"
    ],
    "常用" : ["A", "B", "并","和","，","。","；","、","新","原","将","在","角","墙体","区域","部分"],
    "效果": [
        "打造封闭式", "打造开放式",  "打造非长方形", "实现干湿分离。", "便于后续安装橱柜。", "面积", "增加室内采光", "取消室内采光","改变分区功能。", "打造入户玄关。"
    ],
    "后缀" : ["", "A", "B", "C", "D"]
}
templates={
    "m1":["房间", "后缀","方位","动作","对象"],
    "m2":["动作","房间", "后缀","方位","对象"]
}
num_columns = 8  # 每行显示的按钮数量
# 函数：更新句子
def update_sentence(word):
    st.session_state.sentence += word + ""

# 清除句子函数
def clear_sentence():
    st.session_state.sentence = ""

# 页面标题
st.title("户改描述生成器")

tab_c,tab_m=st.tabs(["常用","模板"])
with tab_c:
    # 常用卡片
    column1 = st.columns(num_columns)
    words = vocabulary["常用"]
    for k, word in enumerate(words):
        with column1[k % num_columns]:
            if st.button(word, key=(f"common_{k}")):
                update_sentence(word)  # 选中卡片时更新句子
with tab_m:
    # 模板1: 在 房间 后缀 方位 动作 对象"
    m1_columns = st.columns(len(templates["m1"]) + 2)
    s = "在"
    with m1_columns[0]:
        st.write("在")
    for t, type in enumerate(templates["m1"]):
        with m1_columns[t+1]:
            s += st.selectbox(type, options=vocabulary[type], key=f"m1_{type}")
    with m1_columns[-1]:
        if st.button("插入", key="m1_bt"):
            update_sentence(s)

    # 模板2
    m2_columns = st.columns(len(templates["m2"])+1)
    s=""
    for t, type in enumerate(templates["m2"]):
        with m2_columns[t]:
            s+=st.selectbox(type, options=vocabulary[type],key=f"m2_{type}")
    with m2_columns[-1]:
        if st.button("插入",key="m2_bt"):
            update_sentence(s)
    # 模板3
    m3_colums = st.columns(7)
    with m3_colums[0]:
        st.write("将")
    with m3_colums[1]:
        room1=st.selectbox("房间",options=vocabulary["房间"],key="m3_1")
    with m3_colums[2]:
        suffix1 = st.selectbox("后缀", options=vocabulary["后缀"], key="m3_3")
    with m3_colums[3]:
        st.write("合并到")
    with m3_colums[4]:
        room2=st.selectbox("房间",vocabulary["房间"],key="m3_2")
    with m3_colums[5]:
        suffix2 = st.selectbox("后缀", options=vocabulary["后缀"], key="m3_4")
    with m3_colums[6]:
        if st.button("插入", key="m3_5"):
            s="将{}{}合并到{}{}，增大{}{}面积".format(room1,suffix1,room2,suffix2,room2,suffix2)
            update_sentence(s)

with st.expander("方位"):
    # 方位卡片
    column1 = st.columns(num_columns)
    words = vocabulary["方位"]
    for k, word in enumerate(words):
        with column1[k % num_columns]:
            if st.button(word, key=(f"direction_{k}")):
                update_sentence(word)  # 选中卡片时更新句子

# 初始化session_state中的句子（如果还没有初始化的话）
if "sentence" not in st.session_state:
    st.session_state.sentence = ""


with st.expander("全部卡片"):
    # 创建选项卡
    tabs = st.tabs(list(vocabulary.keys()))

    # 遍历每个选项卡
    for i, tab_name in enumerate(vocabulary.keys()):
        with tabs[i]:
            words = vocabulary[tab_name]
            columns = st.columns(num_columns)
            for j, word in enumerate(words):
                with columns[j % num_columns]:
                    if st.button(word,key=(i,j)):
                        update_sentence(word)  # 选中卡片时更新句子

# 显示文本框，句子内容会实时更新
modified_sentence=st.text_area("生成的句子", value=st.session_state.sentence, height=100)
# 保存编辑后的文本框内容
if modified_sentence != st.session_state.sentence:
    st.session_state.sentence = modified_sentence  # 更新session_state中的句子内容
# 清除按钮
if st.button("清除"):
    clear_sentence()  # 点击清除按钮时清空句子

# 提示
st.write("点击上方词汇卡片，它们将会被追加到句子的末尾；编辑后点击文本框外部（或者Ctrl+Enter)自动保存；点击清除按钮清空句子。")

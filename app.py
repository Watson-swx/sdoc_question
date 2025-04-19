import streamlit as st
from sdoc_request import get_tianshu_response
import pandas as pd
import time
import json

# 设置页面标题
st.title("SDoc 问题智能分析")

# 创建文件上传组件
st.text("1. 少量问题，请访问链接提问。")
st.markdown("https://aiapi.sheincorp.cn/llm/#/scene/general_app/7180")

uploaded_file = st.file_uploader("2. 大量问题，请上传 Excel 文件，必须含有【问题描述】字段。", type=["xlsx"])

if uploaded_file is not None:
    # 读取上传的 Excel 文件
    sdoc_df = pd.read_excel(uploaded_file)
    questions = sdoc_df["问题描述"].to_list()

    # AI 智能分析
    categories = []
    modules = []
    summaries = []

    # 创建进度条
    progress_bar = st.progress(0)
    total_questions = len(questions)

    for i, qs in enumerate(questions):
        if qs and len(qs) > 0:
            time.sleep(1)
            params = {"HOA_USERINPUT": qs}
            temp_result = get_tianshu_response(params)
            try:
                print(temp_result)
                print(type(temp_result))
                result = json.loads(temp_result)
            except json.JSONDecodeError:
                result = {"类别": '', "模块": '', "问题归类": ''}
                st.warning(f"问题 '{qs}' 的返回结果不是有效的 JSON 格式。")
        else:
            result = {"类别": '', "模块": '', "问题归类": ''}

        st.write(f"问题{i+1}: {qs}")
        st.write(f"答案: {result}")

        categories.append(result.get("类别"))
        modules.append(result.get("模块"))
        summaries.append(result.get("问题归类"))

        # 更新进度条
        progress_bar.progress((i + 1) / total_questions)

    # 结果数据整理
    sdoc_df['类别'] = categories
    sdoc_df['模块'] = modules
    sdoc_df['问题归类'] = summaries

    # 将结果保存为 Excel 文件
    output_file = "smart_analysis.xlsx"
    sdoc_df.to_excel(output_file, index=0)

    # 创建下载链接
    with open(output_file, "rb") as file:
        btn = st.download_button(
            label="下载分析结果",
            data=file,
            file_name="smart_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
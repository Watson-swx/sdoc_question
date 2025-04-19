from sdoc_request import get_tianshu_response
import pandas as pd
import time
import json

# 问题数据导入
sdoc_df = pd.read_excel("sdoc直播观众提问和回复.xlsx")
questions = sdoc_df["描述"].to_list()

# AI智能分析
categories = []
modules = []
summaries = []

for qs in questions:
    if qs and len(qs)>0:
        time.sleep(1)
        params = {"HOA_USERINPUT": qs}
        temp_result = get_tianshu_response(params)
        try:
            result = json.loads(temp_result)
        except json.JSONDecodeError:
            result = {"类别":'', "模块":'', "问题归类": ''}
            print("not json!")
    else:
        result = {"类别":'', "模块":'', "问题归类": ''}
    print("question:", qs)
    print("answer:", result)
    categories.append(result["类别"])
    modules.append(result["模块"])
    summaries.append(result["问题归类"])

# 结果数据整理
sdoc_df['类别'] = categories
sdoc_df['模块'] = modules
sdoc_df['问题归类'] = summaries

sdoc_df.to_excel("smart_analysis.xlsx", index=0)

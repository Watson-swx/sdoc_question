from tianshu import AiHelperClient, generate_serial_number

def get_tianshu_response(params):
    # 请求地址
    base_url = "https://api-aihelper.sheincorp.cn"
    # 流水号，非必填，请求幂等处理，方便后续请求跟踪
    out_id = generate_serial_number()
    # 应用秘钥，必填
    app_secret = "120a6f8685f8652ace71f7a2b0f2d395"
    # 应用id，必填
    scene_id = 7180
    # 业务编码，对应系统编码或工号，必填
    biz_code = "10270178"
    # 构建请求客户端
    client = AiHelperClient(base_url, app_secret, scene_id)
    # 构建请求参数
    # params = {"HOA_USERINPUT": "在线表格可以 @人吗"}


    response = client.post("/open/v1/chat", {
        "out_id": out_id,
        "scene_id": scene_id,
        "biz_code": biz_code,
        "params": params
    })
    print(params)
    print(response)
    if response is not None:
        info = response.get("info")
        print(response)
        if info is not None:
            print(info)
            result = info.get("info")
        else:
            result = None
    else:
        result = None

    return result

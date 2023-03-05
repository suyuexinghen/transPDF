import sys
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
#pip install tencentcloud-sdk-python 
try:
    # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
    # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
    # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
    cred = credential.Credential("YourSecretId ","SecretKey")
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

    # 获取脚本传入的文件路径
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 将文本按照长度小于2000词的文段进行切割
    text_list = []
    while len(text) > 2000:
        index = text.rfind('.', 0, 2000)
        if index == -1:
            index = 2000
        text_list.append(text[:index+1])
        text = text[index+1:]
    text_list.append(text)
    
    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.TextTranslateRequest()
    
    # 分别调用api进行翻译
    result_list = []
    for item in text_list:
        params = {
            "SourceText": item,
            "Source": "en",
            "Target": "zh",
            "ProjectId": 0
        }
        req.from_json_string(json.dumps(params))
        try:
            # 返回的resp是一个TextTranslateResponse的实例，与请求对象对应
            resp = client.TextTranslate(req)
            result_list.append(resp.TargetText)
        except TencentCloudSDKException as err:
            print(err)
    
    # 输出翻译结果
    #print("".join(result_list))
    # 将翻译结果写入output.txt文件
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write("".join(result_list))


except TencentCloudSDKException as err:
    print(err)

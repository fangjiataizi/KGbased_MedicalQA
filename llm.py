# 导入dashscope库
import dashscope
# 设置dashscope的api密钥
dashscope.api_key = "sk-73b98346d02d4edf897925190b19ca97"

# 导入http库的HTTPStatus
from http import HTTPStatus
# 导入dashscope的Generation
from dashscope import Generation
# 导入dashscope.api_entities.dashscope_response的Role
from dashscope.api_entities.dashscope_response import Role

# 定义初始化消息的函数
def init_message():
    # 创建一个包含一条系统消息的列表
    messages = [{'role': Role.SYSTEM, 'content': '你是一个智能客服助手'}]
    return messages

# 定义获取响应的函数
def get_response(user_input, messages):
    # 调用dashscope的Generation.call方法生成响应
    response = Generation.call(
        Generation.Models.qwen_max,
        messages=messages,
        result_format='message',  # 设置结果格式为"message"
    )
    # 如果返回的状态码是200，表示请求成功
    if response.status_code == HTTPStatus.OK:
        # 打印响应内容
        print(response)
        # 将生成的消息添加到messages列表中
        messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
        # 返回生成的消息内容
        return response.output.choices[0]['message']['content']
    else:
        # 如果请求失败，打印错误信息
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        # 返回"Error"
        return "Error"

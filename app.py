# 导入Flask库，用于构建web应用
import traceback

from flask import Flask, request, render_template
# 导入自定义库llm
from llm import init_message, Role, get_response

from question_classifier import *
from question_parser import *
from answer_search import *


'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是医药智能助理，希望可以帮到您。如果没答上来，请多多包涵。'
        try:
            res_classify = self.classifier.classify(sent)
            # print(res_classify)
            if not res_classify:
                return answer
            res_sql = self.parser.parser_main(res_classify)
            # print(res_sql)
            final_answers = self.searcher.search_main(res_sql)
            # print(final_answers)
            if not final_answers:
                return answer
            else:
                return '\n'.join(final_answers)
        except Exception as e:
            traceback.print_exc()
            return answer






# 创建Flask的app实例
app = Flask(__name__)

# 初始化一个空的消息列表
messages = []

# 定义一个函数，用于生成机器人的响应
def generate_response(user_input):
    # 将用户输入添加到messages中
    messages.append({'role': Role.USER, 'content': user_input})
    # 调用模型得到回复
    response = get_response(user_input, messages)
    return response

# 定义根路由，当用户访问主页时会触发该函数
@app.route('/')
def home():
    # 初始化消息
    # messages = init_message()
    # 渲染主页模板并返回
    return render_template('home.html')

# 定义/get路由，当用户发送请求时会触发该函数
@app.route('/get')
def get_bot_response():
    global handler
    # 获取用户发送的消息
    userText = request.args.get('msg')
    print("user input:{}".format(userText))
    # 调用generate_response函数生成机器人的响应
    # botResponse = generate_response(userText)
    botResponse=handler.chat_main(userText)
    # 打印消息列表
    # print(messages)
    # 返回机器人的响应
    return botResponse

# 如果当前脚本是主程序，那么启动Flask应用
if __name__ == "__main__":
    handler = ChatBotGraph()
    app.run()

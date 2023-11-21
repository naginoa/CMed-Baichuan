import random
from http import HTTPStatus
from dashscope import Generation
import dashscope


def call_with_messages():
    messages = [
        {'role': 'user', 'content': '''以下是两条医学训练数据\n1.{"input": "找出指定的实体：\n（二）流感嗜血杆菌流感嗜血杆菌是广泛寄居在正常人上呼吸道的微生物，在健康儿童中，约30%～80%都带有Hi，绝大多数是无荚膜不定型（NTHI），无致病性的，仅少数为有荚膜菌株，而侵袭性疾病大多数为Hib菌株引起。\n类型选项：药物，微生物类，医疗设备，身体部位，医院科室，临床表现，医学检验项目，疾病，医疗程序", "target": "上述句子中的实体包含：\n微生物类实体：流感嗜血杆菌，Hi，NTHI，荚膜菌株，Hib菌株\n身体部位实体：上呼吸道", "answer_choices": ["药物", "微生物类", "医疗设备", "身体部位", "医院科室", "临床表现", "医学检验项目", "疾病", "医疗程序"], "task_type": "ner", "task_dataset": "CMeEE-V2", "sample_id": "train-101455"}\n
2.{"input": "找出指定的实体：\n美国根据药物的效力及毒性反应大小将常用的10种抗结核药物分为三类：一级药物：效力最大而毒力最小，如INH及RFP。\n实体类型选项：疾病，临床表现，药物，医学检验项目，身体部位，医疗程序", "target": "", "answer_choices": ["疾病", "临床表现", "药物", "医学检验项目", "身体部位", "医疗程序"], "task_type": "ner", "task_dataset": "CMeEE-V2", "sample_id": "test-49009"}\n
请根据上述两条训练数据，生成类似相应的5条医学训练数据，医学实体只能为'疾病','临床表现','医疗程序','医疗设备','药物','医学检验项目','身体','科室','微生物类'中的几种。\n生成结果为json的list'''}]
    gen = Generation()
    response = gen.call(
        'qwen-14b-chat',
        messages=messages,
        seed=random.randint(1, 10000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response.get("output").get("choices")[0].get("message").get('content'))
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    dashscope.api_key = 'sk-fca3492adf6b4c4b84fd5d94359d89ab'
    call_with_messages()

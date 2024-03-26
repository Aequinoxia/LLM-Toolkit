import json
from typing import List

from websockets.sync.client import connect as ws_connect
from websockets.exceptions import ConnectionClosed

from .auth import get_wss_url
from .meta import QueryParams, MODEL_MAP


class SparkAPI(object):
    """
    API Doc: https://www.xfyun.cn/doc/spark/Web.html
    """
    def __init__(self, app_id: str, api_key: str, api_secret: str, api_model: str, **kwargs):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_model = api_model

    def chat(self, prompt, history=[]):
        history.append(prompt)
        messages = [
            {
                'role': 'assistant' if i%2 else 'user', 
                'content': content
            } for i, content in enumerate(history)
        ]
        responds = self.interact_with_server(messages)
        return [msg['content'] for msg in responds]

    def interact_with_server(self, messages: List[dict]):
        query = QueryParams(
            app_id=self.app_id,
            domain=MODEL_MAP[self.api_model]['domain'],
            text=messages
        ).dump_json()
        wss_url = get_wss_url(MODEL_MAP[self.api_model]['url'], self.api_secret, self.api_key)
        with ws_connect(wss_url) as websocket:
            websocket.send(query)
            contents = []
            while True:
                try:
                    res = json.loads(websocket.recv())
                    contents.append(
                        res['payload']['choices']['text'][0]['content']
                    )
                    if res['header']['status'] == 2:  # 0: first msg, 1: middle msg, 2: last msg.
                        break
                except ConnectionClosed:
                    break
        return messages + [{'role': 'assistant', 'content': ''.join(contents)}]


if __name__ == "__main__":
    config = {
        'app_id': '', 
        'api_key': '', 
        'api_secret': '', 
        'api_model': 'v3.0'
    }
    api = SparkAPI(**config)
    msgs = api.chat("你好，我是Tom")
    msgs = api.chat("我刚刚提到我的名字是什么？", msgs)
    for content in msgs:
        print(content)

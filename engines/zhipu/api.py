from zhipuai import ZhipuAI


class ZhiPuAPI(object):
    def __init__(self, api_key: str, model='glm-4'):
        self.client = ZhipuAI(api_key=api_key)
        self.model = model

    def chat(self, prompt, history=[]):
        messages = [
            {
                'role': 'assistant' if i%2 else 'user', 
                'content': content
            } for i, content in enumerate(history + [prompt])
        ]
        
        # 同步调用
        # answer = self.client.chat.completions.create(
        #     messages=messages,
        #     model=self.model,
        #     tools=self.tools,
        # ).choices[0].message.content
        
        # 流式调用
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True
        )
        answer = ''
        for chunk in response:
            answer += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end='', flush=True)
        return history + [prompt] + [answer]

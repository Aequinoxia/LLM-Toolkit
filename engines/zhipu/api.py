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
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model
        ).choices[0].message.content
        return history + [prompt] + [response]

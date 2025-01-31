from openai import OpenAI


class DeepSeekAPI(object):
    def __init__(self, api_key: str, model='deepseek-coder'):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.model = model

    def chat(self, prompt, history=[]):
        system_prompt = [{"role": "system", "content": "You are a helpful assistant"}]
        messages = system_prompt + [
            {
                'role': 'assistant' if i%2 else 'user', 
                'content': content
            } for i, content in enumerate(history + [prompt])
        ]
        
        # 流式调用
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=4096,
            stream=True
        )
        answer = ''
        for chunk in response:
            content = chunk.choices[0].delta.content
            reasoning_content = chunk.choices[0].delta.reasoning_content if hasattr(chunk.choices[0].delta, 'reasoning_content') else None
            if reasoning_content:
                print(reasoning_content, end='', flush=True)
            if content:
                answer += content
                print(content, end='', flush=True)
        return history + [prompt] + [answer]

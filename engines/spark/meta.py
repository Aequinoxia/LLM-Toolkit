import json
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass


MODEL_MAP = {
    'v1.5': {
        'domain': 'general',
        'url': 'wss://spark-api.xf-yun.com/v1.1/chat',
    },
    'v2.0': {
        'domain': 'generalv2',
        'url': 'wss://spark-api.xf-yun.com/v2.1/chat',
    },
    'v3.0': {
        'domain': 'generalv3',
        'url': 'wss://spark-api.xf-yun.com/v3.1/chat',
    },
}


class Domain(Enum):
    GENERAL = 'general'
    GENERAL_V2 = 'generalv2'
    GENERAL_V3 = 'generalv3'

    def __str__(self):
        return self.value


class Role(Enum):
    USER = 'user'
    ASSISTANT = 'assistant'

    def __str__(self):
        return self.value


@dataclass
class Text:
    role: Role
    content: str


@dataclass
class QueryParams:
    app_id: str
    text: List[Text]
    domain: Domain

    uid: Optional[str] = None

    temperature: float = 0.5
    max_tokens: int = 4096
    top_k: int = 4
    chat_id: Optional[str] = None

    def dump(self):
        text = [
            {'role': str(t.role), 'content': t.content}
            if isinstance(t, Text) else t
            for t in self.text
        ]
        data = {
            'header': {
                'app_id': self.app_id,
                'uid': self.uid,
            },
            'parameter': {
                'chat': {
                    'domain': str(self.domain),
                    'max_tokens': self.max_tokens,
                    'temperature': self.temperature,
                    'top_k': self.top_k,
                    'chat_id': self.chat_id,
                }
            },
            'payload': {
                'message': {
                    'text': text
                }
            }
        }
        return data

    def dump_json(self):
        return json.dumps(self.dump(), ensure_ascii=False)


if __name__ == '__main__':
    from pprint import pprint
    params = QueryParams(
        app_id='app_id',
        domain=Domain.GENERAL,
        # text=[Text(role=Role.USER, content='hello')],
        text=[{'role': 'user', 'content': 'hello'}],
    )
    pprint(params.dump())
    pprint(params.dump_json())

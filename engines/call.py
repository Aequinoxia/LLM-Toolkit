import configparser
from pathlib import Path

from .spark.api import SparkAPI
from .zhipu.api import ZhiPuAPI
from .deepseek.api import DeepSeekAPI


class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".llm_toolkit"
        self.config_dir.mkdir(exist_ok=True)
        self.config_filepath = self.config_dir / "engines_config.ini"
        if not self.config_filepath.exists():
            self._generate_config_template()
        else:
            self.conf = configparser.ConfigParser()
            self.conf.read(self.config_filepath)
    
    def _generate_config_template(self):
        config = configparser.ConfigParser()
        config_template = {
            'spark': {
                'app_id': '', 
                'api_key': '', 
                'api_secret': '', 
                'api_model': 'v3.5'  # ('v3.0', 'v3.5')
            },
            'zhipu': {
                'api_key': '',
                'model': 'glm-4-air'  # ALL Model: https://open.bigmodel.cn/modelcenter/square, Price: https://open.bigmodel.cn/pricing
            },
            'deepseek': {
                'api_key': '',
                'model': 'deepseek-coder'  # ALL Model: https://platform.deepseek.com/api-docs/zh-cn/pricing/
            }
        }
        for section, options in config_template.items():
            config.read_dict({section: options})
        with open(self.config_filepath, 'w') as configfile:
            config.write(configfile)
        raise Exception(
            f"Configuration file not found. A template has been generated "\
            f"at location '{self.config_filepath}'. Please fill it out."
        )

    def get(self, engine_name):
        engine_config = dict(self.conf[engine_name])
        if '' in engine_config.values():
            raise ValueError(f"Engine '{engine_name}' contains incomplete configurations.")
        return engine_config


class Engine:
    def __init__(self):
        self.engine_classes = {
            'spark': SparkAPI,
            'zhipu': ZhiPuAPI,
            'deepseek': DeepSeekAPI
        }

    def get(self, engine_name):
        return self.engine_classes[engine_name]


class Call:
    def __init__(self, engine_name):
        engine_conf = Config().get(engine_name)
        engine_class = Engine().get(engine_name)
        self.engine = engine_class(**engine_conf)

    def chat(self, prompt, msgs=[]):
        return self.engine.chat(prompt, msgs.copy())


if __name__ == "__main__":
    call = Call('spark')
    msgs = call.chat("你好，我是Tom")
    print(call.chat("我刚刚说我叫什么名字来着？", msgs))
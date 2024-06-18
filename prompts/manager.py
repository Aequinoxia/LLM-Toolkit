import inspect
import importlib

class CustomPrompt:
    def __init__(self):
        self._get_custom_prompts()

    def apply_templates(self, prompt):
        """
        自定义prompt的触发方式：在prompt开头输入自定义prompt的关键词（以空格分隔），然后双冒号接回车。
        """
        prompt = prompt.lstrip()
        line_one = prompt.split('\n')[0]
        delimiter = '::'
        if delimiter in line_one:
            trigger_content, query = prompt.split(delimiter, 1)
            keywords = trigger_content.split(' ')
            for keyword in keywords:
                if '-' in keyword:
                    func_name, params = keyword.split('-', 1)
                    template_func = self._custom_prompts[func_name]
                    query = template_func(query, *params.split('-'))
                else:
                    template_func = self._custom_prompts[keyword]
                    query = template_func(query)
            return query
        else:
            return prompt

    def display_all_templates(self):
        print(', '.join(self._custom_prompts.keys()))

    def _get_custom_prompts(self):
        module = importlib.import_module('.all_prompts', package=__package__)
        self._custom_prompts = {name: obj for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)}
    
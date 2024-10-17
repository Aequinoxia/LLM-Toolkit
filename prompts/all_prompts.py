def comment(prompt, env=''):
    return prompt + f"\n\n请你站在以英文为母语的编程专家的视角，帮我将以上内容**用英文**转化成简洁、自然、合理且专业的{env}注释。"


def naming(prompt, lang='python', item='代码'):
    return prompt + f"\n\n请你站在{lang}编程专家的视角，为表达以上含义的{lang} {item}，提出几个简洁、合理且符合标准代码风格指南的命名建议。"


def guide(prompt, lang='python'):
    return prompt + f"\n\n请你站在{lang}编程专家的视角，教我用{lang}以尽可能简洁、合理且专业的方式实现这个需求。"


def exp(prompt):
    return prompt + f"\n\n---\n\n请用中文对以上内容进行概括"


def expc(prompt, lang='Next.js'):
    """explain codes"""
    return prompt + f"\n\n请你站在一个资深{lang}开发导师的视角，从教学的角度出发，对以上代码的功能意图和相关知识点进行尽可能完整、细致的拆分讲解。"


def pro(prompt):
    prompt = "- " + prompt.replace('\n\n', '\n\n- ')
    pua_words = "Take a deep breath and tackle this problem step by step. "\
                "If you nail it, I'll give you a hefty tip. "\
                "But if you fail, it'll have dire consequences, like the unthinkable happening to 100 grandmothers."
    prompt = f"我需要你完成的任务是：\n\n{prompt}\n\n"\
            f"另外，请你注意：\n\n- {pua_words}"
    return prompt


def trans(prompt, lang='英文'):
    """翻译为指定语言"""
    return f"“{prompt}”" + f"\n\n---\n\n请你作为一位{lang}母语者，帮我将以上内容中用中文引号包裹的段落翻译成简洁、流畅且地道的{lang}:"

def reddit(prompt):
    """翻译为指定语言"""
    return f"“{prompt}”" + f"\n\n---\n\n请你作为一位常年混迹Reddit社区的英文母语者，帮我将以上内容中用中文引号包裹的段落翻译成符合Reddit社区沟通风格的流畅、地道的英文:"

def pnpm(prompt):
    return f"“{prompt}”" + f"\n\n---\n\n是否存在与以上命令严格等价的pnpm命令？如果是的话，与该命令严格等价的pnpm命令为:"

def review(prompt, lang='Next.js'):
    return prompt + f"\n\n我是一个{lang}新手，请你站在资深{lang}开发专家的视角，帮我Review以上代码，检查其中是否有冗余、误用或不良的编码实践。如果你对代码中的部分内容有疑问，你可以提问，我会为你补充相应的代码片段和背景信息。"


def aipic(prompt):
    return f"{prompt}" + f"\n\n---\n\nPlease write a prompt in English from the perspective of an AI drawing prompt expert, based on the requirements mentioned above. Demanding lifelike details, clear imagery, and an engaging presentation. Please express your prompt in a concise and complete paragraph without line breaks."


def ph(prompt):
    """Product Hunt自动回复"""
    command = "**I hope you can provide meaningful, valuable, and constructive feedback on the above product (and related information) from the user's perspective.**\n"\
              "To ensure the quality of the response, you need to complete the following four tasks in order:\n"\
              "1. Analyze what information, in relation to the above text, might bring value or assistance to the author or other users.\n"\
              "2. From the directions you've just listed, select the most helpful and least error-prone perspective, and elaborate on it in approximately 100-200 words.\n"\
                 "Also, make sure to wrap up your response with a **meaningful** question to boost the chances of getting a reply.\n"\
              "3. Based on the content of Task 2, organize our views into a fluent, natural, and constructive response text, keeping the word count under 150 words: \n"\
                 "\t- First, congratulate the other party on their product launch, then provide constructive analysis, evaluation, or suggestions. "\
                 "Finally, pose a valuable question that can attract a response from the other party and casually inquire about their future product iteration plans.\n"\
              "4. Polish the response text obtained from Task 3, without altering the original meaning, to enhance the diction and expression. "\
                 "The goal is to **make the comment appear more authentic, natural, and coherent, as if written by a genuine netizen with sincere intent**."
    return prompt + f"\n\n---\n\n{command}"
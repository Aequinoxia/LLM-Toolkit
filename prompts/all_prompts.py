def 注释(prompt):
    return prompt + "\n\n请你站在以英文为母语的编程专家的视角，帮我将以上内容转化成简洁、合理、地道且专业的英文注释。"

def 命名(prompt):
    return prompt + "\n\n请你站在python编程专家的视角，为表达以上含义的python代码，提出几个简洁、合理且符合PEP 8规范的命名建议。"

def 编程(prompt):
    return prompt + "\n\n请你站在python编程专家的视角，教我用python以尽可能简洁、合理且专业的方式实现这个需求。"

def pua(prompt):
    prompt = "- " + prompt.replace('\n\n', '\n\n- ')
    pua_words = "Take a deep breath and tackle this problem step by step. "\
                "If you nail it, I'll give you a hefty tip. "\
                "But if you fail, it'll have dire consequences, like the unthinkable happening to 100 grandmothers."
    prompt = f"我需要你完成的任务是：\n\n{prompt}\n\n"\
            f"另外，请你注意：\n\n- {pua_words}"
    return prompt
    
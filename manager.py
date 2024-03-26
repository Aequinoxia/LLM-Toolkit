import json
from typing import List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from IPython.display import Markdown, clear_output

from engines.call import Call
from utils.func import paginate


@dataclass
class Dialog:
    id: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    msgs: List[str] = field(default_factory=lambda: list())

    def to_dict(self):
        return self.__dict__


class ChatManager:
    def __init__(self, engine_name):
        self.dialog = None
        self.call = Call(engine_name)
        self.cache = CacheManager()

    def _show_msgs(self):
        if self.dialog:
            if len(self.dialog.msgs) > 2:  # Place history messages within a collapsed block
                content = ""
                for i, msg in enumerate(self.dialog.msgs[:-2]):
                    content += f"\n\n## {'【Answer】' if i%2 else '【Query】'}"
                    content += ("\n\n"+msg+"\n\n---\n")
                content = content.replace('\n', '\n> ')  # Also place history messages within a blockquote
                collapsed_block = f"<details><summary>【History Messages】</summary>\n\n{content}\n</details>"
                display(Markdown(collapsed_block))
            for i, msg in enumerate(self.dialog.msgs[-2:]):  # Display the last Q&A as usual
                display(Markdown(f"## {'【Answer】' if i%2 else '【Query】'}"))
                display(Markdown(msg+"\n\n---\n"))

    def chat(self, prompt='', start_new=False):
        if prompt.strip():
            if (self.dialog is None) or start_new:
                self.dialog = Dialog()
            self.dialog.msgs = self.call.chat(prompt, self.dialog.msgs.copy())
            self._show_msgs()
            self.cache.save_dialog(self.dialog)
        else:  # Empty prompt: Skips engine call and shows prior messages.
            self._show_msgs()
    
    def delete_last_qa(self):
        if self.dialog:
            if len(self.dialog.msgs) <= 2:
                self.dialog = None
            else:
                self.dialog.msgs = self.dialog.msgs[:-2]
    
    def switch_dialog(self, page_size=20, title_length=60):
        all_dialogs = [
            self.cache.dialogs[key] for key in sorted(self.cache.dialogs, reverse=True)
        ]
        page_index = 1

        def truncate(msg):
            msg = msg.strip().replace('\n', ' ')
            if len(msg) <= title_length:
                return msg[:title_length]
            else:
                return f"{msg[:title_length]}..."

        while True:
            clear_output()
            current_page_dialogs, page_index, total_pages = paginate(all_dialogs, page_size, page_index)
            content = ["|Number|Timestamp|Abstract|"] + ["|:---:|:---:|:---|"] + [
                f"|**{i+1}**|{dialog.id}|{truncate(dialog.msgs[0])}|" \
                for i, dialog in enumerate(current_page_dialogs)
            ]
            display(Markdown('\n'.join(content) + '\n\n---\n'))
            display(Markdown(
                f"[{page_index}/{total_pages}] **'q'**: Quit, **'n'**: Next Page, **number**: Load dialog\n\n---\n"
            ))
            
            input_content = input()
            if input_content == 'q':
                clear_output()
                print("Quit.")
                return
            elif input_content == 'n':
                page_index += 1
            elif input_content.isdigit():
                self.dialog = current_page_dialogs[int(input_content) - 1]
                clear_output()
                print("Done.")
                break
            else:
                continue


class CacheManager:
    def __init__(self, cache_dir=None):
        self.dialogs = dict()  # Dict: {dialog.id: dialog}
        self._dialogs_count_limit = 100
        self._init_cache_dir(cache_dir)
        if self._dialogs_filepath.exists():
            self._load_cache_data()

    def _init_cache_dir(self, cache_dir):
        if not cache_dir:
            self._cache_dir = Path('/var/tmp/llm_toolkit')
        else:
            self._cache_dir = Path(cache_dir) if not isinstance(cache_dir, Path) else cache_dir
        self._cache_dir.mkdir(exist_ok=True)
        self._dialogs_filepath = self._cache_dir / 'history_dialogs.json'

    def _load_cache_data(self):
        with open(self._dialogs_filepath, 'r') as read_pipeline:
            try:
                dialog_dicts = json.load(read_pipeline)
            except json.JSONDecodeError:
                dialog_dicts = None
        if dialog_dicts:
            self.dialogs = {item['id']: Dialog(**item) for item in dialog_dicts}

    def _save_cache_data(self):
        dialog_dicts = [dialog.to_dict() for dialog in self.dialogs.values()]
        with open(self._dialogs_filepath, 'w') as write_pipeline:
            json.dump(dialog_dicts, write_pipeline)

    def save_dialog(self, dialog: Dialog):
        assert isinstance(dialog, Dialog)
        self.dialogs[dialog.id] = dialog
        while len(self.dialogs) > self._dialogs_count_limit:
            earliest_id = sorted(self.dialogs)[0]
            self.dialogs.pop(earliest_id)
        self._save_cache_data()

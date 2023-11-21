import requests, os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from languages import LANGUAGES
from config import RAPID_API_KEY

class Compiler:
    URL = "https://online-code-compiler.p.rapidapi.com/v1/"

    def __init__(self):
        self.session = requests.Session()

    def execute(self, language: str, code: str, stdin: str = ""):
        language_lower = language.lower()
        if language_lower not in LANGUAGES:
            available_languages = [f"`{lang}`" for lang in LANGUAGES]
            languages_output = ", ".join(available_languages)
            raise CompilerException(
                f"**List of available languages:**\n\n{languages_output}.")

        payload = {
            "language": language_lower,
            "version": "latest",
            "code": code,
            "input": stdin
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "online-code-compiler.p.rapidapi.com"
        }

        try:
            r = self.session.post(
                self.URL,
                json=payload,
                headers=headers)

            r.raise_for_status()

        except requests.exceptions.RequestException as e:
            raise CompilerException(f"**Error in API request.**\n\n{str(e)}")

        return r.json()

    def convert_bytes(self, size: int):
        if not size:
            return 0.0
        return float(
            "%.4f" % (float(size) / (1024 * 1024)))

    def pastebin(self, text: str):
        url = "https://dpaste.org/api/"
    
        r = self.session.post(
            url=url,
            data={
                "content": text.encode("utf-8"),
            },
        )
    
        resp = r.text
        out = resp.replace('"', "")
        return out

    def generate_output(self, response: str, code: str):
        output = response["output"]
        language_info = response["language"]
        memory = self.convert_bytes(
            response["memory"])
        cpu_time = response["cpuTime"]

        _code = f"```{language_info['id']}\n{code}```" if code and len(code) < 4096 else "" if not code else f"[Code]({self.pastebin(code)})"
        
        _output = f"```text\n{output}```" if output and len(output) < 4096 else "" if not output else f"[Output]({self.pastebin(output)})"

        __output = f"""
**Language:** {language_info['id']}
    __**Version:**__ {language_info['version']}
    __**Version Name:**__ {language_info['version_name']}

**Code:**
{_code}

**Output:**
{_output}

**Memory Usage:** {memory} MiB
**CPU Time:** {cpu_time}"""

        return __output


class CompilerException(Exception):
    pass


def reply_markup(switch_inline_query):
    return InlineKeyboardMarkup([[InlineKeyboardButton("Share", switch_inline_query=switch_inline_query)]])

async def get_code_from_message(message, message_text):
    if message.reply_to_message:
        replied_message = message.reply_to_message

        if replied_message.text:
            return replied_message.text
        elif replied_message.document:
            try:
                document = await replied_message.download()
                with open(document, "r") as file:
                    code = file.read()
                os.remove(document)
                return code
            except Exception as e:
                return await message.reply(f"**Error reading document:**\n```{e}```", parse_mode=ParseMode.MARKDOWN, quote=True)
    else:
        return " ".join(message_text.split(" ")[2:])

def extract_stdin_from_message(message_text):
    stdin = ""
    if "/stdin" in message_text:
        stdin = " ".join(message_text.split("/stdin ")[1:])
        message_text = message_text.replace("/stdin " + stdin, "")
    return stdin, message_text

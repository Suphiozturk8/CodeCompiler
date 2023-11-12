import requests
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
    
        r = requests.post(
            url=url,
            data={
                'content': text.encode('utf-8'),
            },
        )
    
        resp = r.text
        out = resp.replace('"', '')
        return out

    def generate_output(self, response: str, code: str):
        output = response["output"]
        language_info = response["language"]
        memory = self.convert_bytes(
            response["memory"])
        cpu_time = response["cpuTime"]

        _code = f"```{language_info['id']}\n{code}```" if len(code) < 4096 else f"[Code]({self.pastebin(code)})"

        _output = f"```text\n{output}```" if len(output) < 4096 else f"[Output]({self.pastebin(output)})"

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

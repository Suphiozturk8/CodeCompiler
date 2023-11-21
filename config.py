"""
You can get your API ID and API HASH from https://my.telegram.org
You can get your bot token from https://t.me/BotFather
You can get your rapid api key from https://rapidapi.com/Glavier/api/online-code-compiler
"""

NAME = "CodeCompiler"
API_ID = None
API_HASH =  ""
BOT_TOKEN = ""
RAPID_API_KEY = ""

START_MSG = """
**Hello! 👻**

**My name is Code Compiler Bot.**

**Here I can compile codes in various programming languages.**

**You can use the /help command to learn how to use it.**
    """


HELP_MSG = """
**How to Use Code Compiler Bot:**

**To run code, use the following format:**
```
/run <language> <code or reply_code_text or reply_code_document> [/stdin <stdin>]
```

**Examples:**
```
/run python3 print("Hello, World! 👻")
```

```
/run python3 print(input("Enter your name: ")) /stdin Suphi
```

**To use in inline mode:** 
```
@bot_username <language> <code> [/stdin <stdin>]
```

**Replace** `<language>` **with the programming language you're using,** `<code>` **with your actual code, and** `[/stdin <stdin>]` **with optional stdin for your code.**

**Use the button below the printout to share the code in the chat you want! 🚀**
"""
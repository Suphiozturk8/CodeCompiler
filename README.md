
# My Code Compiler Bot

## Overview
This Telegram bot enables compiling and running code snippets in various programming languages using an online code compiler API.

## Inspirations
- This project was inspired by [fswair's CPP17 Compiler](https://github.com/fswair/CPP17_Compiler). Special thanks for their amazing work!

## Features
- Compile code in multiple languages.
- Optionally provide input through stdin.
- View output, memory usage, and CPU time.
- Share the code in the chat you want using the button.

## Getting Started
1. Clone the repository: `git clone https://github.com/suphiozturk8/CodeCompiler.git && cd CodeCompiler`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your Telegram bot token in the `config.py` file.
4. Run the bot: `python main.py`

## Usage
- Use the `/run` command followed by the language and code snippet.
- Optionally use `/stdin` to provide input through stdin.
- ```/run <language> <code or reply_code_text or reply_code_document> [/stdin <stdin>]```

Examples:
```
/run python3 print("Hello, World! 👻")
```
```
/run python3 print(input("Enter your name: ")) /stdin Suphi
```

## Usage in Inline Mode
To use in inline mode, mention the bot followed by the language and code snippet:
```
@bot_username <language> <code> [/stdin <stdin>]
```

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Make your changes and commit: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

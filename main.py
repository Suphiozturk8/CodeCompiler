
import os, requests
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

from utils import Compiler, CompilerException, reply_markup, get_code_from_message, extract_stdin_from_message
from config import NAME, API_ID, API_HASH, BOT_TOKEN, START_MSG, HELP_MSG

app = Client(name=NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

code_compiler = Compiler()

@app.on_message(
    filters.command("start"))
async def start(_, message: Message):
    await message.reply(START_MSG, parse_mode=ParseMode.MARKDOWN, quote=True)

@app.on_message(
    filters.command("help"))
async def help(_, message: Message):
    await message.reply(HELP_MSG, parse_mode=ParseMode.MARKDOWN, quote=True)


@app.on_message(
    filters.command(
        "run",
        prefixes=["/", "!", "?", "."]))
async def run(app: Client, message: Message):
    message_text = message.text

    if len(message_text.split(" ")) < 2:
        return await message.reply(HELP_MSG, parse_mode=ParseMode.MARKDOWN, quote=True)

    language = message.command[1]

    stdin, message_text = extract_stdin_from_message(message_text)

    code = await get_code_from_message(message)

    try:
        response = code_compiler.execute(language=language, code=code, stdin=stdin)

        output_text = code_compiler.generate_output(response, code)
    except CompilerException as e:
        return await message.reply(e, parse_mode=ParseMode.MARKDOWN, quote=True)

    await message.reply(output_text, reply_markup=reply_markup(message.text.replace("/run ", "")), parse_mode=ParseMode.MARKDOWN, quote=True)

@app.on_inline_query()
async def answer(client, inline_query):
    if inline_query.query:
        message_text = inline_query.query

        language = message_text.split()[0]

        stdin, message_text = extract_stdin_from_message(message_text)

        code = " ".join(message_text.split(" ")[1:])

        reply_m = reply_markup(inline_query.query)

        try:
            response = code_compiler.execute(language=language, code=code, stdin=stdin)
    
            output_text = code_compiler.generate_output(response, code)
        except CompilerException as e:
            output_text = e
            reply_m = None
    
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Run Code >_",
                    description="Let's code together! 👻",
                    url="https://github.com/Suphiozturk8/CodeCompiler",
                    thumb_url="https://telegra.ph/file/de4444b6081a455edf9b3.png",
                    input_message_content=InputTextMessageContent(output_text),
                    reply_markup=reply_m
                )
            ],
            cache_time=1)


app.run()

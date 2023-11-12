
import os, requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

from utils import Compiler, CompilerException
from config import (
    NAME,
    API_ID,
    API_HASH,
    BOT_TOKEN,
    START_MSG,
    HELP_MSG)

app = Client(
    name=NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

code_compiler = Compiler()

@app.on_message(
    filters.command("start"))
async def start(_, message: Message):
    await message.reply(
        START_MSG,
        parse_mode=ParseMode.MARKDOWN,
        quote=True)

@app.on_message(
    filters.command("help"))
async def help(_, message: Message):
    await message.reply(
        HELP_MSG,
        parse_mode=ParseMode.MARKDOWN,
        quote=True)


@app.on_message(
    filters.command(
        "run",
        prefixes=["/", "!", "?", "."]))
async def run(_, message: Message):
    message_text = message.text

    if len(message_text.split(" ")) < 2:
        return await message.reply(
            HELP_MSG,
            parse_mode=ParseMode.MARKDOWN,
            quote=True)

    language = message.command[1]

    stdin = ""
    if "/stdin" in message_text:
        stdin = " ".join(message_text.split("/stdin ")[1:])
        message_text = message_text.replace("/stdin " + stdin, "")

    if message.reply_to_message:
        replied_message = message.reply_to_message

        if replied_message.text:
            code = replied_message.text
        elif replied_message.document:
            try:
                document = await replied_message.download()
                with open(document, "r") as file:
                    code = file.read()
                os.remove(document)
            except Exception as e:
                return await message.reply(
                    f"**Error reading document:**\n```{e}```",
                    parse_mode=ParseMode.MARKDOWN,
                    quote=True)
    else:
        code = " ".join(message_text.split(" ")[2:])

    try:
        response = code_compiler.execute(
            language=language,
            code=code,
            stdin=stdin)
    except CompilerException as re:
        return await message.reply(
            re,
            parse_mode=ParseMode.MARKDOWN,
            quote=True)

    output_text = code_compiler.generate_output(
        response,
        code)

    await message.reply(
        output_text,
        parse_mode=ParseMode.MARKDOWN,
        quote=True)


app.run()
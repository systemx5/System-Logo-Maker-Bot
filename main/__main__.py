from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from main.logo import generate_logo

START = """
**🔮 Hello There, You Can Use Me To Create Awesome Logos...**

➤ Click /help Or The Button Below To Know How To Use Me
"""

HELP = """
**🖼 How To Use Me ?**

**To Make Logo -** `/logo Your Name`
**To Make Square Logo - ** `/logosq Your Name`

**♻️ Example:** 
`/logo TechZBots`
`/logosq TechZBots`
"""

# Commands
@app.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply_text(
        START,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Help", callback_data="help_menu"),
                    InlineKeyboardButton(
                        text="Repo",
                        url="https://github.com/systemx5/System-Logo-Maker-Bot",
                    ),
                ]
            ]
        ),
    )


@app.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply_text(
        HELP,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data="start_menu")]]
        ),
    )


@app.on_message(
    filters.command("logo")
    & filters.incoming
    & filters.text
    & ~filters.forwarded
    & (filters.group | filters.private)
)
async def logo(bot, message):
    try:
        text = (" ".join(message.text.split(" ")[1:])).strip()

        if text == "":
            return await message.reply_text(HELP)

        x = await message.reply_text("`🔍 Generating Logo For You...`")
        logo = await generate_logo(text)
        print(logo)

        if "error" in logo:
            return await x.edit(
                f"`❌ Something Went Wrong...`\n\nReport This Error In @SystemBots_Support \n\n`{logo}`"
            )

        await x.edit("`🔄 Done Generated... Now Sending You`")

        await message.reply_photo(
            logo,
            caption="**🖼 Logo Generated By TechZApi**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Upload As File 📁", callback_data=f"flogo {logo}"
                        )
                    ]
                ]
            ),
        )
        await x.delete()
    except FloodWait:
        pass
    except Exception as e:
        try:
            await x.delete()
        except:
            pass
        return await message.reply_text(
            "`❌ Something Went Wrong...`\n\nReport This Error In @SystemBots_Support"
        )


# Square Logo
@app.on_message(
    filters.command("logosq")
    & filters.incoming
    & filters.text
    & ~filters.forwarded
    & (filters.group | filters.private)
)
async def logo(bot, message):
    try:
        text = (" ".join(message.text.split(" ")[1:])).strip()

        if text == "":
            return await message.reply_text(HELP)

        x = await message.reply_text("`🔍 Generating Logo For You...`")
        logo = await generate_logo(text, True)

        if "error" in logo:
            return await x.edit(
                f"`❌ Something Went Wrong...`\n\nReport This Error In @SystemBots_Support \n\n`{logo}`"
            )

        await x.edit("`🔄 Done Generated... Now Sending You`")

        await message.reply_photo(
            logo,
            caption="**🖼 Logo Generated By TechZApi**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Upload As File 📁", callback_data=f"flogo {logo}"
                        )
                    ]
                ]
            ),
        )
        await x.delete()
    except FloodWait:
        pass
    except Exception as e:
        try:
            await x.delete()
        except:
            pass
        return await message.reply_text(
            "`❌ Something Went Wrong...`\n\nReport This Error In @SystemBots_Support"
        )


# Callbacks
@app.on_callback_query(filters.regex("start_menu"))
async def start_menu(_, query):
    await query.answer()
    await query.message.edit(
        START,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Help", callback_data="help_menu"),
                    InlineKeyboardButton(
                        text="Repo",
                        url="https://github.com/systemx5/System-Logo-Maker-Bot",
                    ),
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("help_menu"))
async def help_menu(_, query):
    await query.answer()
    await query.message.edit(
        HELP,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Back", callback_data="start_menu")]]
        ),
    )


@app.on_callback_query(filters.regex("flogo"))
async def logo_doc(_, query):
    await query.answer()
    try:
        x = await query.message.reply_text("`🔄 Sending You The Logo As File`")
        await query.message.edit_reply_markup(reply_markup=None)
        logo = query.data.replace("flogo", "").strip()

        await query.message.reply_document(
            logo, caption="**🖼 Logo Generated By TechZApi**"
        )
    except FloodWait:
        pass
    except Exception as e:
        try:
            return await x.edit(
                f"`❌ Something Went Wrong...`\n\nReport This Error In @SystemBots_Support \n\n`{str(e)}`"
            )
        except:
            return

    return await x.delete()


if __name__ == "__main__":
    print("==================================")
    print("[INFO]: LOGO MAKER BOT STARTED BOT SUCCESSFULLY")
    print("==========JOIN @SYSTEMLOGO_BOT=========")

    idle()
    print("[INFO]: LOGO MAKER BOT STOPPED")

from database import add_user, get_total_users
from database import add_report, get_reports
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from matching import (
    find_match,
    active_chats,
    next_chat,
)

TOKEN = "8742169817:AAHAqOKHPo5DI59uiOyvocH2-sfT3kC2tVo"
ADMIN_ID = 1313242919


async def start(update, context):
    user_id = update.effective_user.id

    add_user(user_id)   # save user

    partner = find_match(user_id)

    if partner:
        await context.bot.send_message(
            user_id,
            "✅ Connected to a stranger!"
        )

        await context.bot.send_message(
            partner,
            "✅ Connected to a stranger!"
        )
    else:
        await update.message.reply_text(
            "⏳ Waiting for a partner..."
        )


async def next_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    partner = next_chat(user_id)

    if partner:
        await context.bot.send_message(
            partner,
            "❌ Stranger left the chat."
        )

    new_partner = find_match(user_id)

    if new_partner:
        await context.bot.send_message(
            user_id,
            "✅ New partner found!"
        )

        await context.bot.send_message(
            new_partner,
            "✅ New partner found!"
        )
    else:
        await update.message.reply_text(
            "⏳ Waiting for a new partner..."
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    partner = next_chat(user_id)

    if partner:
        await context.bot.send_message(
            partner,
            "❌ Stranger disconnected."
        )

    await update.message.reply_text(
        "Chat ended."
    )


async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in active_chats:
        return

    partner = active_chats[user_id]

    await context.bot.send_message(
        partner,
        update.message.text
    )
async def users(update, context):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text(
            "You are not admin."
        )
        return

    total = get_total_users()

    await update.message.reply_text(
        f"📊 Total Users: {total}"
    ) 
async def report(update, context):
    user_id = update.effective_user.id

    if user_id not in active_chats:
        await update.message.reply_text(
            "No active chat."
        )
        return

    partner = active_chats[user_id]

    add_report(partner)

    reports = get_reports(partner)

    await update.message.reply_text(
        "✅ User reported."
    )

    if reports >= 5:
        await context.bot.send_message(
            partner,
            "🚫 Your account has been banned."
        )       


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("next", next_cmd))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("users", users))
app.add_handler(CommandHandler("report", report))
app.add_handler(MessageHandler(filters.TEXT, relay))

app.run_polling()
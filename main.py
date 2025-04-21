from telegram import Update, Message
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# Enable logging
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))  # <- Replace with your Telegram user ID

# Store message references: forwarded_msg_id -> original_user_id
forwarded_map = {}

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message
    user_id = user_msg.from_user.id
    username = user_msg.from_user.username or "No username"

    if user_id == OWNER_ID:
        return
    
    await user_msg.reply_text("Thank you for your message. Please expect a reply soon")

    # Forward message and send username to owner
    forwarded = await context.bot.forward_message(
        chat_id=OWNER_ID,
        from_chat_id=user_id,
        message_id=user_msg.message_id
    )
    
    # await context.bot.send_message(
    #     chat_id=OWNER_ID,
    #     text=f"Message from: @{username} (ID: {user_id})"
    # )

    # Save mapping: owner will reply to this forwarded message
    forwarded_map[forwarded.message_id] = user_id


app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handle all messages
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, forward_message))


print("Bot is running...")
app.run_polling()

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "توکن_جدید_بزار"
ADMIN_ID = 6452958957

# ================= منوی اصلی =================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 خرید سرور VIP", callback_data="vip")],
        [InlineKeyboardButton("🔴 سرور استارلینک", callback_data="starlink")],
        [InlineKeyboardButton("🔴 پشتیبانی", callback_data="support")]
    ])

# ================= استارت =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """🔥 به فروشگاه VIP خوش اومدی

👇 یکی رو انتخاب کن:"""

    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu())

# ================= VIP =================
async def vip_menu(query):
    buttons = [
        [InlineKeyboardButton("🔴 1GB - 250", callback_data="vip_1"),
         InlineKeyboardButton("🔴 2GB - 500", callback_data="vip_2")],
        [InlineKeyboardButton("🔴 3GB - 750", callback_data="vip_3"),
         InlineKeyboardButton("🔴 4GB - 900", callback_data="vip_4")],
        [InlineKeyboardButton("🔴 5GB - 1200", callback_data="vip_5"),
         InlineKeyboardButton("🔴 10GB - 1900", callback_data="vip_10")],
        [InlineKeyboardButton("⬅️ برگشت", callback_data="back")]
    ]

    await query.edit_message_text("💎 لیست VIP:", reply_markup=InlineKeyboardMarkup(buttons))

# ================= STARLINK =================
async def star_menu(query):
    buttons = [
        [InlineKeyboardButton("🔴 1GB - 550", callback_data="s_1"),
         InlineKeyboardButton("🔴 2GB - 1100", callback_data="s_2")],
        [InlineKeyboardButton("🔴 3GB - 1650", callback_data="s_3"),
         InlineKeyboardButton("🔴 4GB - 2100", callback_data="s_4")],
        [InlineKeyboardButton("🔴 5GB - 2650", callback_data="s_5"),
         InlineKeyboardButton("🔴 10GB - 5500", callback_data="s_10")],
        [InlineKeyboardButton("🔴 20GB - 13000", callback_data="s_20")],
        [InlineKeyboardButton("⬅️ برگشت", callback_data="back")]
    ]

    await query.edit_message_text("🛰 لیست استارلینک:", reply_markup=InlineKeyboardMarkup(buttons))

# ================= هندل =================
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "vip":
        await vip_menu(query)

    elif data == "starlink":
        await star_menu(query)

    elif data == "support":
        await query.edit_message_text(
            "📞 پشتیبانی:\n@Mohamadamin1243\n@USAF35J",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ برگشت", callback_data="back")]
            ])
        )

    elif data == "back":
        await start(update, context)

    # 👇 وقتی ادمین تایید کرد
    elif data.startswith("confirm"):
        user_id = int(data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ سفارش شما تایید شد 🚀"
        )

        # 👇 برگشت به اول
        await context.bot.send_message(
            chat_id=user_id,
            text="👇 دوباره انتخاب کن:",
            reply_markup=main_menu()
        )

        await query.edit_message_text("✔ تایید شد")

# ================= اجرا =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handler))

print("RUNNING...")
app.run_polling()

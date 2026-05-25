# auth_bot/bot.py — MusicLSPauth — бот оплати і ключів
import os
import sys
import secrets
import string
import logging
import sqlite3
import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'main_bot'))
import database as db
from config import AUTH_BOT_TOKEN, ADMIN_ID, PLANS, AUTHOR, BOT_NAME

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_key() -> str:
    chars = string.ascii_uppercase + string.digits
    return "LSP-" + "".join(secrets.choice(chars) for _ in range(12))


# ── /start ────────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 7 днів — $0.50", callback_data="buy:week")],
        [InlineKeyboardButton("💎 30 днів — $2.00", callback_data="buy:month")],
        [InlineKeyboardButton("🔑 У мене є ключ → @MusicLSP_bot", url="https://t.me/MusicLSP_bot")],
    ]
    await update.message.reply_text(
        f"💳 <b>MusicLSP — Оплата</b>\n\n"
        f"Обери тариф і отримай ключ активації для @MusicLSP_bot\n\n"
        f"• 7 днів — <b>$0.50</b>\n"
        f"• 30 днів — <b>$2.00</b>\n\n"
        f"<i>Після оплати отримаєш ключ — введи його в головному боті</i>\n\n"
        f"👤 Автор: {AUTHOR}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id

    if data.startswith("buy:"):
        plan = data[4:]
        plan_info = PLANS.get(plan)
        if not plan_info:
            return

        # Інструкції оплати
        keyboard = [
            [InlineKeyboardButton("✅ Я оплатив", callback_data=f"paid:{plan}:{uid}")],
            [InlineKeyboardButton("◀️ Назад", callback_data="back")],
        ]
        await query.message.edit_text(
            f"💳 <b>Оплата: {plan_info['label']}</b>\n\n"
            f"1. Відправ <b>${plan_info['price']}</b> на:\n"
            f"   💳 <code>НОМЕР_КАРТКИ_АБО_КРИПТА</code>\n\n"
            f"2. У коментарі вкажи свій ID: <code>{uid}</code>\n\n"
            f"3. Натисни «Я оплатив» — адмін перевірить і вишле ключ\n\n"
            f"⚡️ Зазвичай до 15 хвилин",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    elif data.startswith("paid:"):
        _, plan, payer_id = data.split(":")
        plan_info = PLANS.get(plan, {})

        # Сповіщаємо адміна
        keyboard = [
            [InlineKeyboardButton(
                f"✅ Підтвердити і надіслати ключ",
                callback_data=f"confirm:{plan}:{payer_id}"
            )],
            [InlineKeyboardButton("❌ Відхилити", callback_data=f"reject:{payer_id}")],
        ]
        try:
            user = await query.get_bot().get_chat(int(payer_id))
            username = f"@{user.username}" if user.username else str(payer_id)
        except Exception:
            username = str(payer_id)

        await query.get_bot().send_message(
            ADMIN_ID,
            f"💰 <b>Новий платіж!</b>\n\n"
            f"👤 Юзер: {username} (<code>{payer_id}</code>)\n"
            f"💎 Тариф: {plan_info.get('label', plan)}\n"
            f"💵 Сума: ${plan_info.get('price', '?')}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

        await query.message.edit_text(
            "⏳ <b>Запит відправлено!</b>\n\n"
            "Адмін перевірить оплату і надішле ключ.\n"
            "Зазвичай до 15 хвилин ⚡️",
            parse_mode="HTML"
        )

    elif data.startswith("confirm:"):
        _, plan, payer_id = data.split(":")
        plan_info = PLANS.get(plan, {})
        days = plan_info.get("days", 7)

        # Генеруємо і зберігаємо ключ
        key = generate_key()
        db.add_key(key, days, plan)

        # Відправляємо ключ юзеру
        try:
            await query.get_bot().send_message(
                int(payer_id),
                f"🎉 <b>Оплату підтверджено!</b>\n\n"
                f"Твій ключ активації:\n<code>{key}</code>\n\n"
                f"1. Перейди в @MusicLSP_bot\n"
                f"2. Натисни «💎 Підписка» → «🔑 Ввести ключ»\n"
                f"3. Встав ключ\n\n"
                f"Приємного прослуховування! 🎵",
                parse_mode="HTML"
            )
            await query.message.edit_text(
                f"✅ Ключ надіслано юзеру {payer_id}:\n<code>{key}</code>",
                parse_mode="HTML"
            )
        except Exception as e:
            await query.message.edit_text(f"❌ Помилка відправки: {e}\nКлюч: <code>{key}</code>", parse_mode="HTML")

    elif data.startswith("reject:"):
        payer_id = data[7:]
        try:
            await query.get_bot().send_message(
                int(payer_id),
                "❌ На жаль, оплату не підтверджено.\n"
                "Зв'яжись з підтримкою якщо вважаєш це помилкою."
            )
        except Exception:
            pass
        await query.message.edit_text("❌ Платіж відхилено.")

    elif data == "back":
        await cmd_start_msg(query.message)


async def cmd_start_msg(message):
    keyboard = [
        [InlineKeyboardButton("💎 7 днів — $0.50", callback_data="buy:week")],
        [InlineKeyboardButton("💎 30 днів — $2.00", callback_data="buy:month")],
    ]
    await message.edit_text(
        f"💳 <b>MusicLSP — Оплата</b>\n\nОбери тариф:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


# ── Адмін: ручна видача ключа ─────────────────────────────────────────────────
async def cmd_give(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    # /give USER_ID ДНІВ
    if len(ctx.args) != 2:
        await update.message.reply_text("Формат: /give USER_ID ДНІВ")
        return
    target_id, days = int(ctx.args[0]), int(ctx.args[1])
    key = generate_key()
    plan = "week" if days <= 7 else "month"
    db.add_key(key, days, plan)

    try:
        await ctx.bot.send_message(
            target_id,
            f"🎁 <b>Ключ від адміна:</b>\n<code>{key}</code>\n\nДнів: {days}",
            parse_mode="HTML"
        )
        await update.message.reply_text(f"✅ Ключ надіслано {target_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}\nКлюч: <code>{key}</code>", parse_mode="HTML")


def main():
    db.init_db()
    app = Application.builder().token(AUTH_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("give",  cmd_give))
    app.add_handler(CallbackQueryHandler(on_callback))

    logger.info("✅ MusicLSPauth бот запущено!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
  

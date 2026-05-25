# bot.py — MusicLSP головний бот
import os
import logging
import asyncio
import tempfile
import datetime

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

import database as db
import music as m
from languages import t, LANGUAGES
from config import (
    MAIN_BOT_TOKEN, ADMIN_ID, MAX_FILE_SIZE_MB,
    QUALITIES, DEFAULT_QUALITY, AUTHOR, BOT_NAME,
    TRIAL_DAYS, REFERRAL_DAILY_LIMIT, PLANS
)

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Хелпери ───────────────────────────────────────────────────────────────────
def lang(uid): return db.get_lang(uid)

def main_menu_keyboard(uid: int):
    l = lang(uid)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_search", l),       callback_data="menu:search"),
         InlineKeyboardButton(t("btn_top100", l),       callback_data="menu:top100")],
        [InlineKeyboardButton(t("btn_library", l),      callback_data="menu:library"),
         InlineKeyboardButton(t("btn_profile", l),      callback_data="menu:profile")],
        [InlineKeyboardButton(t("btn_subscription", l), callback_data="menu:subscription"),
         InlineKeyboardButton(t("btn_referral", l),     callback_data="menu:referral")],
        [InlineKeyboardButton(t("btn_settings", l),     callback_data="menu:settings")],
    ])

def check_access(uid: int) -> bool:
    return db.has_access(uid)

# ── /start ────────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or ""

    # Перевіряємо реферальне посилання
    ref_id = None
    if ctx.args:
        try:
            ref_id = int(ctx.args[0])
            if ref_id == uid:
                ref_id = None
        except ValueError:
            pass

    is_new = db.get_user(uid) is None
    db.create_user(uid, username, referred_by=ref_id)

    # Нараховуємо реферальний бонус
    if is_new and ref_id and db.get_user(ref_id):
        if db.can_add_referral(ref_id, REFERRAL_DAILY_LIMIT):
            db.add_referral(ref_id, uid)
            try:
                await ctx.bot.send_message(
                    ref_id,
                    f"🎁 По твоєму запрошенню зареєструвався новий користувач!\n+1 день до підписки ✅"
                )
            except Exception:
                pass

    # Якщо мова вже встановлена — одразу в меню
    user = db.get_user(uid)
    if user and user["lang"] and user["lang"] != "uk":
        await _show_welcome(update, uid)
        return

    # Вибір мови
    keyboard = []
    row = []
    for code, name in LANGUAGES.items():
        row.append(InlineKeyboardButton(name, callback_data=f"lang:{code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await update.message.reply_text(
        "🌍 <b>Choose your language / Оберіть мову</b>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


async def _show_welcome(update_or_msg, uid: int):
    l = lang(uid)
    text = t("welcome", l, bot_name=BOT_NAME, trial=TRIAL_DAYS, author=AUTHOR)
    kb = main_menu_keyboard(uid)

    if hasattr(update_or_msg, "message") and update_or_msg.message:
        await update_or_msg.message.reply_text(text, reply_markup=kb, parse_mode="HTML")
    else:
        await update_or_msg.reply_text(text, reply_markup=kb, parse_mode="HTML")


# ── Callbacks ─────────────────────────────────────────────────────────────────
async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data
    l = lang(uid)

    # ── Вибір мови ─────────────────────────────────────────────────────────────
    if data.startswith("lang:"):
        code = data[5:]
        db.set_lang(uid, code)
        await query.message.delete()
        await _show_welcome(query.message, uid)

    # ── Головне меню ───────────────────────────────────────────────────────────
    elif data == "menu:home":
        await query.message.edit_text(
            t("main_menu", l),
            reply_markup=main_menu_keyboard(uid),
            parse_mode="HTML"
        )

    elif data == "menu:search":
        db.set_state(uid, "searching")
        await query.message.edit_text(
            t("search_prompt", l),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")
            ]]),
            parse_mode="HTML"
        )

    elif data == "menu:top100":
        await _show_top100(query.message, uid)

    elif data == "menu:library":
        await _show_library(query.message, uid)

    elif data == "menu:profile":
        await _show_profile(query.message, uid)

    elif data == "menu:subscription":
        await _show_subscription(query.message, uid)

    elif data == "menu:referral":
        await _show_referral(query.message, uid)

    elif data == "menu:settings":
        await _show_settings(query.message, uid)

    # ── Ключ активації ─────────────────────────────────────────────────────────
    elif data == "sub:enter_key":
        db.set_state(uid, "entering_key")
        await query.message.reply_text(t("enter_key_prompt", l), parse_mode="HTML")

    # ── Промокод ───────────────────────────────────────────────────────────────
    elif data == "sub:promo":
        db.set_state(uid, "entering_promo")
        promo_text = {"uk": "🎟 Введи промокод:", "ru": "🎟 Введи промокод:", "en": "🎟 Enter promo code:"}
        await query.message.reply_text(promo_text.get(l, promo_text["en"]))

    # ── Завантаження по кешу ────────────────────────────────────────────────────
    elif data.startswith("dl|"):
        if not check_access(uid):
            await query.message.reply_text(t("no_access", l), parse_mode="HTML")
            return
        parts = data.split("|", 2)
        idx = int(parts[1])
        cache_key = parts[2]
        cache = ctx.application.bot_data.get("cache", {})
        tracks = cache.get(cache_key, [])
        if not tracks or idx >= len(tracks):
            await query.message.reply_text("❌ Результат застарів. Зроби новий пошук.")
            return
        track = tracks[idx]
        await _download_and_send(query.message, track["url"], track["title"], track.get("channel", ""), uid, ctx)

    # ── Завантаження по URL ─────────────────────────────────────────────────────
    elif data.startswith("dlurl|"):
        if not check_access(uid):
            await query.message.reply_text(t("no_access", l), parse_mode="HTML")
            return
        parts = data.split("|", 2)
        url = parts[1]
        title = parts[2] if len(parts) > 2 else "трек"
        await _download_and_send(query.message, url, title, "", uid, ctx)

    # ── Всі пісні артиста ─────────────────────────────────────────────────────
    elif data.startswith("artist|"):
        artist = data[7:]
        await _show_artist(query.message, artist, uid, ctx)

    # ── Завантажити 20 пісень артиста ─────────────────────────────────────────
    elif data.startswith("dl20|"):
        if not check_access(uid):
            await query.message.reply_text(t("no_access", l), parse_mode="HTML")
            return
        artist = data[5:]
        await _download_batch(query.message, artist, uid, ctx)

    # ── Бібліотека: видалити ──────────────────────────────────────────────────
    elif data.startswith("lib:del|"):
        lib_id = int(data[8:])
        db.remove_from_library(uid, lib_id)
        await _show_library(query.message, uid)

    # ── Налаштування якості ───────────────────────────────────────────────────
    elif data.startswith("quality|"):
        quality = data[8:]
        ctx.application.bot_data.setdefault("quality", {})[uid] = quality
        await query.answer(f"✅ Якість: {quality} kbps", show_alert=True)

    # ── Додати до бібліотеки ───────────────────────────────────────────────────
    elif data.startswith("addlib|"):
        parts = data.split("|", 3)
        url, title, artist = parts[1], parts[2], parts[3] if len(parts) > 3 else ""
        added = db.add_to_library(uid, title, artist, url)
        msg = "✅ Додано до бібліотеки!" if added else "ℹ️ Вже є в бібліотеці."
        await query.answer(msg, show_alert=True)

    # ── Топ 100 сторінка ──────────────────────────────────────────────────────
    elif data.startswith("top100page|"):
        page = int(data[11:])
        cache = ctx.application.bot_data.get("top100", [])
        await _show_top100_page(query.message, uid, cache, page, ctx, edit=True)


# ── Повідомлення ──────────────────────────────────────────────────────────────
async def on_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.strip()
    l = lang(uid)
    state = db.get_state(uid)

    if not db.get_user(uid):
        db.create_user(uid, update.effective_user.username or "")

    # ── Ввід ключа ────────────────────────────────────────────────────────────
    if state == "entering_key":
        db.set_state(uid, "")
        days = db.use_key(text, uid)
        if days:
            db.extend_subscription(uid, days)
            await update.message.reply_text(
                t("key_success", l, days=days), parse_mode="HTML"
            )
        else:
            await update.message.reply_text(t("key_invalid", l), parse_mode="HTML")
        return

    # ── Ввід промокоду ────────────────────────────────────────────────────────
    if state == "entering_promo":
        db.set_state(uid, "")
        discount = db.use_promo(text.upper())
        if discount:
            await update.message.reply_text(
                f"✅ Промокод активовано! Знижка <b>{discount}%</b> на наступну оплату.\n"
                f"Покажи цей код при оплаті в @MusicLSPauth_bot",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text("❌ Невірний або вичерпаний промокод.")
        return

    # ── Адмін: ввід даних ─────────────────────────────────────────────────────
    if uid == ADMIN_ID and state.startswith("admin:"):
        await _handle_admin_input(update, ctx, state, text)
        return

    # ── Пошук ─────────────────────────────────────────────────────────────────
    if state == "searching" or True:  # Завжди шукаємо якщо не інший стан
        db.set_state(uid, "")
        if not check_access(uid):
            await update.message.reply_text(t("no_access", l), parse_mode="HTML")
            return
        await _do_search(update, text, uid, ctx)


# ── Пошук ─────────────────────────────────────────────────────────────────────
async def _do_search(update: Update, query: str, uid: int, ctx: ContextTypes.DEFAULT_TYPE):
    l = lang(uid)
    msg = await update.message.reply_text(t("searching", l, query=query), parse_mode="HTML")

    tracks = await m.search_all_async(query, limit=10)

    if not tracks:
        await msg.edit_text(t("no_results", l))
        return

    cache_key = f"s_{uid}_{msg.message_id}"
    ctx.application.bot_data.setdefault("cache", {})[cache_key] = tracks

    keyboard = []
    for i, track in enumerate(tracks):
        src_icon = "🎵" if track.get("source") == "youtube" else "☁️"
        label = f"{src_icon} {track['title'][:42]} ({track['duration']})"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"dl|{i}|{cache_key}")])

    artist = tracks[0]["channel"]
    keyboard.append([
        InlineKeyboardButton(t("btn_all_songs", l),   callback_data=f"artist|{artist}"),
        InlineKeyboardButton(t("btn_download_20", l), callback_data=f"dl20|{artist}"),
    ])
    keyboard.append([InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")])

    await msg.edit_text(
        f"🎶 <b>{query}</b> — {len(tracks)} результатів\n\nОбери пісню 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


# ── Всі пісні артиста ─────────────────────────────────────────────────────────
async def _show_artist(message, artist: str, uid: int, ctx: ContextTypes.DEFAULT_TYPE):
    l = lang(uid)
    msg = await message.reply_text(f"🔍 Шукаю пісні: <b>{artist}</b>…", parse_mode="HTML")
    tracks = await m.get_artist_songs_async(artist, limit=50)

    if not tracks:
        await msg.edit_text(t("no_results", l))
        return

    keyboard = []
    for track in tracks:
        label = f"🎵 {track['title'][:42]} ({track['duration']})"
        keyboard.append([InlineKeyboardButton(
            label, callback_data=f"dlurl|{track['url']}|{track['title'][:30]}"
        )])

    keyboard.append([InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")])

    chunk_size = 40
    for i, start in enumerate(range(0, len(keyboard), chunk_size)):
        chunk = keyboard[start:start + chunk_size]
        end = min(start + chunk_size, len(tracks))
        if i == 0:
            await msg.edit_text(
                f"🎤 <b>{artist}</b> — {len(tracks)} пісень:",
                reply_markup=InlineKeyboardMarkup(chunk),
                parse_mode="HTML"
            )
        else:
            await message.reply_text(
                f"🎤 <b>{artist}</b> ({start+1}–{end}):",
                reply_markup=InlineKeyboardMarkup(chunk),
                parse_mode="HTML"
            )


# ── Завантажити 20 пісень ──────────────────────────────────────────────────────
async def _download_batch(message, artist: str, uid: int, ctx: ContextTypes.DEFAULT_TYPE):
    l = lang(uid)
    msg = await message.reply_text(
        f"⬇️ Завантажую 20 пісень <b>{artist}</b>…\n<i>Це займе кілька хвилин</i>",
        parse_mode="HTML"
    )
    tracks = await m.get_artist_songs_async(artist, limit=20)

    if not tracks:
        await msg.edit_text(t("no_results", l))
        return

    success = 0
    for i, track in enumerate(tracks):
        await msg.edit_text(
            f"⬇️ Завантажую {i+1}/20: <b>{track['title'][:40]}</b>…",
            parse_mode="HTML"
        )
        with tempfile.TemporaryDirectory() as tmp:
            quality = ctx.application.bot_data.get("quality", {}).get(uid, DEFAULT_QUALITY)
            try:
                path = await m.download_audio_async(track["url"], tmp, quality)
                if path and os.path.exists(path):
                    size_mb = os.path.getsize(path) / (1024 * 1024)
                    if size_mb <= MAX_FILE_SIZE_MB:
                        with open(path, "rb") as f:
                            await message.reply_audio(
                                audio=f,
                                title=track["title"][:64],
                                performer=track["channel"][:64],
                                filename=f"{track['title'][:50]}.mp3",
                            )
                        db.add_to_history(uid, track["title"], track["channel"])
                        success += 1
            except Exception as e:
                logger.error(f"Batch download error: {e}")
                continue

    await msg.edit_text(f"✅ Завантажено {success} з {len(tracks)} пісень!")


# ── Топ 100 ───────────────────────────────────────────────────────────────────
async def _show_top100(message, uid: int):
    l = lang(uid)
    msg = await message.reply_text("📊 Завантажую Топ 100…")
    tracks = await m.get_top_100_async()
    # Кешуємо
    message._application = None  # скидаємо щоб не було circular ref
    ctx_key = "top100"
    # Зберігаємо в bot_data через message
    await _show_top100_page(msg, uid, tracks, 0, None, edit=True, save_tracks=tracks)


async def _show_top100_page(message, uid: int, tracks: list, page: int, ctx, edit=False, save_tracks=None):
    l = lang(uid)
    per_page = 20
    start = page * per_page
    end = min(start + per_page, len(tracks))
    page_tracks = tracks[start:end]

    keyboard = []
    for i, track in enumerate(page_tracks):
        rank = track.get("rank", start + i + 1)
        label = f"#{rank} {track['title'][:40]}"
        keyboard.append([InlineKeyboardButton(
            label, callback_data=f"dlurl|{track['url']}|{track['title'][:30]}"
        )])

    # Навігація
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("◀️ Назад", callback_data=f"top100page|{page-1}"))
    if end < len(tracks):
        nav.append(InlineKeyboardButton("Далі ▶️", callback_data=f"top100page|{page+1}"))
    if nav:
        keyboard.append(nav)
    keyboard.append([InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")])

    text = f"📊 <b>Топ 100</b> — пісні {start+1}–{end}:"
    markup = InlineKeyboardMarkup(keyboard)

    if edit:
        await message.edit_text(text, reply_markup=markup, parse_mode="HTML")
    else:
        await message.reply_text(text, reply_markup=markup, parse_mode="HTML")


# ── Профіль ───────────────────────────────────────────────────────────────────
async def _show_profile(message, uid: int):
    l = lang(uid)
    user = db.get_user(uid)
    stats = db.get_user_stats(uid)
    ref_stats = db.get_referral_stats(uid)
    status, expires = db.get_sub_status(uid)

    status_text = t(f"status_{status}", l)
    joined = user["joined_at"][:10] if user["joined_at"] else "—"

    text = (
        f"👤 <b>Профіль</b>\n\n"
        f"🆔 ID: <code>{uid}</code>\n"
        f"📅 В боті з: {joined}\n"
        f"💎 Підписка: {status_text} (до {expires})\n\n"
        f"📊 <b>Статистика:</b>\n"
        f"• Скачано пісень: {stats['downloads']}\n"
        f"• В бібліотеці: {stats['library']}\n"
        f"• Рефералів: {ref_stats['count']}\n"
        f"• Зароблено днів: {ref_stats['days']}"
    )

    keyboard = [[InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")]]
    await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")


# ── Підписка ──────────────────────────────────────────────────────────────────
async def _show_subscription(message, uid: int):
    l = lang(uid)
    status, expires = db.get_sub_status(uid)
    status_text = t(f"status_{status}", l)
    text = t("subscription_info", l, status=status_text, expires=expires)

    keyboard = [
        [InlineKeyboardButton(t("btn_pay", l), url="https://t.me/MusicLSPauth_bot")],
        [InlineKeyboardButton(t("btn_enter_key", l), callback_data="sub:enter_key")],
        [InlineKeyboardButton("🎟 Промокод", callback_data="sub:promo")],
        [InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")],
    ]
    await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")


# ── Реферальна ────────────────────────────────────────────────────────────────
async def _show_referral(message, uid: int):
    l = lang(uid)
    stats = db.get_referral_stats(uid)
    bot_info = await message.get_bot().get_me()
    link = f"https://t.me/{bot_info.username}?start={uid}"

    text = t("referral_info", l, count=stats["count"], days=stats["days"], link=link)
    keyboard = [[InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")]]
    await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")


# ── Бібліотека ────────────────────────────────────────────────────────────────
async def _show_library(message, uid: int):
    l = lang(uid)
    songs = db.get_library(uid)

    if not songs:
        text = "📚 <b>Моя бібліотека</b>\n\nПоки порожньо. Шукай музику і додавай!"
        keyboard = [[InlineKeyboardButton(t("btn_back", l), callback_data="menu:home")]]
        await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        return

    keyboard = []
    for song in songs[:40]:
   

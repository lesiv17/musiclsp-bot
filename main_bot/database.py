# database.py
import sqlite3
import datetime
from config import DB_PATH, TRIAL_DAYS


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY,
            username      TEXT,
            lang          TEXT DEFAULT 'uk',
            joined_at     TEXT,
            trial_expires TEXT,
            sub_expires   TEXT,
            referred_by   INTEGER,
            ref_days      INTEGER DEFAULT 0,
            state         TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS keys (
            key       TEXT PRIMARY KEY,
            days      INTEGER,
            used_by   INTEGER DEFAULT NULL,
            used_at   TEXT DEFAULT NULL,
            plan      TEXT
        );

        CREATE TABLE IF NOT EXISTS referrals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            inviter_id  INTEGER,
            invitee_id  INTEGER,
            created_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS daily_referrals (
            user_id    INTEGER,
            date       TEXT,
            count      INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, date)
        );

        CREATE TABLE IF NOT EXISTS library (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            title      TEXT,
            artist     TEXT,
            url        TEXT,
            added_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS history (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            title      TEXT,
            artist     TEXT,
            played_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS promocodes (
            code       TEXT PRIMARY KEY,
            discount   INTEGER,
            uses_left  INTEGER,
            created_at TEXT
        );
        """)


# ── Користувачі ───────────────────────────────────────────────────────────────
def get_user(user_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()


def create_user(user_id: int, username: str, referred_by: int = None):
    now = datetime.datetime.utcnow().isoformat()
    trial_exp = (datetime.datetime.utcnow() + datetime.timedelta(days=TRIAL_DAYS)).isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (id, username, joined_at, trial_expires, referred_by) VALUES (?,?,?,?,?)",
            (user_id, username, now, trial_exp, referred_by)
        )


def set_lang(user_id: int, lang: str):
    with get_conn() as conn:
        conn.execute("UPDATE users SET lang=? WHERE id=?", (lang, user_id))


def get_lang(user_id: int) -> str:
    user = get_user(user_id)
    return user["lang"] if user else "en"


def set_state(user_id: int, state: str):
    with get_conn() as conn:
        conn.execute("UPDATE users SET state=? WHERE id=?", (state, user_id))


def get_state(user_id: int) -> str:
    user = get_user(user_id)
    return user["state"] if user else ""


def has_access(user_id: int) -> bool:
    user = get_user(user_id)
    if not user:
        return False
    now = datetime.datetime.utcnow()
    # Перевіряємо підписку
    if user["sub_expires"]:
        if datetime.datetime.fromisoformat(user["sub_expires"]) > now:
            return True
    # Перевіряємо пробний період
    if user["trial_expires"]:
        if datetime.datetime.fromisoformat(user["trial_expires"]) > now:
            return True
    return False


def get_sub_status(user_id: int) -> tuple[str, str]:
    """Повертає (статус, дата_закінчення)."""
    user = get_user(user_id)
    now = datetime.datetime.utcnow()
    if user["sub_expires"]:
        exp = datetime.datetime.fromisoformat(user["sub_expires"])
        if exp > now:
            return "active", exp.strftime("%d.%m.%Y")
    if user["trial_expires"]:
        exp = datetime.datetime.fromisoformat(user["trial_expires"])
        if exp > now:
            return "trial", exp.strftime("%d.%m.%Y")
    return "expired", "—"


def extend_subscription(user_id: int, days: int):
    user = get_user(user_id)
    now = datetime.datetime.utcnow()
    if user["sub_expires"]:
        base = max(datetime.datetime.fromisoformat(user["sub_expires"]), now)
    else:
        base = now
    new_exp = (base + datetime.timedelta(days=days)).isoformat()
    with get_conn() as conn:
        conn.execute("UPDATE users SET sub_expires=? WHERE id=?", (new_exp, user_id))


def get_all_users():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users").fetchall()


# ── Ключі ─────────────────────────────────────────────────────────────────────
def add_key(key: str, days: int, plan: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO keys (key, days, plan) VALUES (?,?,?)",
            (key, days, plan)
        )


def use_key(key: str, user_id: int) -> int | None:
    """Активує ключ. Повертає кількість днів або None якщо ключ невалідний."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM keys WHERE key=? AND used_by IS NULL", (key,)
        ).fetchone()
        if not row:
            return None
        now = datetime.datetime.utcnow().isoformat()
        conn.execute(
            "UPDATE keys SET used_by=?, used_at=? WHERE key=?",
            (user_id, now, key)
        )
        return row["days"]


# ── Реферали ──────────────────────────────────────────────────────────────────
def can_add_referral(inviter_id: int, limit: int = 3) -> bool:
    today = datetime.date.today().isoformat()
    with get_conn() as conn:
        row = conn.execute(
            "SELECT count FROM daily_referrals WHERE user_id=? AND date=?",
            (inviter_id, today)
        ).fetchone()
        return (row["count"] if row else 0) < limit


def add_referral(inviter_id: int, invitee_id: int):
    now = datetime.datetime.utcnow().isoformat()
    today = datetime.date.today().isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO referrals (inviter_id, invitee_id, created_at) VALUES (?,?,?)",
            (inviter_id, invitee_id, now)
        )
        conn.execute("""
            INSERT INTO daily_referrals (user_id, date, count) VALUES (?,?,1)
            ON CONFLICT(user_id, date) DO UPDATE SET count=count+1
        """, (inviter_id, today))
        conn.execute(
            "UPDATE users SET ref_days=ref_days+1 WHERE id=?", (inviter_id,)
        )
    extend_subscription(inviter_id, 1)


def get_referral_stats(user_id: int) -> dict:
    with get_conn() as conn:
        count = conn.execute(
            "SELECT COUNT(*) as c FROM referrals WHERE inviter_id=?", (user_id,)
        ).fetchone()["c"]
        user = get_user(user_id)
        days = user["ref_days"] if user else 0
    return {"count": count, "days": days}


# ── Бібліотека ────────────────────────────────────────────────────────────────
def add_to_library(user_id: int, title: str, artist: str, url: str):
    now = datetime.datetime.utcnow().isoformat()
    with get_conn() as conn:
        # Перевіряємо чи вже є
        exists = conn.execute(
            "SELECT id FROM library WHERE user_id=? AND url=?", (user_id, url)
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO library (user_id, title, artist, url, added_at) VALUES (?,?,?,?,?)",
                (user_id, title, artist, url, now)
            )
            return True
    return False


def get_library(user_id: int) -> list:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM library WHERE user_id=? ORDER BY added_at DESC",
            (user_id,)
        ).fetchall()


def remove_from_library(user_id: int, lib_id: int):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM library WHERE id=? AND user_id=?", (lib_id, user_id)
        )


# ── Історія ───────────────────────────────────────────────────────────────────
def add_to_history(user_id: int, title: str, artist: str):
    now = datetime.datetime.utcnow().isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO history (user_id, title, artist, played_at) VALUES (?,?,?,?)",
            (user_id, title, artist, now)
        )


def get_history(user_id: int, limit: int = 20) -> list:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM history WHERE user_id=? ORDER BY played_at DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()


def get_user_stats(user_id: int) -> dict:
    with get_conn() as conn:
        downloads = conn.execute(
            "SELECT COUNT(*) as c FROM history WHERE user_id=?", (user_id,)
        ).fetchone()["c"]
        library_count = conn.execute(
            "SELECT COUNT(*) as c FROM library WHERE user_id=?", (user_id,)
        ).fetchone()["c"]
    return {"downloads": downloads, "library": library_count}


# ── Промокоди ─────────────────────────────────────────────────────────────────
def create_promo(code: str, discount: int, uses: int):
    now = datetime.datetime.utcnow().isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO promocodes (code, discount, uses_left, created_at) VALUES (?,?,?,?)",
            (code, discount, uses, now)
        )


def use_promo(code: str) -> int | None:
    """Повертає відсоток знижки або None."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM promocodes WHERE code=? AND uses_left>0", (code,)
        ).fetchone()
        if not row:
            return None
        conn.execute(
            "UPDATE promocodes SET uses_left=uses_left-1 WHERE code=?", (code,)
        )
        return row["discount"]


def get_all_promos():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM promocodes").fetchall()


# ── Адмін статистика ──────────────────────────────────────────────────────────
def get_stats() -> dict:
    now = datetime.datetime.utcnow()
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        active_subs = 0
        trial = 0
        for u in conn.execute("SELECT * FROM users").fetchall():
            if u["sub_expires"] and datetime.datetime.fromisoformat(u["sub_expires"]) > now:
                active_subs += 1
            elif u["trial_expires"] and datetime.datetime.fromisoformat(u["trial_expires"]) > now:
                trial += 1
        keys_used = conn.execute(
            "SELECT COUNT(*) as c FROM keys WHERE used_by IS NOT NULL"
        ).fetchone()["c"]
        keys_total = conn.execute("SELECT COUNT(*) as c FROM keys").fetchone()["c"]
    return {
        "total_users": total,
        "active_subs": active_subs,
        "trial_users": trial,
        "keys_used": keys_used,
        "keys_total": keys_total,
                           }
  

# languages.py

LANGUAGES = {
    "uk": "🇺🇦 Українська",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "pl": "🇵🇱 Polski",
    "tr": "🇹🇷 Türkçe",
    "ar": "🇸🇦 العربية",
    "zh": "🇨🇳 中文",
}

TEXTS = {
    # ── Старт ──────────────────────────────────────────────────────────────────
    "welcome": {
        "uk": (
            "🎵 <b>Ласкаво просимо до {bot_name}!</b>\n\n"
            "Найкращий музичний бот — шукай, слухай і скачуй музику!\n\n"
            "✅ У тебе є <b>{trial} дні безкоштовного доступу</b>\n\n"
            "👤 <i>Автор: {author}</i>"
        ),
        "ru": (
            "🎵 <b>Добро пожаловать в {bot_name}!</b>\n\n"
            "Лучший музыкальный бот — ищи, слушай и скачивай музыку!\n\n"
            "✅ У тебя есть <b>{trial} дня бесплатного доступа</b>\n\n"
            "👤 <i>Автор: {author}</i>"
        ),
        "en": (
            "🎵 <b>Welcome to {bot_name}!</b>\n\n"
            "The best music bot — search, listen and download music!\n\n"
            "✅ You have <b>{trial} days of free access</b>\n\n"
            "👤 <i>Author: {author}</i>"
        ),
        "de": (
            "🎵 <b>Willkommen bei {bot_name}!</b>\n\n"
            "Der beste Musik-Bot — suche, höre und lade Musik herunter!\n\n"
            "✅ Du hast <b>{trial} Tage kostenlosen Zugang</b>\n\n"
            "👤 <i>Autor: {author}</i>"
        ),
        "fr": (
            "🎵 <b>Bienvenue sur {bot_name}!</b>\n\n"
            "Le meilleur bot musical — cherchez, écoutez et téléchargez!\n\n"
            "✅ Vous avez <b>{trial} jours d'accès gratuit</b>\n\n"
            "👤 <i>Auteur: {author}</i>"
        ),
        "es": (
            "🎵 <b>¡Bienvenido a {bot_name}!</b>\n\n"
            "El mejor bot musical — ¡busca, escucha y descarga música!\n\n"
            "✅ Tienes <b>{trial} días de acceso gratuito</b>\n\n"
            "👤 <i>Autor: {author}</i>"
        ),
        "pl": (
            "🎵 <b>Witamy w {bot_name}!</b>\n\n"
            "Najlepszy bot muzyczny — szukaj, słuchaj i pobieraj muzykę!\n\n"
            "✅ Masz <b>{trial} dni bezpłatnego dostępu</b>\n\n"
            "👤 <i>Autor: {author}</i>"
        ),
        "tr": (
            "🎵 <b>{bot_name}'a Hoş Geldiniz!</b>\n\n"
            "En iyi müzik botu — müzik ara, dinle ve indir!\n\n"
            "✅ <b>{trial} günlük ücretsiz erişiminiz</b> var\n\n"
            "👤 <i>Yazar: {author}</i>"
        ),
        "ar": (
            "🎵 <b>مرحباً بك في {bot_name}!</b>\n\n"
            "أفضل بوت موسيقي — ابحث واستمع وحمّل الموسيقى!\n\n"
            "✅ لديك <b>{trial} أيام وصول مجاني</b>\n\n"
            "👤 <i>المؤلف: {author}</i>"
        ),
        "zh": (
            "🎵 <b>欢迎来到 {bot_name}!</b>\n\n"
            "最好的音乐机器人 — 搜索、收听和下载音乐！\n\n"
            "✅ 您有 <b>{trial} 天免费访问</b>\n\n"
            "👤 <i>作者: {author}</i>"
        ),
    },

    "choose_language": {
        "uk": "🌍 Обери мову:",
        "ru": "🌍 Выбери язык:",
        "en": "🌍 Choose your language:",
        "de": "🌍 Wähle deine Sprache:",
        "fr": "🌍 Choisissez votre langue:",
        "es": "🌍 Elige tu idioma:",
        "pl": "🌍 Wybierz język:",
        "tr": "🌍 Dilinizi seçin:",
        "ar": "🌍 اختر لغتك:",
        "zh": "🌍 选择您的语言:",
    },

    # ── Меню ───────────────────────────────────────────────────────────────────
    "main_menu": {
        "uk": "🏠 <b>Головне меню</b>\n\nЩо хочеш зробити?",
        "ru": "🏠 <b>Главное меню</b>\n\nЧто хочешь сделать?",
        "en": "🏠 <b>Main Menu</b>\n\nWhat do you want to do?",
        "de": "🏠 <b>Hauptmenü</b>\n\nWas möchtest du tun?",
        "fr": "🏠 <b>Menu principal</b>\n\nQue voulez-vous faire?",
        "es": "🏠 <b>Menú principal</b>\n\n¿Qué quieres hacer?",
        "pl": "🏠 <b>Menu główne</b>\n\nCo chcesz zrobić?",
        "tr": "🏠 <b>Ana Menü</b>\n\nNe yapmak istersiniz?",
        "ar": "🏠 <b>القائمة الرئيسية</b>\n\nماذا تريد أن تفعل؟",
        "zh": "🏠 <b>主菜单</b>\n\n您想做什么？",
    },

    # ── Кнопки меню ────────────────────────────────────────────────────────────
    "btn_search":       {"uk": "🔍 Пошук музики",    "ru": "🔍 Поиск музыки",     "en": "🔍 Search Music",      "de": "🔍 Musik suchen",      "fr": "🔍 Rechercher",        "es": "🔍 Buscar música",     "pl": "🔍 Szukaj muzyki",    "tr": "🔍 Müzik Ara",        "ar": "🔍 بحث موسيقى",      "zh": "🔍 搜索音乐"},
    "btn_top100":       {"uk": "📊 Топ 100",          "ru": "📊 Топ 100",           "en": "📊 Top 100",           "de": "📊 Top 100",           "fr": "📊 Top 100",           "es": "📊 Top 100",           "pl": "📊 Top 100",          "tr": "📊 Top 100",          "ar": "📊 أفضل 100",        "zh": "📊 前100名"},
    "btn_library":      {"uk": "📚 Моя бібліотека",  "ru": "📚 Моя библиотека",   "en": "📚 My Library",        "de": "📚 Meine Bibliothek",  "fr": "📚 Ma bibliothèque",  "es": "📚 Mi biblioteca",    "pl": "📚 Moja biblioteka",  "tr": "📚 Kütüphanem",      "ar": "📚 مكتبتي",          "zh": "📚 我的音乐库"},
    "btn_profile":      {"uk": "👤 Профіль",          "ru": "👤 Профиль",           "en": "👤 Profile",           "de": "👤 Profil",            "fr": "👤 Profil",            "es": "👤 Perfil",            "pl": "👤 Profil",           "tr": "👤 Profil",           "ar": "👤 الملف الشخصي",   "zh": "👤 个人资料"},
    "btn_subscription": {"uk": "💎 Підписка",         "ru": "💎 Подписка",          "en": "💎 Subscription",      "de": "💎 Abonnement",        "fr": "💎 Abonnement",        "es": "💎 Suscripción",       "pl": "💎 Subskrypcja",      "tr": "💎 Abonelik",         "ar": "💎 الاشتراك",        "zh": "💎 订阅"},
    "btn_referral":     {"uk": "🎁 Реферальна",       "ru": "🎁 Реферальная",       "en": "🎁 Referral",          "de": "🎁 Empfehlung",        "fr": "🎁 Parrainage",        "es": "🎁 Referido",          "pl": "🎁 Referral",         "tr": "🎁 Referans",         "ar": "🎁 الإحالة",         "zh": "🎁 推荐"},
    "btn_settings":     {"uk": "⚙️ Налаштування",    "ru": "⚙️ Настройки",        "en": "⚙️ Settings",         "de": "⚙️ Einstellungen",    "fr": "⚙️ Paramètres",       "es": "⚙️ Configuración",    "pl": "⚙️ Ustawienia",      "tr": "⚙️ Ayarlar",         "ar": "⚙️ الإعدادات",      "zh": "⚙️ 设置"},
    "btn_back":         {"uk": "◀️ Назад",            "ru": "◀️ Назад",             "en": "◀️ Back",              "de": "◀️ Zurück",            "fr": "◀️ Retour",            "es": "◀️ Volver",            "pl": "◀️ Wróć",             "tr": "◀️ Geri",             "ar": "◀️ رجوع",            "zh": "◀️ 返回"},

    # ── Пошук ──────────────────────────────────────────────────────────────────
    "search_prompt": {
        "uk": "🔍 Введи назву пісні або артиста:",
        "ru": "🔍 Введи название песни или артиста:",
        "en": "🔍 Enter song name or artist:",
        "de": "🔍 Gib Songname oder Künstler ein:",
        "fr": "🔍 Entrez le nom de la chanson ou de l'artiste:",
        "es": "🔍 Ingresa el nombre de la canción o artista:",
        "pl": "🔍 Wpisz nazwę piosenki lub artysty:",
        "tr": "🔍 Şarkı adı veya sanatçı girin:",
        "ar": "🔍 أدخل اسم الأغنية أو الفنان:",
        "zh": "🔍 输入歌曲名称或艺术家:",
    },

    "searching": {
        "uk": "🔍 Шукаю: <b>{query}</b>…",
        "ru": "🔍 Ищу: <b>{query}</b>…",
        "en": "🔍 Searching: <b>{query}</b>…",
        "de": "🔍 Suche: <b>{query}</b>…",
        "fr": "🔍 Recherche: <b>{query}</b>…",
        "es": "🔍 Buscando: <b>{query}</b>…",
        "pl": "🔍 Szukam: <b>{query}</b>…",
        "tr": "🔍 Aranıyor: <b>{query}</b>…",
        "ar": "🔍 جاري البحث: <b>{query}</b>…",
        "zh": "🔍 搜索中: <b>{query}</b>…",
    },

    "no_results": {
        "uk": "😔 Нічого не знайдено. Спробуй інший запит.",
        "ru": "😔 Ничего не найдено. Попробуй другой запрос.",
        "en": "😔 Nothing found. Try another query.",
        "de": "😔 Nichts gefunden. Versuche eine andere Suchanfrage.",
        "fr": "😔 Rien trouvé. Essayez une autre requête.",
        "es": "😔 Nada encontrado. Intenta con otra búsqueda.",
        "pl": "😔 Nic nie znaleziono. Spróbuj innego zapytania.",
        "tr": "😔 Hiçbir şey bulunamadı. Başka bir sorgu deneyin.",
        "ar": "😔 لم يتم العثور على شيء. جرب استعلاماً آخر.",
        "zh": "😔 未找到任何内容。请尝试其他查询。",
    },

    # ── Підписка ───────────────────────────────────────────────────────────────
    "subscription_info": {
        "uk": (
            "💎 <b>Підписка</b>\n\n"
            "📅 Статус: {status}\n"
            "⏰ Діє до: {expires}\n\n"
            "💰 <b>Тарифи:</b>\n"
            "• 7 днів — $0.50\n"
            "• 30 днів — $2.00\n\n"
            "Оплата в боті: @MusicLSPauth_bot"
        ),
        "ru": (
            "💎 <b>Подписка</b>\n\n"
            "📅 Статус: {status}\n"
            "⏰ Действует до: {expires}\n\n"
            "💰 <b>Тарифы:</b>\n"
            "• 7 дней — $0.50\n"
            "• 30 дней — $2.00\n\n"
            "Оплата в боте: @MusicLSPauth_bot"
        ),
        "en": (
            "💎 <b>Subscription</b>\n\n"
            "📅 Status: {status}\n"
            "⏰ Expires: {expires}\n\n"
            "💰 <b>Plans:</b>\n"
            "• 7 days — $0.50\n"
            "• 30 days — $2.00\n\n"
            "Payment bot: @MusicLSPauth_bot"
        ),
        "de": (
            "💎 <b>Abonnement</b>\n\n"
            "📅 Status: {status}\n"
            "⏰ Läuft ab: {expires}\n\n"
            "💰 <b>Pläne:</b>\n"
            "• 7 Tage — $0.50\n"
            "• 30 Tage — $2.00\n\n"
            "Zahlungsbot: @MusicLSPauth_bot"
        ),
        "fr": (
            "💎 <b>Abonnement</b>\n\n"
            "📅 Statut: {status}\n"
            "⏰ Expire le: {expires}\n\n"
            "💰 <b>Plans:</b>\n"
            "• 7 jours — $0.50\n"
            "• 30 jours — $2.00\n\n"
            "Bot de paiement: @MusicLSPauth_bot"
        ),
        "es": (
            "💎 <b>Suscripción</b>\n\n"
            "📅 Estado: {status}\n"
            "⏰ Expira: {expires}\n\n"
            "💰 <b>Planes:</b>\n"
            "• 7 días — $0.50\n"
            "• 30 días — $2.00\n\n"
            "Bot de pago: @MusicLSPauth_bot"
        ),
        "pl": (
            "💎 <b>Subskrypcja</b>\n\n"
            "📅 Status: {status}\n"
            "⏰ Wygasa: {expires}\n\n"
            "💰 <b>Plany:</b>\n"
            "• 7 dni — $0.50\n"
            "• 30 dni — $2.00\n\n"
            "Bot płatności: @MusicLSPauth_bot"
        ),
        "tr": (
            "💎 <b>Abonelik</b>\n\n"
            "📅 Durum: {status}\n"
            "⏰ Bitiş: {expires}\n\n"
            "💰 <b>Planlar:</b>\n"
            "• 7 gün — $0.50\n"
            "• 30 gün — $2.00\n\n"
            "Ödeme botu: @MusicLSPauth_bot"
        ),
        "ar": (
            "💎 <b>الاشتراك</b>\n\n"
            "📅 الحالة: {status}\n"
            "⏰ ينتهي في: {expires}\n\n"
            "💰 <b>الخطط:</b>\n"
            "• 7 أيام — $0.50\n"
            "• 30 يوماً — $2.00\n\n"
            "بوت الدفع: @MusicLSPauth_bot"
        ),
        "zh": (
            "💎 <b>订阅</b>\n\n"
            "📅 状态: {status}\n"
            "⏰ 到期: {expires}\n\n"
            "💰 <b>套餐:</b>\n"
            "• 7天 — $0.50\n"
            "• 30天 — $2.00\n\n"
            "支付机器人: @MusicLSPauth_bot"
        ),
    },

    "btn_enter_key":  {"uk": "🔑 Ввести ключ",      "ru": "🔑 Ввести ключ",      "en": "🔑 Enter Key",        "de": "🔑 Schlüssel eingeben", "fr": "🔑 Entrer la clé",   "es": "🔑 Ingresar clave",   "pl": "🔑 Wprowadź klucz",  "tr": "🔑 Anahtar Gir",     "ar": "🔑 إدخال المفتاح",  "zh": "🔑 输入密钥"},
    "btn_pay":        {"uk": "💳 Оплатити",          "ru": "💳 Оплатить",          "en": "💳 Pay",              "de": "💳 Bezahlen",           "fr": "💳 Payer",            "es": "💳 Pagar",             "pl": "💳 Zapłać",           "tr": "💳 Öde",              "ar": "💳 ادفع",            "zh": "💳 支付"},

    "enter_key_prompt": {
        "uk": "🔑 Введи свій ключ активації:",
        "ru": "🔑 Введи свой ключ активации:",
        "en": "🔑 Enter your activation key:",
        "de": "🔑 Gib deinen Aktivierungsschlüssel ein:",
        "fr": "🔑 Entrez votre clé d'activation:",
        "es": "🔑 Ingresa tu clave de activación:",
        "pl": "🔑 Wprowadź swój klucz aktywacji:",
        "tr": "🔑 Aktivasyon anahtarınızı girin:",
        "ar": "🔑 أدخل مفتاح التفعيل الخاص بك:",
        "zh": "🔑 输入您的激活密钥:",
    },

    "key_success": {
        "uk": "✅ Ключ активовано! Доступ відкрито на <b>{days} днів</b>.",
        "ru": "✅ Ключ активирован! Доступ открыт на <b>{days} дней</b>.",
        "en": "✅ Key activated! Access granted for <b>{days} days</b>.",
        "de": "✅ Schlüssel aktiviert! Zugang für <b>{days} Tage</b> gewährt.",
        "fr": "✅ Clé activée! Accès accordé pour <b>{days} jours</b>.",
        "es": "✅ ¡Clave activada! Acceso otorgado por <b>{days} días</b>.",
        "pl": "✅ Klucz aktywowany! Dostęp przyznany na <b>{days} dni</b>.",
        "tr": "✅ Anahtar etkinleştirildi! <b>{days} gün</b> erişim verildi.",
        "ar": "✅ تم تفعيل المفتاح! تم منح الوصول لـ <b>{days} أيام</b>.",
        "zh": "✅ 密钥已激活！已授予 <b>{days} 天</b>访问权限。",
    },

    "key_invalid": {
        "uk": "❌ Невірний або вже використаний ключ.",
        "ru": "❌ Неверный или уже использованный ключ.",
        "en": "❌ Invalid or already used key.",
        "de": "❌ Ungültiger oder bereits verwendeter Schlüssel.",
        "fr": "❌ Clé invalide ou déjà utilisée.",
        "es": "❌ Clave inválida o ya utilizada.",
        "pl": "❌ Nieprawidłowy lub już użyty klucz.",
        "tr": "❌ Geçersiz veya zaten kullanılmış anahtar.",
        "ar": "❌ مفتاح غير صالح أو مستخدم بالفعل.",
        "zh": "❌ 无效或已使用的密钥。",
    },

    # ── Реферал ────────────────────────────────────────────────────────────────
    "referral_info": {
        "uk": (
            "🎁 <b>Реферальна програма</b>\n\n"
            "Запроси друга — отримай <b>+1 день</b> до підписки!\n"
            "Максимум: 3 реферали на день\n\n"
            "👥 Твоїх рефералів: <b>{count}</b>\n"
            "📅 Зароблено днів: <b>{days}</b>\n\n"
            "🔗 Твоє посилання:\n<code>{link}</code>"
        ),
        "ru": (
            "🎁 <b>Реферальная программа</b>\n\n"
            "Пригласи друга — получи <b>+1 день</b> к подписке!\n"
            "Максимум: 3 реферала в день\n\n"
            "👥 Твоих рефералов: <b>{count}</b>\n"
            "📅 Заработано дней: <b>{days}</b>\n\n"
            "🔗 Твоя ссылка:\n<code>{link}</code>"
        ),
        "en": (
            "🎁 <b>Referral Program</b>\n\n"
            "Invite a friend — get <b>+1 day</b> to your subscription!\n"
            "Maximum: 3 referrals per day\n\n"
            "👥 Your referrals: <b>{count}</b>\n"
            "📅 Days earned: <b>{days}</b>\n\n"
            "🔗 Your link:\n<code>{link}</code>"
        ),
        "de": (
            "🎁 <b>Empfehlungsprogramm</b>\n\n"
            "Lade einen Freund ein — erhalte <b>+1 Tag</b> Abonnement!\n"
            "Maximum: 3 Empfehlungen pro Tag\n\n"
            "👥 Deine Empfehlungen: <b>{count}</b>\n"
            "📅 Verdiente Tage: <b>{days}</b>\n\n"
            "🔗 Dein Link:\n<code>{link}</code>"
        ),
        "fr": (
            "🎁 <b>Programme de parrainage</b>\n\n"
            "Invitez un ami — obtenez <b>+1 jour</b> d'abonnement!\n"
            "Maximum: 3 parrainages par jour\n\n"
            "👥 Vos parrainages: <b>{count}</b>\n"
            "📅 Jours gagnés: <b>{days}</b>\n\n"
            "🔗 Votre lien:\n<code>{link}</code>"
        ),
        "es": (
            "🎁 <b>Programa de referidos</b>\n\n"
            "¡Invita a un amigo — obtén <b>+1 día</b> de suscripción!\n"
            "Máximo: 3 referidos por día\n\n"
            "👥 Tus referidos: <b>{count}</b>\n"
            "📅 Días ganados: <b>{days}</b>\n\n"
            "🔗 Tu enlace:\n<code>{link}</code>"
        ),
        "pl": (
            "🎁 <b>Program polecający</b>\n\n"
            "Zaproś znajomego — otrzymaj <b>+1 dzień</b> subskrypcji!\n"
            "Maksimum: 3 polecenia dziennie\n\n"
            "👥 Twoich poleceń: <b>{count}</b>\n"
            "📅 Zarobione dni: <b>{days}</b>\n\n"
            "🔗 Twój link:\n<code>{link}</code>"
        ),
        "tr": (
            "🎁 <b>Referans Programı</b>\n\n"
            "Bir arkadaş davet et — aboneliğine <b>+1 gün</b> kazan!\n"
            "Maksimum: günde 3 referans\n\n"
            "👥 Referansların: <b>{count}</b>\n"
            "📅 Kazanılan günler: <b>{days}</b>\n\n"
            "🔗 Bağlantın:\n<code>{link}</code>"
        ),
        "ar": (
            "🎁 <b>برنامج الإحالة</b>\n\n"
            "ادعُ صديقاً — احصل على <b>+1 يوم</b> في اشتراكك!\n"
            "الحد الأقصى: 3 إحالات يومياً\n\n"
            "👥 إحالاتك: <b>{count}</b>\n"
            "📅 الأيام المكتسبة: <b>{days}</b>\n\n"
            "🔗 رابطك:\n<code>{link}</code>"
        ),
        "zh": (
            "🎁 <b>推荐计划</b>\n\n"
            "邀请朋友 — 获得订阅 <b>+1天</b>！\n"
            "每天最多: 3次推荐\n\n"
            "👥 您的推荐数: <b>{count}</b>\n"
            "📅 获得天数: <b>{days}</b>\n\n"
            "🔗 您的链接:\n<code>{link}</code>"
        ),
    },

    # ── Статуси підписки ───────────────────────────────────────────────────────
    "status_active":  {"uk": "✅ Активна",   "ru": "✅ Активна",    "en": "✅ Active",      "de": "✅ Aktiv",       "fr": "✅ Active",      "es": "✅ Activa",      "pl": "✅ Aktywna",     "tr": "✅ Aktif",       "ar": "✅ نشط",        "zh": "✅ 活跃"},
    "status_trial":   {"uk": "🆓 Пробний",   "ru": "🆓 Пробный",   "en": "🆓 Trial",       "de": "🆓 Testversion", "fr": "🆓 Essai",       "es": "🆓 Prueba",      "pl": "🆓 Próbny",      "tr": "🆓 Deneme",      "ar": "🆓 تجريبي",     "zh": "🆓 试用"},
    "status_expired": {"uk": "❌ Закінчилась","ru": "❌ Истекла",   "en": "❌ Expired",     "de": "❌ Abgelaufen",  "fr": "❌ Expirée",     "es": "❌ Expirada",    "pl": "❌ Wygasła",     "tr": "❌ Süresi Doldu","ar": "❌ منتهية",      "zh": "❌ 已过期"},

    # ── Доступ заборонений ─────────────────────────────────────────────────────
    "no_access": {
        "uk": "⛔ Підписка закінчилась.\n\nОформи підписку → /subscription",
        "ru": "⛔ Подписка истекла.\n\nОформи подписку → /subscription",
        "en": "⛔ Subscription expired.\n\nGet subscription → /subscription",
        "de": "⛔ Abonnement abgelaufen.\n\nAbonnement abschließen → /subscription",
        "fr": "⛔ Abonnement expiré.\n\nPrenez un abonnement → /subscription",
        "es": "⛔ Suscripción expirada.\n\nObtén suscripción → /subscription",
        "pl": "⛔ Subskrypcja wygasła.\n\nKup subskrypcję → /subscription",
        "tr": "⛔ Abonelik sona erdi.\n\nAbonelik al → /subscription",
        "ar": "⛔ انتهى الاشتراك.\n\nاحصل على اشتراك → /subscription",
        "zh": "⛔ 订阅已过期。\n\n获取订阅 → /subscription",
    },

    # ── Завантаження ───────────────────────────────────────────────────────────
    "downloading": {
        "uk": "⬇️ Завантажую: <b>{title}</b>…\n<i>(10–30 секунд)</i>",
        "ru": "⬇️ Скачиваю: <b>{title}</b>…\n<i>(10–30 секунд)</i>",
        "en": "⬇️ Downloading: <b>{title}</b>…\n<i>(10–30 seconds)</i>",
        "de": "⬇️ Herunterladen: <b>{title}</b>…\n<i>(10–30 Sekunden)</i>",
        "fr": "⬇️ Téléchargement: <b>{title}</b>…\n<i>(10–30 secondes)</i>",
        "es": "⬇️ Descargando: <b>{title}</b>…\n<i>(10–30 segundos)</i>",
        "pl": "⬇️ Pobieranie: <b>{title}</b>…\n<i>(10–30 sekund)</i>",
        "tr": "⬇️ İndiriliyor: <b>{title}</b>…\n<i>(10–30 saniye)</i>",
        "ar": "⬇️ جاري التنزيل: <b>{title}</b>…\n<i>(10–30 ثانية)</i>",
        "zh": "⬇️ 下载中: <b>{title}</b>…\n<i>(10–30秒)</i>",
    },

    "btn_download_20": {"uk": "⬇️ Скачати 20 пісень", "ru": "⬇️ Скачать 20 песен", "en": "⬇️ Download 20 songs", "de": "⬇️ 20 Songs herunterladen", "fr": "⬇️ Télécharger 20 chansons", "es": "⬇️ Descargar 20 canciones", "pl": "⬇️ Pobierz 20 piosenek", "tr": "⬇️ 20 şarkı indir", "ar": "⬇️ تنزيل 20 أغنية", "zh": "⬇️ 下载20首歌"},
    "btn_all_songs":   {

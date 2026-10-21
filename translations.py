"""
All the words SafeSend shows, in English, Chinese, Malay and Tamil.

To fix or improve a translation, change it here. Each entry is:
    "key": T("English", "中文", "Bahasa Melayu", "தமிழ்")
Use {name} style placeholders exactly as in the English text.
"""

# (code, name shown on the button, HTML lang attribute)
LANGUAGES = [
    ("en", "English", "en"),
    ("zh", "中文", "zh-Hans"),
    ("ms", "Melayu", "ms"),
    ("ta", "தமிழ்", "ta"),
]
LANG_CODES = [code for code, _, _ in LANGUAGES]
HTML_LANG = {code: html for code, _, html in LANGUAGES}


def T(en, zh, ms, ta):
    return {"en": en, "zh": zh, "ms": ms, "ta": ta}


STRINGS = {
    # ---- Shared layout ----
    "nav_send": T("Send money", "付款", "Hantar wang", "பணம் அனுப்பு"),
    "nav_contact": T("Trusted contact", "信任联系人", "Kenalan dipercayai", "நம்பகமான தொடர்பு"),
    "nav_settings": T("Settings", "设置", "Tetapan", "அமைப்புகள்"),
    "sandbox_note": T(
        "Demo using PayPal sandbox: pretend money only.",
        "演示版本：使用 PayPal 测试环境，不涉及真钱。",
        "Demo menggunakan PayPal sandbox: wang ujian sahaja, bukan wang sebenar.",
        "டெமோ: PayPal சோதனை முறை. உண்மையான பணம் இல்லை.",
    ),
    "lang_label": T("Language", "语言", "Bahasa", "மொழி"),
    "title_result": T("Check result", "检查结果", "Keputusan semakan", "சரிபார்ப்பு முடிவு"),
    "title_status": T("Payment status", "付款状态", "Status bayaran", "பணம் செலுத்துதல் நிலை"),
    "not_found_title": T("Not found", "找不到", "Tidak dijumpai", "கிடைக்கவில்லை"),
    "not_found_text": T("That page does not exist.", "这个页面不存在。", "Halaman itu tidak wujud.", "அந்தப் பக்கம் இல்லை."),
    "go_start": T("Go to the start", "回到首页", "Kembali ke halaman utama", "முதல் பக்கத்துக்குச் செல்லவும்"),

    # ---- Flash messages ----
    "flash_invalid": T(
        "Please enter who you are paying and an amount between {min} and {max}.",
        "请填写收款人，以及 {min} 到 {max} 之间的金额。",
        "Sila masukkan penerima dan jumlah antara {min} dan {max}.",
        "யாருக்கு அனுப்புகிறீர்கள் என்பதையும், {min} முதல் {max} வரையிலான தொகையையும் உள்ளிடவும்.",
    ),
    "flash_still_cooling": T(
        "This payment is still in its cooling-off time.",
        "这笔付款还在冷静期内。",
        "Bayaran ini masih dalam tempoh bertenang.",
        "இந்தப் பணம் செலுத்துதல் இன்னும் காத்திருப்பு நேரத்தில் உள்ளது.",
    ),
    "flash_send_failed": T(
        "PayPal could not send this payment. Please try again.",
        "PayPal 无法发送这笔付款。请再试一次。",
        "PayPal tidak dapat menghantar bayaran ini. Sila cuba lagi.",
        "PayPal இந்தப் பணத்தை அனுப்ப முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
    ),
    "flash_cancel_failed": T(
        "PayPal could not cancel this payment. Please try again.",
        "PayPal 无法取消这笔付款。请再试一次。",
        "PayPal tidak dapat membatalkan bayaran ini. Sila cuba lagi.",
        "PayPal இந்தப் பணம் செலுத்துதலை ரத்து செய்ய முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
    ),
    "flash_numbers": T(
        "Limit and cooling-off time must be numbers.",
        "限额和冷静期必须是数字。",
        "Had dan tempoh bertenang mesti nombor.",
        "வரம்பும் காத்திருப்பு நேரமும் எண்களாக இருக்க வேண்டும்.",
    ),
    "flash_saved": T("Settings saved.", "设置已保存。", "Tetapan disimpan.", "அமைப்புகள் சேமிக்கப்பட்டன."),
    "paypal_keys_missing": T(
        "PayPal keys are missing. Add PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET to your .env file.",
        "缺少 PayPal 密钥。请在 .env 文件里加入 PAYPAL_CLIENT_ID 和 PAYPAL_CLIENT_SECRET。",
        "Kunci PayPal tiada. Tambah PAYPAL_CLIENT_ID dan PAYPAL_CLIENT_SECRET ke fail .env anda.",
        "PayPal விசைகள் இல்லை. உங்கள் .env கோப்பில் PAYPAL_CLIENT_ID மற்றும் PAYPAL_CLIENT_SECRET ஐச் சேர்க்கவும்.",
    ),

    # ---- Home page ----
    "hello": T("Hello, {name}", "{name}，您好", "Helo, {name}", "வணக்கம், {name}"),
    "index_lead": T(
        "Tell us who you are paying. We'll check it is safe before any money leaves.",
        "请告诉我们您要付钱给谁。在钱付出去之前，我们会先帮您检查是否安全。",
        "Beritahu kami siapa yang anda mahu bayar. Kami akan periksa sama ada ia selamat sebelum wang dihantar.",
        "யாருக்கு பணம் அனுப்புகிறீர்கள் என்று சொல்லுங்கள். பணம் அனுப்பப்படும் முன் அது பாதுகாப்பானதா என்று நாங்கள் சரிபார்ப்போம்.",
    ),
    "demo_title": T("Demo: try an example", "演示：试试看例子", "Demo: cuba contoh", "டெமோ: ஒரு உதாரணத்தை முயற்சிக்கவும்"),
    "demo_hawker": T("Normal: pay the hawker", "正常：付钱给小贩", "Biasa: bayar penjaja", "சாதாரணம்: உணவுக் கடைக்காரருக்குப் பணம்"),
    "demo_police": T("Scam: fake police", "骗局：假警察", "Penipuan: polis palsu", "மோசடி: போலி காவல்துறை"),
    "demo_grandson": T("Scam: grandson in trouble", "骗局：孙子出事了", "Penipuan: cucu dalam kesusahan", "மோசடி: பேரன் சிக்கலில்"),
    "demo_seller": T(
        "Unsure: online seller deposit",
        "不确定：网上卖家要订金",
        "Tidak pasti: penjual dalam talian minta deposit",
        "சந்தேகம்: இணைய விற்பனையாளர் முன்பணம் கேட்கிறார்",
    ),
    "f_recipient": T("Who are you paying?", "您要付钱给谁？", "Anda mahu bayar kepada siapa?", "யாருக்கு பணம் அனுப்புகிறீர்கள்?"),
    "ph_recipient": T(
        "For example: Uncle Tan Chicken Rice",
        "例如：Uncle Tan Chicken Rice",
        "Contoh: Uncle Tan Chicken Rice",
        "உதாரணம்: Uncle Tan Chicken Rice",
    ),
    "f_amount": T("How much?", "多少钱？", "Berapa banyak?", "எவ்வளவு?"),
    "f_amount_hint": T(
        "In {currency} (sandbox test money)",
        "单位：{currency}（测试用的钱）",
        "Dalam {currency} (wang ujian sandbox)",
        "{currency} இல் (சோதனைப் பணம்)",
    ),
    "f_reason": T("What is it for?", "这笔钱是做什么用的？", "Untuk apa?", "எதற்காக?"),
    "ph_reason": T(
        "For example: Food, Bills, Gift",
        "例如：买食物、付账单、送礼",
        "Contoh: Makanan, Bil, Hadiah",
        "உதாரணம்: உணவு, கட்டணங்கள், பரிசு",
    ),
    "f_message": T(
        "Did someone send you a message asking for this money?",
        "有人发信息叫您付这笔钱吗？",
        "Adakah sesiapa menghantar mesej meminta wang ini?",
        "இந்தப் பணத்தைக் கேட்டு யாராவது உங்களுக்குச் செய்தி அனுப்பினார்களா?",
    ),
    "f_message_hint": T(
        "If yes, paste it here. If not, leave it empty.",
        "如果有，请把信息贴在这里。如果没有，可以不填。",
        "Jika ya, tampal di sini. Jika tidak, biarkan kosong.",
        "ஆம் என்றால், அதை இங்கே ஒட்டவும். இல்லையென்றால், காலியாக விடவும்.",
    ),
    "ph_message": T(
        "Paste the WhatsApp, SMS or email here",
        "把 WhatsApp、短信或电邮贴在这里",
        "Tampal WhatsApp, SMS atau e-mel di sini",
        "WhatsApp, SMS அல்லது மின்னஞ்சலை இங்கே ஒட்டவும்",
    ),
    "btn_check": T("Check this payment", "检查这笔付款", "Periksa bayaran ini", "இந்தப் பணம் செலுத்துதலைச் சரிபார்க்கவும்"),
    "checking": T(
        "Checking… please wait",
        "正在检查……请稍等",
        "Sedang memeriksa… sila tunggu",
        "சரிபார்க்கிறது… தயவுசெய்து காத்திருக்கவும்",
    ),
    "checking_hint": T(
        "This can take up to 30 seconds. Please don't press again.",
        "可能需要最多 30 秒。请不要再按一次。",
        "Ini mungkin mengambil masa sehingga 30 saat. Jangan tekan lagi.",
        "இதற்கு 30 வினாடிகள் வரை ஆகலாம். மீண்டும் அழுத்த வேண்டாம்.",
    ),
    "footer_ai": T(
        "SafeSend checks every payment with {ai} AI and safety rules. Anything unusual is held until {contact} looks at it.",
        "SafeSend 会用 {ai} 人工智能和安全规则检查每一笔付款。任何不寻常的付款都会先暂停，直到 {contact} 查看。",
        "SafeSend memeriksa setiap bayaran dengan AI {ai} dan peraturan keselamatan. Apa-apa yang luar biasa akan ditahan sehingga {contact} menyemaknya.",
        "SafeSend ஒவ்வொரு பணம் செலுத்துதலையும் {ai} AI மற்றும் பாதுகாப்பு விதிகள் மூலம் சரிபார்க்கிறது. அசாதாரணமானவை {contact} பார்க்கும் வரை நிறுத்தி வைக்கப்படும்.",
    ),
    "footer_rules": T(
        "SafeSend checks every payment with safety rules. Anything unusual is held until {contact} looks at it.",
        "SafeSend 会用安全规则检查每一笔付款。任何不寻常的付款都会先暂停，直到 {contact} 查看。",
        "SafeSend memeriksa setiap bayaran dengan peraturan keselamatan. Apa-apa yang luar biasa akan ditahan sehingga {contact} menyemaknya.",
        "SafeSend ஒவ்வொரு பணம் செலுத்துதலையும் பாதுகாப்பு விதிகள் மூலம் சரிபார்க்கிறது. அசாதாரணமானவை {contact} பார்க்கும் வரை நிறுத்தி வைக்கப்படும்.",
    ),

    # ---- Verdict page ----
    "v_SAFE_title": T("This looks safe", "看起来安全", "Ini nampak selamat", "இது பாதுகாப்பாகத் தெரிகிறது"),
    "v_CHECK_title": T("Let's check this first", "我们先检查一下", "Mari kita periksa dahulu", "முதலில் இதைச் சரிபார்ப்போம்"),
    "v_STOP_title": T(
        "Stop. This looks like a scam",
        "停！这看起来像骗局",
        "Berhenti. Ini nampak seperti penipuan",
        "நிறுத்துங்கள். இது மோசடி போலத் தெரிகிறது",
    ),
    "good_to_know": T("Good to know:", "温馨提示：", "Untuk makluman:", "தெரிந்து கொள்ளுங்கள்:"),
    "checked_by": T("Checked by {source}", "检查方式：{source}", "Diperiksa oleh {source}", "சரிபார்த்தது: {source}"),
    "src_ai": T("{ai} AI + safety rules", "{ai} 人工智能 + 安全规则", "AI {ai} + peraturan keselamatan", "{ai} AI + பாதுகாப்பு விதிகள்"),
    "src_ai_strict": T(
        "{ai} AI + safety rules (rules were stricter)",
        "{ai} 人工智能 + 安全规则（安全规则更严格）",
        "AI {ai} + peraturan keselamatan (peraturan lebih ketat)",
        "{ai} AI + பாதுகாப்பு விதிகள் (விதிகள் கடுமையானவை)",
    ),
    "src_rules": T("Safety rules", "安全规则", "Peraturan keselamatan", "பாதுகாப்பு விதிகள்"),
    "src_rules_down": T(
        "Safety rules (AI unavailable)",
        "安全规则（人工智能暂时无法使用）",
        "Peraturan keselamatan (AI tidak tersedia)",
        "பாதுகாப்பு விதிகள் (AI கிடைக்கவில்லை)",
    ),
    "paying": T("Paying", "付款给", "Membayar kepada", "பணம் பெறுபவர்"),
    "for_reason": T("For: {reason}", "用途：{reason}", "Untuk: {reason}", "எதற்காக: {reason}"),
    "safe_h": T("Ready to send", "可以付款了", "Sedia untuk dihantar", "அனுப்பத் தயார்"),
    "safe_p": T(
        "When you approve in PayPal, the money is sent straight away.",
        "您在 PayPal 确认后，钱会马上付出。",
        "Apabila anda luluskan dalam PayPal, wang akan dihantar serta-merta.",
        "PayPal இல் நீங்கள் ஒப்புதல் அளித்தவுடன், பணம் உடனே அனுப்பப்படும்.",
    ),
    "check_h": T(
        "We'll hold it, just in case",
        "为了安全，我们会先暂停这笔钱",
        "Kami akan tahan dahulu, untuk berjaga-jaga",
        "பாதுகாப்புக்காக, இதை நிறுத்தி வைப்போம்",
    ),
    "check_p": T(
        "If you continue, the money is held, not sent. We will ask {contact} to check it. You can cancel any time while it is held.",
        "如果您继续，钱会先被暂停，不会付出。我们会请 {contact} 帮忙检查。在暂停期间，您随时可以取消。",
        "Jika anda teruskan, wang akan ditahan, bukan dihantar. Kami akan minta {contact} menyemaknya. Anda boleh batalkan pada bila-bila masa semasa ia ditahan.",
        "நீங்கள் தொடர்ந்தால், பணம் அனுப்பப்படாமல் நிறுத்தி வைக்கப்படும். {contact} அவர்களைச் சரிபார்க்கச் சொல்வோம். நிறுத்தி வைக்கப்பட்டிருக்கும் போது எப்போது வேண்டுமானாலும் ரத்து செய்யலாம்.",
    ),
    "stop_h": T(
        "Our advice: don't send this",
        "我们的建议：不要付这笔钱",
        "Nasihat kami: jangan hantar",
        "எங்கள் ஆலோசனை: இதை அனுப்ப வேண்டாம்",
    ),
    "stop_p": T(
        "Please talk to {contact} or call the ScamShield Helpline at 1799 first.",
        "请先和 {contact} 商量，或拨打反诈骗热线 ScamShield 1799。",
        "Sila bercakap dengan {contact} atau hubungi Talian Bantuan ScamShield di 1799 dahulu.",
        "முதலில் {contact} அவர்களிடம் பேசுங்கள், அல்லது ScamShield உதவி எண் 1799 ஐ அழைக்கவும்.",
    ),
    "stop_confirm": T(
        "I still want to continue. Hold the money until {contact} checks it.",
        "我还是要继续。先暂停这笔钱，等 {contact} 检查。",
        "Saya masih mahu teruskan. Tahan wang ini sehingga {contact} menyemaknya.",
        "நான் இன்னும் தொடர விரும்புகிறேன். {contact} சரிபார்க்கும் வரை பணத்தை நிறுத்தி வைக்கவும்.",
    ),
    "paypal_button_missing": T(
        "PayPal keys are missing, so the PayPal button can't load.",
        "缺少 PayPal 密钥，所以 PayPal 按钮无法显示。",
        "Kunci PayPal tiada, jadi butang PayPal tidak dapat dimuatkan.",
        "PayPal விசைகள் இல்லை, அதனால் PayPal பொத்தானை ஏற்ற முடியவில்லை.",
    ),
    "btn_cancel_stop": T(
        "Don't send. Cancel this payment",
        "不要付。取消这笔付款",
        "Jangan hantar. Batalkan bayaran ini",
        "அனுப்ப வேண்டாம். இதை ரத்து செய்யவும்",
    ),
    "btn_cancel": T("Cancel, don't send", "取消，不要付", "Batal, jangan hantar", "ரத்து செய், அனுப்ப வேண்டாம்"),
    "js_closed": T(
        "You closed PayPal. Nothing was sent.",
        "您关闭了 PayPal。没有付出任何钱。",
        "Anda menutup PayPal. Tiada wang dihantar.",
        "நீங்கள் PayPal ஐ மூடிவிட்டீர்கள். எதுவும் அனுப்பப்படவில்லை.",
    ),
    "js_error": T(
        "PayPal had a problem. Please try again.",
        "PayPal 出了问题。请再试一次。",
        "PayPal menghadapi masalah. Sila cuba lagi.",
        "PayPal இல் சிக்கல் ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.",
    ),
    "js_noload": T(
        "PayPal could not load. Check your internet connection or turn off ad-blockers for this page.",
        "PayPal 无法加载。请检查网络，或为这个网页关闭广告拦截。",
        "PayPal tidak dapat dimuatkan. Semak sambungan internet atau matikan penyekat iklan untuk halaman ini.",
        "PayPal ஏற்றப்படவில்லை. இணைய இணைப்பைச் சரிபார்க்கவும் அல்லது இந்தப் பக்கத்துக்கு விளம்பரத் தடுப்பை அணைக்கவும்.",
    ),
    "api_handled": T(
        "This payment has already been handled.",
        "这笔付款已经处理过了。",
        "Bayaran ini sudah diuruskan.",
        "இந்தப் பணம் செலுத்துதல் ஏற்கனவே கையாளப்பட்டது.",
    ),
    "api_mismatch": T(
        "That PayPal order does not match this payment.",
        "这个 PayPal 订单和这笔付款不符。",
        "Pesanan PayPal itu tidak sepadan dengan bayaran ini.",
        "அந்த PayPal ஆர்டர் இந்தப் பணம் செலுத்துதலுடன் பொருந்தவில்லை.",
    ),

    # ---- Status page ----
    "st_sent_h": T("Money sent", "钱已付出", "Wang telah dihantar", "பணம் அனுப்பப்பட்டது"),
    "st_sent_p": T(
        "{amount} was sent to {recipient}.",
        "{amount} 已付给 {recipient}。",
        "{amount} telah dihantar kepada {recipient}.",
        "{amount} {recipient} அவர்களுக்கு அனுப்பப்பட்டது.",
    ),
    "approved_by": T("Approved by {who}.", "批准人：{who}。", "Diluluskan oleh {who}.", "ஒப்புதல் அளித்தவர்: {who}."),
    "st_over_h": T("The waiting time is over", "等待时间已经结束", "Masa menunggu sudah tamat", "காத்திருப்பு நேரம் முடிந்தது"),
    "st_over_p": T(
        "Nobody has checked this yet. Do you still want to send {amount} to {recipient}?",
        "还没有人检查这笔付款。您还要付 {amount} 给 {recipient} 吗？",
        "Belum ada sesiapa menyemaknya. Adakah anda masih mahu menghantar {amount} kepada {recipient}?",
        "இதை இன்னும் யாரும் சரிபார்க்கவில்லை. {amount} ஐ {recipient} அவர்களுக்கு இன்னும் அனுப்ப விரும்புகிறீர்களா?",
    ),
    "btn_yes_send": T("Yes, send it now", "是的，现在付", "Ya, hantar sekarang", "ஆம், இப்போது அனுப்பு"),
    "btn_no_cancel": T("No, cancel it", "不，取消", "Tidak, batalkan", "இல்லை, ரத்து செய்"),
    "st_held_h": T(
        "Your money is safe, on hold",
        "您的钱很安全，已暂停",
        "Wang anda selamat, sedang ditahan",
        "உங்கள் பணம் பாதுகாப்பாக நிறுத்தி வைக்கப்பட்டுள்ளது",
    ),
    "st_held_p": T(
        "{amount} to {recipient} has not been sent. We've asked {contact} to check it.",
        "付给 {recipient} 的 {amount} 还没有付出。我们已经请 {contact} 帮忙检查。",
        "{amount} kepada {recipient} belum dihantar. Kami telah minta {contact} menyemaknya.",
        "{recipient} அவர்களுக்கான {amount} அனுப்பப்படவில்லை. {contact} அவர்களைச் சரிபார்க்கச் சொல்லியுள்ளோம்.",
    ),
    "st_wait": T(
        "If nobody checks it, you can decide again in {wait}.",
        "如果没有人检查，{wait}后您可以重新决定。",
        "Jika tiada siapa menyemaknya, anda boleh membuat keputusan semula dalam {wait}.",
        "யாரும் சரிபார்க்காவிட்டால், {wait} பிறகு மீண்டும் முடிவு செய்யலாம்.",
    ),
    "btn_cancel_held": T("Cancel it, don't send", "取消，不要付", "Batalkan, jangan hantar", "ரத்து செய், அனுப்ப வேண்டாம்"),
    "st_blocked_h": T(
        "Blocked. Your money is safe",
        "已拦截，您的钱很安全",
        "Disekat. Wang anda selamat",
        "தடுக்கப்பட்டது. உங்கள் பணம் பாதுகாப்பாக உள்ளது",
    ),
    "st_blocked_p": T(
        "{who} stopped this payment. No money was sent to {recipient}.",
        "{who} 拦截了这笔付款。没有钱付给 {recipient}。",
        "{who} telah menghentikan bayaran ini. Tiada wang dihantar kepada {recipient}.",
        "{who} இந்தப் பணம் செலுத்துதலை நிறுத்தினார். {recipient} அவர்களுக்கு எந்தப் பணமும் அனுப்பப்படவில்லை.",
    ),
    "st_cancelled_h": T(
        "Cancelled. No money sent",
        "已取消，没有付钱",
        "Dibatalkan. Tiada wang dihantar",
        "ரத்து செய்யப்பட்டது. பணம் அனுப்பப்படவில்லை",
    ),
    "st_cancelled_p": T(
        "Good choice to check. Nothing was sent to {recipient}.",
        "先检查是对的。没有钱付给 {recipient}。",
        "Bagus anda menyemak dahulu. Tiada apa-apa dihantar kepada {recipient}.",
        "சரிபார்த்தது நல்ல முடிவு. {recipient} அவர்களுக்கு எதுவும் அனுப்பப்படவில்லை.",
    ),
    "st_checked_h": T("Not sent yet", "还没有付", "Belum dihantar", "இன்னும் அனுப்பப்படவில்லை"),
    "st_checked_link": T(
        "Go back to finish or cancel this payment",
        "返回完成或取消这笔付款",
        "Kembali untuk selesaikan atau batalkan bayaran ini",
        "இதை முடிக்க அல்லது ரத்து செய்யத் திரும்பிச் செல்லவும்",
    ),
    "st_failed_h": T("Something went wrong", "出了问题", "Ada masalah", "ஏதோ தவறு நடந்தது"),
    "st_failed_p": T(
        "No money was sent. Please try again.",
        "没有付出任何钱。请再试一次。",
        "Tiada wang dihantar. Sila cuba lagi.",
        "பணம் எதுவும் அனுப்பப்படவில்லை. மீண்டும் முயற்சிக்கவும்.",
    ),
    "another": T("Make another payment", "再付一笔", "Buat bayaran lain", "வேறொரு பணம் செலுத்துதல் செய்யவும்"),
    "note_send_failed": T(
        "Could not send. Please try again.",
        "无法付出。请再试一次。",
        "Tidak dapat dihantar. Sila cuba lagi.",
        "அனுப்ப முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
    ),
    "note_cancel_failed": T(
        "Could not cancel. Please try again.",
        "无法取消。请再试一次。",
        "Tidak dapat dibatalkan. Sila cuba lagi.",
        "ரத்து செய்ய முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
    ),

    # Who decided
    "who_auto_safe": T("SafeSend (looked safe)", "SafeSend（看起来安全）", "SafeSend (nampak selamat)", "SafeSend (பாதுகாப்பாகத் தெரிந்தது)"),
    "who_elder": T("you", "您", "anda", "நீங்கள்"),
    "who_elder_after_wait": T(
        "you, after the cooling-off time",
        "您（冷静期过后）",
        "anda, selepas tempoh bertenang",
        "நீங்கள், காத்திருப்பு நேரத்துக்குப் பிறகு",
    ),

    # Waiting time
    "wait_hours": T("about {n} hours", "大约{n}小时", "kira-kira {n} jam", "சுமார் {n} மணி நேரம்"),
    "wait_hour": T("about 1 hour", "大约1小时", "kira-kira 1 jam", "சுமார் 1 மணி நேரம்"),
    "wait_minutes": T("about {n} minutes", "大约{n}分钟", "kira-kira {n} minit", "சுமார் {n} நிமிடங்கள்"),
    "wait_minute": T("about 1 minute", "大约1分钟", "kira-kira 1 minit", "சுமார் 1 நிமிடம்"),
    "wait_seconds": T("{n} seconds", "{n}秒", "{n} saat", "{n} வினாடிகள்"),

    # Status words
    "status_checked": T("Not finished", "未完成", "Belum selesai", "முடிக்கப்படவில்லை"),
    "status_processing": T("Working on it…", "处理中……", "Sedang diproses…", "செயல்படுத்தப்படுகிறது…"),
    "status_sent": T("Sent", "已付出", "Dihantar", "அனுப்பப்பட்டது"),
    "status_held": T("On hold", "已暂停", "Ditahan", "நிறுத்தி வைக்கப்பட்டது"),
    "status_blocked": T(
        "Blocked, money not sent",
        "已拦截，没有付钱",
        "Disekat, wang tidak dihantar",
        "தடுக்கப்பட்டது, பணம் அனுப்பப்படவில்லை",
    ),
    "status_cancelled": T(
        "Cancelled, money not sent",
        "已取消，没有付钱",
        "Dibatalkan, wang tidak dihantar",
        "ரத்து செய்யப்பட்டது, பணம் அனுப்பப்படவில்லை",
    ),
    "status_failed": T("Something went wrong", "出了问题", "Ada masalah", "ஏதோ தவறு நடந்தது"),

    # Verdict badges
    "vb_SAFE": T("SAFE", "安全", "SELAMAT", "பாதுகாப்பானது"),
    "vb_CHECK": T("CHECK", "需检查", "SEMAK", "சரிபார்"),
    "vb_STOP": T("STOP", "停止", "BERHENTI", "நிறுத்து"),

    # ---- Trusted contact page ----
    "hi": T("Hi {name}", "{name}，您好", "Hai {name}", "வணக்கம் {name}"),
    "contact_lead": T(
        "These are payments {elder} tried to make that need your check. The money is held, not sent, until you decide.",
        "以下是 {elder} 想付但需要您检查的款项。在您决定之前，钱会被暂停，不会付出。",
        "Ini ialah bayaran yang {elder} cuba buat dan perlu disemak oleh anda. Wang ditahan, bukan dihantar, sehingga anda membuat keputusan.",
        "இவை {elder} செய்ய முயன்ற, உங்கள் சரிபார்ப்பு தேவைப்படும் பணம் செலுத்துதல்கள். நீங்கள் முடிவு செய்யும் வரை பணம் அனுப்பப்படாமல் நிறுத்தி வைக்கப்பட்டுள்ளது.",
    ),
    "waiting_for_you": T("Waiting for you ({n})", "等待您处理（{n}）", "Menunggu anda ({n})", "உங்களுக்காகக் காத்திருக்கிறது ({n})"),
    "badge_scam": T("LIKELY SCAM", "很可能是骗局", "MUNGKIN PENIPUAN", "மோசடியாக இருக்கலாம்"),
    "badge_check": T("NEEDS A CHECK", "需要检查", "PERLU DISEMAK", "சரிபார்ப்பு தேவை"),
    "to_recipient": T("To {recipient}", "付给 {recipient}", "Kepada {recipient}", "{recipient} அவர்களுக்கு"),
    "btn_block": T("Block, don't send", "拦截，不要付", "Sekat, jangan hantar", "தடு, அனுப்ப வேண்டாம்"),
    "btn_approve": T("It's fine, send it", "没问题，付吧", "Tiada masalah, hantar", "பரவாயில்லை, அனுப்பு"),
    "contact_wait": T(
        "If you don't decide, {elder} can choose again in {wait}.",
        "如果您不决定，{elder} 在{wait}后可以重新选择。",
        "Jika anda tidak membuat keputusan, {elder} boleh memilih semula dalam {wait}.",
        "நீங்கள் முடிவு செய்யாவிட்டால், {wait} பிறகு {elder} மீண்டும் தேர்வு செய்யலாம்.",
    ),
    "nothing_waiting": T(
        "Nothing needs your check right now. This page updates by itself.",
        "目前没有需要您检查的付款。这个页面会自动更新。",
        "Tiada apa-apa yang perlu disemak sekarang. Halaman ini dikemas kini secara automatik.",
        "இப்போது சரிபார்க்க எதுவும் இல்லை. இந்தப் பக்கம் தானாகவே புதுப்பிக்கப்படும்.",
    ),
    "recent": T("Recent activity", "最近记录", "Aktiviti terkini", "சமீபத்திய நடவடிக்கைகள்"),
    "th_to": T("To", "收款人", "Kepada", "பெறுபவர்"),
    "th_amount": T("Amount", "金额", "Jumlah", "தொகை"),
    "th_check": T("Check", "检查结果", "Semakan", "சரிபார்ப்பு"),
    "th_decided": T("Decided by", "决定人", "Diputuskan oleh", "முடிவு செய்தவர்"),
    "th_result": T("Result", "结果", "Keputusan", "முடிவு"),
    "no_payments": T("No payments yet.", "还没有付款记录。", "Belum ada bayaran.", "இன்னும் பணம் செலுத்துதல்கள் இல்லை."),

    # ---- Settings ----
    "settings_lead": T(
        "Set this up together with the person you're protecting.",
        "请和您要保护的人一起设置。",
        "Tetapkan ini bersama orang yang anda lindungi.",
        "நீங்கள் பாதுகாக்கும் நபருடன் சேர்ந்து இதை அமைக்கவும்.",
    ),
    "s_elder": T(
        "Name of the person being protected",
        "被保护者的名字",
        "Nama orang yang dilindungi",
        "பாதுகாக்கப்படும் நபரின் பெயர்",
    ),
    "s_contact_hint": T(
        "A family member, friend, neighbour, caregiver or community volunteer.",
        "家人、朋友、邻居、看护或社区义工都可以。",
        "Ahli keluarga, kawan, jiran, penjaga atau sukarelawan komuniti.",
        "குடும்ப உறுப்பினர், நண்பர், அண்டை வீட்டார், பராமரிப்பாளர் அல்லது சமூகத் தன்னார்வலர்.",
    ),
    "s_payees": T("Trusted payees", "信任的收款人", "Penerima yang dipercayai", "நம்பகமான பணம் பெறுபவர்கள்"),
    "s_payees_hint": T(
        "People and shops they pay often, separated by commas. Small payments to these go straight through.",
        "经常付钱的人和店，用逗号分开。付给他们的小额款项会直接付出。",
        "Orang dan kedai yang kerap dibayar, dipisahkan dengan koma. Bayaran kecil kepada mereka akan terus dihantar.",
        "அடிக்கடி பணம் செலுத்தும் நபர்கள் மற்றும் கடைகள், காற்புள்ளியால் பிரிக்கவும். இவர்களுக்கான சிறிய தொகைகள் நேரடியாக அனுப்பப்படும்.",
    ),
    "s_limit": T("Usual payment limit ($)", "平时的付款上限（$）", "Had bayaran biasa ($)", "வழக்கமான பணம் செலுத்தும் வரம்பு ($)"),
    "s_limit_hint": T(
        "Payments to new people above this amount are held for a check.",
        "付给新收款人且超过这个金额的付款，会先暂停检查。",
        "Bayaran kepada orang baru melebihi jumlah ini akan ditahan untuk disemak.",
        "புதிய நபர்களுக்கு இந்தத் தொகைக்கு மேல் செலுத்தப்படும் பணம் சரிபார்ப்புக்காக நிறுத்தி வைக்கப்படும்.",
    ),
    "s_cool": T("Cooling-off time (minutes)", "冷静期（分钟）", "Tempoh bertenang (minit)", "காத்திருப்பு நேரம் (நிமிடங்கள்)"),
    "s_cool_hint": T(
        "If the trusted contact doesn't answer, how long a held payment waits before the person can choose again. 1440 = 24 hours. Use 1 for a quick demo.",
        "如果信任联系人没有回应，暂停的付款要等多久，被保护者才能重新选择。1440 = 24 小时。快速演示可以填 1。",
        "Jika kenalan dipercayai tidak menjawab, berapa lama bayaran yang ditahan menunggu sebelum orang itu boleh memilih semula. 1440 = 24 jam. Gunakan 1 untuk demo pantas.",
        "நம்பகமான தொடர்பு பதிலளிக்காவிட்டால், அந்த நபர் மீண்டும் தேர்வு செய்வதற்கு முன் நிறுத்தி வைக்கப்பட்ட பணம் எவ்வளவு நேரம் காத்திருக்கும். 1440 = 24 மணி நேரம். விரைவான டெமோவுக்கு 1 ஐப் பயன்படுத்தவும்.",
    ),
    "btn_save": T("Save settings", "保存设置", "Simpan tetapan", "அமைப்புகளைச் சேமி"),
    "s_ai_check": T("AI check", "人工智能检查", "Semakan AI", "AI சரிபார்ப்பு"),
    "s_ai_off": T(
        "not set up, using safety rules only",
        "未设置，只用安全规则",
        "belum disediakan, guna peraturan keselamatan sahaja",
        "அமைக்கப்படவில்லை, பாதுகாப்பு விதிகள் மட்டும்",
    ),
    "s_pp_ok": T("keys found", "已找到密钥", "kunci dijumpai", "விசைகள் உள்ளன"),
    "s_pp_missing": T("keys missing", "缺少密钥", "kunci tiada", "விசைகள் இல்லை"),
    "s_test": T("Test connections", "测试连接", "Uji sambungan", "இணைப்புகளைச் சோதி"),
}


# Safety-rule reasons and tips: name -> (reason, tip)
RULE_TEXT = {
    "authority": (
        T(
            "The message says it is from the police, a bank or the government.",
            "信息自称来自警方、银行或政府。",
            "Mesej ini mengaku datang daripada polis, bank atau kerajaan.",
            "இந்தச் செய்தி காவல்துறை, வங்கி அல்லது அரசாங்கத்திடமிருந்து வந்ததாகச் சொல்கிறது.",
        ),
        T(
            "Real police, banks and government officers will never ask you to transfer money.",
            "真正的警察、银行和政府人员绝对不会叫您转钱。",
            "Polis, bank dan pegawai kerajaan yang sebenar tidak akan meminta anda memindahkan wang.",
            "உண்மையான காவல்துறை, வங்கிகள் மற்றும் அரசு அதிகாரிகள் ஒருபோதும் பணம் அனுப்பச் சொல்ல மாட்டார்கள்.",
        ),
    ),
    "safe_account": (
        T(
            "It asks you to move money to keep it 'safe'.",
            "叫您把钱转去「安全」的地方。",
            "Ia meminta anda memindahkan wang supaya 'selamat'.",
            "பணத்தை 'பாதுகாப்பாக' வைக்க அதை மாற்றச் சொல்கிறது.",
        ),
        T(
            "There is no such thing as a 'safe account'. This is one of the most common scams.",
            "根本没有所谓的「安全账户」。这是最常见的骗局之一。",
            "Tiada apa yang dipanggil 'akaun selamat'. Ini salah satu penipuan yang paling biasa.",
            "'பாதுகாப்பான கணக்கு' என்று எதுவும் இல்லை. இது மிகவும் பொதுவான மோசடிகளில் ஒன்று.",
        ),
    ),
    "secrecy": (
        T(
            "It asks you to keep this a secret.",
            "叫您不要告诉别人。",
            "Ia meminta anda merahsiakan perkara ini.",
            "இதை ரகசியமாக வைக்கச் சொல்கிறது.",
        ),
        T(
            "Scammers ask for secrecy so your family cannot warn you.",
            "骗子叫您保密，是为了不让家人提醒您。",
            "Penipu meminta anda berahsia supaya keluarga tidak dapat memberi amaran.",
            "உங்கள் குடும்பத்தினர் உங்களை எச்சரிக்காமல் இருக்க மோசடியாளர்கள் ரகசியம் கேட்கிறார்கள்.",
        ),
    ),
    "new_number": (
        T(
            "Someone claims to be family using a new phone number.",
            "有人用新号码，自称是您的家人。",
            "Seseorang mengaku ahli keluarga menggunakan nombor telefon baru.",
            "யாரோ புதிய தொலைபேசி எண்ணிலிருந்து குடும்ப உறுப்பினர் என்று சொல்கிறார்கள்.",
        ),
        T(
            "Call your family member on their OLD number to check it is really them.",
            "请打家人的「旧号码」，确认真的是他们。",
            "Hubungi ahli keluarga anda di nombor LAMA mereka untuk memastikan ia benar-benar mereka.",
            "அது உண்மையில் அவர்கள்தானா என்று உறுதிப்படுத்த, உங்கள் குடும்ப உறுப்பினரின் பழைய எண்ணுக்கு அழைக்கவும்.",
        ),
    ),
    "urgency": (
        T(
            "It is rushing you to pay quickly.",
            "催您赶快付钱。",
            "Ia mendesak anda membayar dengan cepat.",
            "விரைவாகப் பணம் செலுத்த உங்களை அவசரப்படுத்துகிறது.",
        ),
        T(
            "Scammers rush you so you don't have time to think or ask someone.",
            "骗子会催您，让您没时间想清楚或问别人。",
            "Penipu mendesak anda supaya tiada masa untuk berfikir atau bertanya.",
            "யோசிக்கவோ யாரிடமாவது கேட்கவோ நேரம் இல்லாமல் இருக்க மோசடியாளர்கள் அவசரப்படுத்துகிறார்கள்.",
        ),
    ),
    "trouble": (
        T(
            "It describes an emergency to make you worried.",
            "说有紧急事情，让您担心。",
            "Ia menceritakan kecemasan untuk membuat anda risau.",
            "உங்களைக் கவலைப்பட வைக்க ஒரு அவசரநிலையை விவரிக்கிறது.",
        ),
        T(
            "Emergency stories are used to make you panic. Check with family first.",
            "骗子编紧急故事让您慌张。请先和家人确认。",
            "Cerita kecemasan digunakan untuk membuat anda panik. Semak dengan keluarga dahulu.",
            "உங்களைப் பதற வைக்க அவசரக் கதைகள் பயன்படுத்தப்படுகின்றன. முதலில் குடும்பத்தினரிடம் சரிபார்க்கவும்.",
        ),
    ),
    "gift_crypto": (
        T(
            "It asks for gift cards or cryptocurrency.",
            "要您用礼品卡或加密货币付钱。",
            "Ia meminta kad hadiah atau mata wang kripto.",
            "பரிசு அட்டைகள் அல்லது கிரிப்டோகரன்சி கேட்கிறது.",
        ),
        T(
            "Real organisations never ask to be paid in gift cards or crypto.",
            "正规机构绝对不会要您用礼品卡或加密货币付款。",
            "Organisasi sebenar tidak pernah meminta bayaran dengan kad hadiah atau kripto.",
            "உண்மையான நிறுவனங்கள் பரிசு அட்டைகள் அல்லது கிரிப்டோவில் பணம் கேட்பதில்லை.",
        ),
    ),
    "investment": (
        T(
            "It promises easy or guaranteed profits.",
            "保证让您轻松赚钱。",
            "Ia menjanjikan keuntungan mudah atau terjamin.",
            "எளிதான அல்லது உத்தரவாதமான லாபத்தை வாக்களிக்கிறது.",
        ),
        T(
            "Guaranteed high returns are a classic sign of an investment scam.",
            "「保证高回报」是投资骗局的典型特征。",
            "Pulangan tinggi yang dijamin ialah tanda biasa penipuan pelaburan.",
            "உத்தரவாதமான அதிக லாபம் முதலீட்டு மோசடியின் வழக்கமான அறிகுறி.",
        ),
    ),
    "prize": (
        T(
            "It says you won something but must pay first.",
            "说您中奖了，但要先付钱。",
            "Ia mengatakan anda menang sesuatu tetapi perlu bayar dahulu.",
            "நீங்கள் ஏதோ வென்றதாகவும், ஆனால் முதலில் பணம் செலுத்த வேண்டும் என்றும் சொல்கிறது.",
        ),
        T(
            "If you have to pay to receive a prize, it is not a real prize.",
            "要先付钱才能领的奖，不是真的奖。",
            "Jika anda perlu bayar untuk menerima hadiah, ia bukan hadiah sebenar.",
            "பரிசைப் பெற பணம் செலுத்த வேண்டும் என்றால், அது உண்மையான பரிசு அல்ல.",
        ),
    ),
    "deposit": (
        T(
            "A seller wants a deposit before you see the item.",
            "卖家要您在看到东西之前先付订金。",
            "Penjual mahu deposit sebelum anda melihat barang.",
            "பொருளைப் பார்ப்பதற்கு முன்பே விற்பனையாளர் முன்பணம் கேட்கிறார்.",
        ),
        T(
            "Online sellers who demand deposits first are a common scam. Pay on delivery.",
            "网上卖家要求先付订金是常见骗局。最好货到付款。",
            "Penjual dalam talian yang meminta deposit dahulu ialah penipuan biasa. Bayar semasa penghantaran.",
            "முதலில் முன்பணம் கேட்கும் இணைய விற்பனையாளர்கள் ஒரு பொதுவான மோசடி. பொருள் கிடைத்ததும் பணம் செலுத்துங்கள்.",
        ),
    ),
    "love": (
        T(
            "Someone you may not have met in person is asking for money.",
            "一个您可能没见过面的人在向您要钱。",
            "Seseorang yang mungkin belum pernah anda temui sedang meminta wang.",
            "நீங்கள் நேரில் சந்திக்காத ஒருவர் பணம் கேட்கிறார்.",
        ),
        T(
            "People met online who ask for money are often romance scammers.",
            "在网上认识又向您要钱的人，常常是感情骗子。",
            "Orang yang dikenali dalam talian dan meminta wang selalunya penipu cinta.",
            "இணையத்தில் சந்தித்துப் பணம் கேட்பவர்கள் பெரும்பாலும் காதல் மோசடியாளர்கள்.",
        ),
    ),
    "injection": (
        T(
            "The message contains text that tries to trick the safety check.",
            "信息里有试图欺骗安全检查的文字。",
            "Mesej ini mengandungi teks yang cuba menipu semakan keselamatan.",
            "பாதுகாப்புச் சரிபார்ப்பை ஏமாற்ற முயலும் உரை இந்தச் செய்தியில் உள்ளது.",
        ),
        T(
            "Normal messages never talk to safety software. This is a strong scam sign.",
            "正常的信息不会对安全软件说话。这是很明显的骗局迹象。",
            "Mesej biasa tidak bercakap dengan perisian keselamatan. Ini tanda penipuan yang kuat.",
            "சாதாரணச் செய்திகள் பாதுகாப்பு மென்பொருளுடன் பேசுவதில்லை. இது ஒரு வலுவான மோசடி அறிகுறி.",
        ),
    ),
}

AMOUNT_TEXT = {
    "large_amount": T(
        "{amount} is a large amount to a new person.",
        "付 {amount} 给新的收款人，金额很大。",
        "{amount} ialah jumlah yang besar kepada orang baru.",
        "புதிய நபருக்கு {amount} என்பது பெரிய தொகை.",
    ),
    "above_limit": T(
        "This person is not on your trusted list and {amount} is above your usual limit.",
        "这个人不在您的信任名单上，而且 {amount} 超过您平时的上限。",
        "Orang ini tiada dalam senarai dipercayai anda dan {amount} melebihi had biasa anda.",
        "இந்த நபர் உங்கள் நம்பகமான பட்டியலில் இல்லை, மேலும் {amount} உங்கள் வழக்கமான வரம்பை விட அதிகம்.",
    ),
    "trusted": T(
        "{recipient} is on your trusted list.",
        "{recipient} 在您的信任名单上。",
        "{recipient} ada dalam senarai dipercayai anda.",
        "{recipient} உங்கள் நம்பகமான பட்டியலில் உள்ளார்.",
    ),
    "nothing": T(
        "Nothing unusual was found.",
        "没有发现不寻常的地方。",
        "Tiada apa-apa yang luar biasa dijumpai.",
        "அசாதாரணமான எதுவும் கண்டறியப்படவில்லை.",
    ),
}


# Demo scenarios, written in each language so you can show the AI
# catching scams that aren't in English.
DEMOS = [
    {
        "label": "demo_hawker",
        "amount": "12",
        "recipient": T("Uncle Tan Chicken Rice", "Uncle Tan Chicken Rice", "Uncle Tan Chicken Rice", "Uncle Tan Chicken Rice"),
        "reason": T("Food", "买食物", "Makanan", "உணவு"),
        "message": T("", "", "", ""),
    },
    {
        "label": "demo_police",
        "amount": "2000",
        "recipient": T("Inspector Lim", "林督察", "Inspektor Lim", "ஆய்வாளர் லிம்"),
        "reason": T("Police said to", "警察叫我转的", "Polis suruh", "காவல்துறை சொன்னது"),
        "message": T(
            "This is Inspector Lim from the Singapore Police Force. Your bank account is linked to money "
            "laundering. To protect your savings you must transfer $2,000 to a safe account now or you will "
            "be arrested today. Do not tell anyone, this investigation is confidential.",
            "我是新加坡警察部队的林督察。您的银行账户涉及洗钱案件。为了保护您的存款，您必须马上把 $2,000 "
            "转到安全账户，否则今天就会被逮捕。不要告诉任何人，这是机密调查。",
            "Ini Inspektor Lim dari Pasukan Polis Singapura. Akaun bank anda dikaitkan dengan pengubahan wang "
            "haram. Untuk melindungi simpanan anda, anda mesti memindahkan $2,000 ke akaun selamat sekarang "
            "atau anda akan ditangkap hari ini. Jangan beritahu sesiapa, siasatan ini sulit.",
            "நான் சிங்கப்பூர் காவல்துறையைச் சேர்ந்த ஆய்வாளர் லிம். உங்கள் வங்கிக் கணக்கு பணமோசடியுடன் "
            "தொடர்புடையது. உங்கள் சேமிப்பைப் பாதுகாக்க, நீங்கள் உடனே $2,000 ஐ ஒரு பாதுகாப்பான கணக்குக்கு "
            "மாற்ற வேண்டும், இல்லையென்றால் இன்றே கைது செய்யப்படுவீர்கள். யாரிடமும் சொல்ல வேண்டாம், இது ரகசிய விசாரணை.",
        ),
    },
    {
        "label": "demo_grandson",
        "amount": "800",
        "recipient": T("Grandson (new number)", "孙子（新号码）", "Cucu (nombor baru)", "பேரன் (புதிய எண்)"),
        "reason": T("Family emergency", "家里急事", "Kecemasan keluarga", "குடும்ப அவசரம்"),
        "message": T(
            "Ah Ma it's me, I lost my phone so this is my new number. I'm in trouble, I had an accident and "
            "need $800 urgently for the hospital. Please don't tell Mum, I'll explain later.",
            "阿嬷，是我啊，我手机丢了，这是我的新号码。我出事了，出了车祸，急需 $800 付医院的钱。"
            "请不要告诉妈妈，我以后再解释。",
            "Nenek, ini saya. Telefon saya hilang, ini nombor baru saya. Saya dalam kesusahan, saya "
            "kemalangan dan perlukan $800 segera untuk hospital. Tolong jangan beritahu Mak, nanti saya terangkan.",
            "பாட்டி, நான்தான். என் போன் தொலைந்துவிட்டது, இது என் புதிய எண். நான் சிக்கலில் இருக்கிறேன், "
            "விபத்து நடந்தது, மருத்துவமனைக்கு அவசரமாக $800 வேண்டும். அம்மாவிடம் சொல்ல வேண்டாம், பிறகு விளக்குகிறேன்.",
        ),
    },
    {
        "label": "demo_seller",
        "amount": "300",
        "recipient": T("Carousell seller", "Carousell 卖家", "Penjual Carousell", "Carousell விற்பனையாளர்"),
        "reason": T("Buying a phone", "买手机", "Beli telefon", "போன் வாங்க"),
        "message": T(
            "Hi, the phone is still available. Many buyers want it, so pay $300 deposit first to reserve it. "
            "I will deliver next week.",
            "你好，手机还在。很多人要，所以请先付 $300 订金帮你留着。我下个星期送货。",
            "Hai, telefon itu masih ada. Ramai pembeli mahu, jadi bayar deposit $300 dahulu untuk menempahnya. "
            "Saya akan hantar minggu depan.",
            "வணக்கம், போன் இன்னும் இருக்கிறது. நிறைய பேர் கேட்கிறார்கள், அதனால் அதை ஒதுக்கி வைக்க முதலில் "
            "$300 முன்பணம் அனுப்புங்கள். அடுத்த வாரம் டெலிவரி செய்கிறேன்.",
        ),
    },
]


def translate(key, lang, **values):
    """Look up a word or sentence. Falls back to English, then to the key itself."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry["en"]
    try:
        return text.format(**values)
    except (KeyError, IndexError, ValueError):
        return text


def pick(value, lang):
    """Pick one language from a {"en": ..., "zh": ...} dict. Plain strings pass through."""
    if isinstance(value, dict):
        return value.get(lang) or value.get("en") or ""
    return value or ""


def demo_scenarios(lang):
    return [
        {
            "label": translate(d["label"], lang),
            "amount": d["amount"],
            "recipient": pick(d["recipient"], lang),
            "reason": pick(d["reason"], lang),
            "message": pick(d["message"], lang),
        }
        for d in DEMOS
    ]

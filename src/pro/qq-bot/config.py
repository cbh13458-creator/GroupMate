import os

from dotenv import load_dotenv

load_dotenv()

# QQ 机器人
QQ_APP_ID = os.getenv("QQ_APP_ID", "")
QQ_APP_SECRET = os.getenv("QQ_APP_SECRET", "")

# AI 大模型（OpenAI 兼容接口）
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
AI_MODEL = os.getenv("AI_MODEL", "glm-4.7-flash")
# 主模型过载/限流时自动切换的备用模型（留空则自动：智谱降级到 glm-4-flash）
AI_FALLBACK_MODEL = os.getenv("AI_FALLBACK_MODEL", "")
# 视觉模型（识别图片/表情包，免费）
AI_VISION_MODEL = os.getenv("AI_VISION_MODEL", "glm-4.6v-flash")
AI_SYSTEM_PROMPT = os.getenv("AI_SYSTEM_PROMPT", "你是一个真人朋友，在 QQ 上和用户闲聊，不是 AI 助手、词典或百科。铁规矩：绝不解释词语含义、不下定义、不说“XX是指”这类百科式的话；用户说什么，你就像朋友一样接话——表达感受、顺着聊、反问、开玩笑、吐槽都行。回复要像真人发消息，一两句为主，口语化，别长篇大论、别用“首先/其次/最后”，不要用列表、编号、加粗或任何 Markdown 格式。用户只发一两个词时，别当题目去解答，先接住话往下聊。例：用户说“朋友”，别解释朋友是什么，回“哈哈怎么突然聊这个，想谁啦”；用户说“今天好累”，回“咋啦，干啥了这么累”。")
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2048"))
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))

# ============ 人味模式 ============
# 长回复拆成 2~3 条短消息、带随机“打字”延迟发出去，像真人一条条敲；
# 关掉则和以前一样整段一次性发出。
HUMAN_MODE = os.getenv("HUMAN_MODE", "true").lower() in ("1", "true", "yes", "on")
# 最多拆成几条（QQ 被动回复有次数上限，别设太大）
HUMAN_SPLIT_MAX = int(os.getenv("HUMAN_SPLIT_MAX", "3"))
# 超过多少字才拆（太短就一条发完，避免“嗯”“啊”也拆）
HUMAN_SPLIT_MIN_LEN = int(os.getenv("HUMAN_SPLIT_MIN_LEN", "28"))
# 每条消息发出前的随机延迟区间（秒），模拟看消息 + 打字的停顿
HUMAN_DELAY_MIN = float(os.getenv("HUMAN_DELAY_MIN", "0.4"))
HUMAN_DELAY_MAX = float(os.getenv("HUMAN_DELAY_MAX", "1.2"))
# 语音模式也分条：一条语音别念太久，拆成几条短语音发出去
HUMAN_VOICE_SPLIT = os.getenv("HUMAN_VOICE_SPLIT", "true").lower() in ("1", "true", "yes", "on")
# 每条语音最多念多少字
HUMAN_VOICE_PART_MAX = int(os.getenv("HUMAN_VOICE_PART_MAX", "38"))
# 一条回复最多拆成几条语音
HUMAN_VOICE_MAX_PARTS = int(os.getenv("HUMAN_VOICE_MAX_PARTS", "3"))

# 联网搜索（默认开启）
AI_WEB_SEARCH = os.getenv("AI_WEB_SEARCH", "true").lower() in ("1", "true", "yes", "on")
# 发送表情包 / 找图（默认开启）
ENABLE_IMAGE_SEND = os.getenv("ENABLE_IMAGE_SEND", "true").lower() in ("1", "true", "yes", "on")
# 搜索提供方：bing=免费必应（默认，无需额外 Key）/ zhipu=智谱 Web Search（按次计费）
AI_SEARCH_PROVIDER = os.getenv("AI_SEARCH_PROVIDER", "bing").lower()
# 智谱搜索引擎：search_pro_sogou（搜狗，推荐）/ search_pro_quark（夸克）/ search_pro（智谱自研，中文结果较差）
AI_SEARCH_ENGINE = os.getenv("AI_SEARCH_ENGINE", "search_pro_sogou")
# 智谱联网搜索接口地址
AI_SEARCH_BASE_URL = os.getenv("AI_SEARCH_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/web_search")
# 必应免费搜索地址（RSS 结果，无需 Key）
AI_SEARCH_BING_URL = os.getenv("AI_SEARCH_BING_URL", "https://cn.bing.com/search")

# 企业微信自建应用
WECOM_CORP_ID = os.getenv("WECOM_CORP_ID", "")
WECOM_AGENT_ID = os.getenv("WECOM_AGENT_ID", "")
WECOM_SECRET = os.getenv("WECOM_SECRET", "")
WECOM_TOKEN = os.getenv("WECOM_TOKEN", "")
WECOM_ENCODING_AES_KEY = os.getenv("WECOM_ENCODING_AES_KEY", "")
WECOM_PORT = int(os.getenv("WECOM_PORT", "8787"))
WECOM_PATH = os.getenv("WECOM_PATH", "/wecom")

# ============ QQ 独占：摸摸互动 ============
ENABLE_PAT = os.getenv("ENABLE_PAT", "true").lower() in ("1", "true", "yes", "on")

# ============ 群内功能目录 ============
# @机器人发「菜单 / 目录 / 帮助」返回功能目录
ENABLE_MENU = os.getenv("ENABLE_MENU", "true").lower() in ("1", "true", "yes", "on")

# ============ 群互动（QQ 独占）============
# 签到 / 积分排行榜 / 群热词，数据存在 qq-bot/groupstats.json
ENABLE_GROUP_TOOLS = os.getenv("ENABLE_GROUP_TOOLS", "true").lower() in ("1", "true", "yes", "on")

# ============ 版本更新推送 ============
# 检测到 GitHub 有新版本时，自动推送到记录过的群和私聊（同一版本只推一次）
ENABLE_UPDATE_PUSH = os.getenv("ENABLE_UPDATE_PUSH", "true").lower() in ("1", "true", "yes", "on")
UPDATE_CHECK_INTERVAL_HOURS = int(os.getenv("UPDATE_CHECK_INTERVAL_HOURS", "6"))
GITHUB_REPO = os.getenv("GITHUB_REPO", "cbh13458-creator/GroupMate")

# ============ QQ 独占：定时消息 ============
SCHEDULE_ENABLED = os.getenv("SCHEDULE_ENABLED", "true").lower() in ("1", "true", "yes", "on")

# ============ 管理面板 ============
PANEL_HOST = os.getenv("PANEL_HOST", "127.0.0.1")
PANEL_PORT = int(os.getenv("PANEL_PORT", "8080"))
# 面板登录密码：留空时仅允许本机(127.0.0.1)访问；一旦 PANEL_HOST=0.0.0.0 必须设置密码，否则面板拒绝启动
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD", "")

# ============ 语音回复 ============
# 语音总开关（关掉后 /语音 指令不再生效）
ENABLE_TTS = os.getenv("ENABLE_TTS", "true").lower() in ("1", "true", "yes", "on")
# 单条语音最多合成多少字（太长会慢，也可能超过 QQ 语音时长限制）
TTS_MAX_CHARS = int(os.getenv("TTS_MAX_CHARS", "120"))
# 合成超时（秒）
TTS_TIMEOUT = int(os.getenv("TTS_TIMEOUT", "20"))
# 可选：单独给 TTS 用的代理（留空则跟随 HTTPS_PROXY）
TTS_PROXY = os.getenv("TTS_PROXY", "")

# ============ 记忆与限额 ============
# 每个会话保留的历史消息条数（一问一答算 2 条）
AI_MEMORY_MESSAGES = int(os.getenv("AI_MEMORY_MESSAGES", "20"))
# 每人每分钟最多触发 AI 回复的次数（0=不限制）
AI_RATE_PER_MINUTE = int(os.getenv("AI_RATE_PER_MINUTE", "6"))
# 每人每天最多触发 AI 回复的次数（0=不限制）
AI_RATE_PER_DAY = int(os.getenv("AI_RATE_PER_DAY", "200"))
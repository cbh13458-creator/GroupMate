"""语音合成与音色管理。

把文字用 edge-tts 合成 MP3，再由 main.py 通过 QQ 官方富媒体接口
（file_type=3，语音支持 silk / wav / mp3 / flac）发成 QQ 语音消息。
"""

from __future__ import annotations

import asyncio
import json
import os
import re

try:  # 没装 edge-tts 时不要让整个机器人起不来，语音退回文字即可
    import edge_tts
except ImportError:  # pragma: no cover
    edge_tts = None

import config

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voices.json")

# 音色预设：名字 -> edge-tts 声音 / 语速 / 音调
VOICE_PRESETS: dict[str, dict[str, str]] = {
    "猫娘": {"voice": "zh-CN-XiaoyiNeural", "rate": "+8%", "pitch": "+30Hz", "desc": "软软的小猫娘"},
    "少女": {"voice": "zh-CN-XiaoyiNeural", "rate": "+2%", "pitch": "+14Hz", "desc": "清亮的少女音"},
    "御姐": {"voice": "zh-CN-XiaoxiaoNeural", "rate": "-6%", "pitch": "-14Hz", "desc": "低沉的御姐音"},
    "幻想乡": {"voice": "zh-CN-XiaoyiNeural", "rate": "-6%", "pitch": "+70Hz", "desc": "油库里那种高音软萌"},
    "元气": {"voice": "zh-CN-XiaoyiNeural", "rate": "+16%", "pitch": "+8Hz", "desc": "元气满满的群友"},
    "正太": {"voice": "zh-CN-YunxiaNeural", "rate": "+6%", "pitch": "+22Hz", "desc": "软糯的正太音"},
    "少年": {"voice": "zh-CN-YunxiNeural", "rate": "0%", "pitch": "+6Hz", "desc": "干净的少年音"},
    "旁白": {"voice": "zh-CN-YunjianNeural", "rate": "-4%", "pitch": "-16Hz", "desc": "讲故事的大叔音"},
}

# 口语化别名
ALIASES = {
    "猫": "猫娘", "猫猫": "猫娘", "喵": "猫娘", "mao": "猫娘", "neko": "猫娘",
    "二次元": "幻想乡", "幻想": "幻想乡", "乡": "幻想乡", "gensokyo": "幻想乡",
    "油库里": "幻想乡", "油库": "幻想乡", "ゆっくり": "幻想乡", "yukkuri": "幻想乡", "馒头": "幻想乡",
    "姐姐": "御姐", "女王": "御姐", "萝莉": "少女", "萌": "少女",
    "热血": "元气", "男": "少年", "大叔": "旁白",
}

DEFAULT_VOICE = "猫娘"


def _read_state() -> dict:
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _write_state(state: dict) -> None:
    try:
        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, STATE_FILE)
    except OSError:
        pass


def _setting(session_id: str) -> dict:
    state = _read_state()
    item = state.get(session_id) or {}
    if not isinstance(item, dict):
        item = {}
    return {
        "enabled": bool(item.get("enabled", False)),
        "voice": normalize_voice(item.get("voice") or DEFAULT_VOICE),
    }


def enabled(session_id: str) -> bool:
    return _setting(session_id)["enabled"]


def get_voice(session_id: str) -> str:
    return _setting(session_id)["voice"]


def set_enabled(session_id: str, value: bool) -> None:
    state = _read_state()
    item = state.get(session_id) or {}
    item["enabled"] = bool(value)
    item.setdefault("voice", DEFAULT_VOICE)
    state[session_id] = item
    _write_state(state)


def set_voice(session_id: str, name: str) -> str:
    voice = normalize_voice(name)
    state = _read_state()
    item = state.get(session_id) or {}
    item["voice"] = voice
    state[session_id] = item
    _write_state(state)
    return voice


def resolve_voice(name: str) -> str | None:
    """把音色名或别名解析成预设名，认不出返回 None。"""
    name = (name or "").strip()
    if name in VOICE_PRESETS:
        return name
    return ALIASES.get(name.lower())


def normalize_voice(name: str) -> str:
    return resolve_voice(name) or DEFAULT_VOICE


def voice_list_text() -> str:
    lines = ["可用音色："]
    for name, preset in VOICE_PRESETS.items():
        lines.append(f"· {name} —— {preset['desc']}")
    lines.append("")
    lines.append("切换：/语音 猫娘　关闭：/语音 关")
    return "\n".join(lines)


def status_text(session_id: str) -> str:
    item = _setting(session_id)
    state = "开启" if item["enabled"] else "关闭"
    preset = VOICE_PRESETS[item["voice"]]
    lines = [
        f"语音回复：{state}",
        f"当前音色：{item['voice']}（{preset['desc']}）",
        "",
        "开启：/语音 开　关闭：/语音 关",
        "换音色：/语音 幻想乡　看全部：/音色",
    ]
    return "\n".join(lines)


_URL_RE = re.compile(r"https?://\S+")
_MD_RE = re.compile(r"[*_`#>]+")
_BRACKET_RE = re.compile(r"\[[^\]]{0,12}\]")


def clean_for_tts(text: str) -> str:
    text = _URL_RE.sub("", text or "")
    text = _MD_RE.sub("", text)
    text = _BRACKET_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    limit = max(20, int(config.TTS_MAX_CHARS))
    if len(text) > limit:
        text = text[:limit].rstrip("，,。.！!？?；;：: ") + "…"
    return text


async def synth(text: str, voice_name: str) -> bytes:
    """合成 MP3 字节。失败会抛异常，由调用方决定是否退回文字。"""
    content = clean_for_tts(text)
    if not content:
        raise ValueError("没有可合成的内容")
    if edge_tts is None:
        raise RuntimeError("未安装 edge-tts（pip install edge-tts）")
    preset = VOICE_PRESETS[normalize_voice(voice_name)]
    proxy = config.TTS_PROXY or os.getenv("HTTPS_PROXY") or os.getenv("https_proxy") or None
    communicate = edge_tts.Communicate(
        content,
        preset["voice"],
        rate=preset["rate"],
        pitch=preset["pitch"],
        proxy=proxy,
    )
    audio = bytearray()
    async with asyncio.timeout(max(10, int(config.TTS_TIMEOUT))):
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
    if not audio:
        raise RuntimeError("语音合成返回为空")
    return bytes(audio)

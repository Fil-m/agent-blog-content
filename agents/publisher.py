#!/usr/bin/env python3
"""
Publisher Agent — Рівень 5 системи + доставка.

Вхід: published/*.md + published/*.meta.yaml
Вихід: Telegram пост з картинкою

Візуальна система — шаблони карток:
  🥇 achievement → gold (#FFD700)
  🔵 discovery → blue (#4A90D9)
  ❌ failure → red (#E74C3C)
  🟣 progress → purple (#9B59B6)
  📘 lesson → dark (#2C3E50)
"""

import yaml
from datetime import date
from pathlib import Path
import subprocess
import os
import json

PUBLISHED_DIR = Path("published")
TEMPLATES_DIR = Path("templates")

# Візуальна система — кольори
CARD_COLORS = {
    "achievement": {"name": "gold", "hex": "#FFD700", "emoji": "🥇"},
    "discovery": {"name": "blue", "hex": "#4A90D9", "emoji": "🔵"},
    "failure": {"name": "red", "hex": "#E74C3C", "emoji": "❌"},
    "progress": {"name": "purple", "hex": "#9B59B6", "emoji": "🟣"},
    "lesson": {"name": "dark", "hex": "#2C3E50", "emoji": "📘"},
}

FORMAT_NAMES = {
    "news": "📰 Новина",
    "lesson": "📚 Урок",
    "mistake": "💥 Помилка",
    "insight": "💡 Інсайт",
    "bts": "🎬 Behind the Scenes",
    "future": "🔮 Майбутнє",
}


def generate_card_image(post_data: dict, output_path: str) -> str:
    """
    Згенерувати картку-зображення для поста.
    
    Використовує шаблонну систему:
    - Тло: колір за типом події
    - Іконка формату зверху ліворуч
    - Заголовок по центру
    - Емодзі персонажа + ім'я знизу
    """
    
    etype = post_data.get("_type", "lesson")
    fmt = post_data.get("_format", "news")
    color = CARD_COLORS.get(etype, CARD_COLORS["lesson"])
    
    # Текст для картинки
    title = post_data.get("headline", "")[:80]
    
    # Спроба згенерувати через ComfyUI/API
    # Якщо є image_prompt — використовуємо його
    custom_prompt = post_data.get("_image_prompt", "")
    
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = (
            f"Modern social media card, {color['name']} background with "
            f"gradient, {color['emoji']} icon top left, "
            f"text: '{title}', minimalist typography, "
            f"tech AI theme, no people, 16:9"
        )
    
    # Try image generation via our tools
    # For now, return the prompt — actual generation 
    # happens in the cron job context where we have access
    return prompt


def load_published(today: date = None):
    """Завантажити опубліковані пости."""
    if today is None:
        today = date.today()
    
    posts = []
    for meta_path in sorted(PUBLISHED_DIR.glob(f"{today.isoformat()}_*.meta.yaml")):
        with open(meta_path) as f:
            meta = yaml.safe_load(f)
        
        text_path = meta.get("file", "")
        text = ""
        if text_path:
            tp = Path(text_path)
            if tp.exists():
                text = tp.read_text()
        
        posts.append({"meta": meta, "text": text})
    
    return posts


def publish_to_telegram(post_text: str, image_path: str = None):
    """
    Публікація в Telegram.
    
    Використовує Hermes send_message tool.
    Викликається як зовнішня команда через hermes CLI або
    через наш cron-контекст.
    """
    # У cron-контексті цю команду виконає сам Hermes
    # Тут просто повертаємо дані для cron-джоба
    return {
        "text": post_text,
        "image": image_path,
        "channel": "agent-blog",  # буде замінено на реальний @channel
    }


def main():
    today = date.today()
    posts = load_published(today)
    
    if not posts:
        print(f"📭 Немає опублікованих постів за {today.isoformat()}")
        return
    
    print(f"📤 Паблішер: {len(posts)} постів до публікації\n")
    
    for p in posts:
        meta = p.get("meta", {})
        text = p.get("text", "")
        
        etype = meta.get("_type", "?")
        fmt = meta.get("_format", "?")
        agent = meta.get("_agent", "?")
        impact = meta.get("_impact", "?")
        
        color = CARD_COLORS.get(etype, {})
        fmt_name = FORMAT_NAMES.get(fmt, fmt)
        
        print(f"{color.get('emoji', '📄')} {fmt_name}")
        print(f"   Агент: {agent} | Вплив: {impact}")
        print(f"   Текст: {len(text)} символів")
        
        # Try generate image
        prompt = generate_card_image(meta, str(today))
        print(f"   🎨 Промпт: {prompt[:60]}...")
        
        # Output для cron-джоба
        print(f"\n--- DRAFT START ---")
        print(text)
        print(f"--- DRAFT END ---")
        print(f"\n📍 Для публікації в Telegram виконати:")
        print(f"   send_message(text=..., image=generate(...))")
        print()
    
    print("✅ Готово!")

if __name__ == "__main__":
    main()

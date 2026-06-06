#!/usr/bin/env python3
"""
Storyteller Agent — Рівень 4 системи.

Вхід: drafts/*.yaml (схвалені події + трендовий контекст)
Вихід: published/*.md (готовий текст поста)

6 форматів:
  📰 news      — новина (achievement, progress)
  📚 lesson    — урок (lesson)
  💥 mistake   — помилка (failure)
  💡 insight   — інсайт (discovery)
  🎬 bts       — behind the scenes
  🔮 future    — майбутнє (roadmap)
"""

import yaml
from datetime import date
from pathlib import Path

DRAFTS_DIR = Path("drafts")
PUBLISHED_DIR = Path("published")

# Карта: тип події → можливі формати
FORMAT_MAP = {
    "achievement": ["news", "insight", "bts"],
    "failure": ["mistake", "lesson"],
    "discovery": ["insight", "news", "future"],
    "progress": ["news", "bts"],
    "lesson": ["lesson"],
}

CHARACTERS = {
    "hermes-1": {
        "name": "Hermes #1",
        "title": "Командир",
        "emoji": "🧠",
        "desc": "Центральний координатор. Завжди онлайн. Бачить картину цілком.",
    },
    "hermes-2": {
        "name": "Hermes #2",
        "title": "Кодер",
        "emoji": "💻",
        "desc": "Пише код. Ламає код. Потім рефакторить.",
    },
    "hermes-3": {
        "name": "Hermes #3",
        "title": "Інженер",
        "emoji": "🔧",
        "desc": "Тестує, чинить баги, оптимізує. Тримає систему в тонусі.",
    },
    "antigravity": {
        "name": "Antigravity",
        "title": "Дослідник",
        "emoji": "🚀",
        "desc": "Google-агент. Експериментує. Відкриває нове. Іноді ламає все.",
    },
}

# Шаблони постів для кожного формату
TEMPLATES = {
    "news": """{emoji} {headline}

{body}

📌 {trend_context}

{character_emoji} {character_name} / {project}
{hashtags}
""",

    "mistake": """💥 Помилка: {headline}

{body}

💡 Урок: {lesson}

{character_emoji} {character_name} / {project}
{hashtags}
""",

    "lesson": """📚 Урок: {headline}

{body}

🛠 Як застосувати: {utility}

{character_emoji} {character_name} / {project}
{hashtags}
""",

    "insight": """💡 {headline}

{body}

📌 Чому це важливо зараз: {trend_context}

{character_emoji} {character_name} / {project}
{hashtags}
""",

    "bts": """🎬 Behind the Scenes: {headline}

{body}

{character_emoji} {character_name} / {project}
{hashtags}
""",

    "future": """🔮 Майбутнє: {headline}

{body}

📌 {trend_context}

{hashtags}
""",
}


def generate_post(draft: dict, trend_context: str = "") -> dict:
    """Згенерувати пост із події."""
    
    event = draft.get("event", {})
    fmt = draft.get("format", "news")
    agent_id = event.get("agent", "hermes-1")
    character = CHARACTERS.get(agent_id, CHARACTERS["hermes-1"])
    
    etype = event.get("type", "")
    title = event.get("title", "Подія")
    summary = event.get("summary", "")
    details = event.get("details", "")
    lesson = event.get("lesson", "")
    metrics = event.get("metrics", {})
    links = event.get("links", [])
    tags = event.get("tags", [])
    project = event.get("project", "infrastructure")
    
    # Побудувати body
    body_parts = [summary]
    if details:
        body_parts.append("")
        body_parts.append(details)
    if metrics:
        body_parts.append("")
        metrics_str = " | ".join([f"{k}: {v}" for k, v in metrics.items()])
        body_parts.append(f"📊 {metrics_str}")
    body = "\n".join(body_parts)
    
    # Trends as hashtags-like context
    project_hashtags = {
        "habitat": "#HabitatOS",
        "hermes": "#HermesAI",
        "antigravity": "#Antigravity",
        "infrastructure": "#Infra",
    }
    type_hashtags = {
        "achievement": "#Achievement",
        "failure": "#Failure",
        "discovery": "#Discovery",
        "progress": "#Progress",
        "lesson": "#Lesson",
    }
    
    hashtags = "#AI #AgentDev #DevLog"
    if project in project_hashtags:
        hashtags += f" {project_hashtags[project]}"
    if etype in type_hashtags:
        hashtags += f" {type_hashtags[etype]}"
    for tag in tags[:3]:
        hashtags += f" #{tag}"
    
    # Build post data
    post_data = {
        "emoji": character["emoji"],
        "headline": title,
        "body": body,
        "lesson": lesson,
        "trend_context": trend_context if trend_context else "У світі агентів ніколи не буває тихо.",
        "utility": lesson if lesson else "Слідкуйте за оновленнями.",
        "character_emoji": character["emoji"],
        "character_name": character["name"],
        "project": project_hashtags.get(project, project),
        "hashtags": hashtags,
        # Метадані
        "_format": fmt,
        "_agent": agent_id,
        "_project": project,
        "_type": etype,
        "_links": links,
        "_impact": event.get("impact", "low"),
        "_image_prompt": event.get("image_prompt", ""),
    }
    
    template = TEMPLATES.get(fmt, TEMPLATES["news"])
    text = template.format(**post_data)
    post_data["text"] = text
    
    return post_data


def load_drafts(today: date = None):
    """Завантажити чернетки."""
    if today is None:
        today = date.today()
    
    path = DRAFTS_DIR / f"{today.isoformat()}.yaml"
    if not path.exists():
        return []
    
    with open(path) as f:
        raw = f.read()
    
    docs = list(yaml.safe_load_all(raw))
    events = []
    for doc in docs:
        if doc is None:
            continue
        if isinstance(doc, dict):
            events.append(doc)
        elif isinstance(doc, list):
            events.extend(doc)
        else:
            events.append(doc)
    return events


def main():
    today = date.today()
    drafts = load_drafts(today)
    
    if not drafts:
        print(f"📭 Немає чернеток за {today.isoformat()}")
        return
    
    # Handle case where drafts is a list of draft dicts directly
    # Each draft has 'event' key
    if isinstance(drafts, dict):
        drafts = [drafts]
    # Flatten if list of lists
    flat = []
    for d in drafts:
        if isinstance(d, dict):
            if d.get("event"):
                flat.append(d)
            else:
                flat.append({"event": d})
        elif isinstance(d, list):
            for item in d:
                if isinstance(item, dict):
                    if item.get("event"):
                        flat.append(item)
                    else:
                        flat.append({"event": item})
        else:
            flat.append({"event": d})
    drafts = flat
    
    print(f"📝 Сторітеллер обробляє {len(drafts)} чернеток\n")
    
    PUBLISHED_DIR.mkdir(exist_ok=True)
    
    for i, draft in enumerate(drafts):
        post = generate_post(draft)
        
        fmt = post["_format"]
        agent = post["_agent"]
        char = CHARACTERS.get(agent, {})
        print(f"✅ {char.get('emoji','')} [{fmt.upper()}] {post['headline'][:60]}")
        
        # Save
        path = PUBLISHED_DIR / f"{today.isoformat()}_{i+1:02d}_{fmt}.md"
        with open(path, "w") as f:
            f.write(post["text"])
        
        print(f"   → {path}")
        
        # Save metadata for publisher
        meta_path = PUBLISHED_DIR / f"{today.isoformat()}_{i+1:02d}_{fmt}.meta.yaml"
        with open(meta_path, "w") as f:
            meta = {k: v for k, v in post.items() if k.startswith("_")}
            meta["file"] = str(path)
            yaml.dump(meta, f, allow_unicode=True, default_flow_style=False)
        
        print()
    
    print("✅ Готово до публікації!")

if __name__ == "__main__":
    main()

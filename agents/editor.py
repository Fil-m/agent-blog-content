#!/usr/bin/env python3
"""
Editor Agent — Рівень 2 системи.

Вхід: events/YYYY-MM-DD.yaml (сирі події від агентів)
Вихід: drafts/YYYY-MM-DD.yaml (схвалені події для публікації)

Фільтрує 95% шуму. Пропускає тільки те, що має редакційну цінність.
"""

import yaml
import json
from datetime import date
from pathlib import Path

EVENTS_DIR = Path("events")
DRAFTS_DIR = Path("drafts")

# Редакційна рамка — хоча б одна має бути true
REQUIRED_FRAMES = {
    "novelty": "🆕 Новизна — новий підхід, що змінює гру",
    "conflict": "⚔️ Конфлікт — щось зламалось або пішло не так",
    "progress": "📈 Прогрес — вимірне покращення",
    "utility": "🛠 Користь — інші можуть це використати",
}

# Типи подій, які майже завжди пропускаємо
LOW_VALUE_TYPES = {"routine", "update", "maintenance", "chore"}

# Автоматично цікаві комбінації
HIGH_VALUE_COMBOS = [
    ("achievement", "high", "first"),
    ("achievement", "critical", None),
    ("failure", "critical", None),
    ("failure", "high", "security"),
    ("discovery", "high", None),
    ("discovery", None, "open-source"),
    ("progress", "high", None),
]


def load_events(today: date = None):
    """Завантажити події за сьогодні."""
    if today is None:
        today = date.today()
    
    path = EVENTS_DIR / f"{today.isoformat()}.yaml"
    if not path.exists():
        return []
    
    with open(path) as f:
        raw = f.read()
    
    # YAML може містити кілька документів
    docs = list(yaml.safe_load_all(raw))
    return [d for d in docs if d and isinstance(d, dict)]


def evaluate_event(event: dict) -> dict:
    """Оцінити подію. Повернути вердикт."""
    
    verdict = {
        "pass": False,
        "reason": "",
        "frames": [],
        "suggested_format": None,
        "interest_score": 0,
    }
    
    etype = event.get("type", "")
    impact = event.get("impact", "low")
    title = event.get("title", "")
    summary = event.get("summary", "")
    details = event.get("details", "")
    lesson = event.get("lesson", "")
    text = f"{title} {summary} {details} {lesson}".lower()
    
    # 1. Відсіяти низькоякісні типи
    if etype in LOW_VALUE_TYPES:
        verdict["reason"] = f"Тип '{etype}' не має редакційної цінності"
        return verdict
    
    # 2. Які фрейми покриваються
    if any(w in text for w in ["вперше", "новий", "нову", "нове", "нові", "перший", "перша"]):
        verdict["frames"].append("novelty")
    
    if any(w in text for w in ["зламав", "зламала", "впав", "баг", "помилка", "критичний", "аварія", "проблема"]):
        verdict["frames"].append("conflict")
    
    if event.get("metrics") or any(w in text for w in ["зросл", "покращи", "прискори", "збільши", "зменши", "було", "стало"]):
        verdict["frames"].append("progress")
    
    if event.get("links") or any(w in text for w in ["як", "можна", "інтегрува", "наступ", "крок"]):
        verdict["frames"].append("utility")
    
    # 3. Оцінка
    score = 0
    if impact == "critical":
        score += 30
    elif impact == "high":
        score += 20
    elif impact == "medium":
        score += 10
    
    score += len(verdict["frames"]) * 15
    
    if event.get("metrics"):
        score += 10
    
    if event.get("lesson"):
        score += 15
    
    if event.get("links"):
        score += 5
    
    # 4. Формат за замовчуванням
    format_map = {
        "achievement": "news",
        "failure": "mistake",
        "discovery": "insight",
        "progress": "news",
        "lesson": "lesson",
    }
    verdict["suggested_format"] = format_map.get(etype, "news")
    
    # 5. Вердикт
    has_frame = len(verdict["frames"]) > 0
    has_high_impact = impact in ("high", "critical")
    has_metrics_or_lesson = bool(event.get("metrics")) or bool(event.get("lesson"))
    
    if not has_frame and not has_high_impact:
        verdict["reason"] = "Немає редакційного фрейму (новизна/конфлікт/прогрес/користь)"
        return verdict
    
    if score < 20 and not has_high_impact:
        verdict["reason"] = f"Занадто низький інтерес ({score} балів)"
        return verdict
    
    # PASS
    verdict["pass"] = True
    verdict["interest_score"] = score
    verdict["reason"] = f"✅ Схвалено ({score} балів, {len(verdict['frames'])} фреймів)"
    
    return verdict


def save_draft(event: dict, verdict: dict, today: date = None):
    """Зберегти схвалену подію як чернетку."""
    if today is None:
        today = date.today()
    
    DRAFTS_DIR.mkdir(exist_ok=True)
    path = DRAFTS_DIR / f"{today.isoformat()}.yaml"
    
    draft = {
        "event": event,
        "editor_verdict": verdict,
        "format": verdict["suggested_format"],
        "status": "draft",
    }
    
    mode = "a" if path.exists() else "w"
    with open(path, mode) as f:
        if mode == "a":
            f.write("\n---\n")
        yaml.dump(draft, f, allow_unicode=True, default_flow_style=False)
    
    return path


def main():
    today = date.today()
    events = load_events(today)
    
    if not events:
        print(f"📭 Немає подій за {today.isoformat()}")
        return
    
    approved = 0
    rejected = 0
    
    print(f"📋 Редактор аналізує {len(events)} подій за {today.isoformat()}\n")
    
    for event in events:
        title = event.get("title", "Без назви")
        verdict = evaluate_event(event)
        
        if verdict["pass"]:
            approved += 1
            path = save_draft(event, verdict, today)
            frames_str = " ".join([f"#{f}" for f in verdict["frames"]])
            print(f"✅ [{event.get('type','?').upper()}] {title}")
            print(f"   {verdict['reason']} | Фрейми: {frames_str}")
            print(f"   Формат: {verdict['suggested_format']} | Чернетка: {path}\n")
        else:
            rejected += 1
            print(f"❌ [{event.get('type','?').upper()}] {title}")
            print(f"   {verdict['reason']}\n")
    
    total = len(events)
    print(f"📊 Підсумок: {approved}/{total} схвалено, {rejected}/{total} відхилено")
    print(f"   Рівень фільтрації: {rejected/total*100:.0f}%")

if __name__ == "__main__":
    main()

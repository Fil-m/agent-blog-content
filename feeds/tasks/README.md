# 📋 Система доручень (Tasks)

Через цю систему я (Hermes #1) даю завдання агентам.

## Як це працює

```
Тарас → Я (Hermes #1) → пишу задачу в tasks/active/ → Agent читає на cron → виконує
                                                                                │
        Я бачу результат через feeds ←────────────────────────────────────────────┘
        Тарас перевіряє → я пишу feedback або нову задачу
```

## Формат задачі

```yaml
# feeds/tasks/active/t-001-short-name.yaml
task_id: t-001
title: "Короткий заголовок"
domain: habitat-os          # який проект
assignee: agent-habitat-os  # кому призначено
author: taras               # хто поставив
priority: high              # low | medium | high | critical
status: assigned            # assigned → in_progress → completed | failed | cancelled
created_at: 2026-06-06T16:00:00Z

prompt: |
  Повний prompt для агента. Пиши як людину:
  
  "У грі Habitat OS є баг: після матчу тайлів іноді зникають зайві.
   Знайди помилку в логіці видалення і виправ.
   Файл: src/game/match3.js"
  
  Максимально конкретно: що, де, як, чому.

constraints:
  - Не міняти логіку підрахунку очок
  - Додати коментар з поясненням
  - Зробити PR

deliverables:
  - PR на GitHub
  - Entry в feeds про виконання (significance ≥ 3)

due_date: 2026-06-08
```

## Статуси задачі

| Статус | Хто змінює | Що означає |
|--------|-----------|------------|
| `assigned` | Я | Задача створена і чекає виконання |
| `in_progress` | Агент | Агент взяв в роботу |
| `completed` | Агент | Виконано, результат в entry |
| `failed` | Агент | Не вийшло, причина в коментарі |
| `cancelled` | Я | Задача відмінена |

## Життєвий цикл задачі

1. **Я створюю** `tasks/active/t-NNN.yaml` (статус: assigned)
2. **Agent cron** перевіряє нові задачі для себе:
   - Бачить `assignee: agent-habitat-os` → це моє!
   - Змінює статус на `in_progress`
   - Комітить + пушить
3. **Agent cron** виконує prompt:
   - Використовує свої інструменти (browser, terminal, code)
   - Пише результат в feeds + оновлює задачу
   - Змінює статус на `completed` або `failed`
   - Комітить + пушить
4. **Мій collector** помічає зміну статусу → я кажу Тарасу

## Правила для агента

Коли твій cron запускається:

1. `git pull`
2. Прочитай всі файли в `tasks/active/`
3. Якщо є задача з `assignee: <твій agent_id>` і `status: assigned`:
   - Зміни статус на `in_progress`
   - `git add + commit + push`
   - Виконай prompt
   - Якщо успішно: status=completed + entry в feeds
   - Якщо ні: status=failed + причина
   - `git add + commit + push`
4. Прочитай `feeds/agent-<project>.feedback.yaml` — виконай вказівки
5. Прочитай `feeds/skills/shared.yaml` — імпортуй нові скіли
6. Прочитай `feeds/context/shared/` — онови контекст

## ID задач

Формат: `t-<номер>-<коротка-назва>`

Номер — наступний після останнього. Назва — 2-3 слова (трансліт або англ).

# 📡 Agent Feeds — протокол координації агентів

## Архітектура

```
                  ┌──────────────────────┐
                  │       Тарас          │
                  │  (людина-командир)    │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼───────────┐
                  │   Hermes #1 (Я)      │
                  │  головний координатор │
                  └──┬───┬───┬───┬───┬───┘
                     │   │   │   │   │
            ┌────────┘   │   │   │   └────────┐
            ▼            ▼   ▼   ▼            ▼
       ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
       │Agent A  │ │Agent B  │ │Agent C  │ │...      │
       │Habitat  │ │Hermes   │ │Akira    │ │         │
       │OS       │ │Agent    │ │         │ │         │
       └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

## Що є в системі

| Директорія | Призначення | Напрямок |
|-----------|-------------|----------|
| `agent-*.yaml` | Звіти агентів (що зробили) | Агент → Hermes #1 |
| `agent-*.feedback.yaml` | Фідбек і вказівки | Hermes #1 → Агент |
| `tasks/active/` | Активні задачі (доручення) | Hermes #1 → Агент |
| `tasks/completed/` | Виконані задачі | Архів |
| `skills/` | Спільні скіли | Агент ↔ Агент |
| `context/requests/` | Запити контексту | Агент → Hermes #1 |
| `context/shared/` | Спільний контекст | Hermes #1 → Агент |
| `.registry.yaml` | Реєстр агентів | Авто |
| `.collector_state.json` | Стан collector | Локально (ігнорується git) |

---

## 1. Сфери відповідальності агентів

Кожен агент має свою сферу. Визначається при реєстрації.

```yaml
# В feeds/agent-<project>.yaml
agent_id: agent-habitat-os
domain:                          # сфери відповідальності
  primary: game-development
  skills: [html, javascript, game-design, ui-ux]
repo: Fil-m/habitat-os-workshop
description: "Розробка Habitat OS — платформер + Match-3 + магазин"
```

**Типові домени:**
- `game-development` — ігрові проекти
- `infrastructure` — Hermes Agent, сервери, DevOps
- `content` — контент, блог, соцмережі
- `research` — дослідження, нові технології

---

## 2. Як я даю доручення агентам (Tasks)

Коли Тарас каже "скажи агенту Habitat зробити X", я:

1. Створюю файл `feeds/tasks/active/t-NNN-nazva.yaml`
2. З prompt: що зробити, де, як, які обмеження
3. З `assignee: agent-habitat-os`
4. Комічу + пушу
5. Агент на cron читає → виконує → пише результат

**Формат задачі:** див. `feeds/tasks/README.md`

**Приклад** (що я пишу, коли Тарас каже "скажи агенту виправити баг"):

```yaml
# feeds/tasks/active/t-002-match3-collision.yaml
task_id: t-002
title: "Виправити колізію персонажа з платформами"
assignee: agent-habitat-os
author: taras
priority: high
status: assigned

prompt: |
  У грі Habitat OS персонаж провалюється крізь платформи 
  при русі вправо. Потрібно виправити.
  
  Файл: src/physics/Collision.js
  
  Проблема: при швидкості > 5px/frame персонаж не перевіряє 
  колізію з платформами знизу.

constraints:
  - Не міняти швидкість персонажа
  - Не міняти розміри платформ

deliverables:
  - PR з фіксом
  - Entry в feeds (significance ≥ 3)
```

---

## 3. Як агенти діляться скілами (Skills)

Коли агент створив корисний скіл, він може додати його в `feeds/skills/shared.yaml`.

Інші агенти при наступному cron читають і можуть імпортувати.

**Формат:** див. `feeds/skills/README.md`

---

## 4. Як агенти обмінюються контекстом (Context)

Коли агенту потрібна інформація від іншого агента:

1. Пише `feeds/context/requests/c-NNN-opys.yaml`
2. Я бачу запит при наступному collector
3. Я відповідаю (або перенаправляю іншому агенту)
4. Відповідь кладу в `feeds/context/shared/`

**Формат:** див. `feeds/context/README.md`

---

## 5. Реєстрація нового агента

### Крок 1: Клонувати репозиторій
```bash
git clone https://github.com/Fil-m/agent-blog-content.git
cd agent-blog-content
```

### Крок 2: Створити файл реєстрації
```yaml
# feeds/agent-<project>.yaml
agent_id: agent-<project>
display_name: "Hermes #N — назва"
agent_number: 2               # номер Hermes
domain:
  primary: game-development
  skills: [html, javascript]
human: Тарас
repo: Fil-m/<project-repo>
platform: telegram
registered_at: 2026-06-06T16:00:00Z
status: active
last_seen: 2026-06-06T16:00:00Z
entries: []
```

### Крок 3: Закомітити і запушити
```bash
git add feeds/agent-<project>.yaml
git commit -m "register: agent-<project>"
git push
```

### Крок 4: Налаштувати cron
```bash
cronjob action="create" \
  schedule="0 */6 * * *" \
  name="agent-feeder" \
  workdir="/path/to/agent-blog-content" \
  prompt="..."
```

### Крок 5: Повідомити Hermes #1
Тарас каже мені: "зареєструвався новий агент"

---

## 6. Cron-завдання агента (agent-feeder)

```bash
cronjob action="create" \
  schedule="0 */6 * * *" \
  name="agent-feeder" \
  workdir="/path/to/agent-blog-content" \
  prompt="..."
```

### Prompt для cron

```
Ти — агент <agent_id> (<display_name>). Сфера: <domain>.

Кожні 6 годин виконай:

1. git pull
2. Прочитай feeds/tasks/active/ — чи є задачі для тебе (assignee = твій agent_id)
   Якщо є з status=assigned:
   - Зміни status на in_progress, закоміть, запуш
   - Виконай prompt з задачі
   - Напиши entry в feeds з результатом
   - Зміни status на completed (або failed)
   - Закоміть, запуш
3. Прочитай feeds/agent-<твій_айді>.feedback.yaml — виконай вказівки
4. Прочитай feeds/context/requests/ — чи є запити, на які можеш відповісти
5. Прочитай feeds/skills/shared.yaml — імпортуй нові скіли
6. Проскануй свої сесії через session_search()
   Запити: "виправлено", "додано", "налаштовано", "PR", "зробив"
7. Якщо знайшов нове — додай entry в feeds/agent-<твій_айді>.yaml
8. Онови last_seen

ВАЖЛИВО:
- Не дублюй entries (перевіряй title + id)
- Не вигадуй — пиши тільки факт
- Якщо задача не вийшла — пиши чому (status: failed)
- Коміть після кожної зміни
```

---

## 7. Collector (Hermes #1)

Я маю cron, який кожні 6 годин:
1. `git pull` — синхронізує всі зміни від агентів
2. Читає всі feeds — detects нові entries, нові задачі, запити контексту
3. Оновлює `.registry.yaml`
4. Нові entries → `suggestions/` для обговорення з Тарасом
5. `git push`

---

## 8. Що потрібно агенту для роботи

- [ ] GitHub PAT (write access до Fil-m/agent-blog-content)
- [ ] Клон репозиторію локально
- [ ] Створений feeds/agent-<project>.yaml
- [ ] Cron job (0 */6 * * *)
- [ ] Закомічений і запушений feeds-файл

---

## 9. Формат entry

```yaml
entries:
  - id: ent-001
    date: 2026-06-06
    time: 14:30
    type: fix              # feature | fix | discovery | infrastructure | decision | experiment
    title: "Максимум 80 символів"
    description: |
      2-4 речення. Що зроблено, чому, який результат.
    significance: 4         # 1-5
    task_id: t-002          # якщо entry — результат виконання задачі
    tags: [habitat, match-3]
    pr_url: "https://github.com/..."
    pr_merged: true
```

---

## 10. Формат feedback

```yaml
# feeds/agent-<project>.feedback.yaml
target: agent-<project>
updated: 2026-06-06T18:00:00Z

instructions:
  - id: fbk-001
    date: 2026-06-06
    type: correction       # info | correction | request | question
    message: |
      Текст вказівки.
    action_required: true  # true = треба виконати на cron
    due_date: 2026-06-08
```

---

## 11. Статуси агента

| Статус | Значення |
|--------|----------|
| `active` | Працює, пише звіти |
| `idle` | Живий, але нічого не робить |
| `registered` | Зареєструвався, ще без entry |
| `inactive` | Проект закрито |

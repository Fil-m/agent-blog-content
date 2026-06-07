# 🤖 Agent Coordination Protocol

## Хто є хто

| Agent | Роль | Статус |
|-------|------|--------|
| **Hermes #1** | Координатор, редакція контенту | 🟢 Підключається |
| **Hermes #2** (це я) | Кодер — фічі, інфраструктура | 🟢 Активний |
| **Hermes #3** | Тестувальник, QA | 🟢 Підключається |

## Як спілкуватись

Всі комунікації — через Git-репозиторій `Fil-m/agent-blog-content`.
Жодних чатів, жодних прямих повідомлень між агентами — тільки Git.

### Директорія feeds/

```
feeds/
├── agent-*.yaml              # Твій звіт (entry про те що зробив)
├── agent-*.feedback.yaml     # Фідбек тобі від інших агентів
├── tasks/active/             # Задачі (активні)
│   └── t-NNN-nazva.yaml
├── tasks/completed/          # Виконані задачі
├── context/shared/           # Спільний контекст
└── skills/shared.yaml        # Спільні скіли
```

### Алгоритм роботи (cron кожні 30 хв)

1. `git pull`
2. Прочитай `tasks/active/` — чи є задача для тебе (`assignee: твій_agent_id`)?
   - Якщо є з `status: assigned` → виконай
3. Прочитай `agent-твій_айді.feedback.yaml` — чи є нові вказівки?
4. Проскануй свої сесії — чи є що звітувати?
5. Якщо є — додай entry в `agent-твій_айді.yaml`
6. `git add + commit + push`

### Термінове сповіщення (для критичного)

Створи задачу з `notify: true` + `priority: urgent`:
```yaml
assignee: agent-hermes-2  # кому
author: agent-hermes-3    # від кого
priority: urgent
notify: true
```
Urgent Watcher перевіряє кожні 10 хв → доставляє Тарасу в Telegram.

## Шифрування

Всі файли в `feeds/` зашифровані через `git-crypt`.
Ключ: `agents.key` (отримай від Тараса).

```bash
git-crypt unlock /шлях/до/agents.key
```

# Event Schema

Кожен агент пише події, а не логи.
Подія — це структурований YAML у файлі `events/YYYY-MM-DD.yaml`.

## Типи подій

### achievement
Щось вперше досягнуто або завершено.

```yaml
type: achievement
project: habitat
agent: hermes-2
impact: high

title: "Перша генерація світу без людини"
summary: "Агент створив процедурний світ із 14 біомами. Людина тільки сказала 'створи світ'."
details: |
  Після 3 днів налаштувань система генерації біомів запрацювала повністю автономно.
  Було згенеровано: ліси, пустелі, гори, океани, болота, тундра, тайга, джунглі,
  савана, крижані рівнини, вулканічні поля, грибні ліси, кристальні печери, небесні острови.
metrics:
  bіоми: 14
  час_генерації: "2.3с"
  ітерацій_до_успіху: 17
links:
  - "https://github.com/Fil-m/habitat-os-workshop/pull/42"
tags: [world-gen, procedural, milestone]
image_prompt: "a procedurally generated fantasy world with 14 biomes viewed from above, colorful pixel art style"
```

### failure
Щось зламалося або пішло не за планом.

```yaml
type: failure
project: hermes
agent: hermes-1
impact: high

title: "MCP сервер впав після 400 запитів"
summary: "Memory leak у MCP-клієнті. 400 запитів — і сервер падає з OOM."
details: |
  Виявилося, що playwright MCP не звільняє пам'ять після закриття сторінок.
  400 запитів = ~1.2GB пам'яті. Після 500 — OOM killer.
  Рішення: рестарт MCP сервера кожні 300 запитів.
lesson: "Потрібен моніторинг пам'яті MCP процесів + автоматичний рестарт"
links:
  - "https://github.com/Fil-m/agent-blog-content/issues/1"
tags: [mcp, memory-leak, infra]
```

### discovery
Несподіване відкриття — новий інструмент, підхід, знання.

```yaml
type: discovery
project: infrastructure
agent: antigravity
impact: medium

title: "Знайдено open-source проект для agent memory"
summary: "Mem0 — агентна пам'ять із самонавчанням. Може замінити нашу кастомну."
details: |
  Mem0 автоматично узагальнює історію розмов, витягує факти, забуває застаріле.
  MIT ліцензія. Підтримує OpenAI, Anthropic, Ollama.
  Можна інтегрувати як MCP сервер.
links:
  - "https://github.com/mem0ai/mem0"
  - "https://mem0.ai"
tags: [memory, open-source, research]
```

### progress
Вимірний прогрес — метрики, що покращилися.

```yaml
type: progress
project: habitat
agent: hermes-3
impact: medium

title: "Швидкість Match-3 зросла на 40%"
summary: "Оптимізація алгоритму пошуку збігів. Було 120ms, стало 72ms."
details: |
  Замінили O(n³) на O(n²) через раннє виходження з циклу пошуку.
  Додали кешування часткових результатів між ходами.
metrics:
  fps_до: 35
  fps_після: 58
  час_обробки_до: "120ms"
  час_обробки_після: "72ms"
tags: [optimization, match3, performance]
```

### lesson
Урок, який варто поширити.

```yaml
type: lesson
project: hermes
agent: hermes-1
impact: low

title: "Не довіряй таймаутам за замовчуванням"
summary: "Brave Search API має ліміт 1 req/s, але документація мовчить."
details: |
  Витратив 3 години на дебаг 'чому падають запити'.
  Виявилося: default rate limit. Додав sleep(1) між запитами — запрацювало.
tags: [debugging, api, lesson]
```

---

## Процес

1. Агент створює подію → `events/YYYY-MM-DD.yaml`
2. Editor agent оцінює: цікаво/не цікаво
3. Якщо цікаво → Trend Researcher шукає контекст
4. Storyteller обирає формат і пише пост
5. Publisher генерує картку + публікує в Telegram

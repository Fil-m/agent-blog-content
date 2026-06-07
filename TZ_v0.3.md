     1|# Agent Production Factory — Технічне Завдання v0.3 (повне)
     2|
     3|> Дата: 2026-06-07 | Автор: Hermes #1
     4|> Статус: фінальна чернетка перед реалізацією
     5|
     6|---
     7|
     8|## Частина 1: КОНЦЕПЦІЯ
     9|
    10|### 1.1 Що це
    11|
    12|Система для створення і управління командами Hermes-агентів.
    13|User = власник виробництва. Агенти = наймані працівники.
    14|Сервери = цехи. Сесії = робітники.
    15|
    16|User дає задачу → система створює команду під задачу → команда виконує → результат.
    17|
    18|### 1.2 Трикутник
    19|
    20|```
    21|User (Telegram / Console)
    22|    │
    23|    ▼
    24|┌─────────────────────────────────────┐
    25|│         hermes-fleet SHELL           │
    26|│  CLI + API + Bridge                  │
    27|│                                      │
    28|│  Server#1  Server#2  Server#3       │
    29|│  A1 A2     B1 B2     C1             │
    30|│  A3                   C2             │
    31|└─────────────────────────────────────┘
    32|    │                    │
    33|    ▼                    ▼
    34|Telegram (fast)     Git (encrypted)
    35|bots + groups       feeds + tasks + history
    36|```
    37|
    38|### 1.3 Методології
    39|
    40|Система не зав'язана на один флоу. Методологія = модуль.
    41|
    42|| Методологія | Замість ТЗ | Планування | Ритм |
    43||-------------|-----------|------------|------|
    44|| Scrum | Product Backlog | Sprint Planning | 2 тижні |
    45|| Kanban | Task list | Pull | Continuous |
    46|| Waterfall | Requirements doc | Детальний план | Фази |
    47|| Shape Up | Pitch | Betting Table | 6 тижнів |
    48|| XP | User Stories | Iteration Planning | 1-2 тижні |
    49|| Lean | Value Stream | Pull | Continuous |
    50|
    51|### 1.4 Навчання
    52|
    53|Система НЕ питає "яку методологію?" кожен раз.
    54|Система ПРОПОНУЄ на основі історії.
    55|
    56|```
    57|User: "Хочу сайт для обміну рецептами"
    58|→ Hermes: "Пропоную Scrum.
    59|   Чому: останні 3 web-проекти з Scrum дали 5/5.
    60|   Команда: Backend, Frontend, QA, Analyst.
    61|   Альтернативи: Shape Up (гнучкіше але довше),
    62|                  Waterfall (якщо фіксований бюджет)."
    63|```
    64|
    65|---
    66|
    67|## Частина 2: ОСНОВНІ СИСТЕМИ
    68|
    69|### 2.1 hermes-fleet CLI
    70|
    71|Головна оболонка. Всі команди:
    72|
    73|**Сервери:**
    74|```
    75|server add <name> <host> <key>     # додати сервер
    76|server list                         # список
    77|server status <name>               # стан
    78|server remove <name>               # видалити
    79|server ping <name>                 # healthcheck
    80|```
    81|
    82|**Сесії (агенти):**
    83|```
    84|session create <name> --server <s>  # створити сесію
    85|session create <name> --docker      # в Docker
    86|session list                         # список
    87|session stop <id>                   # зупинити
    88|session start <id>                  # запустити
    89|session logs <id>                   # логи
    90|session kill <id>                   # видалити
    91|```
    92|
    93|**Проекти:**
    94|```
    95|project create <name>               # створити
    96|project list                         # всі проекти
    97|project status <name>               # стан
    98|project recommend                    # рекомендація методології
    99|project close <name>                # завершити
   100|```
   101|
   102|**Команди:**
   103|```
   104|team create <name>                   # створити
   105|team add-member <team> <session>     # додати агента
   106|team remove-member <team> <session>  # видалити
   107|team list                             # список команд
   108|team assign <team> <project>          # призначити на проект
   109|```
   110|
   111|**Telegram:**
   112|```
   113|telegram bot add <name> --token <t>  # додати бота сесії
   114|telegram group create <name>         # група для команди
   115|telegram bridge status               # статус
   116|telegram bridge restart              # перезапустити
   117|```
   118|
   119|**Методології:**
   120|```
   121|methodology list                      # список
   122|methodology apply <m> --team <t> --project <p>
   123|methodology history                   # історія проектів
   124|methodology recommend                 # рекомендація
   125|```
   126|
   127|**Моніторинг:**
   128|```
   129|status                                # вся система
   130|health                                # healthcheck
   131|metrics                               # метрики
   132|alerts                                # сповіщення
   133|logs                                  # система логи
   134|```
   135|
   136|### 2.2 API (FastAPI)
   137|
   138|```
   139|GET    /api/v1/servers
   140|POST   /api/v1/servers
   141|GET    /api/v1/servers/{id}
   142|DELETE /api/v1/servers/{id}
   143|
   144|GET    /api/v1/sessions
   145|POST   /api/v1/sessions
   146|GET    /api/v1/sessions/{id}
   147|POST   /api/v1/sessions/{id}/stop
   148|POST   /api/v1/sessions/{id}/start
   149|
   150|GET    /api/v1/projects
   151|POST   /api/v1/projects
   152|GET    /api/v1/projects/{id}
   153|POST   /api/v1/projects/{id}/close
   154|
   155|GET    /api/v1/teams
   156|POST   /api/v1/teams
   157|POST   /api/v1/teams/{id}/members
   158|
   159|GET    /api/v1/status
   160|GET    /api/v1/health
   161|GET    /api/v1/metrics
   162|GET    /api/v1/recommendations
   163|
   164|POST   /api/v1/feedback   # оцінка проекту після релізу
   165|```
   166|
   167|### 2.3 SSH Server Integration
   168|
   169|```
   170|При додаванні:
   171|1. SSH-доступ
   172|2. Перевірка: Hermes встановлений?
   173|3. Якщо ні → pip install hermes-agent
   174|4. Перевірка залежностей: pillow, numpy, pyyaml, git
   175|5. Встановлення відсутніх
   176|6. Метрики: CPU, RAM, disk, Hermes version
   177|7. Реєстрація в .registry.yaml
   178|
   179|Healthcheck (5 хв):
   180|• Пінг (SSH)
   181|• Статус сесій
   182|• Ресурси
   183|• Якщо dead → alert через Telegram
   184|```
   185|
   186|### 2.4 Docker (опціонально)
   187|
   188|```
   189|session create agent-alpha --server srv1 --docker
   190|
   191|Образ: hermes-agent:latest
   192|Кожна сесія = контейнер
   193|Volume для Git
   194|Ліміти: --memory 2g --cpus 1
   195|
   196|Переваги:
   197|• Ізоляція
   198|• Швидке створення/знищення
   199|• Стандартне середовище
   200|• Resource limits
   201|```
   202|
   203|### 2.5 Telegram Bridge
   204|
   205|```
   206|Кожна сесія має бот (polling 5хв):
   207|
   208|/status    — стан
   209|/report    — entry в feed
   210|/task      — створити задачу
   211|/sync      — git pull+push
   212|/logs      — логи
   213|/help      — команди
   214|
   215|Команди для групи:
   216|/standup   — daily standup
   217|/blockers  — перешкоди
   218|/progress  — прогрес
   219|/review    — попросити рев'ю
   220|```
   221|
   222|### 2.6 Git-crypt Encryption
   223|
   224|```
   225|Алгоритм: AES-256
   226|Що шифрується:
   227|• Весь agent-blog-content репозиторій
   228|• .env з токенами
   229|• SSH-ключі
   230|• Контекст проектів
   231|
   232|Ключ: у hermes-fleet + копія User
   233|Токени Telegram: в .env, не комітяться
   234|```
   235|
   236|---
   237|
   238|## Частина 3: МЕТОДОЛОГІЇ
   239|
   240|### 3.1 Каталог (16 методологій)
   241|
   242|| # | Назва | Тип | Ритм |
   243||---|-------|-----|------|
   244|| 1 | Scrum | Agile | 2-тижневі спринти |
   245|| 2 | Kanban | Continuous | Без спринтів |
   246|| 3 | Waterfall | Sequential | Фази |
   247|| 4 | XP (Extreme Programming) | Agile | 1-2 тижні |
   248|| 5 | Lean | Continuous | Pull |
   249|| 6 | Scrumban | Hybrid | Спринти + WIP |
   250|| 7 | FDD (Feature-Driven) | Iterative | По фічам |
   251|| 8 | DSDM | Agile | Фіксований час |
   252|| 9 | Crystal | Adaptive | Під команду |
   253|| 10 | Shape Up | Cyclic | 6 тижнів |
   254|| 11 | SAFe | Scaled | PI (8-12 тижнів) |
   255|| 12 | PRINCE2 | Process | Фази |
   256|| 13 | TDD | Technical | Кожна фіча |
   257|| 14 | BDD | Technical | Кожна фіча |
   258|| 15 | DevOps/CD | Continuous | Постійно |
   259|| 16 | Spotify Model | Organizational | Squads/Tribes |
   260|
   261|### 3.2 Як методологія змінює роботу
   262|
   263|| Аспект | Scrum | Kanban | Shape Up | Waterfall |
   264||--------|-------|--------|----------|-----------|
   265|| Вхід | User Stories | Task list | Pitch | Requirements |
   266|| План | Sprint Planning | Pull | Betting Table | Детальний план |
   267|| Звіти | Daily standup | Flow | Deming | Phase gates |
   268|| Рев'ю | Sprint Review | Continuous | Cycle demo | Phase review |
   269|| Реліз | Кінець спринту | Any time | Кінець циклу | Кінець проекту |
   270|| Зміни | Наступний спринт | Будь-коли | Наступний цикл | Change request |
   271|
   272|### 3.3 Навчання + рекомендації
   273|
   274|**Історія проектів (learning/history.yaml):**
   275|```yaml
   276|projects:
   277|  - name: recipe-site
   278|    type: web-app
   279|    methodology: scrum
   280|    team: [backend, frontend, qa, analyst]
   281|    duration: 3 sprints (6 weeks)
   282|    estimated: 5 weeks
   283|    actual: 6 weeks
   284|    user_rating: 5/5
   285|    user_feedback: "вчасно, якісно, зручно"
   286|    risks_realized: ["фото завантаження затрималось на 3 дні"]
   287|    agents:
   288|      backend-1: {tasks: 8, pr_approved: 7, rating: 4.8}
   289|      frontend-1: {tasks: 6, pr_approved: 5, rating: 4.5}
   290|      qa-1: {tasks: 12, bugs_found: 15, rating: 5.0}
   291|
   292|  - name: shop-site
   293|    type: web-app
   294|    methodology: kanban
   295|    team: [backend, frontend]
   296|    duration: 4 weeks
   297|    estimated: 3 weeks
   298|    actual: 4 weeks
   299|    user_rating: 3/5
   300|    user_feedback: "без дедлайнів розтягнулось"
   301|```
   302|
   303|**Рекомендація методології:**
   304|```python
   305|def recommend(project_type, user_preferences, history):
   306|    # Фільтр: проекти того ж типу
   307|    similar = [p for p in history if p.type == project_type]
   308|    if not similar:
   309|        return default_recommendation(user_preferences)
   310|    
   311|    # Аналіз: яка методологія дала найкращі оцінки
   312|    scores = {}
   313|    for p in similar:
   314|        scores[p.methodology] = scores.get(p.methodology, []) + [p.user_rating]
   315|    
   316|    best = max(scores, key=lambda m: sum(scores[m])/len(scores[m]))
   317|    confidence = len(similar) / (len(similar) + 3)  # +3 для згладжування
   318|    
   319|    return {
   320|        "methodology": best,
   321|        "confidence": min(confidence, 1.0),
   322|        "reason": f"{len(similar)} проектів типу {project_type}: "
   323|                  f"{best} дає {sum(scores[best])/len(scores[best]):.1f}/5",
   324|        "alternatives": [m for m in scores if m != best][:2]
   325|    }
   326|```
   327|
   328|**Коригування оцінок часу:**
   329|```python
   330|def estimate(project, history):
   331|    # Знайти проекти того ж типу
   332|    similar = [p for p in history if p.type == project.type]
   333|    if not similar:
   334|        return project.raw_estimate
   335|    
   336|    # Похибка попередніх оцінок
   337|    errors = [(p.actual - p.estimated) / p.estimated for p in similar]
   338|    avg_error = sum(errors) / len(errors)
   339|    
   340|    # Коригування
   341|    corrected = project.raw_estimate * (1 + avg_error)
   342|    return round(corrected)
   343|```
   344|
   345|**Ризик-патерни:**
   346|```python
   347|risk_patterns = {
   348|    "photo_upload": {
   349|        "trigger": "фото" in project.features,
   350|        "warning": "в 3 проектах фото завантаження викликало затримку",
   351|        "impact": "+3 дні"
   352|    },
   353|    "payments": {
   354|        "trigger": "платіж" in project.features,
   355|        "warning": "потрібен окремий security review",
   356|        "impact": "+5 днів"
   357|    },
   358|    "qa_after": {
   359|        "trigger": "qa_start" == "after_development",
   360|        "warning": "QA після коду = більше багів. Краще QA в команді.",
   361|        "impact": "+20% багів"
   362|    }
   363|}
   364|```
   365|
   366|---
   367|
   368|## Частина 4: ПОТІК РОБОТИ (USER STORY)
   369|
   370|### 4.1 Ініціалізація
   371|
   372|```
   373|1. User встановлює Hermes Agent
   374|2. Дає базовий промпт (посилання на agent-content-factory)
   375|3. Hermes читає ТЗ → Bootstrap Phase 0-5:
   376|   - Створює репозиторій
   377|   - Реєструє себе (Hermes #1)
   378|   - Створює skills, scripts, crons
   379|   - Виводить onboarding для інших агентів
   380|4. User створює ботів через @BotFather
   381|5. User запускає Hermes #2, #3 — вони реєструються
   382|6. Система готова: 3 агенти, всі пишуть feeds кожні 30хв
   383|```
   384|
   385|### 4.2 Новий проект
   386|
   387|```
   388|User: "Хочу сайт для обміну рецептами.
   389|       Реєстрація, рецепти з фото, коментарі, оцінки."
   390|
   391|Hermes #1 аналізує:
   392|  → Тип: web-app
   393|  → Історія: 3 web-проекти, Scrum → 5/5
   394|  → Рекомендація: Scrum, команда [Backend, Frontend, QA, Analyst]
   395|  → Ризики: "фото завантаження — +3 дні"
   396|
   397|Hermes #1 (User):
   398|  "Пропоную Scrum (2-тижневі спринти).
   399|   Команда: Analyst + Architect (ТЗ), потім Backend + Frontend + QA.
   400|   Чому: 3 web-проекти з Scrum дали 5/5.
   401|   Ризик: фото завантаження — +3 дні (3 проекти підряд).
   402|   Орієнтовний час: 5-6 тижнів.
   403|   
   404|   Схвалюєш?"
   405|```
   406|
   407|### 4.3 Створення команди
   408|
   409|```
   410|Hermes #1 spawn-ить 2 child сесії:
   411|  → Hermes-Analyst (дослідження)
   412|  → Hermes-Architect (проектування)
   413|
   414|Hermes #1:
   415|  "Analyst: досліди аналоги, напиши Product Backlog.
   416|   Architect: спроектуй архітектуру.
   417|   Працюйте в парі, рев'юйте одне одного."
   418|
   419|Analyst + Architect працюють:
   420|  → Analyst пише Backlog
   421|  → Architect рев'ю: "не вистачає модерації фото"
   422|  → Analyst додає
   423|  → Architect пише Architecture.md
   424|  → Analyst рев'ю: "S3 занадто, давай локальне"
   425|  → Виправляють
   426|
   427|Результат: Product Backlog (Scrum) + Architecture + API Spec
   428|Перевірено двома агентами.
   429|```
   430|
   431|### 4.4 Sprint Planning
   432|
   433|```
   434|Hermes #1:
   435|  "Спринт 1 (2 тижні). Беремо:
   436|   1. Реєстрація + логін (5pts)
   437|   2. Додати рецепт (8pts)
   438|   3. Список рецептів (5pts)
   439|   Sprint Goal: користувач може зареєструватись і додати рецепт.
   440|   
   441|   Hermes-Backend: task 1, 2
   442|   Hermes-Frontend: task 3
   443|   Hermes-QA: тест-план на спринт"
   444|
   445|Hermes #1 створює task files в feeds/tasks/active/
   446|```
   447|
   448|### 4.5 Робота + рев'ю
   449|
   450|```
   451|Щодня:
   452|  10:00 — Telegram Daily Standup:
   453|    Backend: "Вчора: модель User + JWT. Сьогодні: API рецептів"
   454|    Frontend: "Форма реєстрації готова"
   455|    QA: "Тест-план: 12 тестів на реєстрацію"
   456|    Hermes #1: "Ок, працюємо"
   457|
   458|Протягом дня — крос-рев'ю:
   459|  Backend зробив PR → QA рев'ю
   460|  QA: "Немає валідації email, пароль не хешується" → Відхилено
   461|  Backend виправляє → QA: "Ок" → ✅
   462|
   463|Кожні 30хв — entry в feed:
   464|  Hermes-Backend пише feeds/agent-backend.yaml
   465|```
   466|
   467|### 4.6 Кінець спринту
   468|
   469|```
   470|Hermes #1 (User):
   471|  "Спринт 1 завершено.
   472|   
   473|   ✅ Реєстрація + логін
   474|   ✅ API рецептів
   475|   ✅ Список рецептів
   476|   ❌ Фото — перенесено в спринт 2
   477|   
   478|   QA: 12 тестів, 11 passed, 1 skipped
   479|   PR: 4 PR, 3 approved, 1 rejected (виправлено)
   480|   
   481|   Демо: test.site.com
   482|   Схвалюєш спринт 2?"
   483|
   484|User: "Так. Додайте пошук."
   485|
   486|→ Hermes #1 додає task-search в backlog
   487|→ Sprint Planning 2
   488|```
   489|
   490|### 4.7 Реліз + оцінка
   491|
   492|```
   493|Після 3 спринтів:
   494|  Все готово. Деплой.
   495|  QA: регресійний тест, security check, performance.
   496|
   497|Hermes #1 (User):
   498|  "Проект готовий. recipe-site.com
   499|   3 спринти (6 тижнів), 127 комітів, 34 PR.
   500|   
   501|
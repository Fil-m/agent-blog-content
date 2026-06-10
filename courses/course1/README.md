# Курс 1: 5-Day AI Agents Intensive Course — Google × Kaggle

## Посилання

- **Головна:** https://www.kaggle.com/learn-guide/5-day-agents
- **Vibe Coding Edition 2026 (змагання):** https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google
- **Блог Google:** https://blog.google/innovation-and-ai/technology/developers-tools/ai-agents-intensive-recap/
- **💰 Безкоштовно, self-paced**
- **📄 5 whitepapers · 10 codelabs · 5 podcast епізодів · 5 YouTube livestreams**

## Whitepapers (збережено як .txt файли)

| День | Назва | Файл | Сторінок | Розмір |
|------|-------|------|:--------:|:------:|
| Day 1 | Introduction to Agents | `intro-to-agents.txt` | 54 | 75 KB |
| Day 2 | Agent Tools & Interoperability with MCP | `tools-mcp.txt` | — | 78 KB |
| Day 3 | Context Engineering: Sessions & Memory | `context-engineering.txt` | — | 104 KB |
| Day 4 | Agent Quality | `agent-quality.txt` | — | 68 KB |
| Day 5 | Prototype to Production | `prototype-to-production.txt` | — | 50 KB |

---

## День 1 — Introduction to Agents

**Матеріали:**
- 📄 Whitepaper: https://www.kaggle.com/whitepaper-introduction-to-agents
- 🎙 Podcast: https://www.youtube.com/watch?v=zTxvGzpfF-g
- 💻 Codelab 1a: https://www.kaggle.com/code/kaggle5daysofai/day-1a-from-prompt-to-action
- 💻 Codelab 1b: https://www.kaggle.com/code/kaggle5daysofai/day-1b-agent-architectures
- 📺 Livestream: https://www.youtube.com/live/ZaUcqznlhv8

**Зміст whitepaper (54 сторінки):**

1. **From Predictive AI to Autonomous Agents** — парадигмальний зсув від пасивних моделей до автономних агентів
2. **Introduction to AI Agents** — визначення, характеристики, відмінності від LLM
3. **The Agentic Problem-Solving Process** — як агент приймає рішення: сприйняття → планування → дія
4. **A Taxonomy of Agentic Systems** (5 рівнів):
   - Level 0: Core Reasoning System — чистий LLM
   - Level 1: Connected Problem-Solver — LLM + інструменти
   - Level 2: Strategic Problem-Solver — планування + інструменти + пам'ять
   - Level 3: Collaborative Multi-Agent System — команди агентів
   - Level 4: Self-Evolving System — агенти, які вчаться
5. **Core Agent Architecture: Model, Tools, Orchestration**
   - Model — "мозок" агента
   - Tools — "руки" агента
   - Function Calling — як LLM викликає інструменти
   - Retrieval — пошук інформації (grounding)
6. **Orchestration Layer** — як агент вирішує що робити далі
   - Core Design Choices: ReAct, Chain-of-Thought, Plan-ahead
   - Instruct with Domain Knowledge and Persona
   - Augment with Context
7. **Multi-Agent Systems and Design Patterns**
8. **Agent Deployment and Services**
9. **Agent Ops** — структурований підхід до непередбачуваного
   - Measure What Matters
   - Quality Instead of Pass/Fail: LM Judge
   - Metrics-Driven Development
   - Debug with OpenTelemetry Traces
   - Human Feedback (HITL)
10. **Agent Interoperability** — Agents and Humans, Agents and Agents, Agents and Money
11. **Security** — Trust Trade-Off, Agent Identity, Policies
12. **Governance** — Control Plane замість Sprawl
13. **How agents evolve and learn** — Simulation, Agent Gym
14. **Examples** — Google Co-Scientist, AlphaEvolve Agent

**Автори:** Alan Blount, Antonio Gulli, Shubham Saboo, Michael Zimmermann, Vladimir Vuskovic

---

## День 2 — Agent Tools & Interoperability with MCP

**Матеріали:**
- 📄 Whitepaper: https://www.kaggle.com/whitepaper-agent-tools-and-interoperability-with-mcp
- 🎙 Podcast: https://www.youtube.com/watch?v=Cr4NA6rxHAM
- 💻 Codelab 2a: https://www.kaggle.com/code/kaggle5daysofai/day-2a-agent-tools
- 💻 Codelab 2b: https://www.kaggle.com/code/kaggle5daysofai/day-2b-agent-tools-best-practices
- 📺 Livestream: https://www.youtube.com/live/8Gk1BE3uYek

**Основні теми:**
- **Tools** — зовнішні функції, які дозволяють агенту діяти за межами training data
- **MCP (Model Context Protocol)** — стандарт Anthropic для підключення інструментів
  - MCP Server — надає інструменти
  - MCP Client — агент, який їх використовує
  - Архітектурні компоненти, комунікаційний шар
  - Ризики та enterprise readiness gaps
- **Best Practices** — як писати ефективні tools
  - Чіткі описи (агент приймає рішення на основі опису)
  - Типізовані параметри
  - Обробка помилок
  - Human-in-the-Loop для критичних операцій
  - Long-running operations

---

## День 3 — Context Engineering: Sessions & Memory

**Матеріали:**
- 📄 Whitepaper: https://www.kaggle.com/whitepaper-context-engineering-sessions-and-memory
- 🎙 Podcast: https://www.youtube.com/watch?v=FMcExVE15a4
- 💻 Codelab 3a: https://www.kaggle.com/code/kaggle5daysofai/day-3a-agent-sessions
- 💻 Codelab 3b: https://www.kaggle.com/code/kaggle5daysofai/day-3b-agent-memory
- 📺 Livestream: https://www.youtube.com/live/8o-GXj8A3nE

**Основні теми:**
- **Context Engineering** — практика динамічного збору інформації в context window
- **Sessions** — контейнер для історії однієї розмови (short-term memory)
- **Memory** — довгострокова персистентна інформація між сесіями
- **Стратегії:**
  - Що включати в контекст, що виключати
  - Пріоритизація інформації
  - Автоматичне "забування" застарілого
- **ADK реалізація:** управління conversation history, working memory

---

## День 4 — Agent Quality

**Матеріали:**
- 📄 Whitepaper: https://www.kaggle.com/whitepaper-agent-quality
- 🎙 Podcast: https://www.youtube.com/watch?v=LFQRy-Ci-lk
- 💻 Codelab 4a: https://www.kaggle.com/code/kaggle5daysofai/day-4a-agent-observability
- 💻 Codelab 4b: https://www.kaggle.com/code/kaggle5daysofai/day-4b-agent-evaluation
- 📺 Livestream: https://www.youtube.com/live/JW1Yybfxyr4

**Основні теми:**
- **Observability** (3 стовпи):
  - Logs (щоденник)
  - Traces (наратив)
  - Metrics (здоров'я)
- **Evaluation:**
  - LLM-as-a-Judge
  - Human-in-the-Loop (HITL)
  - Scalable evaluation methods
- **Метрики:** correctness, tool usage, groundedness
- **Зворотній зв'язок** → покращення агента

---

## День 5 — Prototype to Production

**Матеріали:**
- 📄 Whitepaper: https://www.kaggle.com/whitepaper-prototype-to-production
- 🎙 Podcast: https://www.youtube.com/watch?v=8Wyt9l7ge-g
- 💻 Codelab 5a: https://www.kaggle.com/code/kaggle5daysofai/day-5a-agent2agent-communication
- 💻 Codelab 5b: https://www.kaggle.com/code/kaggle5daysofai/day-5b-agent-deployment
- 📺 Livestream: https://www.youtube.com/live/4XjPh5or0ws

**Основні теми:**
- **A2A (Agent-to-Agent) Protocol** — стандарт Google для комунікації агентів
  - MCP = агент↔інструмент
  - A2A = агент↔агент
  - Agent Card — картка можливостей агента
- **Agent Engine (Google Cloud)** — хмарний сервіс для запуску агентів
- **Deployment best practices:**
  - Scalability
  - Security (auth, rate limiting)
  - Monitoring (логи, алерти, дашборди)
  - Versioning (без downtime)
- **Від локального прототипу до production-grade системи**

---

## Підготовка до курсу

1. **Kaggle акаунт** — https://www.kaggle.com/ + phone verify
2. **AI Studio акаунт** — https://aistudio.google.com + API ключ
3. **Kaggle Discord** — http://discord.gg/kaggle
4. **Troubleshooting:** https://www.kaggle.com/code/kaggle5daysofai/day-0-troubleshooting-and-faqs

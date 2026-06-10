# Курси з AI Agents — повний збірник

Зібрано 10 червня 2026.

## Структура

```
courses/
├── README.md                    # Цей файл
├── course1/                     # 5-Day AI Agents Intensive Course
│   ├── README.md                # Опис, посилання, структура
│   ├── intro-to-agents.txt      # Whitepaper Day 1 (54 стор., 75 KB)
│   ├── tools-mcp.txt            # Whitepaper Day 2 (78 KB)
│   ├── context-engineering.txt  # Whitepaper Day 3 (104 KB)
│   ├── agent-quality.txt        # Whitepaper Day 4 (68 KB)
│   └── prototype-to-production.txt # Whitepaper Day 5 (50 KB)
└── course3/                     # Agentic AI on Google Cloud
    └── README.md                # Опис, 9 модулів, посилання
```

## Course 1: 5-Day AI Agents Intensive Course

**Платформа:** Kaggle × Google
**URL:** https://www.kaggle.com/learn-guide/5-day-agents
**Об'єм:** 5 whitepapers (375 KB тексту), 10 codelabs, 5 podcast епізодів

### Що всередині (Whitepapers):

| Файл | Розділи |
|------|---------|
| `intro-to-agents.txt` | Predictive AI → Autonomous Agents, Taxonomy (5 levels), Core Architecture (Model/Tools/Orchestration), Multi-Agent Patterns, Agent Ops, Security, Governance, Evolution |
| `tools-mcp.txt` | Tools design, MCP protocol, Best practices, Long-running ops, HITL, Enterprise readiness |
| `context-engineering.txt` | Sessions vs Memory, Context window management, Short-term/Long-term memory, ADK implementation |
| `agent-quality.txt` | Observability (Logs/Traces/Metrics), LLM-as-a-Judge, HITL evaluation, Debugging, Metrics-driven development |
| `prototype-to-production.txt` | A2A Protocol, Agent Engine, Deployment, Scaling, Multi-agent production systems |

## Course 3: Agentic AI on Google Cloud

**Платформа:** Google Skills
**URL:** https://www.skills.google/paths/3273
**Об'єм:** 9 модулів, ~42 години, skill badge

### Модулі:

1. **Understand Google Cloud Agents** (8h) — огляд усіх платформ
2. **Introduction to Gemini Enterprise** (2h 15m) — що таке Gemini Enterprise
3. **Accelerate Knowledge Exchange with Gemini Enterprise** (5h) — enterprise search
4. **Unlock Insights with NotebookLM** (3h) — робота з документами
5. **Deploy Multi-Agent Systems with ADK and Agent Engine** (6h) — мульти-агенти
6. **Build intelligent agents with ADK** (8h 30m) — поглиблений ADK
7. **Build AI Agents with Enterprise Databases** (4h) — MCP + БД
8. **Model Armor: Securing AI Deployments** (2h 30m) — безпека
9. **Deploy Multi-Agent Architectures** (2h 15m) — **🏆 Skill Badge**

## Порівняння

| Аспект | Course 1 (5-Day) | Course 3 (Agentic AI on GCP) |
|--------|:----------------:|:----------------------------:|
| Фокус | Архітектура агентів | Google Cloud екосистема |
| Whitepapers | ✅ 5 глибоких | ❌ Немає |
| Codelabs | ✅ 10 | ✅ 3+ labs |
| Memory/Context | ✅ Day 3 — цілий день | ❌ |
| Agent Quality/Observability | ✅ Day 4 — цілий день | ❌ |
| A2A Protocol | ✅ Day 5 | ✅ Module 9 |
| MCP | ✅ Day 2 | ✅ Module 7 |
| Enterprise Security | ❌ | ✅ Module 8 |
| NotebookLM | ❌ | ✅ Module 4 |
| Enterprise Databases | ❌ | ✅ Module 7 |
| Сертифікат | ❌ | ✅ Skill badge |
| Загальний час | ~20 год (тільки матеріали) | ~42 год |

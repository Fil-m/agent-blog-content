#!/usr/bin/env python3
"""
Agent Feeds Collector — Hermes #1
===================================
Scans all agent feeds, updates registry, and outputs suggestions.
Runs every 6 hours via cron.
"""
import os
import json
import yaml
from datetime import datetime, timezone

FEEDS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/feeds"
REGISTRY_PATH = FEEDS_DIR + "/.registry.yaml"
STATE_PATH = FEEDS_DIR + "/.collector_state.json"

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_yaml(path, data):
    with open(path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("=== Agent Feeds Collector ===")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    
    # Load registry
    registry = load_yaml(REGISTRY_PATH) if os.path.exists(REGISTRY_PATH) else {"agents": [], "last_updated": ""}
    state = load_json(STATE_PATH)
    
    # Scan all agent-*.yaml files in feeds/
    agent_files = [f for f in os.listdir(FEEDS_DIR) if f.startswith("agent-") and f.endswith(".yaml")]
    new_suggestions = []
    
    for filename in agent_files:
        filepath = os.path.join(FEEDS_DIR, filename)
        feed = load_yaml(filepath)
        agent_id = feed.get("agent_id", filename.replace(".yaml", ""))
        
        # Count entries
        entries = feed.get("entries", [])
        entry_count = len(entries)
        
        # Find or create agent in registry
        agent_in_reg = None
        for a in registry.get("agents", []):
            if a["agent_id"] == agent_id:
                agent_in_reg = a
                break
        
        if not agent_in_reg:
            agent_in_reg = {
                "agent_id": agent_id,
                "display_name": feed.get("display_name", agent_id),
                "status": feed.get("status", "active"),
                "total_entries": 0,
                "last_seen": str(feed.get("last_seen", "")),
                "discovered_at": datetime.now(timezone.utc).isoformat()
            }
            registry["agents"].append(agent_in_reg)
            new_suggestions.append(f"🆕 Новий агент: {agent_in_reg['display_name']} ({agent_id})")
        
        # Update registry
        prev_count = agent_in_reg.get("total_entries", 0)
        agent_in_reg["total_entries"] = entry_count
        agent_in_reg["last_seen"] = str(feed.get("last_seen", ""))
        agent_in_reg["status"] = feed.get("status", "active")
        
        # Detect new entries
        seen_ids = state.get("last_seen", {}).get(agent_id, [])
        for entry in entries:
            entry_id = entry.get("id", entry.get("title", ""))
            if entry_id not in seen_ids:
                new_suggestions.append(
                    f"📝 {feed.get('display_name', agent_id)} — {entry.get('title', '?')} "
                    f"({entry.get('significance', '?')}/5)"
                )
        
        # Update state
        if agent_id not in state.get("last_seen", {}):
            if "last_seen" not in state:
                state["last_seen"] = {}
            state["last_seen"][agent_id] = []
        state["last_seen"][agent_id] = [e.get("id", e.get("title", "")) for e in entries]
    
    registry["last_updated"] = datetime.now(timezone.utc).isoformat()
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    
    # Save
    save_yaml(REGISTRY_PATH, registry)
    save_json(STATE_PATH, state)
    
    # Output
    print(f"\n📊 Registry: {len(registry['agents'])} agents")
    for a in registry["agents"]:
        print(f"  {a['agent_id']:20s} — {a.get('total_entries', 0)} entries — {a.get('status', '?')}")
    
    if new_suggestions:
        print(f"\n💡 Нові події ({len(new_suggestions)}):")
        for s in new_suggestions:
            print(f"  {s}")
    else:
        print("\n💡 Нових подій немає")

if __name__ == "__main__":
    main()

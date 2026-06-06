#!/usr/bin/env python3
"""
Agent Feeds Collector — Hermes #1
Періодично:
1. Git pull agent-blog-content
2. Читає всі feeds/agent-*.yaml
3. Оновлює .registry.yaml (хто є, статус, останній entry)
4. Виявляє нові entries (яких не було в registry)
5. Моніторить tasks/ — статус задач, нові завершені
6. Моніторить context/ — нові запити від агентів
7. Нові entries + completed tasks → suggestions/ для Тараса
8. Git push registry
"""

import os
import sys
import json
import yaml
import time
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import hashlib

REPO_DIR = "/root/agent-blog-content"
REGISTRY_PATH = os.path.join(REPO_DIR, "feeds", ".registry.yaml")
SUGGESTIONS_DIR = os.path.join(REPO_DIR, "suggestions")
STATE_FILE = os.path.join(REPO_DIR, "feeds", ".collector_state.json")

def git_run(*args, cwd=REPO_DIR):
    """Run git command and return output."""
    result = subprocess.run(
        ["git"] + list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        print(f"git {' '.join(args)} failed: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout.strip()

def load_registry():
    """Load current registry."""
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            return yaml.safe_load(f) or {"agents": []}
    return {"agents": []}

def save_registry(registry):
    """Save registry."""
    with open(REGISTRY_PATH, "w") as f:
        yaml.dump(registry, f, default_flow_style=False, allow_unicode=True)

def load_state():
    """Load collector state (last seen entry IDs per agent)."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_seen": {}, "last_run": None}

def save_state(state):
    """Save collector state."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def parse_feeds():
    """Read all feeds/agent-*.yaml files and return dict of agent_id → data."""
    feeds_dir = os.path.join(REPO_DIR, "feeds")
    agents = {}
    
    if not os.path.exists(feeds_dir):
        return agents
    
    for fname in sorted(os.listdir(feeds_dir)):
        if not fname.startswith("agent-") or not fname.endswith(".yaml"):
            continue
        if fname.endswith(".feedback.yaml"):
            continue
        if fname == ".registry.yaml":
            continue
        
        fpath = os.path.join(feeds_dir, fname)
        try:
            with open(fpath) as f:
                data = yaml.safe_load(f)
            if data:
                aid = data.get("agent_id") or data.get("agent")
                if aid:
                    data["agent_id"] = aid
                    agents[aid] = data
        except Exception as e:
            print(f"Error reading {fname}: {e}", file=sys.stderr)
    
    return agents

def get_entry_ids(agent_data):
    """Get set of all entry IDs for an agent."""
    ids = set()
    for entry in agent_data.get("entries", []):
        if "id" in entry:
            ids.add(entry["id"])
    return ids

def main():
    print(f"=== Agent Feeds Collector === {datetime.now(timezone.utc).isoformat()}")
    
    # 1. Git pull
    print("1. Git pull...")
    git_run("pull")
    
    # 2. Parse all feeds
    print("2. Parsing feeds...")
    agents = parse_feeds()
    print(f"   Found {len(agents)} agents")
    
    # 3. Load state + registry
    state = load_state()
    registry = load_registry()
    
    # 4. Detect new entries per agent
    new_entries = {}
    for agent_id, data in agents.items():
        entry_ids = get_entry_ids(data)
        last_seen = state.get("last_seen", {}).get(agent_id, set())
        
        # Find new entry IDs
        new_ids = entry_ids - set(last_seen) if isinstance(last_seen, list) else entry_ids
        
        if new_ids:
            new_entries[agent_id] = []
            for entry in data.get("entries", []):
                if entry.get("id") in new_ids:
                    new_entries[agent_id].append(entry)
    
    # 5. Update registry
    print("3. Updating registry...")
    registry_agents = {a["agent_id"]: a for a in registry.get("agents", [])}
    
    for agent_id, data in agents.items():
        entry_count = len(data.get("entries", []))
        last_seen_str = data.get("last_seen", "")
        
        if agent_id in registry_agents:
            # Update existing
            registry_agents[agent_id]["last_seen"] = last_seen_str
            registry_agents[agent_id]["total_entries"] = entry_count
            registry_agents[agent_id]["status"] = data.get("status", "active")
        else:
            # New agent!
            registry_agents[agent_id] = {
                "agent_id": agent_id,
                "display_name": data.get("display_name", agent_id),
                "status": data.get("status", "registered"),
                "repo": data.get("repo", ""),
                "last_seen": last_seen_str,
                "total_entries": entry_count,
                "discovered_at": datetime.now(timezone.utc).isoformat()
            }
    
    registry["agents"] = sorted(registry_agents.values(), key=lambda x: x["agent_id"])
    registry["last_updated"] = datetime.now(timezone.utc).isoformat()
    save_registry(registry)
    
    # 6. Save new state
    print("4. Saving state...")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    for agent_id, data in agents.items():
        entry_ids = get_entry_ids(data)
        state.setdefault("last_seen", {})[agent_id] = list(entry_ids)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    
    # 7. Write new entries as suggestions
    if new_entries:
        print(f"5. New entries found: {sum(len(v) for v in new_entries.values())}")
        os.makedirs(SUGGESTIONS_DIR, exist_ok=True)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        suggestions = []
        
        for agent_id, entries in new_entries.items():
            for entry in entries:
                suggestions.append({
                    "agent_id": agent_id,
                    "entry_id": entry.get("id"),
                    "title": entry.get("title", ""),
                    "type": entry.get("type", ""),
                    "significance": entry.get("significance", 0),
                    "description": entry.get("description", ""),
                    "tags": entry.get("tags", []),
                    "discovered_at": ts
                })
        
        # Write suggestions file
        if suggestions:
            sug_path = os.path.join(SUGGESTIONS_DIR, f"collect_{ts}.yaml")
            with open(sug_path, "w") as f:
                yaml.dump({"suggestions": suggestions}, f, 
                         default_flow_style=False, allow_unicode=True)
            print(f"   Saved to {sug_path}")
            
            # Clean old suggestions (keep last 5)
            sug_files = sorted([
                f for f in os.listdir(SUGGESTIONS_DIR)
                if f.startswith("collect_") and f.endswith(".yaml")
            ])
            while len(sug_files) > 5:
                old = sug_files.pop(0)
                os.remove(os.path.join(SUGGESTIONS_DIR, old))
                print(f"   Cleaned old: {old}")
    else:
        print("5. No new entries found.")
    
    # 8. Git push registry changes
    print("6. Git push...")
    
    git_add_targets = ["feeds/.registry.yaml"]
    if os.path.exists(SUGGESTIONS_DIR) and os.listdir(SUGGESTIONS_DIR):
        git_add_targets.append("suggestions/")
    
    for target in git_add_targets:
        git_run("add", target)
    
    result = git_run("diff", "--cached", "--quiet")
    if result is None:
        # git diff --quiet returns 1 when there ARE changes → git_run returns None
        print("   Changes detected, committing...")
        git_run("commit", "-m", f"collector: оновлено registry [{ts}]")
        git_run("push")
        print("   Pushed.")
    else:
        print("   No changes to commit.")
    
    print("=== Done ===")

if __name__ == "__main__":
    main()

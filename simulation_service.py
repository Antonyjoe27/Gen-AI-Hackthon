# services/simulation_service.py
import uuid, time
import sqlite3
from transformers import pipeline

# simple story generator using text-generation pipeline
gen = pipeline("text-generation", model="distilgpt2")

DB = "data/db.sqlite3"
def _get_conn():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS scenarios(id TEXT PRIMARY KEY, seed TEXT, node TEXT, created REAL)")
    return conn

def create_scenario(seed: str, locale: str="en"):
    prompt = f"Create a short interactive misinformation scenario for learning, seed: {seed}. Provide first node text and 3 choices."
    out = gen(prompt, max_length=200, do_sample=True, num_return_sequences=1)[0]['generated_text']
    scenario_id = str(uuid.uuid4())
    conn = _get_conn()
    conn.execute("INSERT INTO scenarios(id,seed,node,created) VALUES (?,?,?,?)", (scenario_id, seed, out, time.time()))
    conn.commit()
    return {"scenario_id": scenario_id, "initial_node": out}

def progress_choice(scenario_id: str, node_id: str, choice_id: str, user_id: str=None):
    # Very simple: generate next text based on choice
    prompt = f"Scenario {scenario_id}. Node {node_id}. Choice {choice_id}. Continue story and explain consequences and feedback educationally."
    out = gen(prompt, max_length=200, do_sample=True)[0]['generated_text']
    return {"next": out}

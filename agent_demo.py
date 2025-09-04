#!/usr/bin/env python3

import argparse, json, re, time, warnings
from datetime import datetime, timezone
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

warnings.filterwarnings("ignore", category=DeprecationWarning)

def extract_json(s: str):
    i, j = s.find("{"), s.rfind("}")
    if i != -1 and j != -1 and j > i:
        try:
            obj = json.loads(s[i:j+1])
            return obj if isinstance(obj, dict) else None
        except Exception:
            return None
    return None

def enforce(data: dict, title: str):
    tags = data.get("tags") if isinstance(data.get("tags"), list) else []
    tags = [t.lower().strip() for t in tags if isinstance(t, str)][:3]
    if len(tags) < 3:
        for w in re.findall(r"[A-Za-z0-9]+", title.lower()):
            if w not in tags:
                tags.append(w)
            if len(tags) == 3: break
    summary = data.get("summary") if isinstance(data.get("summary"), str) else ""
    words = re.findall(r"\S+", summary)[:25]
    summary = " ".join(words)
    if summary and summary[-1] not in ".!?": summary += "."
    if not summary:
        summary = f"Brief overview of {title}."
    return {"tags": tags[:3], "summary": summary}

def print_block_like_sample(block: dict):
    # print only thought/message/data; issues live inside data (not as a top-level line)
    print(f"\"thought\": {json.dumps(block.get('thought',''), ensure_ascii=False)},")
    print(f"\"message\": {json.dumps(block.get('message',''), ensure_ascii=False)},")
    print(f"\"data\": {json.dumps(block.get('data',{}), ensure_ascii=False, indent=2)}")

def run_agent(llm, system_prompt: str, user_prompt: str):
    t0 = time.perf_counter()
    raw = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]).content
    ms = int((time.perf_counter() - t0) * 1000)
    j = extract_json(raw) or {}
    blk = {
        "thought": j.get("thought",""),
        "message": j.get("message",""),
        "data": j.get("data",{}) if isinstance(j.get("data",{}), dict) else {},
        "issues": j.get("issues", []),
    }
    # move issues into data (to match your sample)
    d = blk.get("data", {})
    d["issues"] = blk.get("issues", [])
    blk["data"] = d
    blk.pop("issues", None)
    return blk, ms

def main():
    ap = argparse.ArgumentParser(description="Planner → Reviewer (minimal, exact format)")
    ap.add_argument("--title", required=True)
    ap.add_argument("--content", required=True)
    ap.add_argument("--model", default="phi3:mini")
    ap.add_argument("--base-url", default="http://localhost:11434")
    args = ap.parse_args()

    llm = ChatOllama(model=args.model, base_url=args.base_url, format="json")

    # ----- Planner -----
    planner_sys = (
        "You are Planner. Return ONLY one JSON object (no prose, no code fences). "
        "Schema: {'thought':str,'message':str,'data':{'tags':[str,str,str],'summary':str},'issues':list}. "
        "data.tags: exactly 3 lowercase tags. data.summary: one sentence, <=25 words."
    )
    planner_usr = f"Title: {args.title}\n\nContent:\n{args.content}\n\nProduce the JSON now."
    planner_block, p_ms = run_agent(llm, planner_sys, planner_usr)
    print(f"\n== Planner ({p_ms} ms) ==")
    print_block_like_sample(planner_block)

    # ----- Reviewer (always return full JSON, with full Planner context) -----
    reviewer_sys = (
        "You are Reviewer. Always return a complete JSON object. "
        "Schema: {'thought':str,'message':str,'data':{'tags':[str,str,str],'summary':str},'issues':list}. "
        "If the Planner output is already good, copy it exactly. Never return empty values."
    )
    reviewer_usr = "Here is the Planner JSON:\n" + json.dumps(planner_block, ensure_ascii=False, indent=2)
    reviewer_block, r_ms = run_agent(llm, reviewer_sys, reviewer_usr)
    print(f"\n== Reviewer ({r_ms} ms) ==")
    print_block_like_sample(reviewer_block)

    # ----- Finalized output (minimal enforcement) -----
    raw = reviewer_block.get("data") or planner_block.get("data") or {}
    final_data = enforce(raw, args.title)
    finalized_block = {
        "thought": "Consolidated schema-checked output.",
        "message": planner_block.get("message") or reviewer_block.get("message") or "",
        "data": {**final_data, "issues": reviewer_block.get("data", {}).get("issues", [])},
    }
    print(f"\n== Finalized output ==")
    print_block_like_sample(finalized_block)

    # ----- Publish Package (top-level issues like your sample) -----
    publish_pkg = {
        "title": args.title,
        "content": args.content.strip(),
        "insight": planner_block.get("message", ""),
        "reviews": [{"role": "reviewer", "content": reviewer_block.get("message", "")}],
        "tags": final_data["tags"],
        "summary": final_data["summary"],
        "issues": reviewer_block.get("data", {}).get("issues", []),
    }
    print(f"\n== Publish Package ==")
    print(json.dumps(publish_pkg, ensure_ascii=False, indent=2))

    # trailing submissionDate line (timezone-aware, no warnings)
    print(f'\n"submissionDate": "{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"')

if __name__ == "__main__":
    main()

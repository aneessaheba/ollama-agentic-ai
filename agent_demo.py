#!/usr/bin/env python3

import argparse, json, re, time, warnings
from datetime import datetime, timezone
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

warnings.filterwarnings("ignore", category=DeprecationWarning)

def run_agent(llm, system_prompt: str, user_prompt: str):
    t0 = time.perf_counter()
    raw = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]).content
    ms = int((time.perf_counter() - t0) * 1000)
    j = json.loads(raw)
    blk = {
        "thought": j.get("thought",""),
        "summary": j.get("summary",""),
        "tags": j.get("tags",[]),
        "issues": j.get("issues", []),
    }
    return blk, ms

def main():
    ap = argparse.ArgumentParser(description="Planner → Reviewer (minimal, exact format)")
    ap.add_argument("--title", required=True)
    ap.add_argument("--content", required=True)
    ap.add_argument("--email", default="aneessaheba.guddi@sjsu.edu")
    ap.add_argument("--model", default="phi3:mini")
    ap.add_argument("--base-url", default="http://localhost:11434")
    args = ap.parse_args()
    email = args.email

    llm = ChatOllama(model=args.model, base_url=args.base_url, format="json")

    # ----- Planner -----
    planner_sys = (
        """You are Planner. Return ONLY one JSON object (no prose, no code fences). 
        Schema: {'thought':str,'tags':[str,str,str],'summary':str,'issues':list}. tags: exactly 3 lowercase tags. 
        summary: one sentence, <=25 words. Respond ONLY with valid JSON."""
    )
    planner_usr = f"Title: {args.title}\n\nContent:\n{args.content}\n\nProduce the JSON now."
    planner_block, p_ms = run_agent(llm, planner_sys, planner_usr)
    print(f"\n== Planner ({p_ms} ms) ==")
    print(json.dumps(planner_block, indent=2, ensure_ascii=False))

    # ----- Reviewer (always return full JSON, with full Planner context) -----
    reviewer_sys = (
        "You are Reviewer. Always return a complete JSON object. "
        "Schema: {'thought':str, 'tags':[str,str,str],'summary':str,'issues':list}. "
        "If the Planner output is already good correct it. Never return empty values."
        "issues should be what was wrong with the planner output (if anything)."
    )
    reviewer_usr = "Here is the Planner JSON:\n" + json.dumps(planner_block, ensure_ascii=False, indent=2)
    reviewer_block, r_ms = run_agent(llm, reviewer_sys, reviewer_usr)
    print(f"\n== Reviewer ({r_ms} ms) ==")
    print(json.dumps(reviewer_block, indent=2, ensure_ascii=False))

    # ----- Finalized output (minimal enforcement) -----
    finalized_block = {
        "title": args.title,
        "content": args.content.strip(),
        "email": email,
        **reviewer_block,
    }
    print(f"\n== Finalized output ==")
    print(json.dumps(finalized_block, indent=2, ensure_ascii=False))

    # ----- Publish Package (top-level issues like your sample) -----
    publish_pkg = {
        "title": args.title,
        "content": args.content.strip(),
        "email": email,
        "reviews": [{"role": "planner", "summary": planner_block.get("summary", "")}, {"role": "reviewer", "summary": reviewer_block.get("summary", "")}],
        "tags": reviewer_block["tags"],
        "summary": reviewer_block["summary"],
        "issues": reviewer_block.get("issues", []),
    }
    print(f"\n== Publish Package ==")
    print(json.dumps(publish_pkg, indent=2, ensure_ascii=False))

    # trailing submissionDate line (timezone-aware, no warnings)
    print(f'\n"submissionDate": "{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"')

if __name__ == "__main__":
    main()

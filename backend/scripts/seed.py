"""
Seed database with chapters, quizzes, and content sections.
Run from backend/ directory: python scripts/seed.py
Requires: database running + alembic upgrade head already applied.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.chapter import Chapter
from app.models.content_section import ContentSection
from app.models.quiz import Quiz, QuizQuestion

# ── Course Content: AI Agent Development (Option A) ──────────────────────────

CHAPTERS_DATA = [
    {
        "order_index": 1,
        "title": "Introduction to AI Agents",
        "tier": "free",
        "summary": "Learn what AI agents are, how they reason, and why they matter.",
        "body": """# Introduction to AI Agents

An AI agent is a software system that perceives its environment, makes decisions, and takes actions to achieve goals. Unlike traditional programs that follow fixed rules, AI agents can adapt to new situations using large language models (LLMs) as their reasoning engine.

## What Makes Something an Agent?

An agent has four key properties:
1. **Perception** – It can receive information from its environment (user messages, tool outputs, database results).
2. **Reasoning** – It can think through a problem and decide what to do next (powered by an LLM).
3. **Action** – It can execute tools, call APIs, write code, or produce responses.
4. **Memory** – It can retain context across multiple turns of a conversation.

## Why AI Agents Matter

Traditional software is deterministic: the same input always produces the same output. AI agents are probabilistic and adaptive — they can handle novel situations that were never explicitly programmed.

The Agent Factory Architecture teaches you to build production-grade agents that are reliable, cost-efficient, and scalable.

## Key Concepts

- **LLM (Large Language Model)**: The brain of the agent. Examples: Claude, GPT-4.
- **Tool**: A function the agent can call to interact with the world (e.g., search, calculator, database).
- **Context window**: The memory the LLM can "see" at one time.
- **Agent loop**: The cycle of perceive → reason → act → perceive.
""",
        "word_count": 220,
    },
    {
        "order_index": 2,
        "title": "Claude Agent SDK",
        "tier": "free",
        "summary": "Build agents with Anthropic's Claude Agent SDK — tools, memory, and multi-turn conversations.",
        "body": """# Claude Agent SDK

The Claude Agent SDK is Anthropic's official library for building agentic applications with Claude. It provides high-level abstractions for creating agents that use tools, maintain context, and execute multi-step workflows.

## Installation

```bash
pip install claude-agent-sdk
```

## Core Components

### 1. Agent
The `Agent` class is the central object. You define its instructions, tools, and model.

```python
from claude_agent_sdk import Agent, Tool

agent = Agent(
    model="claude-sonnet-4-6",
    instructions="You are a helpful coding assistant.",
    tools=[search_tool, code_tool],
)
```

### 2. Tools
Tools are Python functions decorated with `@tool` that the agent can call.

```python
@tool
def search_web(query: str) -> str:
    \"\"\"Search the web for information.\"\"\"
    return perform_search(query)
```

### 3. Threads and Runs
A **Thread** holds the conversation history. A **Run** executes the agent for one turn.

```python
thread = agent.create_thread()
run = agent.run(thread_id=thread.id, user_message="Explain recursion")
print(run.final_message)
```

## Agent Loop

When you call `agent.run()`:
1. Claude receives the conversation history + user message
2. Claude decides whether to use a tool or respond directly
3. If a tool is called, the result is added to context
4. Loop continues until Claude produces a final response

## Key Principles

- Keep tools focused and single-purpose
- Write clear tool descriptions (Claude uses them to decide when to call)
- Handle tool errors gracefully — return error strings, not exceptions
""",
        "word_count": 265,
    },
    {
        "order_index": 3,
        "title": "Model Context Protocol (MCP)",
        "tier": "free",
        "summary": "Understand MCP — the universal standard for connecting AI agents to tools and data.",
        "body": """# Model Context Protocol (MCP)

MCP (Model Context Protocol) is an open standard developed by Anthropic that defines how AI agents connect to external tools, data sources, and services. Think of MCP as USB-C for AI — a single universal connector.

## Why MCP Exists

Before MCP, every AI application had to build custom integrations for every tool. A coding agent needed custom code to connect to GitHub, Jira, Slack, and databases — all separately. MCP solves this by standardising the interface.

## MCP Architecture

```
Claude (MCP Client)
      ↕  MCP Protocol
MCP Server (e.g., GitHub MCP Server)
      ↕
GitHub API
```

## MCP Components

### MCP Server
An MCP Server exposes **resources** and **tools** via a standardised JSON-RPC interface.

- **Resources**: Read-only data (e.g., file contents, database records)
- **Tools**: Executable functions (e.g., create PR, search issues)
- **Prompts**: Reusable prompt templates

### MCP Client
The client (e.g., Claude Code, your agent) connects to one or more MCP servers and discovers available tools automatically.

## Example: Connecting to an MCP Server

```python
from claude_agent_sdk import Agent
from claude_agent_sdk.mcp import MCPServerStdio

agent = Agent(
    model="claude-sonnet-4-6",
    mcp_servers=[
        MCPServerStdio(command="npx", args=["-y", "@modelcontextprotocol/server-github"]),
    ],
)
```

## Key Benefits

- **Reusability**: One MCP server works with any compatible AI client
- **Security**: Each server runs in isolation
- **Discovery**: Agents discover tools dynamically — no hardcoding
- **Ecosystem**: 1000+ community MCP servers available

MCP is the foundation of Layer 6 in the Agent Factory Architecture.
""",
        "word_count": 290,
    },
    {
        "order_index": 4,
        "title": "Agent Skills and SKILL.md",
        "tier": "premium",
        "summary": "Encode agent behaviours as SKILL.md files — the spec-driven approach to consistent AI actions.",
        "body": """# Agent Skills and SKILL.md

An Agent Skill is a named, documented procedure that teaches an AI agent how to perform a specific task consistently. Skills are stored as SKILL.md files — Markdown documents that the agent's system prompt references.

## Why Skills Matter

Without skills, agents improvise. With skills, agents follow repeatable procedures that produce consistent, high-quality outputs. Skills are the "training manuals" for your Digital FTE.

## SKILL.md Structure

Every SKILL.md file must contain:

```markdown
# Skill: concept-explainer

## Metadata
- Name: concept-explainer
- Triggers: "explain", "what is", "how does"
- Version: 1.0.0

## Purpose
Explain technical concepts at the appropriate complexity level for the learner.

## Workflow
1. Identify the concept from the user's question
2. Assess learner level (beginner/intermediate/advanced) from conversation context
3. Fetch relevant content from the backend: GET /search?q={concept}
4. Structure explanation: definition → analogy → example → check understanding
5. Ask: "Does that make sense? Want me to go deeper?"

## Response Templates
**Beginner**: "Think of {concept} like {simple analogy}..."
**Advanced**: "At its core, {concept} is {technical definition}..."

## Key Principles
- Only explain using content from the provided sections
- Never invent facts not in the source material
- Always end with a comprehension check
```

## Skills vs Tools

| | Skills | Tools |
|--|--------|-------|
| What | Procedural knowledge | Executable functions |
| Where | SKILL.md in system prompt | Backend API endpoints |
| How | LLM follows the workflow | LLM calls the function |
| Example | How to explain a concept | GET /chapters/1 |

## Deploying Skills

Skills are embedded in the ChatGPT App system prompt. When a student message matches a trigger keyword, Claude activates the corresponding skill workflow automatically.
""",
        "word_count": 295,
    },
    {
        "order_index": 5,
        "title": "A2A Protocol and Multi-Agent Systems",
        "tier": "premium",
        "summary": "Agent-to-Agent communication — how specialised agents collaborate to solve complex tasks.",
        "body": """# A2A Protocol and Multi-Agent Systems

The A2A (Agent-to-Agent) Protocol enables multiple AI agents to collaborate by communicating with each other through a standardised interface. In complex workflows, a single agent is often insufficient — A2A allows specialist agents to work together.

## The Problem A2A Solves

Consider a research task: one agent searches the web, another analyses documents, a third writes a summary. Without A2A, these agents can't communicate. With A2A, they form a pipeline.

## A2A Architecture

```
Orchestrator Agent
    ├── Search Agent (MCP: web search)
    ├── Analysis Agent (MCP: document tools)
    └── Writing Agent (MCP: text tools)
```

## A2A Message Format

A2A uses JSON messages with a standard envelope:

```json
{
  "from": "orchestrator-agent-id",
  "to": "search-agent-id",
  "task": "search_web",
  "payload": {"query": "AI agent frameworks 2026"},
  "conversation_id": "conv-abc123"
}
```

## Agent Factory Layer 7

In the Agent Factory Architecture, A2A is Layer 7 — the top-most layer responsible for multi-agent orchestration. It sits above:
- L5: Claude Agent SDK (single-agent execution)
- L6: Skills + MCP (tools and knowledge)

## Building A2A Systems

```python
from claude_agent_sdk import Agent
from claude_agent_sdk.a2a import A2AOrchestrator

orchestrator = A2AOrchestrator(agents=[
    search_agent,
    analysis_agent,
    writing_agent,
])

result = await orchestrator.run("Research the latest MCP developments")
```

## Key Principle

In Phase 1 of the Course Companion FTE, A2A is out of scope. It becomes relevant in Phase 2 when the AI Mentor Agent feature needs multi-turn, multi-step tutoring workflows that exceed what a single agent context window can handle.
""",
        "word_count": 300,
    },
]

QUIZZES_DATA = [
    {
        "chapter_order": 1,
        "title": "Chapter 1 Quiz: AI Agent Fundamentals",
        "questions": [
            {
                "position": 1,
                "question_text": "What are the four key properties of an AI agent?",
                "options": {
                    "A": "Speed, accuracy, cost, and reliability",
                    "B": "Perception, reasoning, action, and memory",
                    "C": "Input, processing, output, and storage",
                    "D": "Training, testing, deployment, and monitoring",
                },
                "correct_option": "B",
                "explanation": "An agent perceives its environment, reasons about it (via LLM), takes actions (via tools), and retains memory across turns.",
            },
            {
                "position": 2,
                "question_text": "What is the 'agent loop'?",
                "options": {
                    "A": "A bug where agents run infinitely",
                    "B": "The cycle of: perceive → reason → act → perceive",
                    "C": "A loop construct in Python for iterating over agents",
                    "D": "The process of training an LLM",
                },
                "correct_option": "B",
                "explanation": "The agent loop is the fundamental cycle that drives agentic behaviour: sense the environment, reason about it, act, then sense again.",
            },
            {
                "position": 3,
                "question_text": "How does an AI agent differ from traditional software?",
                "options": {
                    "A": "Agents are faster than traditional software",
                    "B": "Agents are cheaper to build",
                    "C": "Agents are probabilistic and adaptive; traditional software is deterministic",
                    "D": "Agents don't need a programming language",
                },
                "correct_option": "C",
                "explanation": "Traditional software produces the same output for the same input. Agents adapt to novel situations using LLM reasoning.",
            },
            {
                "position": 4,
                "question_text": "What is an LLM's role in an AI agent?",
                "options": {
                    "A": "It stores the agent's data in a database",
                    "B": "It executes the agent's tools",
                    "C": "It serves as the reasoning/decision-making brain",
                    "D": "It handles the agent's network connections",
                },
                "correct_option": "C",
                "explanation": "The LLM is the brain of the agent — it receives context and decides what to do next (use a tool, ask a clarifying question, or respond).",
            },
            {
                "position": 5,
                "question_text": "What is a 'context window' in the context of AI agents?",
                "options": {
                    "A": "The GUI window of an agent application",
                    "B": "The maximum amount of text the LLM can 'see' at one time",
                    "C": "The time window during which an agent is active",
                    "D": "The number of tools an agent can use simultaneously",
                },
                "correct_option": "B",
                "explanation": "The context window is the LLM's working memory — all the text (conversation, tool results, instructions) it can process in one call.",
            },
        ],
    },
    {
        "chapter_order": 2,
        "title": "Chapter 2 Quiz: Claude Agent SDK",
        "questions": [
            {
                "position": 1,
                "question_text": "What is the primary purpose of the Claude Agent SDK?",
                "options": {
                    "A": "To train new Claude models",
                    "B": "To provide high-level abstractions for building agentic applications with Claude",
                    "C": "To replace the Anthropic API entirely",
                    "D": "To create frontend user interfaces",
                },
                "correct_option": "B",
                "explanation": "The Claude Agent SDK simplifies agentic development by providing Agent, Tool, Thread, and Run abstractions.",
            },
            {
                "position": 2,
                "question_text": "In the Claude Agent SDK, what is a 'Thread'?",
                "options": {
                    "A": "A Python threading construct for parallel execution",
                    "B": "An object that holds conversation history",
                    "C": "A tool that runs background tasks",
                    "D": "A connection to the Anthropic API",
                },
                "correct_option": "B",
                "explanation": "A Thread holds the full conversation history, allowing the agent to maintain context across multiple turns.",
            },
            {
                "position": 3,
                "question_text": "How should tool errors be handled in Claude Agent SDK?",
                "options": {
                    "A": "Raise Python exceptions — they are caught automatically",
                    "B": "Return error strings — let Claude decide how to respond",
                    "C": "Exit the agent loop immediately",
                    "D": "Retry the tool call up to 10 times",
                },
                "correct_option": "B",
                "explanation": "Tools should return error strings (not raise exceptions) so Claude can read the error and decide how to handle it gracefully.",
            },
            {
                "position": 4,
                "question_text": "What does the `@tool` decorator do?",
                "options": {
                    "A": "Registers a Python function as a callable tool the agent can use",
                    "B": "Makes a function run asynchronously",
                    "C": "Adds authentication to an API endpoint",
                    "D": "Caches the function's output",
                },
                "correct_option": "A",
                "explanation": "The @tool decorator registers a Python function as a tool the agent can call. The function's docstring tells Claude when and how to use it.",
            },
            {
                "position": 5,
                "question_text": "What happens during `agent.run()`?",
                "options": {
                    "A": "The agent trains on new data",
                    "B": "Claude receives context, may call tools, loops until producing a final response",
                    "C": "The agent creates a new Thread",
                    "D": "The agent connects to MCP servers",
                },
                "correct_option": "B",
                "explanation": "agent.run() executes the agent loop: Claude receives context, decides whether to call tools or respond, and loops until a final answer is produced.",
            },
        ],
    },
    {
        "chapter_order": 3,
        "title": "Chapter 3 Quiz: Model Context Protocol",
        "questions": [
            {
                "position": 1,
                "question_text": "What is the best analogy for MCP?",
                "options": {
                    "A": "MCP is like HTTP for web browsers",
                    "B": "MCP is like USB-C for AI — a universal connector standard",
                    "C": "MCP is like SQL for databases",
                    "D": "MCP is like Docker for containers",
                },
                "correct_option": "B",
                "explanation": "MCP is described as 'USB-C for AI' — a single universal connector standard that allows any compatible AI agent to connect to any compatible tool or data source.",
            },
            {
                "position": 2,
                "question_text": "What are the three types of capabilities an MCP Server can expose?",
                "options": {
                    "A": "APIs, databases, and files",
                    "B": "Resources, tools, and prompts",
                    "C": "Inputs, outputs, and errors",
                    "D": "Read, write, and execute",
                },
                "correct_option": "B",
                "explanation": "MCP Servers expose: Resources (read-only data), Tools (executable functions), and Prompts (reusable prompt templates).",
            },
            {
                "position": 3,
                "question_text": "Why was MCP created?",
                "options": {
                    "A": "To replace the JSON-RPC protocol",
                    "B": "To make AI models faster",
                    "C": "To eliminate custom integrations for every tool in every AI application",
                    "D": "To provide a new database query language",
                },
                "correct_option": "C",
                "explanation": "Before MCP, every AI app needed custom integration code for every tool. MCP standardises the interface so one server works with any compatible client.",
            },
            {
                "position": 4,
                "question_text": "In which Agent Factory Architecture layer does MCP sit?",
                "options": {
                    "A": "L3 — FastAPI",
                    "B": "L5 — Claude Agent SDK",
                    "C": "L6 — Runtime Skills + MCP",
                    "D": "L7 — A2A Protocol",
                },
                "correct_option": "C",
                "explanation": "MCP is part of Layer 6 (Runtime Skills + MCP) in the Agent Factory 8-layer architecture, alongside SKILL.md files.",
            },
            {
                "position": 5,
                "question_text": "What protocol does MCP use for communication?",
                "options": {
                    "A": "REST/HTTP",
                    "B": "GraphQL",
                    "C": "WebSockets",
                    "D": "JSON-RPC",
                },
                "correct_option": "D",
                "explanation": "MCP uses JSON-RPC as its underlying communication protocol between clients and servers.",
            },
        ],
    },
    {
        "chapter_order": 4,
        "title": "Chapter 4 Quiz: Agent Skills",
        "questions": [
            {
                "position": 1,
                "question_text": "What is an Agent Skill?",
                "options": {
                    "A": "A Python class that inherits from BaseAgent",
                    "B": "A named, documented procedure stored as a SKILL.md file",
                    "C": "A machine learning model fine-tuned for a specific task",
                    "D": "An API endpoint exposed by the backend",
                },
                "correct_option": "B",
                "explanation": "An Agent Skill is a named, documented procedure in a SKILL.md file that teaches the agent how to perform a specific task consistently.",
            },
            {
                "position": 2,
                "question_text": "What are the required sections in every SKILL.md file?",
                "options": {
                    "A": "Name, author, date, and changelog",
                    "B": "Metadata, Purpose, Workflow, Response Templates, Key Principles",
                    "C": "Input, output, examples, and tests",
                    "D": "Title, description, and code examples",
                },
                "correct_option": "B",
                "explanation": "Every SKILL.md must contain: Metadata (name, triggers), Purpose, Workflow (step-by-step), Response Templates, and Key Principles.",
            },
            {
                "position": 3,
                "question_text": "How are skills deployed in the Course Companion FTE?",
                "options": {
                    "A": "Uploaded to Cloudflare R2 as JSON files",
                    "B": "Stored in PostgreSQL and fetched at runtime",
                    "C": "Embedded in the ChatGPT App system prompt",
                    "D": "Compiled into the FastAPI backend",
                },
                "correct_option": "C",
                "explanation": "Skills are embedded in the ChatGPT App system prompt in manifest.yaml, making them available to Claude as procedural knowledge for every interaction.",
            },
            {
                "position": 4,
                "question_text": "What is the key difference between Skills and Tools?",
                "options": {
                    "A": "Skills are faster; tools are more accurate",
                    "B": "Skills are procedural knowledge (LLM follows workflow); tools are executable functions (LLM calls function)",
                    "C": "Skills are written in Python; tools are written in JavaScript",
                    "D": "Skills are premium features; tools are free",
                },
                "correct_option": "B",
                "explanation": "Skills = procedural knowledge in the system prompt (LLM follows a workflow). Tools = executable backend functions (LLM calls an API).",
            },
            {
                "position": 5,
                "question_text": "What triggers a skill to activate?",
                "options": {
                    "A": "A specific API call from the backend",
                    "B": "A time-based schedule",
                    "C": "Student message matching trigger keywords defined in Metadata",
                    "D": "A database event",
                },
                "correct_option": "C",
                "explanation": "Skills are activated when the student's message contains trigger keywords defined in the skill's Metadata section (e.g., 'explain', 'quiz me', 'I'm stuck').",
            },
        ],
    },
    {
        "chapter_order": 5,
        "title": "Chapter 5 Quiz: A2A Protocol",
        "questions": [
            {
                "position": 1,
                "question_text": "What does A2A stand for?",
                "options": {
                    "A": "API-to-API",
                    "B": "Agent-to-Agent",
                    "C": "Authentication-to-Authorisation",
                    "D": "Async-to-Async",
                },
                "correct_option": "B",
                "explanation": "A2A stands for Agent-to-Agent Protocol — the standard for communication between multiple AI agents.",
            },
            {
                "position": 2,
                "question_text": "In which Agent Factory Architecture layer does A2A sit?",
                "options": {
                    "A": "L3 — FastAPI",
                    "B": "L5 — Claude Agent SDK",
                    "C": "L6 — Runtime Skills + MCP",
                    "D": "L7 — A2A Protocol",
                },
                "correct_option": "D",
                "explanation": "A2A is Layer 7 — the top-most layer in the Agent Factory Architecture, responsible for multi-agent orchestration.",
            },
            {
                "position": 3,
                "question_text": "In which Phase of the Course Companion FTE is A2A introduced?",
                "options": {
                    "A": "Phase 1 (Zero-Backend-LLM)",
                    "B": "Phase 2 (Hybrid Intelligence, AI Mentor Agent feature)",
                    "C": "Phase 3 (Full Web App)",
                    "D": "It is never used in the Course Companion FTE",
                },
                "correct_option": "B",
                "explanation": "A2A becomes relevant in Phase 2 when the AI Mentor Agent feature needs multi-turn, multi-step tutoring workflows beyond a single agent's context window.",
            },
            {
                "position": 4,
                "question_text": "What problem does A2A solve?",
                "options": {
                    "A": "It makes agents run faster by parallelising LLM calls",
                    "B": "It enables specialist agents to communicate and collaborate on complex tasks",
                    "C": "It reduces the cost of LLM API calls",
                    "D": "It provides authentication between agents and backend services",
                },
                "correct_option": "B",
                "explanation": "A2A enables specialist agents (search agent, analysis agent, writing agent) to communicate and collaborate — each handling what it does best.",
            },
            {
                "position": 5,
                "question_text": "What format does A2A use for messages?",
                "options": {
                    "A": "XML envelopes",
                    "B": "Protocol Buffers (protobuf)",
                    "C": "JSON messages with a standard envelope (from, to, task, payload, conversation_id)",
                    "D": "Plain text with YAML headers",
                },
                "correct_option": "C",
                "explanation": "A2A uses JSON messages with a standard envelope containing: from, to, task, payload, and conversation_id fields.",
            },
        ],
    },
]


async def seed_database():
    engine = create_async_engine(settings.DATABASE_URL)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        # Check if already seeded
        existing = await session.execute(select(Chapter))
        if existing.scalars().first() is not None:
            print("Database already seeded. Skipping.")
            return

        print("Seeding chapters...")
        chapter_map = {}  # order_index → Chapter

        for ch_data in CHAPTERS_DATA:
            slug = ch_data["title"].lower().replace(" ", "-").replace("(", "").replace(")", "")
            r2_key = f"chapters/{ch_data['order_index']}/{slug}.json"

            chapter = Chapter(
                title=ch_data["title"],
                r2_key=r2_key,
                order_index=ch_data["order_index"],
                tier=ch_data["tier"],
                summary=ch_data["summary"],
            )
            session.add(chapter)
            await session.flush()
            chapter_map[ch_data["order_index"]] = chapter

            # Upload to R2
            from app.r2_client import upload_chapter_body
            try:
                upload_chapter_body(r2_key, {
                    "chapter_id": chapter.id,
                    "title": ch_data["title"],
                    "body": ch_data["body"],
                    "word_count": ch_data["word_count"],
                })
                print(f"  ✓ Chapter {ch_data['order_index']}: {ch_data['title']} → R2")
            except Exception as e:
                print(f"  ⚠ R2 upload failed for chapter {ch_data['order_index']}: {e}")

        await session.commit()

        print("\nSeeding quizzes and questions...")
        for quiz_data in QUIZZES_DATA:
            chapter = chapter_map[quiz_data["chapter_order"]]

            quiz = Quiz(chapter_id=chapter.id, title=quiz_data["title"])
            session.add(quiz)
            await session.flush()

            # Update chapter with quiz_id
            chapter.quiz_id = quiz.id
            session.add(chapter)

            for q_data in quiz_data["questions"]:
                question = QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=q_data["question_text"],
                    options=q_data["options"],
                    correct_option=q_data["correct_option"],
                    explanation=q_data["explanation"],
                    position=q_data["position"],
                )
                session.add(question)

            print(f"  ✓ Quiz for Chapter {quiz_data['chapter_order']}: {len(quiz_data['questions'])} questions")

        await session.commit()

        print("\nSeeding content sections for full-text search...")
        for ch_data in CHAPTERS_DATA:
            chapter = chapter_map[ch_data["order_index"]]
            paragraphs = [p.strip() for p in ch_data["body"].split("\n\n") if p.strip() and len(p.strip()) > 50]

            for i, para in enumerate(paragraphs):
                section = ContentSection(
                    chapter_id=chapter.id,
                    section_index=i + 1,
                    text=para,
                )
                session.add(section)

            print(f"  ✓ Chapter {ch_data['order_index']}: {len(paragraphs)} content sections indexed")

        await session.commit()

    await engine.dispose()
    print("\n✅ Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_database())

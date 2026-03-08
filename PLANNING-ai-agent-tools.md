# AI Agent Tools & Frameworks API Endpoints Directory -- Planning Document

> Transition guide for building a new repository modeled after
> [text-generation-ai-llm-tools-endpoints-api-list-repository](https://github.com/TaylorAmarelTech/text-generation-ai-llm-tools-endpoints-api-list-repository)
> and [ai-image-generation-api-endpoints-directory](https://github.com/TaylorAmarelTech/ai-image-generation-api-endpoints-directory).
> Same architecture, adapted for **AI agent tools, frameworks, and orchestration APIs**.

---

## 1. Repo Identity

| Field | Value |
|:------|:------|
| **Repo Name** | `ai-agent-tools-frameworks-api-directory` |
| **Tagline** | The most comprehensive directory of free & affordable AI agent tools, frameworks, and orchestration APIs |
| **Scope** | Agent frameworks, tool/function calling, orchestration platforms, MCP servers, agent-as-a-service, code execution sandboxes, browser automation, memory/RAG, search/retrieval, workflow engines |
| **Version** | 0.1.0 (initial release) |

**Suggested GitHub Topics:**
`ai-agents`, `agent-framework`, `langchain`, `crewai`, `autogen`, `mcp`, `function-calling`, `tool-use`, `agent-orchestration`, `rag`, `ai-tools`, `agentic-ai`, `api-directory`, `free-api`

---

## 2. Known Providers to Catalog

### Tier 1: Truly Free (no credit card, ongoing)

| Provider | Endpoint / Package | Free Limits | Category | SDK / Protocol |
|:---------|:-------------------|:------------|:---------|:---------------|
| **LangChain** | `pip install langchain` | Unlimited (OSS) | Framework | Python, JS |
| **LangGraph** | `pip install langgraph` | Unlimited (OSS) | Orchestration | Python, JS |
| **CrewAI** | `pip install crewai` | Unlimited (OSS) | Multi-agent | Python |
| **AutoGen (Microsoft)** | `pip install autogen-agentchat` | Unlimited (OSS) | Multi-agent | Python |
| **Smolagents (HuggingFace)** | `pip install smolagents` | Unlimited (OSS) | Framework | Python |
| **Haystack (deepset)** | `pip install haystack-ai` | Unlimited (OSS) | RAG + Agents | Python |
| **Semantic Kernel (Microsoft)** | `pip install semantic-kernel` | Unlimited (OSS) | Framework | Python, C#, Java |
| **LlamaIndex** | `pip install llama-index` | Unlimited (OSS) | RAG + Agents | Python, TS |
| **DSPy** | `pip install dspy` | Unlimited (OSS) | Prompt Programming | Python |
| **Pydantic AI** | `pip install pydantic-ai` | Unlimited (OSS) | Framework | Python |
| **Instructor** | `pip install instructor` | Unlimited (OSS) | Structured Output | Python, TS |
| **Marvin** | `pip install marvin` | Unlimited (OSS) | AI Functions | Python |
| **Anthropic Claude Agent SDK** | `pip install claude-agent-sdk` | Unlimited (OSS) | Agent SDK | Python |
| **OpenAI Agents SDK** | `pip install openai-agents` | Unlimited (OSS) | Agent SDK | Python |
| **Google ADK** | `pip install google-adk` | Unlimited (OSS) | Agent SDK | Python |
| **Composio** | `https://api.composio.dev/api/v1/...` | 1000 free actions/mo | Tool Platform | Python, JS |
| **Model Context Protocol (MCP)** | Spec + SDKs | Unlimited (OSS) | Protocol | Python, TS |
| **Ollama** | `http://localhost:11434/api/...` | Unlimited (local) | Local LLM | REST |
| **E2B** | `https://api.e2b.dev/...` | 100 sandbox hrs/mo | Code Sandbox | Python, JS |
| **Mem0** | `pip install mem0ai` | Unlimited (OSS) | Memory Layer | Python |
| **Chroma** | `pip install chromadb` | Unlimited (OSS) | Vector DB | Python, JS |
| **Qdrant** | `pip install qdrant-client` | Unlimited (OSS) | Vector DB | Python, JS, REST |
| **SearXNG** | Self-hosted | Unlimited | Search Engine | REST |
| **Crawl4AI** | `pip install crawl4ai` | Unlimited (OSS) | Web Scraping | Python |
| **Firecrawl (OSS)** | `pip install firecrawl` | Unlimited (self-host) | Web Scraping | Python, JS |
| **Browser Use** | `pip install browser-use` | Unlimited (OSS) | Browser Agent | Python |
| **Playwright** | `pip install playwright` | Unlimited (OSS) | Browser Auto | Python, JS |
| **Stagehand (Browserbase)** | `npm install @browserbasehq/stagehand` | Unlimited (OSS) | AI Browser | JS/TS |

### Tier 2: Generous Free Tier

| Provider | Endpoint | Free Limits | Category |
|:---------|:---------|:------------|:---------|
| **LangSmith** | `https://api.smith.langchain.com/...` | 5K traces/mo | Observability |
| **Tavily** | `https://api.tavily.com/search` | 1000 searches/mo | Agent Search |
| **Browserbase** | `https://api.browserbase.com/v1/...` | 100 sessions/mo | Cloud Browser |
| **Apify** | `https://api.apify.com/v2/...` | $5/mo free | Web Scraping |
| **Serper** | `https://google.serper.dev/search` | 2500 searches/mo | Search API |
| **Jina AI** | `https://r.jina.ai/...` | 1M tokens/mo | Reader/Embeddings |
| **Exa (formerly Metaphor)** | `https://api.exa.ai/search` | 1000 searches/mo | Neural Search |
| **Weaviate Cloud** | `https://{cluster}.weaviate.cloud/...` | 1 free sandbox | Vector DB |
| **Pinecone** | `https://controller.{env}.pinecone.io/...` | 1 free index | Vector DB |
| **Supabase** | `https://{ref}.supabase.co/...` | 500MB + pgvector | Vector DB + Auth |
| **Neon** | `postgresql://...neon.tech/...` | 0.5GB free | Postgres + pgvector |
| **Upstash** | `https://{endpoint}.upstash.io/...` | 10K commands/day | Redis + Vector |
| **AgentOps** | `https://api.agentops.ai/v2/...` | 1000 events/mo | Observability |
| **Helicone** | `https://oai.helicone.ai/v1/...` | 100K logs/mo | LLM Proxy/Logging |
| **Portkey** | `https://api.portkey.ai/v1/...` | 10K logs/mo | AI Gateway |

### Tier 3: Free Credits on Signup

| Provider | Endpoint | Free Credits | Category |
|:---------|:---------|:-------------|:---------|
| **OpenAI (function calling)** | `https://api.openai.com/v1/chat/completions` | $5 credits | Tool Use LLM |
| **Anthropic (tool use)** | `https://api.anthropic.com/v1/messages` | $5 credits | Tool Use LLM |
| **Google Gemini (function calling)** | `https://generativelanguage.googleapis.com/v1beta/...` | Free tier | Tool Use LLM |
| **Groq** | `https://api.groq.com/openai/v1/...` | Free tier | Fast Inference |
| **Together AI** | `https://api.together.xyz/v1/...` | $5 credits | Tool Use LLM |
| **Fireworks AI** | `https://api.fireworks.ai/inference/v1/...` | $1 credits | Tool Use LLM |
| **Cohere** | `https://api.cohere.com/v2/chat` | Free trial | Tool Use LLM |
| **Mistral** | `https://api.mistral.ai/v1/agents/completions` | Free tier | Agent API |
| **DeepInfra** | `https://api.deepinfra.com/v1/openai/...` | $5 credits | Tool Use LLM |
| **Firecrawl (Cloud)** | `https://api.firecrawl.dev/v1/...` | 500 credits | Web Scraping |
| **Toolhouse** | `https://api.toolhouse.ai/v1/...` | Free credits | Tool Platform |
| **Arcade AI** | `https://api.arcade-ai.com/v1/...` | Free tier | Tool Platform |

### Tier 4: Freemium (credit card or paid plan)

| Provider | Endpoint | Free Limits | Category |
|:---------|:---------|:------------|:---------|
| **LangGraph Cloud** | `https://api.langchain.com/...` | Limited free | Managed Orchestration |
| **Relevance AI** | `https://api.relevanceai.com/latest/...` | 100 credits/day | Agent Platform |
| **Wordware** | `https://app.wordware.ai/api/...` | Free tier | Visual Agent Builder |
| **Stack AI** | `https://api.stack-ai.com/...` | Free tier | Visual Agent Builder |
| **n8n Cloud** | `https://{instance}.app.n8n.cloud/...` | Free trial | Workflow Automation |
| **Make (Integromat)** | `https://hook.make.com/...` | 1000 ops/mo | Workflow Automation |
| **Zapier** | `https://hooks.zapier.com/...` | 100 tasks/mo | Workflow Automation |
| **Activepieces** | Self-hosted or cloud | 1000 tasks/mo | Workflow Automation |
| **Flowise** | `http://localhost:3000/api/v1/...` | Unlimited (OSS) | Visual LLM Builder |
| **Dify** | `https://api.dify.ai/v1/...` | 200 messages/day | Agent Platform |
| **Vocode** | `pip install vocode` | Free tier | Voice Agents |
| **Bland AI** | `https://api.bland.ai/v1/...` | Free trial | Voice Agents |

### Tier 5: Pay-per-use

| Provider | Endpoint | Category | Pricing |
|:---------|:---------|:---------|:--------|
| **Scale AI** | `https://api.scale.com/v1/...` | Data/Evaluation | Custom |
| **Fixie (now Humanloop)** | `https://api.humanloop.com/v5/...` | Agent Platform | Pay-per-use |
| **Modal** | Custom deploy | Compute | $30/mo free |
| **Baseten** | Custom deploy | Model Serving | Free tier |
| **RunPod** | `https://api.runpod.ai/v2/...` | GPU Compute | $0.50 credits |
| **Replicate** | `https://api.replicate.com/v1/predictions` | Model Hosting | Pay-per-use |
| **AssemblyAI** | `https://api.assemblyai.com/v2/...` | Audio/Transcription | Free trial |

### Routers / Aggregators

| Provider | Endpoint | Description |
|:---------|:---------|:------------|
| **OpenRouter** | `https://openrouter.ai/api/v1/...` | Routes to 200+ LLMs with tool calling |
| **LiteLLM** | `pip install litellm` | Unified API for 100+ LLMs (OSS) |
| **Portkey** | `https://api.portkey.ai/v1/...` | AI gateway with fallbacks, caching, logging |
| **Martian** | `https://warp.martian.com/v1/...` | Smart model router |
| **Unify** | `https://api.unify.ai/v0/...` | LLM router with benchmarks |

### Local / Self-hosted

| Provider | Endpoint | Description |
|:---------|:---------|:------------|
| **Ollama** | `http://localhost:11434/api/...` | Local LLM with tool calling support |
| **LM Studio** | `http://localhost:1234/v1/...` | Local LLM with OpenAI-compatible API |
| **vLLM** | `http://localhost:8000/v1/...` | High-performance local serving |
| **LocalAI** | `http://localhost:8080/v1/...` | Local OpenAI-compatible API |
| **n8n (self-hosted)** | `http://localhost:5678/...` | Self-hosted workflow automation |
| **Flowise** | `http://localhost:3000/api/v1/...` | Self-hosted LLM flow builder |
| **Dify (self-hosted)** | `http://localhost/v1/...` | Self-hosted agent platform |
| **Langfuse** | `http://localhost:3000/api/public/...` | Self-hosted LLM observability |
| **Chroma** | `http://localhost:8000/api/v1/...` | Self-hosted vector DB |
| **Qdrant** | `http://localhost:6333/...` | Self-hosted vector DB |
| **Milvus** | `http://localhost:19530/...` | Self-hosted vector DB |
| **SearXNG** | `http://localhost:8080/search` | Self-hosted meta search engine |

---

## 3. Provider Data Model

Adapted from the image repo's `Provider` dataclass for agent tools:

```python
from dataclasses import dataclass, field
from enum import Enum

class Tier(str, Enum):
    free = "free"
    generous_free = "generous_free"
    free_credits = "free_credits"
    freemium = "freemium"
    payg = "payg"
    router = "router"
    local = "local"

    @property
    def label(self) -> str:
        labels = {
            "free": "Truly Free (open-source, no credit card)",
            "generous_free": "Generous Free Tier (notable limitations)",
            "free_credits": "Free Credits on Signup (one-time, may expire)",
            "freemium": "Freemium (credit card or paid plan required)",
            "payg": "Pay-per-use (no free tier)",
            "router": "Routers / Aggregators",
            "local": "Local / Self-hosted (unlimited, free forever)",
        }
        return labels.get(self.value, self.value)

class Category(str, Enum):
    framework = "framework"
    multi_agent = "multi_agent"
    orchestration = "orchestration"
    tool_platform = "tool_platform"
    agent_sdk = "agent_sdk"
    protocol = "protocol"
    code_sandbox = "code_sandbox"
    browser = "browser"
    search = "search"
    scraping = "scraping"
    memory = "memory"
    vector_db = "vector_db"
    observability = "observability"
    gateway = "gateway"
    workflow = "workflow"
    voice = "voice"
    llm_provider = "llm_provider"
    compute = "compute"
    agent_platform = "agent_platform"

    @property
    def label(self) -> str:
        labels = {
            "framework": "Agent Framework",
            "multi_agent": "Multi-Agent System",
            "orchestration": "Agent Orchestration",
            "tool_platform": "Tool / Function Platform",
            "agent_sdk": "Agent SDK",
            "protocol": "Protocol / Specification",
            "code_sandbox": "Code Execution Sandbox",
            "browser": "Browser Automation",
            "search": "Search API",
            "scraping": "Web Scraping / Crawling",
            "memory": "Agent Memory",
            "vector_db": "Vector Database",
            "observability": "Observability / Tracing",
            "gateway": "AI Gateway / Proxy",
            "workflow": "Workflow Automation",
            "voice": "Voice Agents",
            "llm_provider": "LLM Provider (with tool calling)",
            "compute": "Compute / Model Serving",
            "agent_platform": "Agent-as-a-Service Platform",
        }
        return labels.get(self.value, self.value)

@dataclass
class Provider:
    name: str
    tier: Tier
    category: Category                  # NEW: what kind of tool is this?
    endpoint: str                       # API URL or package name

    # Authentication
    env_key: str | None = None
    auth_style: str = "bearer"          # "bearer", "x-api-key", "query", "none", "package"

    # Capabilities
    free_limits: str = ""
    capabilities: list[str] = field(default_factory=list)
    # Possible capabilities:
    #   "tool_calling", "function_calling", "multi_agent", "rag",
    #   "code_execution", "browser_control", "web_search", "web_scrape",
    #   "memory", "vector_search", "tracing", "logging", "caching",
    #   "streaming", "async", "human_in_loop", "workflow", "voice",
    #   "mcp_support", "openai_compatible", "structured_output"

    # Integration
    languages: list[str] = field(default_factory=lambda: ["python"])  # NEW: supported languages
    install_command: str = ""           # NEW: "pip install langchain", "npm install ..."
    supports_mcp: bool = False          # NEW: supports Model Context Protocol?
    supports_tool_calling: bool = False # NEW: native function/tool calling?
    supports_streaming: bool = False    # NEW: streaming responses?
    supports_async: bool = False        # NEW: async support?
    openai_compatible: bool = False     # Supports OpenAI API format

    # Metadata
    docs_url: str = ""                  # NEW: link to documentation
    github_url: str = ""               # NEW: link to GitHub repo (if OSS)
    signup_url: str = ""
    test_endpoint: str = ""            # NEW: specific endpoint to test health
    notes: str = ""

    # Scan results (populated at runtime)
    status: str = "unknown"
    latency_ms: float | None = None
    error_detail: str = ""
```

**Key differences from Image/LLM repos:**
- Added `Category` enum (19 categories of agent tools)
- Added `languages` field (Python, JS/TS, C#, Java, Go, Rust)
- Added `install_command` for package-based tools
- Added `supports_mcp`, `supports_tool_calling`, `supports_streaming`, `supports_async`
- Added `docs_url`, `github_url` for OSS projects
- `auth_style` includes `"package"` for tools installed as libraries (no API auth)
- Capabilities list is agent-focused rather than image-focused

---

## 4. Scanner Adaptations

### Test Strategies

Agent tools require different testing than LLM or image endpoints:

**1. API Endpoint (REST)**
```python
# For cloud APIs with standard REST endpoints
GET /health or GET /api/status
# Check: HTTP 200
# Fallback: POST a minimal request and check for valid response structure
```

**2. OpenAI-Compatible (with tool calling)**
```python
POST /v1/chat/completions
{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "What is 2+2?"}],
    "tools": [{
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate math",
            "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}}
        }
    }],
    "max_tokens": 50
}
# Check: response contains tool_calls or valid completion
```

**3. Package Import Check**
```python
# For pip/npm installable frameworks
try:
    import langchain
    # Check: module exists, version accessible
except ImportError:
    # Status: not_installed
```

**4. Local Service Check**
```python
GET http://localhost:{port}/health
# or
GET http://localhost:{port}/api/version
# Check: HTTP 200
```

**5. Vector DB Health Check**
```python
# Chroma
GET http://localhost:8000/api/v1/heartbeat
# Qdrant
GET http://localhost:6333/healthz
# Weaviate
GET http://localhost:8080/v1/.well-known/ready
```

**6. Search API Test**
```python
POST https://api.tavily.com/search
{"query": "test", "max_results": 1}
# Check: results array exists
```

### Status Values
```python
"working"         # Endpoint/tool is functioning
"reachable"       # Endpoint responds but not fully tested
"installed"       # Package is installed locally (for OSS frameworks)
"not_installed"   # Package not found (for OSS frameworks)
"auth_missing"    # API key not configured
"auth_failed"     # 401/403
"needs_credits"   # 402 / credits exhausted
"rate_limited"    # 429
"timeout"         # No response in time
"error"           # Other error
"offline"         # Local server not running
"skipped"         # Not tested
"deprecated"      # Tool/API is deprecated
```

### ScanResult
```python
@dataclass
class ScanResult:
    provider_name: str
    status: str
    latency_ms: float | None = None
    error_detail: str = ""
    version: str = ""              # NEW: detected version of the tool/API
    capabilities_detected: list[str] = field(default_factory=list)  # NEW: capabilities confirmed by test
```

---

## 5. CLI Commands

```
python main.py scan                          # Test all agent tool endpoints
python main.py scan --tier free              # Test only free tier
python main.py scan --category framework     # Test only frameworks
python main.py scan --provider LangChain     # Test specific provider
python main.py scan --report                 # Scan + regenerate README
python main.py report                        # Generate README from last scan
python main.py list                          # List all providers
python main.py list --category search        # List by category
python main.py discover                      # AI-powered discovery of new tools
python main.py models                        # Fetch available models (for LLM providers)
python main.py export --format csv           # Export to JSON/CSV/YAML/HTML
python main.py compare                       # Compare tools in a category
python main.py costs                         # Compare pricing
python main.py setup "langchain"             # Quick setup guide for a tool    # NEW
python main.py check-deps                    # Check which tools are installed  # NEW
python main.py proxy --port 8000             # Local unified agent proxy
```

**New commands:**
- `setup` -- prints quick-start instructions for a specific tool
- `check-deps` -- checks which OSS frameworks/tools are installed locally

---

## 6. Directory Structure

```
ai-agent-tools-frameworks-api-directory/
├── main.py                  # CLI entry point
├── config.py                # Config loader (YAML + env overrides)
├── config.yaml              # All settings
├── providers.py             # Provider registry (80+ tools, 7 tiers, 19 categories)
├── scanner.py               # Async tool/endpoint health checker
├── report_generator.py      # README generator
├── requirements.txt         # Python dependencies
├── __version__.py           # Version (0.1.0)
├── .env.example             # API key template
├── LICENSE                  # MIT
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── .gitignore
├── .gitattributes
│
├── .github/
│   ├── pull_request_template.md
│   └── ISSUE_TEMPLATE/
│       ├── new-tool.md
│       ├── tool-update.md
│       └── bug-report.md
│
├── examples/                # Ready-to-run scripts
│   ├── basic_agent.py       # Simple agent with tool calling
│   ├── multi_agent.py       # Multi-agent collaboration
│   ├── rag_agent.py         # RAG pipeline with vector search
│   ├── web_search_agent.py  # Agent with web search tools
│   ├── browser_agent.py     # Agent controlling a browser
│   ├── code_agent.py        # Agent that writes and executes code
│   ├── mcp_agent.py         # Agent using MCP servers
│   ├── workflow_agent.py    # Agent with multi-step workflows
│   ├── voice_agent.py       # Voice-enabled agent
│   ├── memory_agent.py      # Agent with persistent memory
│   ├── multi_provider.py    # Compare frameworks side-by-side
│   ├── oneliners.py         # One-liner per tool
│   └── curl_examples.sh     # cURL commands (no Python)
│
├── tools/
│   ├── cascade.py           # Failover client for LLM tool calling
│   ├── compare.py           # Side-by-side framework comparison
│   ├── proxy.py             # Local unified agent proxy
│   ├── rate_limiter.py      # Per-provider rate limiting
│   ├── cost_calculator.py   # Per-call cost comparison
│   ├── dep_checker.py       # NEW: Check installed frameworks/versions
│   ├── setup_guide.py       # NEW: Quick-start guide generator per tool
│   └── mcp_registry.py      # NEW: Discover and list MCP servers
│
├── adapters/                # API format normalizers
│   ├── base.py              # BaseAdapter, ToolRequest, ToolResponse
│   ├── openai_adapter.py    # OpenAI function calling format
│   ├── anthropic_adapter.py # Anthropic tool use format
│   ├── langchain_adapter.py # LangChain tool format
│   ├── crewai_adapter.py    # CrewAI agent/task format
│   └── mcp_adapter.py       # Model Context Protocol format
│
├── agents/                  # Meta-agents
│   ├── base.py              # BaseAgent + tool presets
│   ├── discovery_agent.py   # Agent that discovers new tools
│   ├── eval_agent.py        # Agent that evaluates other agent tools
│   ├── setup_agent.py       # Agent that helps set up frameworks
│   └── comparison_agent.py  # Agent that compares frameworks
│
├── search/                  # Web search integrations
│   ├── base.py
│   ├── brave_search.py
│   ├── serper_search.py
│   ├── tavily_search.py
│   ├── exa_search.py
│   └── web_scraper.py
│
├── discovery/               # AI-powered tool discovery
│   ├── engine.py
│   └── strategies/
│       ├── base.py
│       ├── web_search.py
│       ├── github_search.py
│       ├── llm_search.py
│       ├── pypi_search.py   # NEW: search PyPI for agent packages
│       ├── npm_search.py    # NEW: search npm for agent packages
│       └── awesome_lists.py # NEW: scrape awesome-* lists on GitHub
│
├── plugins/
│   ├── base.py
│   ├── builtin/
│   │   ├── benchmark.py     # Agent task completion benchmarks
│   │   ├── model_list.py    # Fetch available models
│   │   ├── export.py        # JSON/CSV/YAML/HTML
│   │   ├── pricing.py       # Per-call cost tracking
│   │   ├── notify.py        # Webhooks / Slack
│   │   ├── compatibility.py # NEW: check cross-framework compatibility
│   │   └── security.py      # NEW: check for known vulnerabilities
│   └── custom/
│
├── recipes/
│   └── README.md            # Step-by-step guides
│
└── data/
    └── .gitkeep
```

---

## 7. Key Differences from LLM & Image Repos

| Aspect | LLM Repo | Image Repo | Agent Tools Repo |
|:-------|:---------|:-----------|:-----------------|
| **Scope** | Text generation APIs | Image generation APIs | Frameworks, tools, platforms, protocols |
| **Provider type** | Cloud APIs | Cloud APIs | Mix of OSS packages + cloud APIs + protocols |
| **Test method** | Send prompt, check text response | Send prompt, check image | Health check, import check, API test |
| **Categories** | 1 (LLM) | 1 (Image Gen) | 19 (framework, search, memory, etc.) |
| **Install method** | API key only | API key only | pip install + API key (or just pip install) |
| **Cost unit** | Per token | Per image | Per call, per trace, per seat, or free (OSS) |
| **Local options** | Ollama, LM Studio | A1111, ComfyUI | Ollama, Flowise, n8n, vector DBs, etc. |
| **Key metric** | Response quality | Image quality | Task completion, latency, reliability |
| **Streaming** | Token-by-token | No | Yes (most frameworks) |
| **Unique features** | Function calling | ControlNet, LoRA | MCP, multi-agent, RAG, tool orchestration |

---

## 8. Cost Calculator Adaptations

Agent tool pricing varies widely -- some are free OSS, others charge per API call, per trace, or per seat:

```python
@dataclass
class AgentToolPricing:
    provider: str
    category: str
    pricing_model: str          # "free_oss", "per_call", "per_trace", "per_seat", "per_compute", "credits"
    free_tier: str              # "Unlimited (OSS)", "1000 calls/mo", "$5 credits"
    cost_per_unit: float        # Cost per call/trace/etc
    unit: str                   # "call", "trace", "message", "search", "hour", "seat/mo"
    notes: str = ""

PRICING = [
    # Free OSS
    AgentToolPricing("LangChain", "framework", "free_oss", "Unlimited", 0.00, "N/A"),
    AgentToolPricing("CrewAI", "multi_agent", "free_oss", "Unlimited", 0.00, "N/A"),
    AgentToolPricing("AutoGen", "multi_agent", "free_oss", "Unlimited", 0.00, "N/A"),
    AgentToolPricing("LlamaIndex", "framework", "free_oss", "Unlimited", 0.00, "N/A"),
    AgentToolPricing("Chroma", "vector_db", "free_oss", "Unlimited", 0.00, "N/A"),
    AgentToolPricing("MCP", "protocol", "free_oss", "Unlimited", 0.00, "N/A"),

    # Per-call services
    AgentToolPricing("Tavily", "search", "per_call", "1000/mo", 0.001, "search"),
    AgentToolPricing("Serper", "search", "per_call", "2500/mo", 0.001, "search"),
    AgentToolPricing("Exa", "search", "per_call", "1000/mo", 0.003, "search"),
    AgentToolPricing("Firecrawl", "scraping", "credits", "500 credits", 0.002, "page"),

    # Per-trace observability
    AgentToolPricing("LangSmith", "observability", "per_trace", "5K/mo", 0.0005, "trace"),
    AgentToolPricing("AgentOps", "observability", "per_trace", "1000/mo", 0.001, "event"),
    AgentToolPricing("Helicone", "observability", "per_trace", "100K/mo", 0.00, "log", "Free tier very generous"),

    # Compute
    AgentToolPricing("E2B", "code_sandbox", "per_compute", "100 hrs/mo", 0.0001, "second"),
    AgentToolPricing("Modal", "compute", "per_compute", "$30/mo free", 0.0003, "second"),
    AgentToolPricing("Browserbase", "browser", "per_call", "100 sessions/mo", 0.01, "session"),
]
```

---

## 9. Example Scripts

### basic_agent.py
```python
"""Build a simple agent with tool calling using the OpenAI SDK."""
from openai import OpenAI
import json

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    }
]

def get_weather(city: str) -> str:
    return f"72°F and sunny in {city}"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    result = get_weather(**args)
    print(f"Tool called: {tool_call.function.name}({args})")
    print(f"Result: {result}")
```

### multi_agent.py (CrewAI)
```python
"""Multi-agent collaboration with CrewAI."""
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Researcher",
    goal="Find the latest information",
    backstory="Expert at gathering and analyzing information",
)
writer = Agent(
    role="Writer",
    goal="Write clear, concise content",
    backstory="Skilled technical writer",
)

task = Task(
    description="Research AI agent frameworks and write a comparison",
    expected_output="A comparison table of top 5 frameworks",
    agent=researcher,
)

crew = Crew(agents=[researcher, writer], tasks=[task])
result = crew.kickoff()
print(result)
```

### mcp_agent.py
```python
"""Agent using Model Context Protocol (MCP) servers."""
from anthropic import Anthropic
# Connect to MCP servers for filesystem, web search, databases
# MCP provides a standardized way to give agents access to tools
```

### curl_examples.sh
```bash
# Tavily Search (agent-optimized search)
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{"api_key": "'$TAVILY_API_KEY'", "query": "best AI agent frameworks 2026", "max_results": 5}'

# OpenAI with tool calling
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "What is 2+2?"}],
    "tools": [{"type": "function", "function": {"name": "calc", "parameters": {"type": "object", "properties": {"expr": {"type": "string"}}}}}]
  }'

# E2B Code Sandbox
curl -X POST https://api.e2b.dev/sandboxes \
  -H "Authorization: Bearer $E2B_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"template": "base"}'

# Jina Reader (convert URL to LLM-friendly text)
curl https://r.jina.ai/https://example.com \
  -H "Authorization: Bearer $JINA_API_KEY"
```

---

## 10. New Tools (Agent-Specific)

### dep_checker.py
```python
"""Check which agent frameworks and tools are installed locally."""

PACKAGES = {
    "langchain": "LangChain",
    "langgraph": "LangGraph",
    "crewai": "CrewAI",
    "autogen": "AutoGen",
    "smolagents": "Smolagents",
    "haystack": "Haystack",
    "semantic_kernel": "Semantic Kernel",
    "llama_index": "LlamaIndex",
    "dspy": "DSPy",
    "pydantic_ai": "Pydantic AI",
    "instructor": "Instructor",
    "chromadb": "Chroma",
    "qdrant_client": "Qdrant",
    "openai": "OpenAI SDK",
    "anthropic": "Anthropic SDK",
    "litellm": "LiteLLM",
    "mem0ai": "Mem0",
    "crawl4ai": "Crawl4AI",
    "browser_use": "Browser Use",
    "playwright": "Playwright",
    "firecrawl": "Firecrawl",
}

def check_all() -> dict[str, str | None]:
    """Check installed versions of all known agent packages."""
    results = {}
    for package, display_name in PACKAGES.items():
        try:
            mod = __import__(package)
            version = getattr(mod, "__version__", "installed")
            results[display_name] = version
        except ImportError:
            results[display_name] = None
    return results
```

### setup_guide.py
```python
"""Generate quick-start guides for specific tools."""

GUIDES = {
    "langchain": {
        "install": "pip install langchain langchain-openai",
        "env_vars": ["OPENAI_API_KEY"],
        "quickstart": '''
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
llm = ChatOpenAI(model="gpt-4o-mini")
# ... define tools, create agent, run
''',
        "docs": "https://python.langchain.com/docs/",
    },
    "crewai": {
        "install": "pip install crewai crewai-tools",
        "env_vars": ["OPENAI_API_KEY"],
        "quickstart": '''
from crewai import Agent, Task, Crew
agent = Agent(role="Researcher", goal="...", backstory="...")
# ... define tasks, create crew, kickoff
''',
        "docs": "https://docs.crewai.com/",
    },
    # ... more tools
}
```

### mcp_registry.py
```python
"""Discover and list available MCP (Model Context Protocol) servers."""

MCP_SERVERS = {
    "filesystem": {
        "package": "@anthropic-ai/mcp-filesystem",
        "description": "Read/write files on the local filesystem",
        "install": "npx @anthropic-ai/mcp-filesystem",
    },
    "github": {
        "package": "@anthropic-ai/mcp-github",
        "description": "Interact with GitHub repos, issues, PRs",
        "install": "npx @anthropic-ai/mcp-github",
    },
    "postgres": {
        "package": "@anthropic-ai/mcp-postgres",
        "description": "Query PostgreSQL databases",
        "install": "npx @anthropic-ai/mcp-postgres",
    },
    "brave-search": {
        "package": "@anthropic-ai/mcp-brave-search",
        "description": "Web search via Brave Search API",
        "install": "npx @anthropic-ai/mcp-brave-search",
    },
    # ... more MCP servers
}

def list_mcp_servers() -> list[dict]: ...
def check_mcp_server(name: str) -> str: ...  # Check if installed
```

---

## 11. Recipes (Use Cases)

| Recipe | Description | Difficulty |
|:-------|:------------|:-----------|
| **Quick Agent** | Build a tool-calling agent in 10 lines | Beginner |
| **Web Research Agent** | Agent that searches the web and summarizes | Beginner |
| **RAG Pipeline** | Ingest docs, embed, retrieve, answer | Intermediate |
| **Multi-Agent Team** | CrewAI/AutoGen multi-agent collaboration | Intermediate |
| **Code Interpreter** | Agent that writes and executes code (E2B) | Intermediate |
| **Browser Agent** | Agent that navigates websites | Intermediate |
| **MCP Integration** | Connect agents to MCP tool servers | Intermediate |
| **Memory + RAG** | Agent with persistent memory (Mem0 + Chroma) | Intermediate |
| **Voice Agent** | Build a voice-enabled AI agent | Advanced |
| **Agent Evaluation** | Benchmark agents on task completion | Advanced |
| **Multi-Provider Cascade** | Failover between LLM providers for tool calling | Advanced |
| **Custom MCP Server** | Build your own MCP server for custom tools | Advanced |
| **Agent Monitoring** | Trace agent runs with LangSmith/Helicone | Intermediate |
| **Self-Improving Agent** | Agent that evaluates and improves its own tools | Advanced |

---

## 12. Config Adaptations

```yaml
scan:
  concurrency: 10               # Higher than image (most are just health checks)
  timeout_seconds: 30            # Faster than image gen
  test_prompt: "What is 2 plus 2?"
  retry_count: 1
  skip_local: false
  check_packages: true           # NEW: check installed pip packages

search:
  max_results_per_query: 10
  search_queries:
    - "free AI agent framework 2026"
    - "best agent tools open source"
    - "AI agent API free tier"
    - "LLM tool calling free API"
    - "MCP server directory"
    - "AI agent orchestration platform"
    - "free RAG API"
    - "agent memory vector database free"

discovery:
  enabled: true
  strategies:
    - web_search
    - github_search
    - llm_search
    - pypi_search
    - awesome_lists
  llm_provider: groq
  llm_model: llama-3.3-70b-versatile

plugins:
  enabled_plugins:
    - benchmark
    - model_list
    - export
    - compatibility

report:
  output_file: README.md
  group_by: category             # NEW: group providers by category in README

proxy:
  port: 8000
  default_provider: openai
```

---

## 13. Dependencies

```
# requirements.txt
httpx>=0.27.0               # Async HTTP client
openai>=1.30.0              # OpenAI SDK (for testing tool calling)
rich>=13.7.0                # Terminal formatting
pydantic>=2.5.0             # Data validation
python-dotenv>=1.0.0        # Environment management
tenacity>=8.2.0             # Retry logic
pyyaml>=6.0.0               # Config file parsing
importlib-metadata>=6.0.0   # NEW: package version detection
```

---

## 14. README Structure (sections in order)

1. Title + badges (version, tools count, free count, categories, stars)
2. Tagline + key stats
3. Table of Contents (collapsible)
4. Why This Exists
5. Highlights table (key stats at a glance)
6. Quick Start (basic tool-calling agent)
7. cURL Quick Start (no Python)
8. Tool Overview (summary table)
9. Category sections (19 categories, grouped):
   - Agent Frameworks & SDKs
   - Multi-Agent Systems
   - Search & Web Tools
   - Memory & Vector Databases
   - Code Execution & Browsers
   - Observability & Gateways
   - Workflow Automation
   - Voice Agents
   - Agent Platforms
10. Tier sections (7 tiers)
11. MCP Server Directory
12. Framework Comparison Table
13. Toolkit (setup, CLI reference, discovery, plugins, proxy)
14. Examples (13 scripts)
15. Adapters (OpenAI, Anthropic, LangChain, CrewAI, MCP)
16. Utility Tools (cascade, dep checker, setup guide, MCP registry)
17. Recipes & Use Cases
18. Architecture diagram
19. Status Legend
20. Project Structure
21. FAQ & Troubleshooting
22. Keeping Up to Date
23. Contributing
24. Sister Projects (LLM repo + Image repo)
25. Credits & Acknowledgments
26. License

---

## 15. Implementation Order

**Phase 1: Foundation (MVP)**
1. `providers.py` -- Provider + Tier + Category dataclasses, initial 80+ tools
2. `scanner.py` -- Async health checker (API, package import, local service)
3. `main.py` -- CLI with scan, list, report, check-deps commands
4. `config.py` + `config.yaml` -- Configuration system
5. `report_generator.py` -- README generation (grouped by category)
6. `.env.example` -- API key template
7. `requirements.txt` -- Dependencies
8. Community files (LICENSE, CONTRIBUTING.md, CHANGELOG.md, etc.)

**Phase 2: Examples & Tools**
9. `examples/basic_agent.py` -- Simple tool-calling agent
10. `examples/multi_agent.py` -- CrewAI multi-agent
11. `examples/rag_agent.py` -- RAG pipeline
12. `examples/web_search_agent.py` -- Agent with search
13. `examples/curl_examples.sh` -- cURL commands
14. `examples/oneliners.py` -- One-liner per tool
15. `tools/dep_checker.py` -- Check installed packages
16. `tools/setup_guide.py` -- Quick-start guide generator
17. `tools/cascade.py` -- Failover client
18. `tools/cost_calculator.py` -- Per-call pricing

**Phase 3: Advanced**
19. `tools/mcp_registry.py` -- MCP server directory
20. `adapters/` -- OpenAI, Anthropic, LangChain, CrewAI, MCP adapters
21. `agents/` -- Discovery, eval, setup, comparison agents
22. `discovery/` -- AI-powered discovery (web, GitHub, PyPI, npm, awesome-lists)
23. `plugins/` -- Benchmark, export, compatibility, security
24. `tools/compare.py` + `tools/proxy.py`
25. `examples/` -- Remaining examples (browser, code, mcp, voice, memory)
26. `recipes/README.md` -- Use case guides

---

## 16. Cross-Linking

All three repos should reference each other:

**In the LLM repo README:**
> Looking for **AI agent tools & frameworks**? See: [ai-agent-tools-frameworks-api-directory](https://github.com/TaylorAmarelTech/ai-agent-tools-frameworks-api-directory)
> Looking for **AI image generation** APIs? See: [ai-image-generation-api-endpoints-directory](https://github.com/TaylorAmarelTech/ai-image-generation-api-endpoints-directory)

**In the image repo README:**
> Looking for **AI agent tools & frameworks**? See: [ai-agent-tools-frameworks-api-directory](https://github.com/TaylorAmarelTech/ai-agent-tools-frameworks-api-directory)
> Looking for **LLM / text generation** APIs? See: [text-generation-ai-llm-tools-endpoints-api-list-repository](https://github.com/TaylorAmarelTech/text-generation-ai-llm-tools-endpoints-api-list-repository)

**In the agent tools repo README:**
> Looking for **LLM / text generation** APIs? See: [text-generation-ai-llm-tools-endpoints-api-list-repository](https://github.com/TaylorAmarelTech/text-generation-ai-llm-tools-endpoints-api-list-repository)
> Looking for **AI image generation** APIs? See: [ai-image-generation-api-endpoints-directory](https://github.com/TaylorAmarelTech/ai-image-generation-api-endpoints-directory)

---

## 17. Code Reuse from Image / LLM Repos

These files can be copied and adapted with minimal changes:

| File | Changes Needed |
|:-----|:---------------|
| `config.py` | Update search queries, add `check_packages` setting |
| `config.yaml` | Update queries, increase concurrency, add category grouping |
| `main.py` | Add `setup`, `check-deps` commands; add `--category` filter |
| `search/*` | Copy as-is (generic web search) |
| `discovery/*` | Add PyPI, npm, awesome-list strategies |
| `plugins/base.py` | Copy as-is |
| `plugins/builtin/export.py` | Add Category field handling |
| `plugins/builtin/notify.py` | Copy as-is |
| `tools/rate_limiter.py` | Copy as-is |
| `.gitignore` | Copy as-is |
| `.gitattributes` | Copy as-is |
| `.github/*` | Update templates (tool → provider) |
| `CONTRIBUTING.md` | Update repo name and instructions |
| `SECURITY.md` | Update repo name |
| `CODE_OF_CONDUCT.md` | Copy as-is |

---

## 18. Unique Value Propositions

What makes this directory different from "awesome-agent" lists:

1. **Auto-scanned** -- CI checks tool availability, not just a static list
2. **Categorized** -- 19 categories vs flat lists
3. **Pricing comparison** -- clear free tier limits and per-call costs
4. **Install-ready** -- pip commands, env vars, and quick-start code for every tool
5. **MCP directory** -- first comprehensive MCP server catalog
6. **Framework comparison** -- side-by-side feature matrix
7. **Cross-linked** -- part of a family of directories (LLM, Image, Agents)
8. **Community-maintained** -- issue templates for adding/updating tools

---

*Document created: 2026-03-07*
*For: TaylorAmarelTech*
*Reference repos: text-generation-ai-llm-tools-endpoints-api-list-repository v0.4.0, ai-image-generation-api-endpoints-directory v0.1.0*

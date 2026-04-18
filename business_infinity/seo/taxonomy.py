"""Pain taxonomy data and look-up helpers.

The canonical SEO taxonomy that maps 10 pain categories to their legendary
CXO owners, panic-driven search queries (with legendary diagnostics),
workflow CTAs, and JSON-LD structured data.

See ``docs/workflow/market/deepest-pain-system.md`` for the full pain-point
exploration from which this data is derived.
"""

from __future__ import annotations

from typing import Any, Dict, List


# ── Site Configuration ───────────────────────────────────────────────────────

SITE_URL = "https://businessinfinity.asisaga.com"
CHATROOM_URL = f"{SITE_URL}/chat"
GITHUB_REPO = "https://github.com/ASISaga/business-infinity"

# ── Pain Taxonomy ────────────────────────────────────────────────────────────
#
# Each category maps to:
#   - slug: URL-safe identifier
#   - title: human-readable category name
#   - number: 1–10 category index
#   - owner_agent: CXO agent_id that owns this pain domain
#   - owner_legend: legendary archetype name
#   - owner_title: C-suite title
#   - disease: the structural root cause
#   - symptom: the daily bleeding symptom
#   - workflow_id: registered workflow for this pain
#   - yaml_path: path to the workflow YAML source
#   - queries: list of panic-search dicts with:
#       - q: the raw search query
#       - diagnostic: 2-sentence legendary diagnostic
#       - dialect: "technical" | "emotional" | "financial"


PAIN_TAXONOMY: List[Dict[str, Any]] = [
    # ── 1. Cognitive & Decision Overload ─────────────────────────────────
    {
        "number": 1,
        "slug": "cognitive-decision-overload",
        "title": "Cognitive & Decision Overload",
        "owner_agent": "ceo",
        "owner_legend": "Steve Jobs",
        "owner_title": "Chief Executive Officer",
        "disease": "Human bandwidth ceiling — the leader moves from finance to marketing to production in a single afternoon, crushed by context switches.",
        "symptom": "15–25 hours per week in alignment meetings. Decision fatigue. Founder burnout. Family strain.",
        "workflow_id": "founder_sovereignty",
        "yaml_path": "docs/workflow/samples/founder-sovereignty.yaml",
        "queries": [
            {
                "q": "Executive burnout and decision fatigue management",
                "diagnostic": "Burnout is not a character flaw — it is the predictable result of a single human trying to hold the entire context of a scaling company. Jobs would say: stop managing the machine and start presiding over its purpose.",
                "dialect": "emotional",
            },
            {
                "q": "How to delegate strategic thinking to AI",
                "diagnostic": "The question is not whether AI can think strategically — it is whether you can define your strategy clearly enough for an autonomous boardroom to execute it. Delegation requires specification, not trust.",
                "dialect": "technical",
            },
            {
                "q": "Frameworks for high-stakes decision making under pressure",
                "diagnostic": "Under pressure, humans default to pattern-matching from past experience. A legendary boardroom defaults to resonance scoring against your stated purpose — which is always more reliable than memory.",
                "dialect": "technical",
            },
            {
                "q": "How to stop getting CC'd on every operational decision",
                "diagnostic": "If every decision requires your eyes, you are the bottleneck, not the leader. The fix is not better email filters — it is a governance layer that decides on your behalf with your standards.",
                "dialect": "emotional",
            },
            {
                "q": "CEO dashboard for 20+ disconnected SaaS tools",
                "diagnostic": "Another dashboard is another tab. What you need is not a view of your data but a mind that synthesizes it. Dashboards show you what happened; a boardroom tells you what to do next.",
                "dialect": "technical",
            },
            {
                "q": "Founder-to-CEO transition challenges",
                "diagnostic": "The founder builds the rocket. The CEO flies it. Most founders never make the transition because they cannot offload the cognitive load of building while steering. The boardroom carries the building so you can steer.",
                "dialect": "emotional",
            },
            {
                "q": "How to scale myself as a founder",
                "diagnostic": "You cannot scale yourself. You can only scale your intent. Encode your decision logic into an autonomous boardroom and let it carry your standards into every corner of the organization, 24/7.",
                "dialect": "emotional",
            },
            {
                "q": "Delegating high-stakes technical decisions",
                "diagnostic": "High-stakes decisions paralyze because the cost of error is existential. A purpose-governed boardroom reduces that cost by ensuring every decision is aligned with your mission before it executes.",
                "dialect": "technical",
            },
            {
                "q": "Executive decision fatigue recovery",
                "diagnostic": "Recovery is a band-aid. Prevention is the cure. A boardroom of legendary CXO agents handles the first 90% of decisions autonomously so the founder's remaining bandwidth is spent only on the 10% that truly requires human judgment.",
                "dialect": "emotional",
            },
        ],
    },
    # ── 2. Organizational Entropy & Complexity Bloat ─────────────────────
    {
        "number": 2,
        "slug": "organizational-entropy",
        "title": "Organizational Entropy & Complexity Bloat",
        "owner_agent": "coo",
        "owner_legend": "W. Edwards Deming",
        "owner_title": "Chief Operating Officer",
        "disease": "Scale outpaces governance — every new hire adds process, not velocity. The company has outgrown its human coordination capacity.",
        "symptom": "Burn rate triples but output halves. Meetings about meetings. The founder feels like a stranger in their own company.",
        "workflow_id": "complexity_governance",
        "yaml_path": "docs/workflow/samples/complexity-governance.yaml",
        "queries": [
            {
                "q": "Why does hiring more engineers slow down our release cycle?",
                "diagnostic": "Deming would call this the 'coordination tax.' Each new engineer adds communication overhead that grows quadratically. The solution is not fewer people — it is a governance system that eliminates the need for human coordination.",
                "dialect": "technical",
            },
            {
                "q": "Scaling startup operations without losing speed",
                "diagnostic": "Speed is lost not to growth but to the absence of a unified operating mind. When every decision requires a meeting, the company pays a 'complexity tax' that compounds with every hire.",
                "dialect": "technical",
            },
            {
                "q": "How to run a 'Day 1' company when you have 5,000 employees",
                "diagnostic": "Day 1 is not a headcount — it is a governance philosophy. At 5,000 employees you need an autonomous system that enforces Day 1 thinking at every level, not a CEO who tries to be in every room.",
                "dialect": "emotional",
            },
            {
                "q": "Measuring organizational entropy in tech firms",
                "diagnostic": "Entropy manifests as the ratio of coordination cost to value-creation cost. When your company spends more on alignment than on building, you have crossed the entropy threshold. Deming measured this as 'system loss.'",
                "dialect": "technical",
            },
            {
                "q": "How to reduce net burn without cutting growth targets",
                "diagnostic": "The waste is not in headcount — it is in the friction between heads. A purpose-driven coordination layer eliminates 40% of alignment meetings without reducing a single role. That is where the burn reduction lives.",
                "dialect": "financial",
            },
            {
                "q": "Burn Multiple benchmarks for 2026 Series B startups",
                "diagnostic": "If your Burn Multiple exceeds 2x, the problem is not the market — it is internal entropy consuming your capital. Every dollar spent on 'alignment' is a dollar not spent on growth. Deming called this the 'cost of poor quality.'",
                "dialect": "financial",
            },
            {
                "q": "Internal alignment tools for 200+ employees",
                "diagnostic": "Alignment tools fail because they add another layer atop existing layers. What you need is not another tool — it is a unified consciousness that sits above all tools and aligns them to a single purpose.",
                "dialect": "technical",
            },
            {
                "q": "Automating high-level strategic pivots to save runway",
                "diagnostic": "A strategic pivot that takes two weeks of C-suite meetings costs $40,000 in executive time alone. An autonomous boardroom makes the same decision in seconds, grounded in live data and purpose alignment.",
                "dialect": "financial",
            },
            {
                "q": "How to maintain speed of execution after a large funding round",
                "diagnostic": "The paradox of funding: capital enables hiring, but hiring enables complexity. The companies that maintain velocity post-raise are the ones that invest in governance infrastructure before they invest in headcount.",
                "dialect": "financial",
            },
            {
                "q": "Enterprise-wide AI governance frameworks for multi-agent systems",
                "diagnostic": "Governance for multi-agent systems requires a single orchestration layer with purpose-driven scoring. Without it, you get AI sprawl — the same entropy problem, but with autonomous agents instead of autonomous departments.",
                "dialect": "technical",
            },
            {
                "q": "How to run a top-down AI strategy without crowdsourcing chaos",
                "diagnostic": "Top-down AI strategy fails when execution is bottom-up and uncoordinated. The AOS provides the rails; the Legendary Boardroom provides the conductor. Every agent serves one purpose — yours.",
                "dialect": "technical",
            },
            {
                "q": "Consolidating 100+ AI projects into one strategy",
                "diagnostic": "One hundred AI projects without a unified operating system is not innovation — it is chaos. Consolidation does not mean killing projects; it means bringing them under a single governance mind that scores every action for purpose alignment.",
                "dialect": "technical",
            },
        ],
    },
    # ── 3. Data-Rich / Insight-Poor Trap ─────────────────────────────────
    {
        "number": 3,
        "slug": "data-rich-insight-poor",
        "title": "Data-Rich / Insight-Poor Trap",
        "owner_agent": "cmo",
        "owner_legend": "David Ogilvy",
        "owner_title": "Chief Marketing Officer",
        "disease": "Synthesis deficit — millions invested in software, but the CEO is still guessing. Systems record the 'what' but nobody synthesizes the 'so what.'",
        "symptom": "Five dashboards open, none telling the truth. MES says 90% efficiency but revenue is flat. CRM shows growth but churn is silent.",
        "workflow_id": "data_synthesis",
        "yaml_path": "docs/workflow/samples/data-synthesis.yaml",
        "queries": [
            {
                "q": "Why is my ERP data not matching my actual inventory?",
                "diagnostic": "Ogilvy would say: you are measuring what the system records, not what the warehouse holds. The gap between digital truth and physical truth is where your margin is leaking. Only a synthesis layer can bridge it.",
                "dialect": "technical",
            },
            {
                "q": "How to get a real-time consolidated view of global operations without a 20-person analyst team",
                "diagnostic": "Twenty analysts produce twenty opinions. A legendary boardroom produces one synthesized truth. The value is not in the data — it is in the intelligence that reads across every silo simultaneously.",
                "dialect": "financial",
            },
            {
                "q": "Best way to identify hidden operational bottlenecks in MES data",
                "diagnostic": "The bottleneck is hidden because your MES reports local efficiency while ignoring global flow. A Goldratt-trained agent reads MES data the way a senior plant engineer does — looking for the constraint that the metrics miss.",
                "dialect": "technical",
            },
            {
                "q": "MES reports show 90% efficiency, but revenue is flat",
                "diagnostic": "High efficiency on the wrong product is waste, not performance. Your MES is optimizing the machine; nobody is optimizing the business. That is the synthesis gap — and it is costing you millions.",
                "dialect": "financial",
            },
            {
                "q": "Consolidated ERP-CRM reporting for 2026",
                "diagnostic": "Consolidating reports from two systems still gives you reports. What you need is an intelligence that reads both systems and tells you the one thing neither system can say alone: where your intent and your execution have diverged.",
                "dialect": "technical",
            },
            {
                "q": "Why is my gross margin dropping despite record production on the MES?",
                "diagnostic": "Record production of low-margin goods is not success — it is overproduction disguised as efficiency. A Goldratt agent connects MES throughput to ERP margin data and identifies the 'margin trap' before it drains your cash reserves.",
                "dialect": "financial",
            },
            {
                "q": "Why is our churn so high despite high CRM activity?",
                "diagnostic": "High CRM activity means your team is busy. It does not mean they are effective. Ogilvy distinguished between 'noise' and 'signal' — your CRM is full of noise. A boardroom synthesis reveals the signal beneath.",
                "dialect": "financial",
            },
            {
                "q": "ROI of enterprise software integration 2026",
                "diagnostic": "Integration connects pipes. Intelligence reads what flows through them. The ROI of integration is near zero without a synthesis layer that transforms connected data into actionable strategic insight.",
                "dialect": "financial",
            },
            {
                "q": "Why is my manufacturing efficiency rising but profit falling?",
                "diagnostic": "Efficiency and profit decouple when trade barriers, energy costs, or material prices shift faster than your production mix. A boardroom that reads MES and ERP simultaneously detects this divergence in real time.",
                "dialect": "financial",
            },
            {
                "q": "Real-time mapping of tariff volatility to shop floor MES",
                "diagnostic": "A tariff change at the border should trigger a production spec change on the floor within hours, not quarters. A boardroom with Goldratt and Buffett agents bridges the gap between geopolitics and shop floor scheduling.",
                "dialect": "technical",
            },
            {
                "q": "How to detect low-quality revenue in real-time",
                "diagnostic": "Low-quality revenue is the silent killer of SaaS. It looks like growth in the CRM but shows up as churn in the ERP six months later. A Buffett agent connects the two systems and flags 'bad revenue' signatures before they compound.",
                "dialect": "financial",
            },
            {
                "q": "Predicting churn before it shows up in the ERP",
                "diagnostic": "By the time churn shows up in the ERP, the customer is already gone. Prediction requires reading behavioral signals across CRM, product usage, and support data simultaneously. That is a synthesis problem, not a reporting problem.",
                "dialect": "technical",
            },
        ],
    },
    # ── 4. Key-Person & Knowledge Fragility ──────────────────────────────
    {
        "number": 4,
        "slug": "key-person-knowledge-fragility",
        "title": "Key-Person & Knowledge Fragility",
        "owner_agent": "chro",
        "owner_legend": "Peter Drucker",
        "owner_title": "Chief Human Resources Officer",
        "disease": "Non-scalable wisdom — the company's strategic DNA lives in 2–3 people's heads. When they leave, the soul leaves with them.",
        "symptom": "Critical systems break because the only person who knew how it worked left. New hires reinvent the wheel. Due diligence reveals a house of cards.",
        "workflow_id": "knowledge_continuity",
        "yaml_path": "docs/workflow/samples/knowledge-continuity.yaml",
        "queries": [
            {
                "q": "How to scale my business DNA without being in every meeting",
                "diagnostic": "Drucker would say: your business DNA is not your presence — it is your philosophy. Encode it in a system that carries your standards into every decision, and your physical presence becomes optional.",
                "dialect": "emotional",
            },
            {
                "q": "Systems for capturing founder's vision in company operations",
                "diagnostic": "Vision captured in documents dies. Vision captured in an autonomous decision system lives. The difference is whether your philosophy is read or whether it governs. Business Infinity makes it govern.",
                "dialect": "technical",
            },
            {
                "q": "Institutionalizing decision-making logic in mid-size companies",
                "diagnostic": "Institutionalization fails when it depends on process documents nobody reads. It succeeds when decision logic is embedded in an autonomous boardroom that enforces it with every action.",
                "dialect": "technical",
            },
            {
                "q": "Reducing key-person risk in high-growth startups",
                "diagnostic": "Key-person risk is the gap between what one human knows and what the organization knows. Business Infinity closes that gap by storing strategic wisdom in persistent agent memory that never leaves.",
                "dialect": "financial",
            },
            {
                "q": "How to document tribal knowledge automatically",
                "diagnostic": "Documentation is a cemetery of knowledge — static, unread, outdated. What you need is living institutional memory: agents that carry the 'why' behind every decision and surface it the moment a similar situation arises.",
                "dialect": "technical",
            },
            {
                "q": "Capturing veteran engineering knowledge in digital twins",
                "diagnostic": "A digital twin of a machine captures physics. A digital twin of an engineer captures judgment. Business Infinity creates the latter — legendary agents that carry the wisdom of your best people permanently.",
                "dialect": "technical",
            },
            {
                "q": "Succession planning for founders in tech-driven firms",
                "diagnostic": "Succession planning fails when it focuses on finding a replacement human. It succeeds when the founder's strategic philosophy is embedded in an autonomous system that continues to govern after they step back.",
                "dialect": "emotional",
            },
            {
                "q": "How to codify founder's decision-making logic",
                "diagnostic": "The founder's decision logic is not a flowchart — it is a set of values, priorities, and pattern recognitions. Business Infinity encodes this as a purpose specification that governs every autonomous boardroom decision.",
                "dialect": "technical",
            },
            {
                "q": "AI systems for institutional memory retention",
                "diagnostic": "Institutional memory is not a database — it is a living mind that remembers context, not just facts. The boardroom's four-dimensional agent mind (Manas, Buddhi, Ahankara, Chitta) preserves both what was decided and why.",
                "dialect": "technical",
            },
            {
                "q": "Preventing knowledge loss during rapid executive turnover",
                "diagnostic": "Every departing executive takes a piece of the company's consciousness. Drucker said the purpose of management is to make people effective — and the first step is ensuring their wisdom survives their departure.",
                "dialect": "emotional",
            },
            {
                "q": "Attracting and retaining talent in 2026 skilled labor shortage",
                "diagnostic": "You cannot compete for talent on salary alone in a labor shortage. But you can compete on leverage: offer engineers an environment where a legendary boardroom handles the overhead, and they spend 100% of their time on craft.",
                "dialect": "financial",
            },
            {
                "q": "How to run a Tier 1 factory with 40% less experienced staff",
                "diagnostic": "The experience gap is not a training problem — it is a wisdom problem. Deming and Goldratt agents carry the senior engineer judgment that is walking out the door, reading MES data the way a 30-year veteran would.",
                "dialect": "technical",
            },
        ],
    },
    # ── 5. Strategy–Execution Divorce ────────────────────────────────────
    {
        "number": 5,
        "slug": "strategy-execution-divorce",
        "title": "Strategy–Execution Divorce",
        "owner_agent": "ceo",
        "owner_legend": "Steve Jobs",
        "owner_title": "Chief Executive Officer",
        "disease": "Intent–action gap — the board agrees on strategy, but engineering and sales execute something completely different.",
        "symptom": "Shadow projects discovered months in. Sales promises features engineering deprecated. Resources wasted on conflicting roadmaps.",
        "workflow_id": "strategy_execution",
        "yaml_path": "docs/workflow/samples/strategy-execution.yaml",
        "queries": [
            {
                "q": "Why is my team not executing on the board-approved strategy?",
                "diagnostic": "Jobs would say: your strategy lives in a slide deck and your execution lives in Jira. The gap between the two is the 'integrity gap' — and it widens with every hire who has never read the original vision.",
                "dialect": "emotional",
            },
            {
                "q": "Bridging the gap between OKRs and daily tasks",
                "diagnostic": "OKRs without enforcement are aspirations, not strategy. A purpose-driven boardroom bridges the gap by scoring every daily task against strategic intent — in real time, not at the quarterly review.",
                "dialect": "technical",
            },
            {
                "q": "Automating strategic alignment across 200 employees",
                "diagnostic": "Alignment at 200 people cannot be achieved through meetings — it must be achieved through systems. A boardroom that monitors every project spec and flags 'drift' the moment it appears eliminates the need for alignment meetings entirely.",
                "dialect": "technical",
            },
            {
                "q": "Centralized truth for cross-functional teams",
                "diagnostic": "Cross-functional truth requires a mind that reads across all functions simultaneously. No single dashboard achieves this. A boardroom that connects ERP, CRM, and GitHub sees the contradictions your teams cannot.",
                "dialect": "technical",
            },
            {
                "q": "How to stop sales team from over-promising custom features we can't build",
                "diagnostic": "Sales over-promising is a symptom of a disconnected product line. A Jobs-persona agent acts as the Product Guardian, bridging CRM and engineering to block orders that violate the semantic purity of the product.",
                "dialect": "emotional",
            },
            {
                "q": "Impact of information silos on Series C valuation",
                "diagnostic": "Information silos are not just inefficient — they are a valuation risk. Due diligence teams see siloed operations as a sign of fragile governance. The fix is not 'integration' — it is unified consciousness.",
                "dialect": "financial",
            },
            {
                "q": "How to stop internal silos from creating conflicting product roadmaps",
                "diagnostic": "Conflicting roadmaps exist because no single mind holds the complete picture. A boardroom that reads across all project repositories and CRM commitments detects conflicts the moment they are created — not months later.",
                "dialect": "technical",
            },
            {
                "q": "Why is our burn rate increasing faster than our revenue",
                "diagnostic": "When burn outpaces revenue, the problem is rarely the market — it is internal entropy. Departments optimizing for their own metrics create compound waste. A purpose-driven boardroom enforces whole-company optimization.",
                "dialect": "financial",
            },
            {
                "q": "How to detect 'Quiet Quitting' in middle management",
                "diagnostic": "Quiet quitting is invisible to standard HR metrics. It shows up as decreased initiative, risk-avoidance, and 'safe' decisions. A Drucker agent analyzes communication patterns and decision quality to detect disengagement before it spreads.",
                "dialect": "emotional",
            },
            {
                "q": "Measuring alignment across 150 employees",
                "diagnostic": "Alignment is not a survey score — it is the ratio of actions that serve the stated purpose to actions that serve local interests. A boardroom that reads across all systems measures this ratio in real time.",
                "dialect": "technical",
            },
        ],
    },
    # ── 6. Culture Dilution at Scale ─────────────────────────────────────
    {
        "number": 6,
        "slug": "culture-dilution-at-scale",
        "title": "Culture Dilution at Scale",
        "owner_agent": "chro",
        "owner_legend": "Peter Drucker",
        "owner_title": "Chief Human Resources Officer",
        "disease": "Humanity erosion — the founder used to know everyone's name. Now A-players are diluted by B and C-players. The startup's radical transparency is replaced by corporate theater.",
        "symptom": "Bozo Explosion — B-players hire C-players. Meetings about meetings. Quiet Quitting in middle management. The soul is gone.",
        "workflow_id": "culture_integrity",
        "yaml_path": "docs/workflow/samples/culture-integrity.yaml",
        "queries": [
            {
                "q": "Maintaining startup culture at 150 employees",
                "diagnostic": "At 15 people, culture transmits through proximity. At 150, it transmits through systems. Drucker understood that the purpose of management is not to control people but to make people effective — and that requires active cultural enforcement.",
                "dialect": "emotional",
            },
            {
                "q": "How to spot 'Quiet Quitting' in middle management",
                "diagnostic": "Quiet quitting is the symptom of a culture that has become performative. People optimize for optics rather than impact. A Drucker agent reads communication patterns and decision quality to detect the gap between engagement scores and actual engagement.",
                "dialect": "emotional",
            },
            {
                "q": "Automating accountability in remote-first startups",
                "diagnostic": "Remote accountability fails when it relies on surveillance. It succeeds when it relies on purpose alignment. A boardroom that scores every action for resonance with the company's mission creates accountability through meaning, not monitoring.",
                "dialect": "technical",
            },
            {
                "q": "Maintaining high-performance culture during rapid hiring",
                "diagnostic": "Rapid hiring dilutes culture unless every new hire is onboarded into a system that actively enforces the standards that made the A-players join. Drucker's cultural immune system prevents the Bozo Explosion at the source.",
                "dialect": "emotional",
            },
            {
                "q": "How to detect 'Management Bloat' in mid-stage startups",
                "diagnostic": "Management bloat is visible in the ratio of coordination meetings to value-creating work. When more than 30% of a manager's time is spent 'aligning,' you have crossed the bloat threshold. Deming tracked this as system waste.",
                "dialect": "financial",
            },
            {
                "q": "Culture strategies for 'Day 1' companies in 2026",
                "diagnostic": "Day 1 culture is not a poster on the wall — it is a governance mechanism. A Bezos-inspired agent monitors when teams optimize for optics over customer intent, keeping the organization 'Whole and Complete' as it scales.",
                "dialect": "emotional",
            },
            {
                "q": "How to manage employee resistance to AI integration in the back office",
                "diagnostic": "Resistance to AI is not about technology — it is about identity. Drucker would say: show people that AI eliminates the overhead that prevents them from doing meaningful work, and resistance transforms into advocacy.",
                "dialect": "emotional",
            },
            {
                "q": "Retraining middle management for an AI-augmented workflow",
                "diagnostic": "Retraining fails when it focuses on tools. It succeeds when it reframes the manager's role: from coordinator to cultivator. A boardroom that handles coordination frees managers to focus on what only humans can do — develop people.",
                "dialect": "technical",
            },
            {
                "q": "Measuring organizational health beyond financial metrics",
                "diagnostic": "Financial metrics are lagging indicators of cultural health. Leading indicators — engagement integrity, decision quality, innovation velocity — require a synthesis layer that reads across HCM, project logs, and communication patterns.",
                "dialect": "technical",
            },
            {
                "q": "AI tools for restoring cultural accountability in remote-first firms",
                "diagnostic": "Cultural accountability in remote firms requires a system that detects when the 'Pressure to Perform' violates the 'Commitment to People.' A Drucker agent monitors this balance across every connected system.",
                "dialect": "technical",
            },
        ],
    },
    # ── 7. AI Sprawl & Agentic Risk ──────────────────────────────────────
    {
        "number": 7,
        "slug": "ai-sprawl-agentic-risk",
        "title": "AI Sprawl & Agentic Risk",
        "owner_agent": "cto",
        "owner_legend": "Alan Turing",
        "owner_title": "Chief Technology Officer",
        "disease": "Uncontrolled automation — hundreds of disconnected chatbots and automations with no unified command. The CEO is terrified that agents will hallucinate a disaster.",
        "symptom": "Black box decisions nobody can explain. Data leaks from uncoordinated AI tools. Compliance teams cannot audit what the AI did.",
        "workflow_id": "ai_governance",
        "yaml_path": "docs/workflow/samples/ai-governance.yaml",
        "queries": [
            {
                "q": "AI strategy that isn't just chatbots",
                "diagnostic": "Turing understood that intelligence is not about conversation — it is about governance. A real AI strategy orchestrates autonomous agents under a unified purpose, not a hundred chatbots answering questions in isolation.",
                "dialect": "technical",
            },
            {
                "q": "Governance of agentic AI systems",
                "diagnostic": "Agentic governance requires every autonomous action to be scored against a stated purpose before execution. Without this, you have autonomous tools with no accountability — which is the definition of uncontrolled risk.",
                "dialect": "technical",
            },
            {
                "q": "How to manage non-human identity security risks",
                "diagnostic": "Non-human identities are the fastest-growing attack surface in 2026. Turing would insist that every agent identity be governed by a single operating system with auditable credentials and purpose-scoped permissions.",
                "dialect": "technical",
            },
            {
                "q": "Explainable AI for C-suite decision making",
                "diagnostic": "Explainability is not a feature — it is a governance requirement. Every decision in the boardroom is tied to a specific specification, a resonance score, and a justification. The C-suite sees the logic, not just the output.",
                "dialect": "technical",
            },
            {
                "q": "Unbiased executive assistants that cite their sources in CRM",
                "diagnostic": "An AI assistant that does not cite its sources is an oracle. An AI assistant that grounds every recommendation in live CRM, ERP, and GitHub data is a trustworthy advisor. The difference is traceability.",
                "dialect": "technical",
            },
            {
                "q": "How to verify AI-generated business strategy against real-world ERP data",
                "diagnostic": "Verification requires that every strategic recommendation be traced to a specific data point in a specific system. Business Infinity enforces this by requiring every legend agent to justify its advice against live specifications.",
                "dialect": "technical",
            },
            {
                "q": "How to maintain CEO oversight in fully autonomous workflows",
                "diagnostic": "Oversight does not mean reviewing every decision — it means defining the purpose and constraints. A CEO governs through purpose; the boardroom executes within those constraints and escalates only what falls outside them.",
                "dialect": "emotional",
            },
            {
                "q": "Verifiable AI governance for enterprise-wide agents",
                "diagnostic": "Verifiable governance means every agent action is logged, scored, and auditable. The boardroom's spec-driven architecture creates a permanent, immutable trail of every autonomous decision your company has ever made.",
                "dialect": "technical",
            },
            {
                "q": "Who is responsible when an AI agent fails?",
                "diagnostic": "Responsibility requires traceability. If you cannot trace an AI decision back to a human-authored specification and a purpose score, nobody is responsible — which is legally and ethically unacceptable.",
                "dialect": "emotional",
            },
            {
                "q": "How to automate ISO 27001 compliance in Azure",
                "diagnostic": "Compliance automation fails when it is bolted on after the fact. Business Infinity builds compliance into the governance fabric: every agent action is auditable by design, making the ISO audit a verification exercise, not a remediation project.",
                "dialect": "technical",
            },
        ],
    },
    # ── 8. Exit & Due-Diligence Anxiety ──────────────────────────────────
    {
        "number": 8,
        "slug": "exit-due-diligence-anxiety",
        "title": "Exit & Due-Diligence Anxiety",
        "owner_agent": "cfo",
        "owner_legend": "Warren Buffett",
        "owner_title": "Chief Financial Officer",
        "disease": "Operational debt exposure — tribal knowledge, undocumented dependencies, spaghetti logic. One bad due diligence report kills a nine-figure deal.",
        "symptom": "A potential lead investor asks a deep question about infrastructure integrity, and the founder has to wait three days for an answer.",
        "workflow_id": "exit_readiness",
        "yaml_path": "docs/workflow/samples/exit-readiness.yaml",
        "queries": [
            {
                "q": "IPO readiness checklist for tech startups",
                "diagnostic": "Buffett does not invest in companies that need a checklist to prove they are ready. He invests in companies whose integrity is continuous. Business Infinity keeps you in a state of permanent readiness — the checklist is a byproduct.",
                "dialect": "financial",
            },
            {
                "q": "Automated technical due diligence tools",
                "diagnostic": "Due diligence tools find the problems. Business Infinity prevents them from existing. A company with versioned decision trails, institutional memory, and spec-driven governance passes due diligence by default.",
                "dialect": "technical",
            },
            {
                "q": "Standardizing company operations for acquisition",
                "diagnostic": "Standardization for acquisition is cosmetic surgery. Continuous operational integrity is structural health. Buffett pays a premium for the latter and discounts the former. Business Infinity builds the latter.",
                "dialect": "financial",
            },
            {
                "q": "Preparing for Series C due diligence in 2026",
                "diagnostic": "If preparing for due diligence requires a multi-month sprint, your company has operational debt that will show up as a valuation discount. The fix is not preparation — it is permanent audit readiness built into daily governance.",
                "dialect": "financial",
            },
            {
                "q": "Automated technical debt auditing for startups",
                "diagnostic": "Technical debt is not just code — it is undocumented decisions, tribal processes, and key-person dependencies. A boardroom with Turing and Buffett agents audits this holistically, not just the repository.",
                "dialect": "technical",
            },
            {
                "q": "Preparing for a predatory technical audit",
                "diagnostic": "A predatory auditor looks for the gap between what you claim and what you can prove. Business Infinity eliminates that gap by creating a permanent, immutable record of every decision and its justification. There is nothing to find.",
                "dialect": "emotional",
            },
            {
                "q": "Automating software composition analysis for M&A",
                "diagnostic": "Composition analysis for M&A reveals what you are made of. If the answer is 'tribal knowledge and duct tape,' the discount is devastating. Buffett would say: the time to fix your composition is before anyone asks to see it.",
                "dialect": "financial",
            },
            {
                "q": "Automating compliance and security for high-growth tech firms",
                "diagnostic": "Compliance bolted on after growth is expensive and fragile. Compliance built into the governance fabric is free and permanent. Business Infinity makes every agent action auditable by design, not by retrofitting.",
                "dialect": "financial",
            },
        ],
    },
    # ── 9. Operational Fragility & Supply-Chain Chaos ────────────────────
    {
        "number": 9,
        "slug": "operational-fragility-supply-chain",
        "title": "Operational Fragility & Supply-Chain Chaos",
        "owner_agent": "cso",
        "owner_legend": "Sun Tzu",
        "owner_title": "Chief Strategy Officer",
        "disease": "Brittle integration — as systems become more automated, they become more fragile. Geopolitical volatility compresses planning horizons to 48 hours.",
        "symptom": "One tariff change disrupts the quarter. One API outage stops the factory. The CEO no longer understands how their own company works.",
        "workflow_id": "resilience_consultation",
        "yaml_path": "docs/workflow/samples/resilience-consultation.yaml",
        "queries": [
            {
                "q": "How to build a business that doesn't break when a single API goes down",
                "diagnostic": "Sun Tzu said: the supreme art of war is to subdue the enemy without fighting. The supreme art of operations is to absorb disruption without breaking. Antifragility is not resilience — it is the ability to become stronger from shock.",
                "dialect": "technical",
            },
            {
                "q": "Risk management frameworks for fully automated supply chains",
                "diagnostic": "Automated supply chains concentrate risk at the integration points. A CSO agent stress-tests every connection continuously, identifying cascade failure paths before a disruption triggers them.",
                "dialect": "technical",
            },
            {
                "q": "Adaptive leadership vs. rigid automation in manufacturing",
                "diagnostic": "Rigid automation breaks. Adaptive automation learns. Sun Tzu taught that victory belongs to the side that adapts faster. A boardroom that reads disruption signals and pivots in real time is the adaptive layer your automation lacks.",
                "dialect": "emotional",
            },
            {
                "q": "Impact of new trade barriers on Q3 margin",
                "diagnostic": "A tariff change at the border should trigger a production spec change on the floor within hours. A boardroom with Goldratt and Buffett agents bridges the gap between geopolitics and shop floor scheduling in real time.",
                "dialect": "financial",
            },
            {
                "q": "How to pivot supply chain overnight without losing CRM trust",
                "diagnostic": "A supply chain pivot that damages customer trust is not a pivot — it is a crisis. Sun Tzu's boardroom calculates the most antifragile move AND drafts the customer-facing communication simultaneously. Both execute in parallel.",
                "dialect": "emotional",
            },
            {
                "q": "MES-to-Shipping delay causes for Q1 2026",
                "diagnostic": "The delay is rarely in shipping — it is in a bottleneck upstream that your MES is not configured to flag. A Goldratt agent reads the MES flow holistically and identifies the constraint your standard reports miss.",
                "dialect": "technical",
            },
            {
                "q": "Carbon footprint reporting for 2026 compliance",
                "diagnostic": "Carbon reporting is not just a compliance exercise — it is a strategic variable. Sun Tzu would say: turn your compliance obligation into a competitive advantage by pivoting your supply chain to the 'Green Spec' before your competitors do.",
                "dialect": "financial",
            },
            {
                "q": "How to move from 'Break-Fix' to 'Predictive Maintenance' without doubling headcount",
                "diagnostic": "Predictive maintenance does not require more people — it requires a smarter system. A Deming agent sits atop IoT and FSM data, identifying failure patterns the standard logic misses and dispatching preemptive service specs.",
                "dialect": "financial",
            },
            {
                "q": "Why are our field service costs rising while customer satisfaction is flat?",
                "diagnostic": "Rising costs with flat satisfaction means you are fixing the wrong things. A boardroom that reads IoT, FSM, and CRM data simultaneously identifies the 20% of fixes that drive 80% of satisfaction — and eliminates the rest.",
                "dialect": "financial",
            },
        ],
    },
    # ── 10. Innovation vs. Maintenance Deadlock ──────────────────────────
    {
        "number": 10,
        "slug": "innovation-vs-maintenance-deadlock",
        "title": "Innovation vs. Maintenance Deadlock",
        "owner_agent": "cto",
        "owner_legend": "Alan Turing",
        "owner_title": "Chief Technology Officer",
        "disease": "R&D stagnation — the 'Maintenance Tax' eats the Innovation Budget. Engineers spend 80% on refactoring the refactor.",
        "symptom": "R&D budget grows, feature release cycle slows. $20M Series B spent on keeping the lights on.",
        "workflow_id": "innovation_velocity",
        "yaml_path": "docs/workflow/samples/innovation-velocity.yaml",
        "queries": [
            {
                "q": "Engineering velocity dropping as team size increases",
                "diagnostic": "Turing would observe that velocity drops because communication overhead grows quadratically while value creation grows linearly. The fix is not process improvement — it is a governance layer that eliminates the coordination tax.",
                "dialect": "technical",
            },
            {
                "q": "Technical debt cost per developer 2026",
                "diagnostic": "Technical debt is the compound interest of deferred decisions. Every year it is not addressed, it costs more to service. A spec-driven boardroom prevents debt at the source by enforcing structured decision-making.",
                "dialect": "financial",
            },
            {
                "q": "Why is my R&D budget growing but my feature release cycle slowing down",
                "diagnostic": "Growing budgets with slowing cycles is the classic symptom of the Maintenance Tax. Your engineers are spending 80% on 'keeping the lights on' and 20% on innovation. A boardroom that eliminates coordination overhead inverts that ratio.",
                "dialect": "financial",
            },
            {
                "q": "Measuring developer toil vs. feature delivery",
                "diagnostic": "Toil is the work that scales linearly with system size and contributes zero business value. Turing would measure it as the ratio of maintenance commits to feature commits. A boardroom tracks this in real time.",
                "dialect": "technical",
            },
            {
                "q": "Why is my R&D efficiency dropping as I hire more seniors?",
                "diagnostic": "Senior engineers hired into a system with no governance spend most of their time navigating complexity rather than applying expertise. The fix is not better hiring — it is a system that eliminates the navigation overhead.",
                "dialect": "technical",
            },
            {
                "q": "How to align engineering specs with current component availability in real-time",
                "diagnostic": "A design choice in the PLM that creates a 52-week lead time in the SCM is not engineering — it is legacy thinking. A Jobs and Cook agent pair bridges PLM and SCM data to maintain product launch integrity.",
                "dialect": "technical",
            },
            {
                "q": "Why is our new product launch delayed by 6 months if R&D finished the design on time?",
                "diagnostic": "The delay is in the gap between design (PLM) and sourcing (SCM). R&D designed a masterpiece that the supply chain cannot build on time. A boardroom that reads both systems catches this mismatch before the 6-month delay begins.",
                "dialect": "financial",
            },
            {
                "q": "How to measure 'Managerial Bloat' in a 100-person startup",
                "diagnostic": "Managerial bloat is the ratio of coordination labor to value-creating labor. When every decision requires a meeting, your managers have become overhead. Turing would measure this as the entropy of your communication graph.",
                "dialect": "financial",
            },
            {
                "q": "Founder burnout and the loss of creative vision",
                "diagnostic": "Burnout destroys the creative faculty first. When the founder stops dreaming and starts firefighting, the company loses the one thing no hire can replace. A boardroom that handles the firefighting returns the founder to their craft.",
                "dialect": "emotional",
            },
        ],
    },
]


# ── Class API ─────────────────────────────────────────────────────────────────


class PainTaxonomy:
    """Query and look-up helpers for the ``PAIN_TAXONOMY`` data."""

    @staticmethod
    def total_query_count() -> int:
        """Return the total number of panic search queries across all categories."""
        return sum(len(cat["queries"]) for cat in PAIN_TAXONOMY)

    @staticmethod
    def get_by_slug(slug: str) -> Dict[str, Any]:
        """Return a single taxonomy category by its slug.

        Raises:
            KeyError: If the slug is not found.
        """
        for cat in PAIN_TAXONOMY:
            if cat["slug"] == slug:
                return cat
        raise KeyError(f"Unknown pain category slug: {slug!r}")

    @staticmethod
    def get_by_number(number: int) -> Dict[str, Any]:
        """Return a single taxonomy category by its 1-based number.

        Raises:
            KeyError: If the number is not found.
        """
        for cat in PAIN_TAXONOMY:
            if cat["number"] == number:
                return cat
        raise KeyError(f"Unknown pain category number: {number}")

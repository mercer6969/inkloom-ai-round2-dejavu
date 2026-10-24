"""
Inkloom AI — Round 2 Multi-Agent Brand Governance Backend (FastAPI)
Team DejaVu | Parallel Multi-Agent RAG + WCAG 2.1 + Cryptographic Audit Trail
"""
import asyncio
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Inkloom AI Governance Engine API",
    version="2.4.0",
    description="Parallel Multi-Agent Brand Governance Co-Pilot by Team DejaVu"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VisualMetadata(BaseModel):
    primary_hex: str = "#2B2F55"
    foreground_hex: str = "#FFFFFF"
    hero_alt_text: Optional[str] = None

class EvaluationRequest(BaseModel):
    tenant_id: str = "acme-enterprise-in"
    intake_channel: str = "Web App Studio"
    document_title: str
    content_body: str
    visual_metadata: VisualMetadata

class KnowledgeRule(BaseModel):
    id: str
    dimension: str
    agent: str
    severity: str
    trigger: str
    replacement: str
    source_doc: str
    source_page: str
    explanation: str

KNOWLEDGE_BASE: List[KnowledgeRule] = [
    KnowledgeRule(
        id="rule-facts-1",
        dimension="facts",
        agent="Fact-Checking & RAG Agent",
        severity="Critical",
        trigger="₹3,999",
        replacement="₹4,999",
        source_doc="Q3-Pricing-Matrix.pdf",
        source_page="Page 4, Table 2.1",
        explanation="Outdated pricing tier. According to Q3-Pricing-Matrix.pdf (Page 4), the starting tier is ₹4,999/month, not ₹3,999/month."
    ),
    KnowledgeRule(
        id="rule-tone-1",
        dimension="tone",
        agent="Tone & Style Agent",
        severity="Warning",
        trigger="synergistic paradigm-shifting disruptor",
        replacement="collaborative enterprise cloud platform",
        source_doc="Brand-Voice-Handbook-v4.2.pdf",
        source_page="Page 12, Sec 3.2",
        explanation="Prohibited buzzwords. Brand Voice Handbook (Page 12) prohibits empty hype terms in favor of clear value statements."
    ),
    KnowledgeRule(
        id="rule-legal-1",
        dimension="legal",
        agent="Policy & Compliance Agent",
        severity="Critical",
        trigger="100% guaranteed zero downtime forever",
        replacement="99.99% financially backed uptime SLA",
        source_doc="Regulatory-Claims-Policy-2026.pdf",
        source_page="Page 7, Clause 4.1",
        explanation="Unsupported absolute guarantee. Legal Policy (Page 7) requires citing the contractual 99.99% SLA."
    ),
]

AUDIT_TRAIL: List[Dict] = []

def hex_to_luminance(hex_code: str) -> float:
    clean = hex_code.lstrip("#")
    r, g, b = [int(clean[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
     convert = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * convert(r) + 0.7152 * convert(g) + 0.0722 * convert(b)

def compute_wcag_ratio(hex1: str, hex2: str) -> float:
    l1, l2 = hex_to_luminance(hex1), hex_to_luminance(hex2)
    return round((max(l1, l2) + 0.05) / (min(l1, l2) + 0.05), 2)

async def run_text_agent(dimension: str, text: str) -> List[Dict]:
    await asyncio.sleep(0.02)
    matches = []
    lower = text.lower()
    for rule in KNOWLEDGE_BASE:
        if rule.dimension == dimension and rule.trigger.lower() in lower:
            matches.append(rule.dict())
    return matches

async def run_visual_wcag_agent(meta: VisualMetadata) -> List[Dict]:
    await asyncio.sleep(0.01)
    flags = []
    if meta.primary_hex.upper() not in {"#2B2F55", "#4F46E5", "#0F172A"}:
        flags.append({
            "id": "rule-visual-hex",
            "dimension": "visual",
            "agent": "Visual & Accessibility Agent",
            "severity": "Warning",
            "trigger": f"Banner Hex {meta.primary_hex}",
            "replacement": "#2B2F55 (Approved Ink Navy)",
            "source_doc": "Visual-Identity-WCAG-Spec.pdf",
            "source_page": "Page 6, Sec 2.1",
            "explanation": "Primary brand color outside approved enterprise token list."
        })
    ratio = compute_wcag_ratio(meta.primary_hex, meta.foreground_hex)
    if ratio < 4.5:
        flags.append({
            "id": "rule-wcag-contrast",
            "dimension": "accessibility",
            "agent": "Visual & Accessibility Agent",
            "severity": "Critical",
            "trigger": f"Contrast Ratio {ratio}:1",
            "replacement": "4.5:1+ WCAG AA (#2B2F55 on #FFFFFF = 12.6:1)",
            "source_doc": "Visual-Identity-WCAG-Spec.pdf",
            "source_page": "Page 14, Sec 5.1",
            "explanation": f"Contrast ratio {ratio}:1 fails WCAG 2.1 AA minimum (4.5:1)."
        })
    if not meta.hero_alt_text or len(meta.hero_alt_text.strip()) < 8:
        flags.append({
            "id": "rule-wcag-alt",
            "dimension": "accessibility",
            "agent": "Visual & Accessibility Agent",
            "severity": "Warning",
            "trigger": "Missing Hero Image Alt-Text",
            "replacement": "Descriptive screen-reader alt-text for campaign graphic",
            "source_doc": "Visual-Identity-WCAG-Spec.pdf",
            "source_page": "Page 16, Sec 5.4",
            "explanation": "Mandatory alt-text missing for screen-reader accessibility."
        })
    return flags

@app.post("/api/v2/governance/evaluate")
async def evaluate_draft(req: EvaluationRequest):
    t0 = time.perf_counter()
    tone_flags, fact_flags, legal_flags, visual_flags = await asyncio.gather(
        run_text_agent("tone", req.content_body),
        run_text_agent("facts", req.content_body),
        run_text_agent("legal", req.content_body),
        run_visual_wcag_agent(req.visual_metadata),
    )
    all_flags = tone_flags + fact_flags + legal_flags + visual_flags
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)

    audit_hash = hashlib.sha256(f"{req.document_title}:{time.time()}".encode()).hexdigest()[:12]
    AUDIT_TRAIL.append({
        "timestamp": datetime.utcnow().isoformat(),
        "tenant_id": req.tenant_id,
        "channel": req.intake_channel,
        "flags_count": len(all_flags),
        "audit_hash": f"0x{audit_hash}"
    })
    return {
        "status": "completed",
        "execution_ms": elapsed_ms,
        "flags_detected": all_flags,
        "audit_hash": f"0x{audit_hash}"
    }

@app.post("/api/v2/knowledge/ingest")
async def ingest_rule(rule: KnowledgeRule):
    KNOWLEDGE_BASE.append(rule)
    return {"status": "indexed", "total_rules": len(KNOWLEDGE_BASE)}

@app.get("/api/v2/audit")
async def get_audit_trail():
    return {"records": AUDIT_TRAIL}

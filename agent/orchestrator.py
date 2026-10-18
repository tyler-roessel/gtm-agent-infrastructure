"""
Synthetic GTM infrastructure orchestrator.

This is a public-safe reference implementation. It demonstrates the workflow:

source -> identity -> enrich -> score -> draft -> review -> CRM write plan

Sandbox mode uses synthetic data only and calls no external APIs.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("gtm-orchestrator")


ICP_SEGMENTS = [
    "Growth-First Founder",
    "Revenue Operations Lead",
    "VP of Sales",
    "GTM Platform Builder",
]

SOURCES = ["directory", "referral", "job_signal", "manual", "partner", "content_signal"]
INDUSTRIES = ["B2B SaaS", "FinTech", "Marketplace", "Enterprise SaaS", "Developer Tools", "Vertical SaaS"]
FUNDING_STAGES = ["Pre-Seed", "Seed", "Series A", "Series B", "Series C", "Bootstrapped", "Growth"]
COMPANY_NAMES = [
    "Synthwave AI",
    "DataPond",
    "BuildCore",
    "MeshLabs",
    "FluxGen",
    "TerraMetric",
    "CircuitPath",
    "PulseField",
    "VertexStack",
    "HarborLine",
    "CoveSync",
    "AtlasGrid",
    "PrismScale",
    "EchoBridge",
    "NexusForge",
    "ApexRoute",
]

TECH_STACKS = [
    ["Attio", "Airtable", "n8n"],
    ["Salesforce", "Gong", "Marketo"],
    ["HubSpot", "Clay", "Zapier"],
    ["Salesforce", "Snowflake", "Outreach"],
    ["Airtable", "Make", "Slack"],
    ["HubSpot", "Intercom", "Clearbit"],
]


@dataclass
class Company:
    company_id: str
    name: str
    domain: str
    source: str
    industry: str
    employee_count: int
    funding_stage: str
    funding_amount: int | None
    tech_stack: list[str]
    discovered_at: str
    pipeline_stage: str = "discovered"
    enrichment_status: str = "pending"
    icp_segment: str | None = None
    icp_score: float = 0.0
    error: str | None = None


@dataclass
class ReviewRecord:
    review_id: str
    company_id: str
    company_name: str
    icp_segment: str
    icp_score: float
    draft_summary: str
    suggested_actions: list[str]
    status: str = "pending"
    reviewer_notes: str = ""
    write_plan: dict = field(default_factory=dict)
    approved_by: str | None = None


def normalize_domain(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "", name.lower())
    return f"{slug}.test"


def synthetic_companies(count: int, *, seed: int = 0) -> list[Company]:
    if count < 0:
        raise ValueError("record count cannot be negative")
    rng = random.Random(seed)
    now = datetime.now(timezone.utc).isoformat()
    companies = []
    for idx in range(count):
        name = COMPANY_NAMES[idx % len(COMPANY_NAMES)]
        stage = rng.choice(FUNDING_STAGES)
        funding_amount = None if stage == "Bootstrapped" else rng.choice([750_000, 3_000_000, 8_000_000, 15_000_000, 40_000_000, 90_000_000])
        companies.append(
            Company(
                company_id=f"COMP-{idx + 1:04d}",
                name=name,
                domain=normalize_domain(name),
                source=rng.choice(SOURCES),
                industry=rng.choice(INDUSTRIES),
                employee_count=rng.choice([8, 18, 35, 80, 150, 300, 700, 1200]),
                funding_stage=stage,
                funding_amount=funding_amount,
                tech_stack=list(rng.choice(TECH_STACKS)),
                discovered_at=now,
            )
        )
    return companies


def score_icp(company: Company) -> tuple[str, float]:
    """Illustrative deterministic fit rubric; not a calibrated probability."""
    if isinstance(company.employee_count, bool) or company.employee_count <= 0:
        raise ValueError("employee count must be positive")
    if company.funding_amount is not None and company.funding_amount < 0:
        raise ValueError("funding amount cannot be negative")
    scores = {}

    founder = 0.0
    founder += 0.25 if company.employee_count <= 50 else 0
    founder += 0.25 if company.funding_stage in {"Pre-Seed", "Seed"} else 0
    founder += 0.2 if company.funding_amount and company.funding_amount < 10_000_000 else 0
    founder += 0.15 if company.source in {"job_signal", "content_signal", "directory"} else 0
    scores["Growth-First Founder"] = founder

    revops = 0.0
    revops += 0.25 if 50 <= company.employee_count <= 500 else 0
    revops += 0.2 if company.funding_stage in {"Series A", "Series B"} else 0
    revops += 0.2 if {"Salesforce", "HubSpot", "Attio"} & set(company.tech_stack) else 0
    revops += 0.15 if company.industry in {"B2B SaaS", "Marketplace", "Enterprise SaaS"} else 0
    scores["Revenue Operations Lead"] = revops

    vp_sales = 0.0
    vp_sales += 0.3 if company.employee_count >= 200 else 0
    vp_sales += 0.2 if company.funding_stage in {"Series B", "Series C", "Growth"} else 0
    vp_sales += 0.2 if "Salesforce" in company.tech_stack else 0
    vp_sales += 0.15 if company.industry in {"Enterprise SaaS", "FinTech"} else 0
    scores["VP of Sales"] = vp_sales

    builder = 0.0
    builder += 0.25 if {"Attio", "Airtable", "n8n", "Make"} & set(company.tech_stack) else 0
    builder += 0.2 if company.industry in {"Developer Tools", "B2B SaaS", "Vertical SaaS"} else 0
    builder += 0.15 if company.source in {"job_signal", "content_signal"} else 0
    builder += 0.15 if company.employee_count <= 700 else 0
    scores["GTM Platform Builder"] = builder

    segment = max(scores, key=scores.get)
    score = scores[segment]
    return segment, round(score, 2)


def enrich(company: Company, simulate_rate_limit: bool = False, *, rng: random.Random | None = None) -> Company:
    if simulate_rate_limit and (rng or random.Random(0)).random() < 0.15:
        raise RuntimeError("simulated_rate_limit")
    company.enrichment_status = "complete"
    company.pipeline_stage = "enriched"
    company.icp_segment, company.icp_score = score_icp(company)
    return company


def build_review(company: Company) -> ReviewRecord:
    summary = (
        f"{company.name} ({company.domain}) is a {company.industry} company with "
        f"{company.employee_count} employees. Source={company.source}. "
        f"ICP={company.icp_segment} score={company.icp_score}."
    )
    actions = [
        "verify identity",
        "dedupe by domain",
        "prepare CRM company payload",
        "route to review queue",
    ]
    return ReviewRecord(
        review_id=f"REVIEW-{company.company_id}",
        company_id=company.company_id,
        company_name=company.name,
        icp_segment=company.icp_segment or "Unscored",
        icp_score=company.icp_score,
        draft_summary=summary,
        suggested_actions=actions,
    )


def review(record: ReviewRecord, *, approved_by: str | None = None) -> ReviewRecord:
    record.write_plan = {}
    record.approved_by = None
    if approved_by is not None and (not isinstance(approved_by, str) or not approved_by.strip()):
        raise ValueError("reviewer must be non-empty")
    if approved_by:
        record.status = "approved"
        record.approved_by = approved_by.strip()
        record.reviewer_notes = "Explicit local review decision; mapping plan only."
        record.write_plan = {
            "crm_object": "company",
            "operation": "upsert",
            "dedupe_key": "domain",
            "payload_fields": ["name", "domain", "icp_segment", "icp_score", "source"],
        }
    elif record.icp_score < 0.35:
        record.status = "rejected"
        record.reviewer_notes = "Low illustrative fit score. Retain for manual triage."
    else:
        record.status = "pending"
        record.reviewer_notes = "Needs human review before CRM handoff."
    return record


def run_pipeline(args: argparse.Namespace) -> tuple[list[Company], list[ReviewRecord], list[dict]]:
    companies = synthetic_companies(args.records, seed=args.seed)
    rng = random.Random(args.seed)
    reviews: list[ReviewRecord] = []
    failures: list[dict] = []

    log.info("Stage 1: discovery and intake (%s records)", len(companies))

    log.info("Stage 2: identity cleanup and dedupe")
    seen_domains = set()
    unique = []
    for company in companies:
        if company.domain in seen_domains:
            failures.append({"company_id": company.company_id, "error": "duplicate_domain", "domain": company.domain})
            continue
        seen_domains.add(company.domain)
        company.pipeline_stage = "identified"
        unique.append(company)

    log.info("Stage 3: verification, enrichment, and scoring")
    for idx, company in enumerate(unique):
        try:
            if args.simulate_20pct_failure and idx % 5 == 0:
                raise RuntimeError("simulated_validation_failure")
            enrich(company, simulate_rate_limit=args.simulate_rate_limit, rng=rng)
        except Exception as exc:
            company.enrichment_status = "failed"
            company.pipeline_stage = "enrichment_failed"
            company.error = str(exc)
            failures.append({"company_id": company.company_id, "error": str(exc), "stage": "enrichment"})

    log.info("Stage 4: drafting, recommendation, and review")
    for company in unique:
        if company.enrichment_status == "complete":
            company.pipeline_stage = "reviewing"
            item = build_review(company)
            reviewer = args.reviewer if item.review_id in args.approve else None
            reviews.append(review(item, approved_by=reviewer))

    unknown = set(args.approve) - {item.review_id for item in reviews}
    if unknown:
        raise ValueError("approval IDs are absent or failed enrichment: " + ", ".join(sorted(unknown)))

    log.info("Stage 5: CRM handoff and automation-ready execution")
    approved = [item for item in reviews if item.status == "approved"]
    for item in approved:
        matching = next(company for company in unique if company.company_id == item.company_id)
        matching.pipeline_stage = "write_planned"

    return unique, reviews, failures


def export_csv(path: Path, companies: list[Company], reviews: list[ReviewRecord], failures: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    review_by_company = {item.company_id: item for item in reviews}
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "company_id",
                "company_name",
                "domain",
                "source",
                "icp_segment",
                "icp_score",
                "pipeline_stage",
                "review_status",
            ],
        )
        writer.writeheader()
        for company in companies:
            review_record = review_by_company.get(company.company_id)
            writer.writerow(
                {
                    "company_id": company.company_id,
                    "company_name": company.name,
                    "domain": company.domain,
                    "source": company.source,
                    "icp_segment": company.icp_segment,
                    "icp_score": company.icp_score,
                    "pipeline_stage": company.pipeline_stage,
                    "review_status": review_record.status if review_record else "none",
                }
            )

    failure_path = path.with_name(path.stem + "-failures.json")
    failure_path.write_text(json.dumps(failures, indent=2), encoding="utf-8")


def display(companies: list[Company], reviews: list[ReviewRecord], failures: list[dict]) -> None:
    print("\n--- PIPELINE VIEW (Sandbox) ---")
    print(f"Total records: {len(companies)}")
    for segment in ICP_SEGMENTS:
        records = [item for item in companies if item.icp_segment == segment]
        if records:
            avg = sum(item.icp_score for item in records) / len(records)
            print(f"  {segment}: {len(records)} records ({avg:.2f} avg rubric score)")

    print("\n--- REVIEW QUEUE ---")
    for status in ["pending", "approved", "rejected"]:
        print(f"  {status}: {sum(1 for item in reviews if item.status == status)}")

    print("\n--- FAILURE LOG ---")
    print(f"  failures preserved: {len(failures)}")
    print("\nAll sandbox data is synthetic. No external APIs were called.\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GTM infrastructure sandbox orchestrator")
    parser.add_argument("--sandbox", action="store_true", help="Run with synthetic data only")
    parser.add_argument("--records", type=int, default=25, help="Number of synthetic records")
    parser.add_argument("--seed", type=int, default=0, help="Reproducible synthetic fixture seed")
    parser.add_argument("--approve", action="append", default=[], metavar="REVIEW_ID", help="Explicitly approve a synthetic review ID")
    parser.add_argument("--reviewer", help="Name recorded for explicit local approval decisions")
    parser.add_argument("--simulate-rate-limit", action="store_true", help="Simulate intermittent rate limit errors")
    parser.add_argument("--simulate-20pct-failure", action="store_true", help="Simulate one failure per five records")
    parser.add_argument("--export", type=Path, help="Export synthetic pipeline output to CSV")
    args = parser.parse_args(argv)
    if args.records < 0:
        parser.error("--records cannot be negative")
    if args.approve and (not args.reviewer or not args.reviewer.strip()):
        parser.error("--approve requires a non-empty --reviewer")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if not args.sandbox:
        log.error("Only --sandbox mode is implemented in the public showcase.")
        return 2

    companies, reviews, failures = run_pipeline(args)
    display(companies, reviews, failures)

    if args.export:
        export_csv(args.export, companies, reviews, failures)
        log.info("Exported sandbox output to %s", args.export)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


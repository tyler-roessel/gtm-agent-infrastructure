from dataclasses import asdict, replace
import csv

import pytest

from agent.orchestrator import (
    build_review, enrich, export_csv, parse_args, review, run_pipeline, score_icp, synthetic_companies,
)


def test_same_facts_produce_the_same_score():
    company = synthetic_companies(1)[0]
    assert len({score_icp(company) for _ in range(20)}) == 1
    company = replace(company, employee_count=10, funding_stage="Seed", funding_amount=1_000_000, source="job_signal")
    segment, score = score_icp(company)
    assert segment == "Growth-First Founder"
    assert score == 0.85


def test_synthetic_fixture_seed_is_repeatable():
    first = synthetic_companies(5, seed=7)
    second = synthetic_companies(5, seed=7)
    for a, b in zip(first, second):
        assert asdict(a) == asdict(b)


def test_high_score_cannot_self_approve():
    item = build_review(synthetic_companies(1)[0])
    item.icp_score = 0.99
    assert review(item).status == "pending"
    assert item.write_plan == {}
    assert review(item, approved_by="fixture-reviewer").status == "approved"
    assert item.approved_by == "fixture-reviewer"


def test_re_review_does_not_retain_an_earlier_write_plan():
    item = build_review(synthetic_companies(1)[0])
    review(item, approved_by="fixture-reviewer")
    review(item)
    assert item.write_plan == {}
    assert item.approved_by is None


def test_pipeline_holds_all_records_without_explicit_approval():
    companies, reviews, _ = run_pipeline(parse_args(["--sandbox", "--records", "10"]))
    assert not any(item.write_plan for item in reviews)
    assert not any(item.pipeline_stage == "write_planned" for item in companies)


def test_pipeline_only_plans_the_selected_record():
    _, baseline, _ = run_pipeline(parse_args(["--sandbox", "--records", "10"]))
    selected = baseline[0].review_id
    args = parse_args(["--sandbox", "--records", "10", "--approve", selected, "--reviewer", "fixture-reviewer"])
    companies, reviews, _ = run_pipeline(args)
    assert [item.review_id for item in reviews if item.status == "approved"] == [selected]
    assert sum(item.pipeline_stage == "write_planned" for item in companies) == 1


def test_failed_enrichment_cannot_receive_approval_or_a_write_plan():
    args = parse_args(["--sandbox", "--records", "10", "--simulate-20pct-failure"])
    companies, reviews, failures = run_pipeline(args)
    failed_ids = {item.company_id for item in companies if item.enrichment_status == "failed"}
    assert len(failed_ids) == 2
    assert not failed_ids.intersection(item.company_id for item in reviews)
    assert len(failures) == 2


def test_unknown_approval_id_is_rejected():
    args = parse_args(["--sandbox", "--approve", "missing", "--reviewer", "fixture-reviewer"])
    with pytest.raises(ValueError, match="absent or failed"):
        run_pipeline(args)


@pytest.mark.parametrize("arguments", [
    ["--sandbox", "--records", "-1"],
    ["--sandbox", "--approve", "REVIEW-COMP-0001"],
])
def test_invalid_cli_arguments_are_rejected(arguments):
    with pytest.raises(SystemExit):
        parse_args(arguments)


def test_invalid_employee_count_is_rejected():
    with pytest.raises(ValueError):
        score_icp(replace(synthetic_companies(1)[0], employee_count=-1))


def test_approval_from_a_different_packet_is_rejected():
    _, original, _ = run_pipeline(parse_args(["--sandbox", "--records", "1", "--seed", "0"]))
    args = parse_args(["--sandbox", "--records", "1", "--seed", "1", "--approve", original[0].review_id, "--reviewer", "fixture-reviewer"])
    with pytest.raises(ValueError, match="absent or failed"):
        run_pipeline(args)


def test_export_retains_the_review_identity_and_reviewer(tmp_path):
    _, baseline, _ = run_pipeline(parse_args(["--sandbox", "--records", "1"]))
    args = parse_args(["--sandbox", "--records", "1", "--approve", baseline[0].review_id, "--reviewer", "fixture-reviewer"])
    companies, reviews, failures = run_pipeline(args)
    path = tmp_path / "output.csv"
    export_csv(path, companies, reviews, failures)
    with path.open() as handle:
        row = next(csv.DictReader(handle))
    assert row["review_id"] == baseline[0].review_id
    assert row["approved_by"] == "fixture-reviewer"


def test_direct_rate_limit_simulation_can_fail(monkeypatch):
    monkeypatch.setattr("agent.orchestrator.random.random", lambda: 0.1)
    with pytest.raises(RuntimeError, match="simulated_rate_limit"):
        enrich(synthetic_companies(1)[0], simulate_rate_limit=True)


def test_invalid_reviewer_does_not_mutate_an_existing_approval():
    item = review(build_review(synthetic_companies(1)[0]), approved_by="fixture-reviewer")
    before = asdict(item)
    with pytest.raises(ValueError, match="non-empty"):
        review(item, approved_by=" ")
    assert asdict(item) == before


def test_failed_direct_enrichment_never_claims_completion():
    company = replace(synthetic_companies(1)[0], employee_count=-1)
    before = asdict(company)
    with pytest.raises(ValueError):
        enrich(company)
    assert asdict(company) == before
    assert company.enrichment_status == "pending"

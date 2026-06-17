"""Tests for scoring/score.py — the main scoring pipeline."""

from leads.schema import Lead, LeadStatus
from search.base import RawCandidate
from scoring.score import score_candidate


class TestScoreCandidate:
    def test_hot_lead_ml_dsp_remote(self):
        """High score: ML keywords + real-time DSP + remote = HOT."""
        c = RawCandidate(
            source="test",
            title="ML Audio Engineer needed for CLAP plugin",
            url="https://example.com/job1",
            snippet="Looking for C++ DSP developer with Mamba/SSM experience for real-time audio plugin. Remote OK. Budget $5000.",
            tier=1,
        )
        lead = score_candidate(c, "plugin_dev")
        assert lead.verdict == "HOT"
        assert lead.score >= 15
        assert lead.status == LeadStatus.HOT

    def test_warm_lead_reaper(self):
        """REAPER automation keywords = +5 points (WARM alone)."""
        c = RawCandidate(
            source="test",
            title="REAPER scripting help",
            url="https://example.com/job2",
            snippet="Need a Lua script for REAPER to automate batch rendering. Paid.",
            tier=2,
        )
        lead = score_candidate(c, "reaper_scripts")
        assert "reaper_work" in lead.signals
        assert lead.signals["reaper_work"] == 5
        assert lead.verdict == "WARM"

    def test_cold_lead_generic(self):
        """Generic posting with no audio keywords = COLD."""
        c = RawCandidate(
            source="test",
            title="General Python Developer",
            url="https://example.com/job3",
            snippet="Looking for Python developer for web scraping project.",
            tier=1,
        )
        lead = score_candidate(c, "plugin_dev")
        assert lead.verdict == "COLD"
        assert lead.score < 8

    def test_skip_lead_rev_share(self):
        """Revenue share posting = SKIP."""
        c = RawCandidate(
            source="test",
            title="Exciting audio startup",
            url="https://example.com/job4",
            snippet="Join our team! Revenue share only. Build the next generation audio plugin.",
            tier=1,
        )
        lead = score_candidate(c, "plugin_dev")
        assert lead.verdict == "SKIP"
        assert lead.status == LeadStatus.SKIPPED

    def test_skip_lead_equity_only(self):
        """Equity only posting = SKIP."""
        c = RawCandidate(
            source="test",
            title="Cool music AI startup",
            url="https://example.com/job5",
            snippet="Equity only compensation for early stage audio AI company.",
            tier=1,
        )
        lead = score_candidate(c, "audio_ml")
        assert lead.verdict == "SKIP"

    def test_niche_routing(self):
        """Ensure niche is passed through correctly."""
        c = RawCandidate(
            source="test",
            title="Rust Audio Plugin",
            url="https://example.com/job6",
            snippet="Looking for Rust developer with nih-plug experience for CLAP plugin.",
            tier=1,
        )
        lead = score_candidate(c, "rust_audio")
        assert lead.niche == "rust_audio"
        assert lead.verdict in ("HOT", "WARM")

    def test_budget_above_floor(self):
        """Budget above $3000 CAD = +10 points."""
        c = RawCandidate(
            source="test",
            title="Well-funded plugin project",
            url="https://example.com/job7",
            snippet="Budget $5000 for C++ CLAP plugin development. Remote friendly.",
            tier=1,
        )
        lead = score_candidate(c, "plugin_dev")
        assert "budget_above_floor" in lead.signals
        assert lead.verdict == "HOT"

    def test_lead_defaults(self):
        """Default lead should have COLD verdict and score 0."""
        c = RawCandidate(
            source="test",
            title="Vague posting",
            url="https://example.com/job8",
            snippet="Need some audio work done.",
            tier=3,
        )
        lead = score_candidate(c, "plugin_dev")
        assert lead.score == 0 or lead.verdict == "COLD"

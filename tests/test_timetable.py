"""Tests for next Metromare train selection."""

import runpy
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

module = runpy.run_path(
    str(
        Path(__file__).resolve().parents[1]
        / "custom_components"
        / "astral_metromare"
        / "timetable.py"
    )
)
next_arrivals = module["next_arrivals"]
AstralApiError = module["AstralApiError"]
ROME = ZoneInfo("Europe/Rome")


def transit(time, delay="0", status="N", date="2026-10-01"):
    return {
        "orario": time,
        "ritardo": delay,
        "soppressa": status,
        "created_at": f"{date}T01:33:02Z",
    }


class TimetableTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 1, 18, 41, tzinfo=ROME)

    def test_selects_three_future_adjusted_arrivals_in_time_order(self):
        records = [
            transit("18:25"),
            transit("18:45", "15"),
            transit("18:56"),
            transit("19:02", status="S"),
            transit("19:10"),
            transit("19:25"),
        ]
        self.assertEqual(
            next_arrivals(records, self.now),
            (
                datetime(2026, 10, 1, 18, 56, tzinfo=ROME),
                datetime(2026, 10, 1, 19, 0, tzinfo=ROME),
                datetime(2026, 10, 1, 19, 10, tzinfo=ROME),
            ),
        )

    def test_delay_can_move_past_train_into_future(self):
        self.assertEqual(
            next_arrivals([transit("18:25", "25")], self.now),
            (datetime(2026, 10, 1, 18, 50, tzinfo=ROME), None, None),
        )

    def test_empty_delay_means_no_reported_delay(self):
        self.assertEqual(
            next_arrivals([transit("18:45", "")], self.now),
            (datetime(2026, 10, 1, 18, 45, tzinfo=ROME), None, None),
        )

    def test_fewer_than_three_future_trains(self):
        self.assertEqual(
            next_arrivals([transit("18:45"), transit("19:00")], self.now),
            (
                datetime(2026, 10, 1, 18, 45, tzinfo=ROME),
                datetime(2026, 10, 1, 19, 0, tzinfo=ROME),
                None,
            ),
        )

    def test_no_future_train_or_only_cancelled_trains(self):
        self.assertEqual(
            next_arrivals([transit("18:25"), transit("18:55", status="S")], self.now),
            (None, None, None),
        )
        self.assertEqual(next_arrivals([], self.now), (None, None, None))

    def test_rejects_previous_day_records(self):
        self.assertEqual(
            next_arrivals([transit("19:00", date="2026-09-30")], self.now),
            (None, None, None),
        )

    def test_invalid_record_fails_instead_of_reporting_no_trains(self):
        with self.assertRaises(AstralApiError):
            next_arrivals([{"orario": "25:15"}], self.now)


if __name__ == "__main__":
    unittest.main()

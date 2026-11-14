"""Small regression tests for data cleaning and the two research questions."""

import tempfile
from pathlib import Path
import unittest

import pandas as pd

from analyze_sales import (
    DataValidationError,
    analyze_genres,
    analyze_platform_regions,
    build_report,
    load_and_clean_data,
    SAMPLE_DATA,
)


class VideoGameSalesTests(unittest.TestCase):
    """Confirm that the project gives predictable, correct results."""

    def setUp(self) -> None:
        """Build a tiny independent dataset for deterministic assertions."""
        self.data = pd.DataFrame(
            {
                "Name": ["Game A", "Game B", "Game C"],
                "Genre": ["Sports", "Sports", "Action"],
                "Platform": ["PS", "PS", "XB"],
                "Global_Sales": [3.0, 2.0, 6.0],
                "NA_Sales": [1.5, 1.0, 5.0],
                "EU_Sales": [1.0, 0.8, 0.2],
            }
        )

    def test_genres_are_grouped_and_ranked(self) -> None:
        """Ensure the top genre reflects the sum, not the largest single game."""
        result = analyze_genres(self.data)
        self.assertEqual(result.iloc[0]["Genre"], "Action")
        self.assertEqual(result.iloc[1]["Genre"], "Sports")
        self.assertAlmostEqual(result.iloc[1]["Global_Sales_Millions"], 5.0)

    def test_platforms_rank_by_combined_regional_sales(self) -> None:
        """Verify Q2 uses NA+EU, and identifies the larger region."""
        result = analyze_platform_regions(self.data)
        self.assertEqual(result.iloc[0]["Platform"], "XB")
        self.assertAlmostEqual(result.iloc[0]["Combined_NA_EU_Millions"], 5.2)
        self.assertEqual(result.iloc[0]["Larger_Region"], "North America")

    def test_rejects_invalid_limits(self) -> None:
        """Reject a request for zero rows instead of returning silent output."""
        with self.assertRaises(ValueError):
            analyze_genres(self.data, limit=0)
        with self.assertRaises(ValueError):
            analyze_platform_regions(self.data, limit=0)

    def test_empty_genre_is_excluded(self) -> None:
        """Ignore incomplete category rows during cleaning."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.csv"
            rows = self.data.copy()
            rows.loc[0, "Genre"] = ""
            rows.to_csv(path, index=False)
            cleaned, stats = load_and_clean_data(path)
            self.assertEqual(len(cleaned), 2)
            self.assertEqual(stats["excluded_rows"], 1)

    def test_missing_column_raises_error(self) -> None:
        """Give a helpful message if the input file has the wrong structure."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.csv"
            self.data.drop(columns=["EU_Sales"]).to_csv(path, index=False)
            with self.assertRaises(DataValidationError):
                load_and_clean_data(path)

    def test_sample_dataset_has_50_real_records(self) -> None:
        """Check the distributed example really loads and contains 50 entries."""
        frame, stats = load_and_clean_data(SAMPLE_DATA)
        self.assertEqual(stats["original_rows"], 50)
        self.assertEqual(stats["excluded_rows"], 0)
        self.assertEqual(len(frame), 50)

    def test_report_contains_both_questions(self) -> None:
        """Ensure the report includes conclusions and labels the sample."""
        frame, stats = load_and_clean_data(SAMPLE_DATA)
        report = build_report(
            SAMPLE_DATA, stats, analyze_genres(frame),
            analyze_platform_regions(frame), True,
        )
        self.assertIn("QUESTION 1", report)
        self.assertIn("QUESTION 2", report)
        self.assertIn("TOP-50 SAMPLE ONLY", report)


if __name__ == "__main__":
    unittest.main()

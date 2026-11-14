

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib

# A non-interactive backend allows charts to be saved without opening a window.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = BASE_DIR / "data" / "vgsales.csv"
SAMPLE_DATA = BASE_DIR / "data" / "sample_vgsales.csv"
DEFAULT_OUTPUT = BASE_DIR / "output"
REQUIRED_COLUMNS = {"Name", "Genre", "Platform", "Global_Sales", "NA_Sales", "EU_Sales"}
SALES_COLUMNS = ["Global_Sales", "NA_Sales", "EU_Sales"]


class DataValidationError(ValueError):
    """Explain why a dataset cannot safely be analyzed."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line options to choose a dataset and output directory."""
    parser = argparse.ArgumentParser(description="Analyze historical video game sales")
    parser.add_argument(
        "--data", type=Path, default=DEFAULT_DATA,
        help="CSV dataset path (default: data/vgsales.csv)",
    )
    parser.add_argument(
        "--sample", action="store_true",
        help="Analyze the bundled top-50 sample (not the complete dataset)",
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Directory for CSV results, charts, and a text report",
    )
    return parser.parse_args(argv)


def load_and_clean_data(csv_path: Path) -> tuple[pd.DataFrame, dict[str, int]]:
    """Load CSV, validate necessary columns, and remove unusable sales rows.

    Missing release years are not removed because our two questions do not
    require the Year field. Missing genre, platform, or sales data are removed.
    """
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    frame = pd.read_csv(csv_path, encoding="utf-8-sig", low_memory=False)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise DataValidationError("Missing required columns: " + ", ".join(sorted(missing)))

    initial_rows = len(frame)
    frame = frame.copy()
    frame["Genre"] = frame["Genre"].astype("string").str.strip()
    frame["Platform"] = frame["Platform"].astype("string").str.strip()

    # Convert mixed strings/integers to numbers; invalid entries become NaN.
    for column in SALES_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    # Invalid numbers, empty identifiers, and negative sales are excluded.
    frame = frame.dropna(subset=["Genre", "Platform"] + SALES_COLUMNS)
    frame = frame[(frame["Genre"] != "") & (frame["Platform"] != "")]
    for column in SALES_COLUMNS:
        frame = frame[frame[column] >= 0]

    if frame.empty:
        raise DataValidationError("The dataset has no usable rows after cleaning.")

    stats = {
        "original_rows": initial_rows,
        "analyzed_rows": len(frame),
        "excluded_rows": initial_rows - len(frame),
        "genres": int(frame["Genre"].nunique()),
        "platforms": int(frame["Platform"].nunique()),
    }
    return frame, stats


def analyze_genres(frame: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    """Answer Q1: rank genres by summed worldwide sales (millions)."""
    if limit < 1:
        raise ValueError("limit must be positive")

    totals = (
        frame.groupby("Genre", as_index=False)
        .agg(Global_Sales_Millions=("Global_Sales", "sum"), Game_Entries=("Name", "count"))
        .sort_values(["Global_Sales_Millions", "Genre"], ascending=[False, True])
        .head(limit)
        .reset_index(drop=True)
    )
    return totals


def analyze_platform_regions(frame: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    """Answer Q2: compare the five highest NA+EU platform sales totals."""
    if limit < 1:
        raise ValueError("limit must be positive")

    totals = frame.groupby("Platform", as_index=False).agg(
        NA_Sales_Millions=("NA_Sales", "sum"),
        EU_Sales_Millions=("EU_Sales", "sum"),
        Game_Entries=("Name", "count"),
    )
    totals["Combined_NA_EU_Millions"] = (
        totals["NA_Sales_Millions"] + totals["EU_Sales_Millions"]
    )
    totals["Larger_Region"] = totals.apply(
        lambda row: (
            "North America" if row["NA_Sales_Millions"] > row["EU_Sales_Millions"]
            else "Europe" if row["EU_Sales_Millions"] > row["NA_Sales_Millions"]
            else "Tie"
        ),
        axis=1,
    )
    return (
        totals.sort_values(["Combined_NA_EU_Millions", "Platform"], ascending=[False, True])
        .head(limit).reset_index(drop=True)
    )


def make_genre_chart(results: pd.DataFrame, out_path: Path) -> None:
    """Save the main question's results as a horizontal bar chart."""
    fig, axis = plt.subplots(figsize=(10, 5.2))
    ordered = results.iloc[::-1]
    axis.barh(ordered["Genre"], ordered["Global_Sales_Millions"], color="#4668AA")
    axis.set_title("Top five genres by worldwide video game sales")
    axis.set_xlabel("Global sales (million units)")
    axis.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def make_platform_chart(results: pd.DataFrame, out_path: Path) -> None:
    """Save a stacked chart comparing regional sales across five platforms."""
    fig, axis = plt.subplots(figsize=(10, 5.2))
    ordered = results.iloc[::-1]
    axis.barh(ordered["Platform"], ordered["NA_Sales_Millions"], label="North America", color="#4668AA")
    axis.barh(
        ordered["Platform"], ordered["EU_Sales_Millions"],
        left=ordered["NA_Sales_Millions"], label="Europe", color="#D69553",
    )
    axis.set_title("Top five platforms — North America + Europe")
    axis.set_xlabel("Sales (million units)")
    axis.legend()
    axis.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def format_table(table: pd.DataFrame) -> str:
    """Return human-readable table text without Pandas index numbers."""
    return table.to_string(index=False, float_format=lambda value: f"{value:.2f}")


def build_report(
    source: Path, stats: dict[str, int],
    genre_results: pd.DataFrame, platform_results: pd.DataFrame,
    is_sample: bool,
) -> str:
    """Create an evidence-based explanation of each research question."""
    first_genre = genre_results.iloc[0]
    first_platform = platform_results.iloc[0]
    scope = "TOP-50 SAMPLE ONLY" if is_sample else "USER-SUPPLIED DATASET"
    lines = [
        "VIDEO GAME SALES ANALYZER",
        f"Scope: {scope}",
        f"Source file: {source.name}",
        "Sales are in millions of units, not dollars.",
        "A record represents a game/platform entry, not always a unique game.",
        f"Loaded rows: {stats['original_rows']}",
        f"Usable rows: {stats['analyzed_rows']}",
        f"Excluded rows: {stats['excluded_rows']}",
        f"Distinct genres: {stats['genres']}; platforms: {stats['platforms']}",
        "",
        "QUESTION 1: Which five genres have the highest global sales?",
        format_table(genre_results),
        (f"Answer: {first_genre['Genre']} ranks first with "
         f"{first_genre['Global_Sales_Millions']:.2f} million units in this dataset."),
        "",
        "QUESTION 2: Which five platforms lead in North America + Europe sales,",
        "and which region contributes more for each?",
        format_table(platform_results),
        (f"Answer: {first_platform['Platform']} ranks first with "
         f"{first_platform['Combined_NA_EU_Millions']:.2f} million combined units."),
        "See the Larger_Region column for each platform's regional comparison.",
        "",
        "LIMITATIONS",
        "Historical source data may be incomplete or contain category errors.",
        "Results depend on the file analyzed; a top-50 subset is not representative.",
        "Worldwide totals are taken from Global_Sales rather than recalculated",
        "from regional columns (rounding may cause small differences).",
    ]
    return "\n".join(lines) + "\n"


def save_outputs(
    output_dir: Path, genre_results: pd.DataFrame,
    platform_results: pd.DataFrame, report: str,
) -> None:
    """Write result tables, a readable report, and two chart PNG files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    genre_results.to_csv(output_dir / "top_genres.csv", index=False)
    platform_results.to_csv(output_dir / "top_platforms.csv", index=False)
    (output_dir / "analysis_results.txt").write_text(report, encoding="utf-8")
    make_genre_chart(genre_results, output_dir / "top_genres.png")
    make_platform_chart(platform_results, output_dir / "top_platforms.png")


def main(argv: list[str] | None = None) -> int:
    """Run loading, analysis, visualization, and reporting from the terminal."""
    args = parse_args(argv)
    data_path = SAMPLE_DATA if args.sample else args.data
    if not data_path.exists():
        print(
            "Full dataset missing. First run: python download_dataset.py\n"
            "Or run the bundled demonstration: python analyze_sales.py --sample",
            file=sys.stderr,
        )
        return 2

    try:
        frame, stats = load_and_clean_data(data_path)
        genres = analyze_genres(frame)
        platforms = analyze_platform_regions(frame)
        report = build_report(data_path, stats, genres, platforms, args.sample)
        save_outputs(args.output, genres, platforms, report)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Analysis failed: {error}", file=sys.stderr)
        return 1

    print(report)
    print(f"Charts and tables were saved to: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

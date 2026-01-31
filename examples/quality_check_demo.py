#!/usr/bin/env python3
"""
Example: Code Quality Analysis

This script demonstrates the CodeChecker capabilities:
- Analyzing Python files for quality issues
- Generating metrics and reports
- Understanding code maintainability
"""

import tempfile
from pathlib import Path
from devtools_helper import CodeChecker


def demonstrate_code_checker() -> None:
    """Demonstrate CodeChecker features."""

    print("🔍 DevTools Helper - Code Quality Checker Demo")
    print("=" * 55)

    # Create a temporary directory with sample code
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create sample Python files
        print("\n1️⃣ Creating sample code files...")

        # Good quality code
        good_code = '''
"""
A well-documented module with good practices.
"""

from typing import List, Optional


def calculate_average(numbers: List[float]) -> Optional[float]:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The average value, or None if the list is empty.

    Examples:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
        >>> calculate_average([])
        None
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


class DataProcessor:
    """
    A class for processing data with various transformations.

    Attributes:
        data: The data to be processed.
        processed: Whether the data has been processed.
    """

    def __init__(self, data: List[float]) -> None:
        """Initialize the DataProcessor with data."""
        self.data = data
        self.processed = False

    def normalize(self) -> List[float]:
        """
        Normalize data to range [0, 1].

        Returns:
            List of normalized values.
        """
        if not self.data:
            return []

        min_val = min(self.data)
        max_val = max(self.data)

        if min_val == max_val:
            return [0.5] * len(self.data)

        return [(x - min_val) / (max_val - min_val) for x in self.data]

    def process(self) -> None:
        """Mark data as processed."""
        self.processed = True
'''

        (temp_path / "good_module.py").write_text(good_code)
        print("   ✓ Created good_module.py (well-documented)")

        # Code with some issues
        needs_work = '''
# No module docstring

def process(x):
    # Missing type hints, short docstring
    """Process x."""
    result = []
    for i in range(len(x)):
        if x[i] > 0:
            result.append(x[i] * 2)
    return result

class Handler:
    # Missing class docstring
    def handle(self, data):
        # Missing method docstring
        try:
            return self.internal_process(data)
        except:  # Bare except
            return None

    def internal_process(self, data):
        # Long method with complexity
        if data is None:
            return None
        elif isinstance(data, list):
            if len(data) == 0:
                return []
            elif len(data) == 1:
                return data[0]
            else:
                return sum(data)
        elif isinstance(data, dict):
            return list(data.values())
        else:
            return data
'''

        (temp_path / "needs_improvement.py").write_text(needs_work)
        print("   ✓ Created needs_improvement.py (has issues)")

        # 2. Run analysis
        print("\n2️⃣ Analyzing code quality...")
        checker = CodeChecker()
        report = checker.analyze(str(temp_path))

        # 3. Display metrics
        print("\n3️⃣ Code Metrics:")
        metrics = report.get("metrics", {})

        print(f"   📊 Total files: {metrics.get('total_files', 0)}")
        print(f"   📝 Total lines: {metrics.get('total_lines', 0)}")
        print(f"   🔧 Functions: {metrics.get('total_functions', 0)}")
        print(f"   📦 Classes: {metrics.get('total_classes', 0)}")
        print(f"   📏 Avg function length: {metrics.get('avg_function_length', 0):.1f} lines")
        print(f"   📚 Docstring coverage: {metrics.get('docstring_coverage', 0):.1f}%")
        print(f"   ⭐ Maintainability: {metrics.get('maintainability_score', 0)}/100")

        # 4. Display issues
        print("\n4️⃣ Issues Found:")
        issues = report.get("issues", [])

        if not issues:
            print("   ✓ No issues found!")
        else:
            issue_types = {}
            for issue in issues:
                issue_type = issue.get("type", "unknown")
                issue_types[issue_type] = issue_types.get(issue_type, 0) + 1

            for issue_type, count in sorted(issue_types.items()):
                print(f"   • {issue_type}: {count} occurrence(s)")

            # Show first few issues
            print("\n   First 3 issues:")
            for issue in issues[:3]:
                print(f"   └─ [{issue.get('type')}] {issue.get('message', 'No message')}")
                if issue.get("file"):
                    print(f"      in {Path(issue['file']).name}:{issue.get('line', '?')}")

        # 5. Summary
        print("\n5️⃣ Summary:")
        summary = report.get("summary", {})
        print(f"   Total issues: {summary.get('total_issues', 0)}")
        print(f"   Warnings: {summary.get('warnings', 0)}")
        print(f"   Errors: {summary.get('errors', 0)}")

    # Summary
    print("\n" + "=" * 55)
    print("✅ Code quality analysis demonstration complete!")
    print("\n💡 Tip: Use 'devtools check-quality' to analyze your own code:")
    print("   devtools check-quality ./src --format json --output report.json")


if __name__ == "__main__":
    demonstrate_code_checker()

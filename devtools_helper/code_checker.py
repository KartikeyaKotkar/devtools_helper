"""
Code quality checker for analyzing Python code and providing quality reports.
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List


class CodeChecker:
    """Analyzes Python code quality and provides detailed reports."""

    def __init__(self):
        self.issues = []
        self.metrics = {}

    def analyze(self, path: str) -> Dict[str, Any]:
        """
        Analyze code quality for a given path.

        Args:
            path: File or directory path to analyze

        Returns:
            Dictionary containing analysis results
        """
        path_obj = Path(path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Path '{path}' does not exist")

        self.issues = []
        self.metrics = {
            "total_files": 0,
            "total_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "complexity_score": 0,
            "documentation_score": 0,
            "maintainability_score": 0,
        }

        if path_obj.is_file():
            if path_obj.suffix == ".py":
                self._analyze_file(path_obj)
        else:
            self._analyze_directory(path_obj)

        return self._generate_report()

    def _analyze_directory(self, directory: Path):
        """Analyze all Python files in a directory."""
        python_files = list(directory.rglob("*.py"))

        for file_path in python_files:
            if not self._should_skip_file(file_path):
                self._analyze_file(file_path)

    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content, filename=str(file_path))

            # Update metrics
            self.metrics["total_files"] += 1
            self.metrics["total_lines"] += len(content.splitlines())

            # Analyze the AST
            analyzer = ASTAnalyzer(file_path)
            analyzer.visit(tree)

            # Collect results
            self.issues.extend(analyzer.issues)
            self.metrics["total_functions"] += analyzer.function_count
            self.metrics["total_classes"] += analyzer.class_count

            # Check specific quality aspects
            self._check_line_length(content, file_path)
            self._check_imports(tree, file_path)
            self._check_naming_conventions(tree, file_path)
            self._check_documentation(tree, file_path)

        except Exception as e:
            self.issues.append(
                {
                    "type": "syntax_error",
                    "file": str(file_path),
                    "line": 0,
                    "message": f"Failed to parse file: {str(e)}",
                    "severity": "error",
                }
            )

    def _check_line_length(self, content: str, file_path: Path):
        max_length = 88
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                self.issues.append(
                    {
                        "type": "line_too_long",
                        "file": str(file_path),
                        "line": i,
                        "message": f"Line too long ({len(line)} > {max_length} characters)",
                        "severity": "warning",
                    }
                )

    def _check_imports(self, tree: ast.AST, file_path: Path):
        """Check import organization and unused imports."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(
                    {
                        "line": node.lineno,
                        "type": type(node).__name__,
                        "module": getattr(node, "module", None),
                        "names": [alias.name for alias in node.names],
                    }
                )

        # Check if imports are at the top
        first_import_line = min([imp["line"] for imp in imports]) if imports else 0

        for node in ast.walk(tree):
            if (
                isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Assign))
                and hasattr(node, "lineno")
                and node.lineno < first_import_line
            ):
                self.issues.append(
                    {
                        "type": "import_not_at_top",
                        "file": str(file_path),
                        "line": first_import_line,
                        "message": "Imports should be at the top of the file",
                        "severity": "warning",
                    }
                )
                break

    def _check_naming_conventions(self, tree: ast.AST, file_path: Path):
        """Check Python naming conventions."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
                    self.issues.append(
                        {
                            "type": "naming_convention",
                            "file": str(file_path),
                            "line": node.lineno,
                            "message": f"Function name '{node.name}' should be snake_case",
                            "severity": "info",
                        }
                    )

            elif isinstance(node, ast.ClassDef):
                if not re.match(r"^[A-Z][a-zA-Z0-9]*$", node.name):
                    self.issues.append(
                        {
                            "type": "naming_convention",
                            "file": str(file_path),
                            "line": node.lineno,
                            "message": f"Class name '{node.name}' should be PascalCase",
                            "severity": "info",
                        }
                    )

            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if node.id.isupper() and len(node.id) > 1 and "_" not in node.id:
                    # Constant should have underscores
                    pass

    def _check_documentation(self, tree: ast.AST, file_path: Path):
        """Check for documentation strings."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    self.issues.append(
                        {
                            "type": "missing_docstring",
                            "file": str(file_path),
                            "line": node.lineno,
                            "message": f"{type(node).__name__} '{node.name}' is missing a docstring",
                            "severity": "info",
                        }
                    )

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped from analysis."""
        skip_patterns = [
            "__pycache__",
            ".git",
            "venv",
            "env",
            ".venv",
            "node_modules",
            ".pytest_cache",
        ]

        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _calculate_complexity_score(self) -> float:
        """Calculate overall complexity score."""
        if self.metrics["total_functions"] == 0:
            return 100.0

        # Simple complexity based on functions per file ratio
        avg_functions_per_file = self.metrics["total_functions"] / max(
            self.metrics["total_files"], 1
        )

        if avg_functions_per_file <= 5:
            return 100.0
        elif avg_functions_per_file <= 10:
            return 80.0
        elif avg_functions_per_file <= 20:
            return 60.0
        else:
            return 40.0

    def _calculate_documentation_score(self) -> float:
        """Calculate documentation score."""
        missing_docstrings = len(
            [issue for issue in self.issues if issue["type"] == "missing_docstring"]
        )

        total_documentable = (
            self.metrics["total_functions"] + self.metrics["total_classes"]
        )

        if total_documentable == 0:
            return 100.0

        documented = total_documentable - missing_docstrings
        return (documented / total_documentable) * 100

    def _calculate_maintainability_score(self) -> float:
        """Calculate overall maintainability score."""
        error_count = len([i for i in self.issues if i["severity"] == "error"])
        warning_count = len([i for i in self.issues if i["severity"] == "warning"])

        # Base score
        score = 100.0

        # Deduct for issues
        score -= error_count * 20
        score -= warning_count * 5

        return max(0.0, score)

    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        # Calculate scores
        self.metrics["complexity_score"] = self._calculate_complexity_score()
        self.metrics["documentation_score"] = self._calculate_documentation_score()
        self.metrics["maintainability_score"] = self._calculate_maintainability_score()

        # Group issues by type
        issues_by_type = {}
        for issue in self.issues:
            issue_type = issue["type"]
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        # Generate summary
        summary = {
            "total_issues": len(self.issues),
            "errors": len([i for i in self.issues if i["severity"] == "error"]),
            "warnings": len([i for i in self.issues if i["severity"] == "warning"]),
            "info": len([i for i in self.issues if i["severity"] == "info"]),
        }

        return {
            "summary": summary,
            "metrics": self.metrics,
            "issues": self.issues,
            "issues_by_type": issues_by_type,
            "recommendations": self._get_recommendations(),
        }

    def _get_recommendations(self) -> List[str]:
        """Get recommendations based on analysis."""
        recommendations = []

        if self.metrics["documentation_score"] < 70:
            recommendations.append(
                "Add docstrings to functions and classes to improve documentation score"
            )

        if self.metrics["maintainability_score"] < 80:
            recommendations.append(
                "Address code quality issues to improve maintainability"
            )

        line_length_issues = [i for i in self.issues if i["type"] == "line_too_long"]
        if len(line_length_issues) > 5:
            recommendations.append(
                "Consider using a code formatter like Black to fix line length issues"
            )

        naming_issues = [i for i in self.issues if i["type"] == "naming_convention"]
        if len(naming_issues) > 3:
            recommendations.append(
                "Follow Python naming conventions (snake_case for functions, PascalCase for classes)"
            )

        return recommendations

    def print_report(self, report: Dict[str, Any]):
        """Print a formatted report to console."""
        print("🔍 Code Quality Analysis Report")
        print("=" * 40)

        # Summary
        summary = report["summary"]
        print(f"\n📊 Summary:")
        print(f"   Total Issues: {summary['total_issues']}")
        print(f"   Errors: {summary['errors']}")
        print(f"   Warnings: {summary['warnings']}")
        print(f"   Info: {summary['info']}")

        # Metrics
        metrics = report["metrics"]
        print(f"\n📈 Metrics:")
        print(f"   Files Analyzed: {metrics['total_files']}")
        print(f"   Total Lines: {metrics['total_lines']}")
        print(f"   Functions: {metrics['total_functions']}")
        print(f"   Classes: {metrics['total_classes']}")

        # Scores
        print(f"\n🎯 Scores:")
        print(f"   Complexity: {metrics['complexity_score']:.1f}/100")
        print(f"   Documentation: {metrics['documentation_score']:.1f}/100")
        print(f"   Maintainability: {metrics['maintainability_score']:.1f}/100")

        # Top issues
        if report["issues"]:
            print(f"\n⚠️  Top Issues:")
            for issue in report["issues"][:5]:
                severity_icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}
                icon = severity_icon.get(issue["severity"], "•")
                print(f"   {icon} {issue['file']}:{issue['line']} - {issue['message']}")

        # Recommendations
        if report["recommendations"]:
            print(f"\n💡 Recommendations:")
            for rec in report["recommendations"]:
                print(f"   • {rec}")


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing Python code structure."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.issues = []
        self.function_count = 0
        self.class_count = 0
        self.complexity = 0

    def visit_FunctionDef(self, node):
        """Visit function definitions."""
        self.function_count += 1

        # Check function length
        if hasattr(node, "end_lineno") and node.end_lineno:
            func_length = node.end_lineno - node.lineno
            if func_length > 50:
                self.issues.append(
                    {
                        "type": "function_too_long",
                        "file": str(self.file_path),
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is too long ({func_length} lines)",
                        "severity": "warning",
                    }
                )

        # Check parameter count
        if len(node.args.args) > 5:
            self.issues.append(
                {
                    "type": "too_many_parameters",
                    "file": str(self.file_path),
                    "line": node.lineno,
                    "message": f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                    "severity": "warning",
                }
            )

        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visit class definitions."""
        self.class_count += 1

        # Check class length
        if hasattr(node, "end_lineno") and node.end_lineno:
            class_length = node.end_lineno - node.lineno
            if class_length > 200:
                self.issues.append(
                    {
                        "type": "class_too_long",
                        "file": str(self.file_path),
                        "line": node.lineno,
                        "message": f"Class '{node.name}' is too long ({class_length} lines)",
                        "severity": "warning",
                    }
                )

        self.generic_visit(node)

    def visit_If(self, node):
        """Visit if statements for complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        """Visit for loops for complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """Visit while loops for complexity."""
        self.complexity += 1
        self.generic_visit(node)

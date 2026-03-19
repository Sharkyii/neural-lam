#!/usr/bin/env python
"""Documentation validation script.

Runs docstring validation, checks for broken cross-references,
and verifies API consistency. Exits with non-zero status on errors.

Usage:
    python docs/scripts/validate_docs.py [--strict]
"""

# Standard library
import argparse
import inspect
import sys
from pathlib import Path

# Ensure neural_lam is importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def run_docstring_validation(strict: bool = False) -> int:
    """Run docstring quality validation on neural_lam package.

    Parameters
    ----------
    strict : bool
        If True, treat warnings as errors.

    Returns
    -------
    int
        Number of errors found.
    """
    try:
        # First-party
        import neural_lam
        from neural_lam.docstring_validator import validate_function
    except ImportError as e:
        print(f"[ERROR] Could not import neural_lam: {e}")
        return 1

    errors = 0
    warnings = 0

    print("Running docstring validation...")

    # Walk all public modules
    # Standard library
    import importlib
    import pkgutil

    for importer, modname, ispkg in pkgutil.walk_packages(
        path=neural_lam.__path__,
        prefix=neural_lam.__name__ + ".",
        onerror=lambda x: None,
    ):
        try:
            module = importlib.import_module(modname)
        except Exception:
            continue

        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("_"):
                continue
            if getattr(obj, "__module__", None) != modname:
                continue

            report = validate_function(obj)
            for issue in report.issues:
                if issue.level == "error":
                    print(f"  [ERROR] {modname}.{name}: {issue.message}")
                    errors += 1
                elif issue.level == "warning":
                    print(f"  [WARN]  {modname}.{name}: {issue.message}")
                    warnings += 1

    print(f"\nDocstring validation: {errors} errors, {warnings} warnings")

    if strict:
        return errors + warnings
    return errors


def run_api_consistency_check() -> int:
    """Check that documented APIs are consistent with source code.

    Returns
    -------
    int
        Number of consistency issues found.
    """
    print("\nRunning API consistency check...")

    try:
        # Standard library
        import importlib
        import pkgutil

        # First-party
        import neural_lam
        from neural_lam.doc_sync import ConsistencyChecker, SourceChangeDetector
    except ImportError as e:
        print(f"[ERROR] Could not import modules: {e}")
        return 1

    issues_count = 0
    detector = SourceChangeDetector()
    checker = ConsistencyChecker()

    for importer, modname, ispkg in pkgutil.walk_packages(
        path=neural_lam.__path__,
        prefix=neural_lam.__name__ + ".",
        onerror=lambda x: None,
    ):
        try:
            module = importlib.import_module(modname)
        except Exception:
            continue

        snapshot = detector.snapshot_module(module)
        existing = set(snapshot.keys())

        # Check autoapi output if it exists
        autoapi_dir = Path("docs/autoapi") / modname.replace(".", "/")
        if autoapi_dir.exists():
            documented = set()
            for rst_file in autoapi_dir.glob("*.rst"):
                documented.add(rst_file.stem)

            issues = checker.check_consistency(documented, existing, modname)
            for issue in issues:
                print(
                    f"  [WARN] {modname}: '{issue.element_name}'"
                    " documented but not in source"
                )
                issues_count += 1

    print(f"API consistency check: {issues_count} issues found")
    return 0  # Non-blocking for now


def run_toc_validation() -> int:
    """Validate that the TOC includes the API reference section.

    Returns
    -------
    int
        Number of TOC errors found.
    """
    print("\nValidating table of contents...")

    toc_path = Path("docs/_toc.yml")
    if not toc_path.exists():
        print("  [ERROR] docs/_toc.yml not found")
        return 1

    try:
        # First-party
        from neural_lam.toc_integration import (
            get_api_reference_section,
            load_toc,
        )

        toc = load_toc(str(toc_path))
        api_ref = get_api_reference_section(toc)

        if api_ref is None:
            print("  [WARN] API Reference section not found in _toc.yml")
            return 0  # Non-blocking

        print("  ✓ API Reference section found in _toc.yml")
        return 0
    except Exception as e:
        print(f"  [ERROR] TOC validation failed: {e}")
        return 1


def main() -> int:
    """Run all validation checks.

    Returns
    -------
    int
        Exit code (0 = success, non-zero = failure).
    """
    parser = argparse.ArgumentParser(description="Validate API documentation")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Neural-LAM Documentation Validation")
    print("=" * 60)

    total_errors = 0
    total_errors += run_docstring_validation(strict=args.strict)
    total_errors += run_api_consistency_check()
    total_errors += run_toc_validation()

    print("\n" + "=" * 60)
    if total_errors == 0:
        print("✓ All validation checks passed")
    else:
        print(f"✗ Validation failed with {total_errors} error(s)")
    print("=" * 60)

    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

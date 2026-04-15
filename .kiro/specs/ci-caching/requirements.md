# Requirements Document: CI Caching

## Introduction

This document specifies requirements for implementing dependency caching in GitHub Actions CI workflows to reduce build times and PyPI load. The project currently reinstalls all dependencies from scratch on every CI run across two workflows (install-and-test.yml and pre-commit.yml), resulting in unnecessary delays and resource usage.

The caching implementation must handle the project's unique constraints: a matrix testing approach with both pip and uv package managers, CPU and GPU PyTorch variants, and a workaround for PyTorch installation that prevents using standard lock files.

## Glossary

- **CI_System**: The GitHub Actions continuous integration system
- **Package_Manager**: Either pip or uv used to install Python dependencies
- **Cache_Layer**: A storage mechanism for reusing downloaded or installed dependencies
- **Cache_Key**: A unique identifier for cached data based on dependency specifications
- **Virtual_Environment**: An isolated Python environment containing installed packages (.venv)
- **Package_Download_Cache**: Storage for downloaded package files from PyPI
- **Lock_File**: A file specifying exact dependency versions (uv.lock)
- **PyTorch_Variant**: Either CPU or GPU version of PyTorch with different installation sources
- **Test_Data_Cache**: Existing cache for test dataset files (already implemented)
- **Workflow**: A GitHub Actions YAML file defining CI jobs and steps

## Requirements

### Requirement 1: Two-Layer Caching Architecture

**User Story:** As a developer, I want CI builds to reuse both downloaded packages and installed environments, so that builds complete faster when dependencies haven't changed.

#### Acceptance Criteria

1. WHEN dependencies are unchanged, THE CI_System SHALL reuse the Package_Download_Cache to avoid re-downloading from PyPI
2. WHEN dependencies are unchanged, THE CI_System SHALL reuse the Virtual_Environment to avoid reinstalling packages
3. WHEN dependencies change, THE CI_System SHALL invalidate both cache layers and rebuild from scratch
4. THE CI_System SHALL maintain separate caches for Package_Download_Cache and Virtual_Environment
5. THE CI_System SHALL apply both cache layers to all package manager variants (pip and uv)

### Requirement 2: Pip Caching Implementation

**User Story:** As a developer using pip, I want pip's download cache to be preserved across CI runs, so that package downloads are reused when possible.

#### Acceptance Criteria

1. WHEN using pip as the Package_Manager, THE CI_System SHALL enable pip caching through actions/setup-python@v5
2. THE CI_System SHALL configure pip caching using the cache parameter set to 'pip'
3. WHEN pip cache is enabled, THE CI_System SHALL store downloaded packages between CI runs
4. THE CI_System SHALL restore pip cache before installing dependencies
5. THE CI_System SHALL apply pip caching to both CPU and GPU test jobs

### Requirement 3: UV Package Download Caching

**User Story:** As a developer using uv, I want uv's package download cache to be preserved across CI runs, so that package downloads are reused when possible.

#### Acceptance Criteria

1. WHEN using uv as the Package_Manager, THE CI_System SHALL enable uv caching through astral-sh/setup-uv@v1
2. THE CI_System SHALL configure uv caching using the enable-cache parameter set to true
3. WHEN uv cache is enabled, THE CI_System SHALL store downloaded packages between CI runs
4. THE CI_System SHALL restore uv cache before installing dependencies
5. THE CI_System SHALL apply uv caching to both CPU and GPU test jobs

### Requirement 4: UV Virtual Environment Caching

**User Story:** As a developer using uv, I want the .venv directory to be cached across CI runs, so that package installation is skipped when dependencies haven't changed.

#### Acceptance Criteria

1. WHEN using uv as the Package_Manager, THE CI_System SHALL cache the .venv directory using actions/cache@v4
2. THE CI_System SHALL generate cache keys based on the hash of uv.lock
3. WHEN uv.lock is unchanged, THE CI_System SHALL restore the cached .venv directory
4. WHEN uv.lock changes, THE CI_System SHALL invalidate the .venv cache and rebuild
5. THE CI_System SHALL include runner.os in the cache key to separate platform-specific builds
6. THE CI_System SHALL apply .venv caching to both CPU and GPU test jobs

### Requirement 5: Cache Key Strategy

**User Story:** As a developer, I want cache invalidation to be based on actual dependency changes, so that builds are reproducible and caches are used correctly.

#### Acceptance Criteria

1. THE CI_System SHALL use uv.lock as the primary cache key input for uv-based caching
2. THE CI_System SHALL NOT use pyproject.toml as a cache key input
3. THE CI_System SHALL include runner.os in all cache keys to separate platform-specific dependencies
4. WHEN uv.lock does not exist, THE CI_System SHALL generate it before computing cache keys
5. THE CI_System SHALL use separate cache keys for CPU and GPU PyTorch variants

### Requirement 6: PyTorch Installation Compatibility

**User Story:** As a developer, I want caching to work with the current PyTorch installation workaround, so that both CPU and GPU variants can be tested correctly.

#### Acceptance Criteria

1. THE CI_System SHALL preserve the existing PyTorch installation approach (install torch first, then neural-lam)
2. WHEN caching is enabled, THE CI_System SHALL correctly handle different PyTorch index URLs (cpu vs cu128)
3. THE CI_System SHALL invalidate caches when PyTorch variant changes
4. THE CI_System SHALL document the dependency on resolving the PyTorch installation workaround
5. WHEN the PyTorch workaround is resolved in the future, THE CI_System SHALL allow migration to lock file-based caching

### Requirement 7: Install-and-Test Workflow Caching

**User Story:** As a developer, I want the main test workflow to use caching, so that test runs complete faster.

#### Acceptance Criteria

1. THE CI_System SHALL apply caching to all jobs in install-and-test.yml
2. WHEN using pip, THE CI_System SHALL enable pip download caching
3. WHEN using uv, THE CI_System SHALL enable both uv download caching and .venv caching
4. THE CI_System SHALL preserve existing CPU/GPU matrix testing functionality
5. THE CI_System SHALL preserve existing pip/uv matrix testing functionality
6. THE CI_System SHALL preserve existing Test_Data_Cache functionality

### Requirement 8: Pre-commit Workflow Caching

**User Story:** As a developer, I want the linting workflow to use caching, so that pre-commit checks complete faster.

#### Acceptance Criteria

1. THE CI_System SHALL apply caching to all Python version jobs in pre-commit.yml
2. THE CI_System SHALL enable pip download caching for pre-commit dependencies
3. THE CI_System SHALL preserve existing Python version matrix (3.10-3.14)
4. THE CI_System SHALL preserve existing pre-commit hook functionality
5. WHEN pre-commit dependencies are unchanged, THE CI_System SHALL reuse cached packages

### Requirement 9: Cache Performance and Correctness

**User Story:** As a developer, I want caching to improve CI performance without breaking builds, so that I can trust the CI results.

#### Acceptance Criteria

1. WHEN caches are hit, THE CI_System SHALL complete dependency installation faster than without caching
2. WHEN caches are missed, THE CI_System SHALL complete builds successfully by installing from scratch
3. THE CI_System SHALL ensure all existing tests pass with caching enabled
4. THE CI_System SHALL correctly invalidate caches when dependencies change
5. THE CI_System SHALL not cause test failures due to stale cached dependencies

### Requirement 10: Documentation and Maintainability

**User Story:** As a developer, I want to understand how CI caching works, so that I can troubleshoot issues and maintain the system.

#### Acceptance Criteria

1. THE CI_System SHALL include inline comments in workflow files explaining the caching strategy
2. THE CI_System SHALL document the two-layer caching approach in workflow comments
3. THE CI_System SHALL document cache key generation logic in workflow comments
4. THE CI_System SHALL document the relationship between caching and the PyTorch installation workaround
5. THE CI_System SHALL document how to debug cache-related issues

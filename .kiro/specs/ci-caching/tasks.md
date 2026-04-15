# Implementation Plan: CI Caching

## Overview

This implementation plan adds two-layer caching to GitHub Actions workflows: package download caching (via setup-python and setup-uv actions) and virtual environment caching (via actions/cache). The approach minimizes changes to existing workflows while maximizing performance improvements.

## Tasks

- [x] 1. Add pip caching to install-and-test.yml workflow
  - Modify setup-python step to enable pip caching with `cache: 'pip'`
  - Apply to both CPU and GPU matrix jobs
  - Add inline comments explaining pip caching strategy
  - _Requirements: 2.1, 2.2, 2.4, 2.5, 7.2_

- [ ]* 1.1 Write property test for pip cache reuse
  - **Property 1: Package Download Cache Reuse**
  - **Validates: Requirements 1.1, 2.3**

- [x] 2. Add uv download caching to install-and-test.yml workflow
  - Modify setup-uv step to enable caching with `enable-cache: true`
  - Apply to both CPU and GPU matrix jobs
  - Add inline comments explaining uv download caching
  - _Requirements: 3.1, 3.2, 3.4, 3.5, 7.3_

- [ ]* 2.1 Write property test for uv download cache reuse
  - **Property 1: Package Download Cache Reuse**
  - **Validates: Requirements 1.1, 3.3**

- [x] 3. Add .venv caching to install-and-test.yml workflow
  - Add actions/cache@v4 step before uv installation
  - Configure cache path as `.venv`
  - Generate cache key: `uv-venv-${{ runner.os }}-${{ matrix.device }}-${{ hashFiles('uv.lock') }}`
  - Add restore-keys for fallback matching
  - Apply to both CPU and GPU uv matrix jobs
  - Add inline comments explaining .venv caching strategy and cache key format
  - _Requirements: 4.1, 4.2, 4.5, 4.6, 5.1, 5.3, 5.5_

- [ ]* 3.1 Write property test for .venv cache reuse
  - **Property 2: Virtual Environment Cache Reuse**
  - **Validates: Requirements 1.2, 4.3**

- [ ]* 3.2 Write property test for cache invalidation
  - **Property 3: Cache Invalidation on Dependency Change**
  - **Validates: Requirements 1.3, 4.4, 9.4**

- [x] 4. Handle missing uv.lock file
  - Add step to generate uv.lock if it doesn't exist
  - Use `uv lock` command before cache key computation
  - Add conditional check for lock file existence
  - Add inline comments explaining lock file generation
  - _Requirements: 5.4_

- [ ]* 4.1 Write property test for lock file generation
  - **Property 5: Lock File Generation**
  - **Validates: Requirements 5.4**

- [x] 5. Ensure PyTorch variant compatibility
  - Verify cache keys include device type (cpu/gpu)
  - Verify existing PyTorch installation order preserved
  - Verify different index URLs don't conflict
  - Add inline comments documenting PyTorch workaround relationship
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ]* 5.1 Write property test for PyTorch variant caching
  - **Property 6: PyTorch Variant Compatibility**
  - **Validates: Requirements 6.2**

- [x] 6. Add pip caching to pre-commit.yml workflow
  - Modify setup-python step to enable pip caching with `cache: 'pip'`
  - Apply to all Python version matrix jobs (3.10-3.14)
  - Add inline comments explaining caching strategy
  - _Requirements: 8.1, 8.2, 8.3_

- [ ]* 6.1 Write property test for pre-commit cache reuse
  - **Property 1: Package Download Cache Reuse**
  - **Validates: Requirements 8.5**

- [x] 7. Add cache key validation
  - Verify pyproject.toml is NOT in cache keys
  - Verify runner.os is in all cache keys
  - Verify device type is in uv .venv cache keys
  - _Requirements: 5.2, 5.3, 5.5_

- [ ]* 7.1 Write unit tests for cache key format
  - Test cache key includes runner.os
  - Test cache key includes device type
  - Test cache key excludes pyproject.toml
  - Test cache key includes uv.lock hash

- [x] 8. Add comprehensive documentation comments
  - Document two-layer caching approach in workflow files
  - Document cache key generation logic
  - Document PyTorch workaround relationship
  - Document how to debug cache issues
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 9. Checkpoint - Verify workflows are valid
  - Run `actionlint` on modified workflow files
  - Verify YAML syntax is correct
  - Ensure all tests pass, ask the user if questions arise

- [ ]* 10. Integration testing
  - Run full test suite with caching enabled
  - Verify all existing tests pass
  - Verify no test failures introduced by caching
  - _Requirements: 7.4, 7.5, 7.6, 8.4, 9.3_

- [ ]* 10.1 Write property test for existing functionality preservation
  - **Property 10: Existing Functionality Preservation**
  - **Validates: Requirements 7.4, 7.5, 7.6, 8.4, 9.3**

- [ ]* 10.2 Write property test for cache miss resilience
  - **Property 8: Cache Miss Resilience**
  - **Validates: Requirements 9.2**

- [ ]* 10.3 Write property test for no stale dependencies
  - **Property 9: No Stale Dependency Failures**
  - **Validates: Requirements 9.5**

- [ ]* 11. Performance validation
  - Measure baseline installation time without caching
  - Measure installation time with cache hit
  - Calculate and report performance improvement
  - Verify improvement meets expected benchmarks (30-90% faster)
  - _Requirements: 9.1_

- [ ]* 11.1 Write property test for cache hit performance
  - **Property 7: Cache Hit Performance Improvement**
  - **Validates: Requirements 9.1**

- [x] 12. Final checkpoint - Verify all workflows pass
  - Run install-and-test.yml workflow on test branch
  - Run pre-commit.yml workflow on test branch
  - Verify cache hits logged in workflow output
  - Verify all tests pass
  - Ensure all tests pass, ask the user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties across workflow runs
- Unit tests validate specific YAML configuration and cache key formats
- The implementation preserves all existing functionality while adding caching layers
- Cache keys are designed to prevent conflicts between platforms and PyTorch variants

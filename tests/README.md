# Testing Guide - JobMetrics Pro

## Overview

This directory contains the test suite for JobMetrics Pro, ensuring code quality and reliability.

---

## Test Structure

```
tests/
├── unit/                    # Unit tests (individual functions/classes)
│   ├── test_analytics.py    # Tests for SaaSAnalytics
│   └── test_ai_query.py     # Tests for AIQueryEngine (future)
│
├── integration/             # Integration tests (component interactions)
│   └── test_dashboard.py    # Tests for dashboard workflows (future)
│
└── README.md               # This file
```

---

## Running Tests

### Prerequisites

Install testing dependencies:
```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
# From project root
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/unit/test_analytics.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

This generates a coverage report in `htmlcov/index.html`

---

## Writing Tests

### Unit Test Example

```python
import pytest
from src.core import SaaSAnalytics

class TestMetricCalculation:
    @pytest.fixture
    def analytics(self):
        return SaaSAnalytics()

    def test_mrr_is_positive(self, analytics):
        mrr = analytics.get_current_mrr()
        assert mrr > 0
```

### Best Practices

1. **One concept per test**: Each test should verify one thing
2. **Descriptive names**: `test_mrr_is_positive` not `test_1`
3. **Arrange-Act-Assert**: Setup, execute, verify
4. **Use fixtures**: Share setup code with `@pytest.fixture`
5. **Test edge cases**: Empty data, zero values, boundary conditions

---

## Test Coverage Goals

- **Core modules**: 80%+ coverage
- **Critical paths**: 100% coverage
- **UI components**: Visual testing (manual for now)

---

## Current Status

✅ **Unit Tests**: Basic structure created
⏳ **Integration Tests**: To be implemented
⏳ **End-to-End Tests**: To be implemented

---

## Future Enhancements

- [ ] Complete unit test coverage for all analytics methods
- [ ] AI query engine tests (mocked API calls)
- [ ] Dashboard rendering tests (Streamlit testing)
- [ ] Performance benchmarks
- [ ] Data validation tests
- [ ] CI/CD integration (GitHub Actions)

---

## CI/CD Integration (Future)

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest tests/ --cov=src
```

---

**Last Updated**: 2025-10-26

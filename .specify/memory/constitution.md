<!--
Sync Impact Report

- Version change: unspecified -> 1.0.0
- Modified principles:
	- PRINCIPLE_1_NAME (placeholder) -> Code Quality (NON-NEGOTIABLE)
	- PRINCIPLE_2_NAME (placeholder) -> Testing Standards (Test-First, Coverage & Automation)
	- PRINCIPLE_3_NAME (placeholder) -> User Experience Consistency (Design System & Accessibility)
	- PRINCIPLE_4_NAME (placeholder) -> Performance & Resource Efficiency
	- PRINCIPLE_5_NAME (placeholder) -> Observability, Versioning & Simplicity
- Added sections: Operational Constraints & Security Requirements; Development Workflow & Quality Gates
- Removed sections: none
- Templates reviewed:
	- .specify/templates/plan-template.md ✅ reviewed (no change required)
	- .specify/templates/spec-template.md ✅ reviewed (no change required)
	- .specify/templates/tasks-template.md ✅ reviewed (no change required)
	- .specify/templates/commands/ ⚠ pending (directory not found)
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): original adoption date unknown — project maintainer must supply
	- Confirm whether repository previously had a constitution version (old version unknown)
-->

# Planner Speckit Constitution

## Core Principles

### Code Quality (NON-NEGOTIABLE)
All production code MUST be readable, maintainable, and provably correct to the
extent practical. Requirements:

- **MUST** pass static analysis and linting configured in repository CI before
	merges to protected branches.
- **MUST** include concise public API documentation for any exported module or
	package and a short usage example for public interfaces.
- **MUST** be reviewed via pull request by at least one maintainer with
	approval required; large or risky changes (complexity score above threshold)
	**MUST** include a short design note describing trade-offs and alternatives.
- **SHOULD** aim for small, focused functions and modules; complexity must be
	justified and tracked in the plan when unavoidable.

Rationale: Maintainable code reduces bugs, accelerates onboarding, and enables
safe refactors.

### Testing Standards (Test-First, Coverage & Automation)
Testing is mandatory and gate-enforced.

- **MUST** provide automated unit tests that cover core logic; integration and
	end-to-end tests are required for cross-component contracts and user journeys.
- **MUST** include test coverage targets (repository default: 80% line coverage
	for core modules) which can be adjusted per-module with documented rationale.
- **MUST** have all tests passing in CI; flaky tests **MUST** be quarantined and
	fixed — flaky tests are not acceptable as a permanent state.
- **MUST** follow test-first practices where practical: write failing tests to
	capture expected behavior before implementation for new features and
	bugfixes.
- **SHOULD** use deterministic test fixtures, dependency injection, and
	lightweight mocks to keep tests fast and reliable.

Rationale: Automated, repeatable tests ensure correctness and prevent regressions.

### User Experience Consistency (Design System & Accessibility)
User-facing behaviors MUST be consistent and accessible.

- **MUST** reuse shared components from the project design system for UI and
	interaction patterns where applicable.
- **MUST** meet WCAG 2.1 AA accessibility standards for all public UIs unless a
	documented exception is approved in governance records.
- **MUST** provide consistent error messaging, internationalization hooks, and
	accessible states for interactive elements.
- **SHOULD** document UX decisions in the feature spec and include a small set
	of acceptance screenshots or interactable examples where relevant.

Rationale: Consistent UX reduces user confusion, decreases support load, and
improves product quality.

### Performance & Resource Efficiency
Performance goals are part of feature acceptance criteria and are testable.

- **MUST** define measurable performance targets (latency, throughput, memory)
	in the plan for any feature where performance is material to user experience.
- **MUST** include profiling data when optimizing hotspots and include
	performance tests in the CI pipeline for features with performance budgets.
- **MUST** enforce reasonable resource limits for services and batch jobs;
	memory and CPU budgets **MUST** be documented in the plan.
- **SHOULD** prefer efficient algorithms and incremental optimizations over
	premature micro-optimizations; trade-offs **MUST** be justified in design
	notes.

Rationale: Explicit performance criteria keep the product responsive and
cost-effective at scale.

### Observability, Versioning & Simplicity
Systems MUST be observable, follow semantic versioning, and prefer simplicity.

- **MUST** emit structured logs, expose key metrics, and provide distributed
	traces for cross-service flows where applicable.
- **MUST** follow semantic versioning (MAJOR.MINOR.PATCH) for public packages
	and clearly document deprecation and migration plans for breaking changes.
- **MUST** include a deprecation period for public APIs (minimum 1 minor
	release) unless emergency removal is approved by governance.
- **SHOULD** default to the simplest design that meets requirements and avoid
	unnecessary subsystems; complexity requires explicit justification.

Rationale: Observability enables rapid diagnosis; versioning and simplicity
reduce user friction and maintenance burden.

## Operational Constraints & Security Requirements

- **MUST** run regular dependency vulnerability scans and address critical
	findings within SLA defined by the security team.
- **MUST** avoid committing secrets to the repo; secrets management policies
	and tooling **MUST** be followed for CI and deployments.
- **MUST** document supported runtime versions; unsupported runtimes **MUST**
	be flagged and a migration plan provided.

Rationale: Operational discipline protects users and the project from avoidable
risks.

## Development Workflow & Quality Gates

- **MUST** enforce CI checks on all pull requests: lint, static analysis, unit
	tests, and any feature-level governance gates defined in the plan.
- **MUST** require at least one approving review from a maintainer for merges to
	protected branches; release merges **MUST** include changelogs and migration
	notes when applicable.
- **MUST** include a short checklist in each PR referencing relevant principles
	(quality, tests, UX, performance, observability).

Rationale: Consistent workflows reduce human error and ensure standards are met.

## Governance

Amendments, versioning, and compliance:

- Amendments to this constitution **MUST** be proposed in a PR targeting the
	`.specify/memory/constitution.md` file and include a migration or compliance
	plan for affected repositories or templates.
- A simple majority of project maintainers is required to ratify non-breaking
	amendments; breaking changes to principles (removals or redefinitions) **MUST**
	use a MAJOR version bump and require a documented migration path and a 2/3
	maintainer approval.
- The constitution **MUST** include the following fields and formats: `Version`
	(semantic), `Ratified` (ISO YYYY-MM-DD or TODO marker), `Last Amended` (ISO
	YYYY-MM-DD).
- Compliance reviews **SHOULD** be performed as part of release retrospectives
	and during periodic audits; repositories **SHOULD** surface Constitution Check
	results in plan.md and tasks.md as applicable.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2026-01-09

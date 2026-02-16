# Neural Restoration PRD (V2 & V5)

## HR Eng

| Neural Restoration PRD |  | Fix and optimize the V2 Neural Map and V5 Neural Constellation modules. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick | **Status**: Draft **Created**: 2026-02-14 | **Context**: Restoration of non-functional viz modules. |

## Introduction

V2 (Cytoscape) and V5 (Force-Graph Canvas) are currently suboptimal or broken due to color logic mismatches and type errors in data handling.

## Problem Statement

- **V2**: `blendColors` fails on HSL strings returned by the semantic color generator.
- **V5**: Color indexing (`group % COLORS.length`) fails when `group` is a string (e.g., "MATCH").

## Objective & Scope

**Objective**: Ensure V2 and V5 render correctly with full interactivity and correct cluster coloring.

### In-scope
- Refactor `blendColors` in V2.
- Implement a string-to-index hash for V5 colors.
- Verify data loading in both modules.

## Product Requirements

### Functional Requirements
- **P0**: V2 must display cluster-blended edges without crashing.
- **P0**: V5 must assign distinct colors to string-based groups.
- **P1**: Both modules must use the local library paths.

## Business Benefits
- Complete visualization suite coverage.
- Better topological and abstract data insights.

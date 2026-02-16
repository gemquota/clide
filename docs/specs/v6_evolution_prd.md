# V6 Integrated Control Evolution PRD

## HR Eng

| V6 Evolution PRD |  | Transforming V6 from a static dashboard into a real-time system command center with VNC and Audio telemetry. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick | **Status**: Draft **Created**: 2026-02-14 | **Context**: Enhancement of V6 module with advanced telemetry. |

## Introduction

V6 is the "Integrated Control" module. Currently, it lacks direct system visibility (VNC) and advanced agent telemetry (Audio/VQ tokens).

## Problem Statement

- **Visibility**: Developers cannot see the GUI or terminal of the system being controlled without leaving the dashboard.
- **Telemetry**: Agent "thoughts" are represented only by text, ignoring the rich semantic audio tokens (VQ-06) provided by the new audio engine.
- **Dependency Slop**: Current V6 implementation uses external CDNs for GridStack and other libs.

## Objective & Scope

**Objective**: Upgrade V6 into a true "Command Center".

### In-scope
- Integrate a VNC viewer panel (noVNC).
- Integrate an Audio telemetry panel (VQ-06 visualizer).
- Localize all JS/CSS dependencies.
- Implement 'God Mode' terminal override.

## Product Requirements

### Functional Requirements
- **P0**: noVNC viewer must connect to a local/remote VNC server.
- **P0**: Audio visualizer must map VQ-06 tokens to a spectral display.
- **P1**: GridStack and Cytoscape must be served locally.

## Risks
- VNC latency on Termux/Android.
- High CPU usage for real-time spectral analysis.

# CLIDE Engineering - Master TODO

## 🛠 Active System Tasks
- [x] **Core UI Parity:** Overwrote `clide/serve/ui.py` with the high-fidelity v5.0 logic (Rolling Metrics, Streaks, Color Interpolation).
- [x] **Legend Correction:** Removed the contradictory "`♥️` = Success Streak" definition. `♥️` is now strictly part of the **Health Gradient** (Bad -> Danger).
- [x] **Command Consolidation:** Merged high-similarity tool pairs (e.g., `mockup`/`design`, `find_file`/`locate`) in the theorycrafting report.
- [x] **Deep Ingestion:** Extracted **149 additional unique intents** from historical logs, bringing the theorycrafted total to **805 unique commands**.

## 📋 User-Requested Logic (Restored)
- [x] **UI Refinement:** Refactored panels in `dashboard.py` to use multiple lines for field/value pairs, preventing truncation.
- [x] **Error Legend Expansion:** Integrated historical error probabilities into the `ERR PROB` modal in the dashboard.
- [x] **Finalization Report:** Overhauled `print_finalization_report` in `ui.py` to match the high-fidelity v5.0 style.
- [x] **Audit Pass:** Verified all `docs/` files; heart emoji is now exclusively assigned to the Health Gradient.

## 📊 Neural Parity Status
- **Unique Command Intent:** 795 / ~1000 estimated unique signatures (Consolidated).
- **Shell History Saturation:** 1749 unique historical signatures ingested.
- **Total Kernel Saturation:** 52.78% (Consolidated and categorized).
- [x] Finish the last 2.4% of the merging task and ensure 'General/Misc' is the last category.
- [x] Sector 04 (Executive): Implemented functional logic for `forge evolve`, `forge design`, `forge skill`, `forge persona`, and `forge bench`.

- [ ] Finish the remaining 2.4% of the task. Reorder categories so 'General/Misc' is last. This is related to merging semantically similar tools. (Extracted from: can we finish that last 2.4% a...)

import re
import os

merges = [
    ('mockup', 'design'),
    ('combine', 'batch_process_urls'),
    ('recursive_critique', 'recursive_critique_redesign'),
    ('check', 'moltbot'),
    ('delimiter', 'draw_lines'),
    ('deconstruct', 'describe_project'),
    ('parse_status', 'checker')
]

# Additional merges found by similarity
extra_merges = [
    ('understand_and_document', 'analyze_and_document'),
    ('automate_task', 'automate_agent_building'),
    ('enhance_categorization_and_db', 'enhance_categorization_and_persistence'),
    ('find_file', 'locate'),
    ('rename_folder_and_test_all_features', 'rename_and_test')
]

all_merges = merges + extra_merges + [
    ('retest_scheduling', 'retest_schedule'),
    ('retest_scheduling', 'retest_pruned_periodically'),
    ('retest_scheduling', 'schedule_purgatory_retest'),
    ('retest_scheduling', 'reschedule_purgatory_retest'),
    ('revert', 'revert_util_csv_change'),
    ('revert', 'revert_util_csv'),
    ('monitor_run', 'monitor_proxy_run'),
    ('improve_tui', 'tweak_ui'),
    ('improve_tui', 'improve_interface'),
    ('improve_tui', 'redesign_table_ui'),
    ('improve_tui', 'visual_table_customization'),
    ('visualize_data', 'visualize_blocks'),
    ('visualize_data', 'regenerate_graph'),
    ('resume', 'resume_logic_export'),
    ('resume', 'resume_with_categories'),
    ('resume', 'resume_categorize')
]

def merge_in_file(path):
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    secondary_data = {}
    
    for line in lines:
        found_secondary = False
        for _, secondary in all_merges:
            if f"| `{secondary}` |" in line:
                parts = line.split('|')
                if len(parts) > 3:
                    vals = [p.strip().replace('*', '') for p in parts[2:4]]
                    rec = 1
                    for v in vals:
                        if v.isdigit(): rec = int(v); break
                    secondary_data[secondary] = rec
                found_secondary = True
                break
        if not found_secondary:
            new_lines.append(line)
            
    final_lines = []
    for line in new_lines:
        updated_line = line
        for primary, secondary in all_merges:
            if f"| `{primary}` |" in line and secondary in secondary_data:
                parts = line.split('|')
                for i in [2, 3]:
                    val = parts[i].strip().replace('*', '')
                    if val.isdigit():
                        new_val = int(val) + secondary_data[secondary]
                        if '*' in parts[i]: parts[i] = f" **{new_val}** "
                        else: parts[i] = f" {new_val} "
                        break
                updated_line = '|'.join(parts)
        final_lines.append(updated_line)
        
    with open(path, 'w') as f:
        f.writelines(final_lines)

if __name__ == "__main__":
    merge_in_file('ingestion_logs/theorycrafting_report.md')
    print(f"Merged {len(all_merges)} sets of duplicates.")
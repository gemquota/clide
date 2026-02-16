import json
import csv
import os
import argparse
import random
import time
import math
from collections import Counter
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich.table import Table

def get_data(min_count=1, top_n=100):
    counts = Counter()
    
    csv_path = "ingestion_logs/commands.csv"
    if os.path.exists(csv_path):
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cmd = row.get("Command")
                    occ = row.get("Occurrences")
                    if cmd and occ:
                        counts[cmd] += int(occ)
        except: pass

    json_path = "clide/enriched_logs.json"
    stopwords = {"can", "i", "does", "you", "the", "a", "so", "now", "it", "to", "and", "is", "of", "in", "for", "with", "this", "that", "on", "if", "where", "why", "how", "what", "then", "also", "no", "yes", "maybe", "have", "those", "don't", "let's"}
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
                for entry in logs:
                    if entry.get("clide_metadata", {}).get("category") == "NEW_COMMAND":
                        msg = entry.get("message", "").strip().lower().split()[0]
                        if msg and msg not in stopwords and len(msg) > 1:
                            counts[msg] += 1
        except: pass

    filtered = {k: v for k, v in counts.items() if v >= min_count}
    return Counter(filtered).most_common(top_n)

def get_spectrum_style(ratio):
    """
    Maps command frequency to the Electromagnetic Spectrum.
    High Frequency Usage -> High Energy Waves (Violet/Gamma)
    Low Frequency Usage -> Low Energy Waves (Red/Radio)
    """
    # 20-tier spectral mapping
    spectrum = [
        (0.95, "bold #ff00ff"), # Gamma (White-Magenta)
        (0.85, "bold #af00ff"), # X-Ray (Deep Violet)
        (0.75, "bold #5f00ff"), # Ultraviolet
        (0.65, "bold #0000ff"), # Deep Blue
        (0.55, "#005fff"),      # Royal Blue
        (0.45, "#00afff"),      # Sky Blue
        (0.35, "#00ffff"),      # Cyan
        (0.28, "#00ffaf"),      # Turquoise
        (0.22, "#00ff5f"),      # Spring Green
        (0.18, "#00ff00"),      # Green
        (0.15, "#5fff00"),      # Lime
        (0.12, "#afff00"),      # Chartreuse
        (0.10, "#ffff00"),      # Yellow
        (0.08, "#ffaf00"),      # Gold
        (0.06, "#ff8700"),      # Orange
        (0.04, "#ff5f00"),      # Deep Orange
        (0.03, "#ff0000"),      # Red
        (0.02, "#d70000"),      # Dark Red
        (0.01, "#af0000"),      # Infrared
        (0.00, "#888888")       # Radio (Gray/Background)
    ]
    
    for threshold, style in spectrum:
        if ratio >= threshold:
            return style
    return "#888888"

def make_legend():
    tiers = [
        ("GAMMA (>90%)", "#ff00ff"),
        ("UV (>70%)", "#5f00ff"),
        ("VISIBLE (>30%)", "#00ffff"),
        ("INFRARED (>5%)", "#ff8700"),
        ("RADIO", "#af0000")
    ]
    
    legend_items = []
    for label, style in tiers:
        legend_items.append(f"[{style}]●[/] {label}")
    
    return Text.from_markup("  ".join(legend_items))

def generate_static(data):
    console = Console()
    if not data: return
    max_count = data[0][1]
    cloud_text = Text()
    
    # Sort data randomly for visual cloud effect but keep frequencies
    display_data = list(data)
    random.shuffle(display_data)

    for cmd, count in display_data:
        ratio = count / max_count
        style = get_spectrum_style(ratio)
        
        # Variable spacing based on frequency (Physics mimic)
        # More frequent items get "gravity" (closer spacing)
        # Less frequent items "orbit" (wider spacing)
        orbit_gap = int((1 - ratio) * 4) + 1
        cloud_text.append(" " * orbit_gap)
        cloud_text.append(cmd, style=style)
        cloud_text.append(" " * orbit_gap)

    console.print("\n")
    console.print(Panel(
        cloud_text, 
        title="[bold white]CLIDE // ELECTROMAGNETIC COMMAND SPECTRUM[/]", 
        border_style="white",
        subtitle=make_legend()
    ))
    console.print("\n")

def generate_live(data):
    console = Console()
    if not data: return
    max_count = data[0][1]
    words = []
    for cmd, count in data:
        words.append({
            "text": cmd,
            "count": count,
            "x": random.uniform(0, 20),
            "vx": random.uniform(-0.2, 0.2),
            "ratio": count / max_count
        })
    
    frame = 0
    with Live(refresh_per_second=10, screen=True) as live:
        try:
            while True:
                frame += 1
                cloud_text = Text()
                for w in words:
                    w["x"] += w["vx"]
                    if w["x"] < 0 or w["x"] > 30: w["vx"] *= -1
                    
                    # Spectral pulse (frequency shift)
                    pulse = (math.sin(frame * 0.3 + words.index(w)) + 1) / 2
                    style = get_spectrum_style(w["ratio"])
                    
                    if pulse < 0.15: style = "dim white"
                    
                    pad = int(w["x"] + ((1-w["ratio"]) * 10))
                    cloud_text.append(" " * pad)
                    cloud_text.append(w["text"], style=style)
                    cloud_text.append("  ", style="dim")
                    
                layout = Layout()
                layout.split(
                    Layout(Panel(Align.center(cloud_text, vertical="middle"), title="[bold white]NEURAL SPECTRUM DRIFT[/]", border_style="white"), name="body"),
                    Layout(Align.center(make_legend()), name="footer", size=1)
                )
                live.update(layout)
                time.sleep(0.05)
        except KeyboardInterrupt:
            pass

def generate_html(data):
    if not data: return
    max_count = data[0][1]
    nodes = []
    for cmd, count in data:
        ratio = count / max_count
        # Dramatic logarithmic scaling for sizes
        size = 6 + (math.log(count + 1) / math.log(max_count + 1)) * 80
        
        # Spectral Color Mapping (Hex)
        if ratio > 0.9: color = "#ff00ff"
        elif ratio > 0.7: color = "#5f00ff"
        elif ratio > 0.5: color = "#00afff"
        elif ratio > 0.3: color = "#00ffff"
        elif ratio > 0.2: color = "#00ff00"
        elif ratio > 0.1: color = "#ffff00"
        elif ratio > 0.05: color = "#ff8700"
        else: color = "#ff0000"
        
        nodes.append({
            "id": cmd,
            "count": count,
            "size": size,
            "color": color,
            "ratio": ratio
        })

    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>CLIDE // Neural Spectrum Cloud</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { margin: 0; background: #020202; color: #eee; font-family: 'JetBrains Mono', monospace; overflow: hidden; }
        .node { cursor: pointer; transition: all 0.3s; opacity: 0.8; }
        .node:hover { opacity: 1; filter: drop-shadow(0 0 8px currentColor); font-weight: bold; }
        
        #controls { position: absolute; top: 40px; left: 40px; background: rgba(0,0,0,0.85); padding: 30px; border: 1px solid #444; border-top: 4px solid #af00ff; }
        .legend-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 0.8rem; }
        .swatch { width: 14px; height: 14px; border-radius: 2px; margin-right: 12px; }
        .title { color: #fff; font-weight: bold; letter-spacing: 6px; margin-bottom: 15px; font-size: 1.6rem; border-bottom: 1px solid #333; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div id="controls">
        <div class="title">NEURAL SPECTRUM</div>
        <div style="font-size: 0.7rem; color: #888; margin-bottom: 20px;">COMMAND FREQUENCY -> EM ENERGY</div>
        
        <div class="legend">
            <div class="legend-item"><div class="swatch" style="background:#ff00ff"></div> GAMMA / HIGH FREQ</div>
            <div class="legend-item"><div class="swatch" style="background:#5f00ff"></div> ULTRAVIOLET</div>
            <div class="legend-item"><div class="swatch" style="background:#00ffff"></div> VISIBLE LIGHT</div>
            <div class="legend-item"><div class="swatch" style="background:#00ff00"></div> THERMAL / GREEN</div>
            <div class="legend-item"><div class="swatch" style="background:#ff8700"></div> INFRARED</div>
            <div class="legend-item"><div class="swatch" style="background:#ff0000"></div> RADIO / TRACE</div>
        </div>
    </div>
    <svg id="cloud"></svg>

    <script>
        const data = DATA_JSON;
        const width = window.innerWidth;
        const height = window.innerHeight;

        const svg = d3.select("#cloud")
            .attr("width", width)
            .attr("height", height);

        const simulation = d3.forceSimulation(data)
            .force("charge", d3.forceManyBody().strength(d => -30 * Math.sqrt(d.ratio + 0.1) - 20))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => d.size * 0.7 + 20))
            .on("tick", ticked);

        const node = svg.append("g")
            .selectAll("text")
            .data(data)
            .join("text")
            .attr("class", "node")
            .attr("text-anchor", "middle")
            .attr("font-size", d => d.size + "px")
            .attr("fill", d => d.color)
            .text(d => d.id)
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        function ticked() {
            node.attr("x", d => d.x).attr("y", d => d.y);
        }

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    </script>
</body>
</html>
""";
    html_content = html_template.replace("DATA_JSON", json.dumps(nodes))
    html_content = html_content.replace("NODE_COUNT", str(len(nodes)))
    
    output_path = "command_cloud.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[v] Neural Spectrum Cloud generated at {output_path}")

def main():
    parser = argparse.ArgumentParser(description="CLIDE Dynamic Command Cloud")
    parser.add_argument("--live", action="store_true", help="Run animated terminal cloud")
    parser.add_argument("--html", action="store_true", help="Generate interactive HTML physics cloud")
    parser.add_argument("--top", type=int, default=100, help="Top N commands")
    parser.add_argument("--min", type=int, default=1, help="Minimum occurrences")
    
    args = parser.parse_args()
    
    data = get_data(min_count=args.min, top_n=args.top)
    
    if args.html:
        generate_html(data)
    elif args.live:
        generate_live(data)
    else:
        generate_static(data)

if __name__ == "__main__":
    main()
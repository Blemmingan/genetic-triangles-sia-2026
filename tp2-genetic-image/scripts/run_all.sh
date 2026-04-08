#!/bin/bash
set -e

# Asegurar que ejecutamos desde la raíz del proyecto para encontrar venv/ y inputs/
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Make sure venv exists and is activated
if [ ! -d "venv" ]; then
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
else
    . venv/bin/activate
fi

# Directory to store the absolute best results
BEST_DIR="outputs/best_results"
EXP_DIR="outputs/experiments"

echo "Clearing previous results to avoid contamination..."
rm -rf "${BEST_DIR:?}"/* "${EXP_DIR:?}"/* 2>/dev/null || true
mkdir -p "$BEST_DIR" "$EXP_DIR"

echo "Running systematic experiments on all input images..."

# Find all images recursively in inputs/
find inputs/ -type f -name "*.png" | sort | while read -r img; do
    echo "======================================"
    echo "Processing image: $img"
    base=$(basename "$img" .png)
    
    # Meaningful name for the clear experiment folder
    out_dir="outputs/experiments/${base}_test_run"
    
    python run_experiments.py \
      --image "$img" \
      --output-dir "$out_dir" \
      --image-size 32 \
      --population-size 30 \
      --triangles 40 \
      --generations 50 \
      --selection-methods tournament_deterministic,universal,elite,roulette,boltzmann,tournament_probabilistic,ranking \
      --crossover-methods uniform,two_point,one_point,annular \
      --mutation-methods multigen,non_uniform,gen \
      --replacement-methods additive,exclusive \
      --repetitions 1
      
    # Extraction of the best image from the run that gave the best fitness
    # summary.json has the runs sorted by best_fitness descending, so index 0 is best
    best_entry=$(python -c "import json; print(json.dumps(json.load(open('$out_dir/summary.json'))[0]))" 2>/dev/null || echo "")
    
    if [ -n "$best_entry" ]; then
        best_run_dir=$(echo "$best_entry" | python -c "import json, sys; print(json.load(sys.stdin)['run_dir'])")
        
        if [ -f "$best_run_dir/best.png" ]; then
            cp "$best_run_dir/best.png" "$BEST_DIR/${base}.png"
            cp "$best_run_dir/best_triangles.txt" "$BEST_DIR/${base}_triangles.txt"
            
            # Append method details
            echo "------------------------------------------------------------" >> "$BEST_DIR/${base}_triangles.txt"
            echo "MEJOR CONFIGURACIÓN ENCONTRADA" >> "$BEST_DIR/${base}_triangles.txt"
            echo "$best_entry" | python -c "
import json, sys
data = json.load(sys.stdin)
print('Seed               : ' + str(data.get('seed')))
print('Selection Method   : ' + str(data.get('selection_method')))
print('Crossover Method   : ' + str(data.get('crossover_method')))
print('Mutation Method    : ' + str(data.get('mutation_method')))
print('Replacement Method : ' + str(data.get('replacement_method')))
" >> "$BEST_DIR/${base}_triangles.txt"

            echo "--> Best result for $base extracted safely to: $BEST_DIR/${base}.png"
        else
            echo "--> Warning: Could not find best.png in $best_run_dir"
        fi
    else
        echo "--> Warning: Could not read summary.json for $base"
    fi
done

echo ""
echo "===== GLOBAL TOP 10 ACROSS ALL IMAGES ====="
python -c "
import json
from pathlib import Path

all_results = []
for p in Path('outputs/experiments').rglob('summary.json'):
    try:
        with open(p, 'r') as f:
            all_results.extend(json.load(f))
    except Exception:
        pass

all_results.sort(key=lambda x: x.get('best_fitness', 0), reverse=True)

for idx, row in enumerate(all_results[:10], start=1):
    # Extract image name from run_dir (e.g. outputs/experiments/za_test_run/...)
    img_name = row.get('run_dir', '').split('/')[-2].replace('_test_run', '')
    print(
        f\"{idx:02d}. img={img_name} | fitness={row.get('best_fitness',0):.6f} | \"
        f\"sel={row.get('selection_method')} | cross={row.get('crossover_method')} | \"
        f\"mut={row.get('mutation_method')} | rep={row.get('replacement_method')} | seed={row.get('seed')}\"
    )
"

echo "All experiments completed."

import argparse
import csv
import json
import os
import random
import time
from itertools import product
from pathlib import Path

import numpy as np
from PIL import Image

from engine.genetic_algorithm import GeneticAlgorithm
from rendering.renderer import render


def parse_csv_list(value: str):
    return [item.strip() for item in value.split(",") if item.strip()]


def load_target_image(image_path: str, image_size: int) -> Image.Image:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No se encontró la imagen: {image_path}")

    image = Image.open(image_path).convert("RGBA")
    image = image.resize((image_size, image_size))
    return image


def save_best_triangles(best_individual, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Triángulos del mejor individuo\n")
        f.write("=" * 60 + "\n")
        f.write(f"Fitness: {best_individual.fitness:.6f}\n")
        f.write(f"Cantidad de triángulos: {len(best_individual.chromosome)}\n\n")

        for i, triangle in enumerate(best_individual.chromosome):
            f.write(f"Triángulo {i}:\n")
            f.write(f"{triangle}\n\n")


def set_global_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def build_ga(target_image: Image.Image, args, config: dict) -> GeneticAlgorithm:
    return GeneticAlgorithm(
        target_image=target_image,
        population_size=args.population_size,
        num_triangles=args.triangles,
        generations=args.generations,
        selection_method=config["selection_method"],
        tournament_k=args.tournament_k,
        tournament_threshold=args.tournament_threshold,
        boltzmann_temperature=args.boltzmann_temperature,
        boltzmann_decay=args.boltzmann_decay,
        min_temperature=args.min_temperature,
        crossover_method=config["crossover_method"],
        crossover_rate=args.crossover_rate,
        uniform_swap_probability=args.uniform_swap_probability,
        annular_min_segment_length=args.annular_min_segment_length,
        annular_max_segment_length=args.annular_max_segment_length,
        mutation_method=config["mutation_method"],
        mutation_rate=args.mutation_rate,
        mutation_mode=args.mutation_mode,
        sigma=args.sigma,
        multigen_min_genes=args.multigen_min_genes,
        multigen_max_genes=args.multigen_max_genes,
        non_uniform_b=args.non_uniform_b,
        elite_fraction=args.elite_fraction,
        replacement_method=config["replacement_method"],
        fitness_threshold=args.fitness_threshold,
        no_improvement_generations=args.no_improvement_generations,
        improvement_epsilon=args.improvement_epsilon,
        init_method=args.init_method,
        init_alpha_min=args.init_alpha_min,
        init_alpha_max=args.init_alpha_max,
        init_triangle_size_min=args.init_triangle_size_min,
        init_triangle_size_max=args.init_triangle_size_max,
        init_color_jitter=args.init_color_jitter,
    )


def run_single_experiment(
    target_image: Image.Image, args, config: dict, run_dir: Path, seed: int
):
    set_global_seed(seed)
    run_dir.mkdir(parents=True, exist_ok=True)

    target_path = run_dir / "target.png"
    target_image.save(target_path)

    ga = build_ga(target_image, args, config)

    t0 = time.perf_counter()
    best_individual = ga.run()
    elapsed = time.perf_counter() - t0

    best_image = render(best_individual, target_image.size, target_image=target_image)
    best_image_path = run_dir / "best.png"
    best_image.save(best_image_path)

    triangles_path = run_dir / "best_triangles.txt"
    save_best_triangles(best_individual, triangles_path)

    ga.save_metrics(str(run_dir))

    stop_generation = ga.tracker.generations[-1] if ga.tracker.generations else None
    stop_reason = ga.stopper.get_stop_reason()

    result = {
        "seed": seed,
        "selection_method": config["selection_method"],
        "crossover_method": config["crossover_method"],
        "mutation_method": config["mutation_method"],
        "replacement_method": config["replacement_method"],
        "best_fitness": float(best_individual.fitness),
        "stop_generation": stop_generation,
        "stop_reason": stop_reason,
        "elapsed_seconds": elapsed,
        "run_dir": str(run_dir),
    }

    with open(run_dir / "run_summary.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result


def write_summary_csv(results, output_path: Path):
    if not results:
        return

    fieldnames = [
        "seed",
        "selection_method",
        "crossover_method",
        "mutation_method",
        "replacement_method",
        "best_fitness",
        "stop_generation",
        "stop_reason",
        "elapsed_seconds",
        "run_dir",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta múltiples experimentos del algoritmo genético y guarda un resumen comparativo."
    )

    parser.add_argument(
        "--image", type=str, required=True, help="Ruta de la imagen objetivo"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/experiments",
        help="Carpeta base de resultados",
    )
    parser.add_argument(
        "--image-size", type=int, default=32, help="Tamaño cuadrado de la imagen"
    )

    parser.add_argument("--population-size", type=int, default=120)
    parser.add_argument("--triangles", type=int, default=60)
    parser.add_argument("--generations", type=int, default=250)

    parser.add_argument(
        "--selection-methods",
        type=str,
        default="tournament_deterministic,universal,ranking",
    )
    parser.add_argument("--crossover-methods", type=str, default="uniform,two_point")
    parser.add_argument("--mutation-methods", type=str, default="multigen,non_uniform")
    parser.add_argument("--replacement-methods", type=str, default="additive")

    parser.add_argument(
        "--repetitions",
        type=int,
        default=3,
        help="Cantidad de repeticiones por configuración",
    )
    parser.add_argument("--base-seed", type=int, default=42, help="Seed inicial")

    parser.add_argument("--elite-fraction", type=float, default=0.3)

    parser.add_argument("--tournament-k", type=int, default=3)
    parser.add_argument("--tournament-threshold", type=float, default=0.75)

    parser.add_argument("--boltzmann-temperature", type=float, default=5.0)
    parser.add_argument("--boltzmann-decay", type=float, default=0.98)
    parser.add_argument("--min-temperature", type=float, default=1e-3)

    parser.add_argument("--crossover-rate", type=float, default=0.4)
    parser.add_argument("--uniform-swap-probability", type=float, default=0.5)
    parser.add_argument("--annular-min-segment-length", type=int, default=1)
    parser.add_argument("--annular-max-segment-length", type=int, default=None)

    parser.add_argument("--mutation-rate", type=float, default=0.95)
    parser.add_argument(
        "--mutation-mode", type=str, default="delta", choices=["reset", "delta"]
    )
    parser.add_argument("--sigma", type=float, default=0.02)
    parser.add_argument("--multigen-min-genes", type=int, default=8)
    parser.add_argument("--multigen-max-genes", type=int, default=20)
    parser.add_argument("--non-uniform-b", type=float, default=2.0)

    parser.add_argument("--replacement-method", type=str, default=None)

    parser.add_argument("--fitness-threshold", type=float, default=None)
    parser.add_argument("--no-improvement-generations", type=int, default=40)
    parser.add_argument("--improvement-epsilon", type=float, default=1e-6)

    parser.add_argument(
        "--init-method", type=str, default="guided", choices=["random", "guided"]
    )
    parser.add_argument("--init-alpha-min", type=float, default=0.2)
    parser.add_argument("--init-alpha-max", type=float, default=0.8)
    parser.add_argument("--init-triangle-size-min", type=float, default=0.05)
    parser.add_argument("--init-triangle-size-max", type=float, default=0.35)
    parser.add_argument("--init-color-jitter", type=float, default=0.05)

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    target_image = load_target_image(args.image, args.image_size)

    selection_methods = parse_csv_list(args.selection_methods)
    crossover_methods = parse_csv_list(args.crossover_methods)
    mutation_methods = parse_csv_list(args.mutation_methods)
    replacement_methods = (
        [args.replacement_method]
        if args.replacement_method is not None
        else parse_csv_list(args.replacement_methods)
    )

    experiment_grid = list(
        product(
            selection_methods,
            crossover_methods,
            mutation_methods,
            replacement_methods,
        )
    )

    all_results = []

    print(
        f"Se ejecutarán {len(experiment_grid)} configuraciones x {args.repetitions} repeticiones."
    )
    print(f"Imagen objetivo: {args.image}")

    for config_index, (
        selection_method,
        crossover_method,
        mutation_method,
        replacement_method,
    ) in enumerate(experiment_grid, start=1):
        config = {
            "selection_method": selection_method,
            "crossover_method": crossover_method,
            "mutation_method": mutation_method,
            "replacement_method": replacement_method,
        }

        print(
            f"\n[{config_index}/{len(experiment_grid)}] "
            f"selection={selection_method} | "
            f"crossover={crossover_method} | "
            f"mutation={mutation_method} | "
            f"replacement={replacement_method}"
        )

        for rep in range(args.repetitions):
            seed = args.base_seed + config_index * 1000 + rep

            run_name = (
                f"sel-{selection_method}"
                f"__cross-{crossover_method}"
                f"__mut-{mutation_method}"
                f"__rep-{replacement_method}"
                f"__seed-{seed}"
            )
            run_dir = output_dir / run_name

            print(f"  Repetición {rep + 1}/{args.repetitions} | seed={seed}")

            result = run_single_experiment(
                target_image=target_image,
                args=args,
                config=config,
                run_dir=run_dir,
                seed=seed,
            )
            all_results.append(result)

    all_results.sort(key=lambda x: x["best_fitness"], reverse=True)

    write_summary_csv(all_results, output_dir / "summary.csv")

    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)

    print(f"\n===== TOP 10 RESULTADOS PARA {Path(args.image).name.upper()} =====")
    for idx, row in enumerate(all_results[:10], start=1):
        print(
            f"{idx:02d}. fitness={row['best_fitness']:.6f} | "
            f"sel={row['selection_method']} | "
            f"cross={row['crossover_method']} | "
            f"mut={row['mutation_method']} | "
            f"rep={row['replacement_method']} | "
            f"seed={row['seed']}"
        )

    print("\nResumen guardado en:")
    print(f"- {output_dir / 'summary.csv'}")
    print(f"- {output_dir / 'summary.json'}")


if __name__ == "__main__":
    main()

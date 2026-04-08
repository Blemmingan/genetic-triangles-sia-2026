import argparse
from pathlib import Path

from PIL import Image

from engine.genetic_algorithm import GeneticAlgorithm
from rendering.renderer import render
from utils.config_loader import load_config


def save_best_triangles(best_individual, output_path: Path):
    """
    Guarda en un archivo de texto la lista de triángulos
    del mejor individuo encontrado.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Triángulos del mejor individuo\n")
        f.write("=" * 60 + "\n")
        f.write(f"Fitness: {best_individual.fitness:.6f}\n")
        f.write(f"Cantidad de triángulos: {len(best_individual.chromosome)}\n\n")

        for i, triangle in enumerate(best_individual.chromosome):
            f.write(f"Triángulo {i}:\n")
            f.write(f"{triangle}\n\n")


def build_ga(
    target_image: Image.Image, config: dict, num_triangles: int
) -> GeneticAlgorithm:
    """
    Construye el motor genético usando la configuración cargada.
    """

    return GeneticAlgorithm(
        target_image=target_image,
        population_size=config.get("population_size", 50),
        num_triangles=num_triangles,
        generations=config.get("generations", 100),
        # Selección
        selection_method=config.get("selection_method", "tournament_deterministic"),
        tournament_k=config.get("tournament_k", 3),
        tournament_threshold=config.get("tournament_threshold", 0.75),
        # Crossover
        crossover_method=config.get("crossover_method", "uniform"),
        crossover_rate=config.get("crossover_rate", 0.8),
        uniform_swap_probability=config.get("uniform_swap_probability", 0.5),
        # Mutación
        mutation_method=config.get("mutation_method", "multigen"),
        mutation_rate=config.get("mutation_rate", 0.8),
        mutation_mode=config.get("mutation_mode", "delta"),
        sigma=config.get("sigma", 0.03),
        multigen_min_genes=config.get("multigen_min_genes", 3),
        multigen_max_genes=config.get("multigen_max_genes", 12),
        # Replacement
        elite_fraction=config.get("elite_fraction", 0.3),
        replacement_method=config.get("replacement_method", "additive"),
        # Stopping
        fitness_threshold=config.get("fitness_threshold", None),
        no_improvement_generations=config.get(
            "no_improvement_generations", config.get("convergence_generations", 20)
        ),
        improvement_epsilon=config.get("improvement_epsilon", 1e-6),
        # Inicialización
        init_method=config.get("init_method", "guided"),
        init_alpha_min=config.get("init_alpha_min", 0.2),
        init_alpha_max=config.get("init_alpha_max", 0.8),
        init_triangle_size_min=config.get("init_triangle_size_min", 0.05),
        init_triangle_size_max=config.get("init_triangle_size_max", 0.35),
        init_color_jitter=config.get("init_color_jitter", 0.05),
    )


def main():
    """
    Punto de entrada principal del proyecto.
    """

    parser = argparse.ArgumentParser(
        description="Genetic Algorithm for Image Approximation with Triangles"
    )

    # ---------------------------------------------------------
    # 1) Parámetros principales
    # ---------------------------------------------------------
    parser.add_argument("--image", type=str, help="Path to target image")
    parser.add_argument("--triangles", type=int, help="Number of triangles to use")
    parser.add_argument(
        "--config", type=str, default="config/default.json", help="Path to config file"
    )

    # ---------------------------------------------------------
    # 2) Overrides simples
    # ---------------------------------------------------------
    parser.add_argument("--population-size", type=int, help="Override population size")
    parser.add_argument("--generations", type=int, help="Override generations count")
    parser.add_argument("--selection", type=str, help="Override selection method")
    parser.add_argument("--crossover", type=str, help="Override crossover method")
    parser.add_argument("--mutation", type=str, help="Override mutation method")
    parser.add_argument("--replacement", type=str, help="Override replacement method")

    # ---------------------------------------------------------
    # 3) Opciones más detalladas
    # ---------------------------------------------------------
    parser.add_argument(
        "--image-size",
        type=int,
        default=64,
        help="Resize target image to a square of this size",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory where results will be saved",
    )

    parser.add_argument(
        "--tournament-k", type=int, help="Tournament size for deterministic tournament"
    )
    parser.add_argument(
        "--tournament-threshold",
        type=float,
        help="Threshold for probabilistic tournament",
    )

    parser.add_argument("--crossover-rate", type=float, help="Probability of crossover")
    parser.add_argument(
        "--uniform-swap-probability",
        type=float,
        help="Swap probability for uniform crossover",
    )

    parser.add_argument("--mutation-rate", type=float, help="Mutation probability")
    parser.add_argument(
        "--mutation-mode",
        type=str,
        choices=["reset", "delta"],
        help="Internal mutation mode",
    )
    parser.add_argument("--sigma", type=float, help="Delta mutation intensity")
    parser.add_argument(
        "--multigen-min-genes",
        type=int,
        help="Minimum scalar genes to mutate in multigen",
    )
    parser.add_argument(
        "--multigen-max-genes",
        type=int,
        help="Maximum scalar genes to mutate in multigen",
    )

    parser.add_argument(
        "--elite-fraction", type=float, help="Fraction of population used as parents"
    )

    parser.add_argument(
        "--fitness-threshold", type=float, help="Stop when reaching this fitness"
    )
    parser.add_argument(
        "--no-improvement-generations",
        type=int,
        help="Stop after N generations without improvement",
    )
    parser.add_argument(
        "--improvement-epsilon", type=float, help="Minimum significant improvement"
    )

    parser.add_argument(
        "--init-method",
        type=str,
        choices=["random", "guided"],
        help="Initialization method",
    )
    parser.add_argument(
        "--init-alpha-min", type=float, help="Minimum alpha for guided init"
    )
    parser.add_argument(
        "--init-alpha-max", type=float, help="Maximum alpha for guided init"
    )
    parser.add_argument(
        "--init-triangle-size-min",
        type=float,
        help="Minimum triangle size for guided init",
    )
    parser.add_argument(
        "--init-triangle-size-max",
        type=float,
        help="Maximum triangle size for guided init",
    )
    parser.add_argument(
        "--init-color-jitter", type=float, help="Color jitter for guided init"
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # 4) Cargar configuración
    # ---------------------------------------------------------
    config = load_config(args.config, args)

    # ---------------------------------------------------------
    # 5) Determinar imágenes a procesar
    # ---------------------------------------------------------
    images_to_process = []

    if args.image:
        images_to_process.append(Path(args.image))
    else:
        inputs_dir = Path("inputs")
        if inputs_dir.exists():
            images_to_process.extend(inputs_dir.rglob("*.png"))

    if not images_to_process:
        print(
            "No images found to process. Please provide --image or add .png files to inputs directory."
        )
        return

    # ---------------------------------------------------------
    # 6) Procesar cada imagen
    # ---------------------------------------------------------
    for image_path in images_to_process:
        print(f"\nProcessing image: {image_path}")

        try:
            if not image_path.exists():
                print(f"Image not found: {image_path}")
                continue

            # Cargar imagen objetivo
            target_image = Image.open(image_path).convert("RGBA")
            image_size = config.get("image_size", 64)
            target_image = target_image.resize((image_size, image_size))

            # Cantidad de triángulos
            num_triangles = config.get("triangles", 100)
            if num_triangles is None:
                num_triangles = 100

            # Carpeta de salida específica para esta imagen
            run_output_dir = Path(config.get("output_dir", "outputs")) / image_path.stem
            run_output_dir.mkdir(parents=True, exist_ok=True)

            # Guardar target redimensionada
            target_output_path = run_output_dir / "target.png"
            target_image.save(target_output_path)

            # Construir y ejecutar GA
            ga = build_ga(
                target_image=target_image,
                config=config,
                num_triangles=num_triangles,
            )

            best_individual = ga.run()

            # Guardar mejor imagen
            best_image = render(best_individual, target_image.size, target_image=target_image)
            best_image_path = run_output_dir / "best.png"
            best_image.save(best_image_path)

            # Guardar triángulos
            triangles_path = run_output_dir / "best_triangles.txt"
            save_best_triangles(best_individual, triangles_path)

            # Guardar métricas
            ga.save_metrics(str(run_output_dir))

            print("\n===== RESUMEN FINAL =====")
            print(f"Image                     : {image_path}")
            print(f"Output dir                : {run_output_dir}")
            print(f"Image size                : {image_size}x{image_size}")
            print(f"Population                : {config.get('population_size', 50)}")
            print(f"Triangles                 : {num_triangles}")
            print(f"Generations               : {config.get('generations', 100)}")
            print(
                f"Selection                 : {config.get('selection_method', 'tournament_deterministic')}"
            )
            print(
                f"Crossover                 : {config.get('crossover_method', 'uniform')}"
            )
            print(
                f"Mutation                  : {config.get('mutation_method', 'multigen')}"
            )
            print(
                f"Replacement               : {config.get('replacement_method', 'additive')}"
            )
            print(f"Init                      : {config.get('init_method', 'guided')}")
            print(f"Best global fitness       : {best_individual.fitness:.6f}")

            print("\nGenerated files:")
            print(f"- Target image            : {target_output_path}")
            print(f"- Best image              : {best_image_path}")
            print(f"- Triangles               : {triangles_path}")
            print(f"- Metrics JSON            : {run_output_dir / 'metrics.json'}")
            print(f"- Fitness plot            : {run_output_dir / 'fitness_plot.png'}")

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()

import argparse
import os

from PIL import Image

from engine.genetic_algorithm import GeneticAlgorithm
from rendering.renderer import render


def load_target_image(image_path: str, image_size: int) -> Image.Image:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No se encontró la imagen: {image_path}")

    image = Image.open(image_path).convert("RGBA")
    image = image.resize((image_size, image_size))
    return image


def save_best_triangles(best_individual, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Triángulos del mejor individuo\n")
        f.write("=" * 60 + "\n")
        f.write(f"Fitness: {best_individual.fitness:.6f}\n")
        f.write(f"Cantidad de triángulos: {len(best_individual.chromosome)}\n\n")

        for i, triangle in enumerate(best_individual.chromosome):
            f.write(f"Triángulo {i}:\n")
            f.write(f"{triangle}\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Test completo del algoritmo genético con una imagen real"
    )

    # ---------------------------------------------------------
    # 1) Entrada / salida
    # ---------------------------------------------------------
    parser.add_argument(
        "--image", type=str, required=True, help="Ruta de la imagen objetivo"
    )
    parser.add_argument("--image-size", type=int, default=64, help="Tamaño cuadrado")
    parser.add_argument(
        "--output-dir", type=str, default="outputs/ga_test", help="Carpeta de salida"
    )

    # ---------------------------------------------------------
    # 2) Parámetros principales del GA
    # ---------------------------------------------------------
    parser.add_argument(
        "--population-size", type=int, default=50, help="Cantidad de individuos"
    )
    parser.add_argument(
        "--triangles", type=int, default=40, help="Cantidad de triángulos por individuo"
    )
    parser.add_argument(
        "--generations", type=int, default=100, help="Cantidad máxima de generaciones"
    )
    parser.add_argument(
        "--elite-fraction", type=float, default=0.3, help="Fracción usada como padres"
    )

    # ---------------------------------------------------------
    # 3) Selección
    # ---------------------------------------------------------
    parser.add_argument(
        "--selection-method",
        type=str,
        default="tournament_deterministic",
        choices=[
            "elite",
            "roulette",
            "universal",
            "boltzmann",
            "tournament_deterministic",
            "tournament_probabilistic",
            "ranking",
        ],
        help="Método de selección",
    )
    parser.add_argument(
        "--tournament-k", type=int, default=3, help="Tamaño del torneo determinístico"
    )
    parser.add_argument(
        "--tournament-threshold",
        type=float,
        default=0.75,
        help="Threshold del torneo probabilístico",
    )
    parser.add_argument(
        "--boltzmann-temperature",
        type=float,
        default=100.0,
        help="Temperatura inicial para selección Boltzmann",
    )
    parser.add_argument(
        "--boltzmann-decay",
        type=float,
        default=0.99,
        help="Factor de decaimiento de temperatura para Boltzmann",
    )
    parser.add_argument(
        "--min-temperature",
        type=float,
        default=1e-3,
        help="Temperatura mínima para Boltzmann",
    )

    # ---------------------------------------------------------
    # 4) Crossover
    # ---------------------------------------------------------
    parser.add_argument(
        "--crossover-method",
        type=str,
        default="uniform",
        choices=["one_point", "two_point", "uniform", "annular"],
        help="Método de crossover",
    )
    parser.add_argument(
        "--annular-min-segment-length",
        type=int,
        default=1,
        help="Longitud mínima del segmento en annular crossover",
    )
    parser.add_argument(
        "--annular-max-segment-length",
        type=int,
        default=None,
        help="Longitud máxima del segmento en annular crossover",
    )
    parser.add_argument(
        "--crossover-rate", type=float, default=0.9, help="Probabilidad de crossover"
    )
    parser.add_argument(
        "--uniform-swap-probability",
        type=float,
        default=0.5,
        help="Swap probability para uniform",
    )

    # ---------------------------------------------------------
    # 5) Mutación
    # ---------------------------------------------------------
    parser.add_argument(
        "--mutation-method",
        type=str,
        default="multigen",
        choices=["gen", "multigen", "non_uniform"],
        help="Método de mutación",
    )
    parser.add_argument(
        "--non-uniform-b",
        type=float,
        default=2.0,
        help="Parámetro b de la mutación no uniforme",
    )
    parser.add_argument(
        "--mutation-rate", type=float, default=0.8, help="Probabilidad de mutación"
    )
    parser.add_argument(
        "--mutation-mode",
        type=str,
        default="delta",
        choices=["reset", "delta"],
        help="Modo de mutación",
    )
    parser.add_argument(
        "--sigma", type=float, default=0.03, help="Intensidad de mutación delta"
    )
    parser.add_argument(
        "--multigen-min-genes",
        type=int,
        default=3,
        help="Mínimo de genes a mutar en multigen",
    )
    parser.add_argument(
        "--multigen-max-genes",
        type=int,
        default=12,
        help="Máximo de genes a mutar en multigen",
    )

    # ---------------------------------------------------------
    # 6) Replacement
    # ---------------------------------------------------------
    parser.add_argument(
        "--replacement-method",
        type=str,
        default="additive",
        choices=["exclusive", "additive"],
        help="Método de replacement",
    )

    # ---------------------------------------------------------
    # 7) Criterios de parada
    # ---------------------------------------------------------
    parser.add_argument(
        "--fitness-threshold", type=float, default=None, help="Umbral de fitness"
    )
    parser.add_argument(
        "--no-improvement-generations",
        type=int,
        default=20,
        help="Generaciones sin mejora",
    )
    parser.add_argument(
        "--improvement-epsilon",
        type=float,
        default=1e-6,
        help="Mejora mínima significativa",
    )

    # ---------------------------------------------------------
    # 8) Inicialización
    # ---------------------------------------------------------
    parser.add_argument(
        "--init-method",
        type=str,
        default="guided",
        choices=["random", "guided"],
        help="Método de inicialización",
    )
    parser.add_argument(
        "--init-alpha-min", type=float, default=0.2, help="Alpha mínimo en guided init"
    )
    parser.add_argument(
        "--init-alpha-max", type=float, default=0.8, help="Alpha máximo en guided init"
    )
    parser.add_argument(
        "--init-triangle-size-min",
        type=float,
        default=0.05,
        help="Tamaño mínimo de triángulo",
    )
    parser.add_argument(
        "--init-triangle-size-max",
        type=float,
        default=0.35,
        help="Tamaño máximo de triángulo",
    )
    parser.add_argument(
        "--init-color-jitter",
        type=float,
        default=0.05,
        help="Ruido agregado al color inicial",
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    target_image = load_target_image(args.image, args.image_size)
    target_output_path = os.path.join(args.output_dir, "target.png")
    target_image.save(target_output_path)

    ga = GeneticAlgorithm(
        target_image=target_image,
        population_size=args.population_size,
        num_triangles=args.triangles,
        generations=args.generations,
        selection_method=args.selection_method,
        tournament_k=args.tournament_k,
        tournament_threshold=args.tournament_threshold,
        boltzmann_temperature=args.boltzmann_temperature,
        boltzmann_decay=args.boltzmann_decay,
        min_temperature=args.min_temperature,
        crossover_method=args.crossover_method,
        crossover_rate=args.crossover_rate,
        uniform_swap_probability=args.uniform_swap_probability,
        mutation_method=args.mutation_method,
        mutation_rate=args.mutation_rate,
        mutation_mode=args.mutation_mode,
        sigma=args.sigma,
        multigen_min_genes=args.multigen_min_genes,
        multigen_max_genes=args.multigen_max_genes,
        elite_fraction=args.elite_fraction,
        replacement_method=args.replacement_method,
        fitness_threshold=args.fitness_threshold,
        no_improvement_generations=args.no_improvement_generations,
        improvement_epsilon=args.improvement_epsilon,
        init_method=args.init_method,
        init_alpha_min=args.init_alpha_min,
        init_alpha_max=args.init_alpha_max,
        init_triangle_size_min=args.init_triangle_size_min,
        init_triangle_size_max=args.init_triangle_size_max,
        init_color_jitter=args.init_color_jitter,
        non_uniform_b=args.non_uniform_b,
        annular_min_segment_length=args.annular_min_segment_length,
        annular_max_segment_length=args.annular_max_segment_length,
    )

    best_individual = ga.run()

    best_image = render(best_individual, target_image.size)
    best_image_path = os.path.join(args.output_dir, "best.png")
    best_image.save(best_image_path)

    triangles_path = os.path.join(args.output_dir, "best_triangles.txt")
    save_best_triangles(best_individual, triangles_path)

    ga.save_metrics(args.output_dir)

    print("\n===== RESUMEN FINAL =====")
    print(f"Imagen objetivo               : {args.image}")
    print(f"Tamaño usado                  : {args.image_size}x{args.image_size}")
    print(f"Población                     : {args.population_size}")
    print(f"Triángulos por individuo      : {args.triangles}")
    print(f"Generaciones máximas          : {args.generations}")
    print(f"Init                          : {args.init_method}")
    print(f"Selection                     : {args.selection_method}")
    print(f"Crossover                     : {args.crossover_method}")
    print(f"Mutation                      : {args.mutation_method}")
    print(f"Replacement                   : {args.replacement_method}")
    print(f"Best global fitness           : {best_individual.fitness:.6f}")

    print("\nArchivos generados:")
    print(f"- Imagen target               : {target_output_path}")
    print(f"- Mejor imagen                : {best_image_path}")
    print(f"- Triángulos                  : {triangles_path}")
    print(
        f"- Métricas JSON               : {os.path.join(args.output_dir, 'metrics.json')}"
    )
    print(
        f"- Gráfico fitness             : {os.path.join(args.output_dir, 'fitness_plot.png')}"
    )


if __name__ == "__main__":
    main()

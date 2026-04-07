from PIL import Image

from engine.population import Population

# Crear imagen objetivo simple
target = Image.new("RGBA", (64, 64), (255, 255, 255, 255))

# Crear población
pop = Population(size=10, num_triangles=5)

# Inicializar población aleatoria
pop.initialize_random()

print(pop)
print("Cantidad de individuos:", len(pop))

# Evaluar toda la población
pop.evaluate_all(target)

# Mostrar estadísticas simples
best = pop.get_best()
worst = pop.get_worst()
avg = pop.get_average_fitness()

print("Mejor fitness:", best.fitness)
print("Peor fitness:", worst.fitness)
print("Fitness promedio:", avg)
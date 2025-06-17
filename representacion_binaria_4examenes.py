import random
import numpy as np
import pandas as pd

df = pd.read_csv('notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()

def crear_cromosoma():
    """Genera un cromosoma con 10 alumnos en A, B, C y 9 en D."""
    asignaciones = ['A'] * 10 + ['B'] * 10 + ['C'] * 10 + ['D'] * 9
    random.shuffle(asignaciones)
    cromosoma = []
    examenes = ['A', 'B', 'C', 'D']
    for asignacion in asignaciones:
        genes = [0, 0, 0, 0]
        genes[examenes.index(asignacion)] = 1
        cromosoma.extend(genes)
    return cromosoma

def decodificar_cromosoma(cromosoma):
    asignaciones = {'A': [], 'B': [], 'C': [], 'D': []}
    examenes = ['A', 'B', 'C', 'D']
    
    for i in range(39):
        idx = i * 4
        for j in range(4):
            if cromosoma[idx + j] == 1:
                asignaciones[examenes[j]].append(i)
                break
    
    return asignaciones

def calcular_fitness(cromosoma):
    asignaciones = decodificar_cromosoma(cromosoma)

    if (len(asignaciones['A']) != 10 or
        len(asignaciones['B']) != 10 or
        len(asignaciones['C']) != 10 or
        len(asignaciones['D']) != 9):
        return -1000

    promedios = {}
    varianzas = {}
    diversidad = 0

    for examen in ['A', 'B', 'C', 'D']:
        indices = asignaciones[examen]
        notas_examen = [notas[i] for i in indices]

        promedios[examen] = np.mean(notas_examen)
        varianzas[examen] = np.var(notas_examen)

        categorias = set()
        for nota in notas_examen:
            if nota >= 15:
                categorias.add('alta')
            elif nota < 11:
                categorias.add('baja')
            else:
                categorias.add('media')
        diversidad += len(categorias) / 3

    desv_promedios = np.std(list(promedios.values()))
    promedio_varianzas = np.mean(list(varianzas.values()))

    fitness = -desv_promedios - 0.1 * promedio_varianzas + 0.1 * diversidad
    return fitness

def mutacion(cromosoma):
    cromosoma_mutado = cromosoma.copy()
    
    alumno1 = random.randint(0, 38)
    alumno2 = random.randint(0, 38)
    
    idx1 = alumno1 * 4
    idx2 = alumno2 * 4
    
    examen1 = [i for i in range(4) if cromosoma_mutado[idx1 + i] == 1][0]
    examen2 = [i for i in range(4) if cromosoma_mutado[idx2 + i] == 1][0]
    
    if examen1 != examen2:
        cromosoma_mutado[idx1:idx1+4] = [0, 0, 0, 0]
        cromosoma_mutado[idx1 + examen2] = 1

        cromosoma_mutado[idx2:idx2+4] = [0, 0, 0, 0]
        cromosoma_mutado[idx2 + examen1] = 1
    
    return cromosoma_mutado

def algoritmo_genetico(generaciones=100, tam_poblacion=50):
    poblacion = [crear_cromosoma() for _ in range(tam_poblacion)]
    
    for gen in range(generaciones):
        fitness_scores = [(crom, calcular_fitness(crom)) for crom in poblacion]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        nueva_poblacion = []
        
        elite = int(tam_poblacion * 0.2)
        for i in range(elite):
            nueva_poblacion.append(fitness_scores[i][0])
        
        while len(nueva_poblacion) < tam_poblacion:
            padre = random.choice(poblacion[:tam_poblacion//2])
            hijo = mutacion(padre)
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
        
        if gen % 20 == 0:
            mejor_fitness = fitness_scores[0][1]
            print(f"Generación {gen}: Mejor fitness = {mejor_fitness:.4f}")
    
    mejor_cromosoma = fitness_scores[0][0]
    return mejor_cromosoma

print("REPRESENTACIÓN BINARIA - 4 EXÁMENES")
print("Problema: Distribuir 39 alumnos en 4 exámenes (A, B, C, D)")
print("Cromosoma: 156 bits (39 alumnos × 4 bits cada uno)")
print("Gen: [0,1,0,0] significa alumno asignado a examen B\n")

mejor_solucion = algoritmo_genetico()
asignaciones_finales = decodificar_cromosoma(mejor_solucion)

print("\nDistribución final:")
for examen in ['A', 'B', 'C', 'D']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]
    promedio = np.mean(notas_examen)
    print(f"Examen {examen}: {len(indices)} alumnos, promedio = {promedio:.2f}")
    print(f"  Alumnos: {[alumnos[i] for i in indices[:5]]}... (mostrando primeros 5)")

print("\nVerificación de equilibrio:")
promedios = []
for examen in ['A', 'B', 'C', 'D']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]
    promedios.append(np.mean(notas_examen))
print(f"Desviación estándar entre promedios: {np.std(promedios):.4f}")

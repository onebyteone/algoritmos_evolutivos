import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import representacion_binaria as rb
import representacion_real as rr
import representacion_permutacional as rp

# Cargar notas para generar histogramas
notas_df = pd.read_csv('notas_1u.csv')
notas = notas_df['Nota'].tolist()


def run_binaria(generaciones=100, tam_poblacion=50):
    poblacion = [rb.crear_cromosoma() for _ in range(tam_poblacion)]
    historial = []
    for _ in range(generaciones):
        fitness_scores = [(crom, rb.calcular_fitness(crom)) for crom in poblacion]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        historial.append(fitness_scores[0][1])
        nueva_poblacion = []
        elite = int(tam_poblacion * 0.2)
        for i in range(elite):
            nueva_poblacion.append(fitness_scores[i][0])
        while len(nueva_poblacion) < tam_poblacion:
            padre = random.choice(poblacion[:tam_poblacion//2])
            hijo = rb.mutacion(padre)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
    mejor_cromosoma = fitness_scores[0][0]
    asignaciones = rb.decodificar_cromosoma(mejor_cromosoma)
    return historial, asignaciones


def run_real(generaciones=150, tam_poblacion=100, sigma_gauss=0.1):
    poblacion = [rr.crear_cromosoma() for _ in range(tam_poblacion)]
    historial = []
    for _ in range(generaciones):
        fitness_scores = [(crom, rr.calcular_fitness(crom)) for crom in poblacion]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        historial.append(fitness_scores[0][1])
        nueva_poblacion = []
        elite = int(tam_poblacion * 0.1)
        for i in range(elite):
            nueva_poblacion.append(fitness_scores[i][0])
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = random.choice(poblacion[:tam_poblacion//4])
            padre2 = random.choice(poblacion[:tam_poblacion//4])
            hijo = rr.cruce(padre1, padre2)
            hijo = rr.mutacion_gaussiana(hijo, sigma=sigma_gauss)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
    mejor_cromosoma = fitness_scores[0][0]
    asignaciones = rr.decodificar_cromosoma(mejor_cromosoma)
    return historial, asignaciones


def run_permutacional(generaciones=50, tam_poblacion=30):
    mejor, historial = rp.algoritmo_genetico(generaciones, tam_poblacion)
    asignaciones = rp.decodificar_cromosoma(mejor)
    return historial, asignaciones


def notas_por_examen(asignaciones):
    return {ex: [notas[i] for i in idxs] for ex, idxs in asignaciones.items()}


def main():
    hist_bin, asig_bin = run_binaria()
    hist_real, asig_real = run_real()
    hist_perm, asig_perm = run_permutacional()

    # Evolución del fitness
    plt.figure(figsize=(8, 5))
    plt.plot(hist_bin, label='Binaria')
    plt.plot(hist_real, label='Real')
    plt.plot(hist_perm, label='Permutacional')
    plt.xlabel('Generación')
    plt.ylabel('Mejor Fitness')
    plt.title('Evolución del Fitness por Representación')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Histogramas de notas por examen
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
    for ax, (titulo, asign) in zip(
        axes,
        [('Binaria', asig_bin), ('Real', asig_real), ('Permutacional', asig_perm)],
    ):
        for ex in ['A', 'B', 'C']:
            sns.histplot(
                notas_por_examen(asign)[ex],
                bins=range(0, 21),
                element='step',
                stat='count',
                fill=False,
                ax=ax,
                label=f'Examen {ex}',
            )
        ax.set_title(titulo)
        ax.set_xlabel('Notas')
        ax.set_ylabel('Frecuencia')
        ax.legend()
    fig.tight_layout()
    plt.show()

    # Comparación de promedios de notas
    datos = []
    for nombre, asign in [
        ('Binaria', asig_bin),
        ('Real', asig_real),
        ('Permutacional', asig_perm),
    ]:
        for ex in ['A', 'B', 'C']:
            notas_ex = notas_por_examen(asign)[ex]
            datos.append({
                'Representación': nombre,
                'Examen': ex,
                'Promedio': np.mean(notas_ex),
            })
    df_prom = pd.DataFrame(datos)

    plt.figure(figsize=(6, 4))
    sns.barplot(data=df_prom, x='Examen', y='Promedio', hue='Representación')
    plt.title('Promedio de notas por examen y representación')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

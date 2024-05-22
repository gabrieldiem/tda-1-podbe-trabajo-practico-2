# TDA 1 - Trabajo Práctico 2 - Grupo "Matcheados por G-S"

Curso: Víctor Podberezski

## Ejercicio 1

### Cómo correrlo

El código se encuentra en el `ej_1.py`. Sólo requiere Python instalado, ningún paquete extra.

Se puede correr por consola como muestra el enunciado, ejemplo:

```shell
python ./ej_1.py ./carpeta/archivo.txt personasMaximas pesoMaximo
```

Ejemplo particular:

```shell
python ./ej_1.py personas.csv 5 1000
```

O también se puede iniciar el script sin argumentos y por entrada estándar escribir el nombre/ubicación del archivo, peso máximo y cantidad de personas máxima.

### Tests

Se provee un archivo `ej_1_tests.py` que corre un set de pruebas sobre el módulo `ej_1.py`, utilizando archivos de prueba guardados en la carpeta `ej_1_test_files`.

## Ejercicio 2

### Cómo correrlo

El código se encuentra en el `ej_2.py`. Además de tener Python instalado se requiere instalar la librería de pip llamada [PuLP](https://pypi.org/project/PuLP/). PuLP es un framework para modelar problemas lineales y resolverlos con distintos algoritmos de programación lineal. Se puede instalar corriendo el comando de pip:

```shell
python -m pip install pulp
```

El código requiere un archivo de tipo CSV que tenga la siguiente estructura, donde cada actor tiene asignado su subconjunto de papeles con las respectivas ganancias:

```csv
Nombre de actor, id papel 1, ganancia papel 1, id papel 2, ganancia papel 2
Nombre de actor, id papel 1, ganancia papel 1
```

Se provee uno dentro de la carpeta `ej_2_test_files`, por lo que el código se puede ejecutar de la siguiente manera:

```shell
python ./ej_2.py ./ej_2_test_files/1.csv
```

O también se puede iniciar el script sin argumentos y por entrada estándar escribir el nombre/ubicación del archivo.

Se imprimirá por pantalla la asignación que maximice la potencialidad del problema si se encuentra una solución óptima.

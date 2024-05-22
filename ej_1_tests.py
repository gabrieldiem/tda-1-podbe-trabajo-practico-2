from ej_1 import main as mainEjercicio1


def getNombres(investigadores):
    nombres = []
    for investigador in investigadores:
        nombres.append(investigador.nombre)
    return nombres


def test01ArchivoDeLaConsigna(resultadoTests):
    print("══════════════════════════════════════════════")
    try:
        filename = "./ej_1_test_files/1.csv"
        personasMaximas = 4
        pesoMaximo = 500
        gananciaFinal, pesoFinal, investigadoresElegidos = mainEjercicio1(
            filename, personasMaximas, pesoMaximo
        )

        assert 1600 == gananciaFinal
        assert 400 == pesoFinal
        assert ["Claude Shannon", "John von Neumann", "Alan Turing"] == getNombres(
            investigadoresElegidos
        )
    except:
        print(
            "No Pasó ❌ Test 01 'test01ArchivoDeLaConsigna' con distinto peso de la consigna"
        )
        resultadoTests["noPasaron"] += 1
        return

    print(
        "Pasó ✅ Test 01 'test01ArchivoDeLaConsigna' con distinto peso de la consigna"
    )
    resultadoTests["pasaron"] += 1


def test02ArchivoDeLaConsigna(resultadoTests):
    print("══════════════════════════════════════════════")
    try:
        filename = "./ej_1_test_files/2.csv"
        personasMaximas = 5
        pesoMaximo = 1000
        gananciaFinal, pesoFinal, investigadoresElegidos = mainEjercicio1(
            filename, personasMaximas, pesoMaximo
        )

        assert 2550 == gananciaFinal
        assert 850 == pesoFinal
        assert [
            "Tim Berners-Lee",
            "Claude Shannon",
            "Dennis Ritchie",
            "John von Neumann",
            "Alan Turing",
        ] == getNombres(investigadoresElegidos)
    except:
        print("No Pasó ❌ Test 02 'test02ArchivoDeLaConsigna' con peso de la consigna")
        resultadoTests["noPasaron"] += 1
        return

    print("Pasó ✅ Test 02 'test02ArchivoDeLaConsigna' con peso de la consigna")
    resultadoTests["pasaron"] += 1


if __name__ == "__main__":
    resultadoTests = {"pasaron": 0, "noPasaraon": 0}

    test01ArchivoDeLaConsigna(resultadoTests)
    test02ArchivoDeLaConsigna(resultadoTests)

    print("══════════════════════════════════════════════")
    print(
        f"Pasaron {resultadoTests['pasaron']} tests. Fallaron {resultadoTests['noPasaraon']} tests."
    )

# (A01796071) Pruebas de sowftware y aseguramiento de la calidad

Repositorio que contiene todas las tareas de código realizadas en la materia.
Alumno: ALI MATEO CAMPOS MARTÍNEZ

## Folders

La organización de los folders es la siguiente: Número de tarea (6.2) > Ejercicio (P1) > resultados (imágenes), source (código), test (archivos txt)

## Notas

Profesor a continuación he dejado algunos comentarios justificando mis acciones dentro del código o dando claridad, con el objetivo de evitar la reducción de puntos en la tarea.


### (Tarea 6.2) Ejercicio 1
- El carpeta de resultados están las capturas de pantalla que muestea el correcto funcionamiento de la aplicación.

- pylint_2.png muestra errores de muchos argumentos, es un error de diseño, mi idea era manejar ambos CRUD (hotel y clientes) en una misma función para reutilizar funciones, aquí me doy cuenta que en pylint lo detecta como código "oloroso", probablemente sea cierto y debido al tiempo de entrega no me es posible realizar una refactorización del código.

- flake8_3.png, muestra que la línea 65 es muy larga, sin embargo, aquí no encontré otra forma de acortar la línea, sin sacrificar claridad en el código, considero que en estos casos está bien preferir un error en flake8 que intentar una asginación de variables o un cambio de nombre que no puede ser claro.

- 


### (Tarea 5.2) Ejercicio 1
- El primer resultado me dió un resultado exacto con respecto al del profesor.

- Los siguientes dos resultados fueron diferentes, al igual en en los ejercicios pasados, me temo que es debido a como el profesor manejó los errores, según entendí en las instrucciones, solo se deben gestionar los errores (para que no pare la ejecución del programa) y señalarlos (imprimirlos en consola y en el txt), me temo que tal vez el profesor convirtió los números a positivos por ejemplo.

- Los resultados (imágenes de las pruebas de ejecución), siguen el mismo patrón de la tarea pasada.


### (Tarea 4.2) Ejercicio 1
- Adicional a las pruebas otorgadas por el profesor, yo generé un archivo de texto con menos números para verificar que los cálculos fueran correctos.

- En la prueba "TC5.txt" obtengo diferentes resultados referentes a los proporcionados por el profesor, debido a que mi código no considera como un número flotante válido los siguientes textos: (ABA, 23,45, 11;54, ll). Ninguno de estos datos es válido para "python" porque no logra hacer un casteo a un número flotante, por lo que simplemente los ignora.

- En la prueba "TC6.txt" me da diferentes valores que el profesor, comprobe que estuviera obteniendo los valores reales del documento y no vi ninguna discrepancia, y como en las pruebas anterior obtuve resultado correctos puedo suponer que estos cálculos también lo son.

- Al igual que en los casos anteriores, en la prueba "TC7.txt" no pude realizar el casteo a flotante de los siguientes textos (ABBA y ERROR), en los demás números tampoco observé una discrepancia por lo que puede inferir que los cálculos son correctos.


### (Tarea 4.2) Ejercicio 2
- Para convertir a números decimales a binarios negativos me base en el siguiente artículo [CAMBIO DE SIGNO DE UN NÚMERO EN BINARIO](https://portalacademico.cch.unam.mx/cibernetica1/sistemas-de-numeracion/cambio-de-signo).

- Para comprobar el resultado de los número binarios con signo utilizé la siguiente calculadora [Código binario, inverso y complemento](https://es.planetcalc.com/747/#google_vignette).

- En un principio podría parecer que no coinciden los números binarios, sin embargo, en el programa primero tomamos el valor en binario más alto, esto va a representar los bits a utilizar, por lo que no utilizamos "arbitrariamente" cierta cantidad de bits, en el resultado del profesor, el ocupa 10 bits, según mis resultados con 7 bits es más que suficiente para representar los números de "TC4.txt".

- No entendí de donde sacó los resultados el profesor de "TC1.txt" si en el archivo todos son números altos.

- Para obtener los datos en hexadecimal me basé en el siguinete artículo [Convert Decimal To Hexa-Decimal including negative numbers](https://www.geeksforgeeks.org/dsa/convert-decimal-to-hexa-decimal-including-negative-numbers/) y en la siguinete calculadora [RapidTables](https://www.rapidtables.com/convert/number/decimal-to-binary.html?x=82)


### (Tarea 4.2) Ejercicio 3
- Ya no acomodé la frecuencia por orden descentende, sin embargo, sí comprobé que mis resultados fueran iguales.
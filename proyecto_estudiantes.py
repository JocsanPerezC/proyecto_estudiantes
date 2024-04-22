import shelve
import datetime

# Función para cargar los estudiantes desde la base de datos
def cargar_estudiantes():
    with shelve.open('estudiantes_db') as db:
        return db.get('estudiantes', {})

# Función para guardar los estudiantes en la base de datos
def guardar_estudiantes(estudiantes):
    with shelve.open('estudiantes_db') as db:
        db['estudiantes'] = estudiantes
        print("Estudiantes guardados correctamente en la base de datos.")

# Función para crear un nuevo estudiante
def crear_estudiante():
    estudiantes = cargar_estudiantes()
    
    carne = input("\nIngrese el carnet del estudiante: ")
    if carne in estudiantes:
        print("El estudiante ya existe.")
        return
    
    nombre = input("Ingrese el nombre del estudiante: ")
    carrera = input("Ingrese la carrera del estudiante: ")
    
    estudiantes[carne] = {
        "nombre": nombre,
        "carrera": carrera,
        "direccion": "",
        "telefono": "",
        "email": "",
        "fecha_nac": "",
        "cursos": {}  # Inicializar el diccionario de cursos vacío para el estudiante nuevo
    }
    guardar_estudiantes(estudiantes) # se hace el cambio en la base de datos
    print(f"Estudiante {nombre} agregado correctamente.")

# Función para matricular un nuevo curso para un estudiante existente
def matricular_curso():
    estudiantes = cargar_estudiantes()
    
    carne = input("\nIngrese el carnet del estudiante: ")
    if carne in estudiantes:
        curso = input("Ingrese el nombre del nuevo curso: ")
        nota = input("Ingrese la nota del curso (0 si aún no tiene nota): ")
        
        try:
            nota = float(nota) # se convierte en float
            if 0 <= nota <= 10:
                estudiantes[carne]["cursos"][curso] = nota
                guardar_estudiantes(estudiantes)
                print(f"Curso '{curso}' matriculado correctamente para el estudiante.")
            else:
                print("La nota debe ser un número entre 0 y 10.")
        except ValueError:
            print("Ingrese una nota válida como número entre 0 y 10.")
    else:
        print("Estudiante no encontrado.")

# Función para leer la información de todos los estudiantes
def leer_todos_los_estudiantes():
    estudiantes = cargar_estudiantes()

    print("\n--------------------------------------------")
    for estudiante_id, info in estudiantes.items():
        print(f"Información del estudiante con ID {estudiante_id}:")
        print(f"Nombre: {info['nombre']}")
        print(f"Carrera: {info['carrera']}")
        print(f"Dirección: {info['direccion']}")
        print(f"Teléfono: {info['telefono']}")
        print(f"Email: {info['email']}")
        print(f"Fecha de Nacimiento: {info['fecha_nac']}")
        print("Cursos Matriculados:")
        if info['cursos']:
            for curso, nota in info['cursos'].items():
                print(f"- {curso}: Nota {nota}")
        else:
            print("- No tiene cursos matriculados.")
        print("--------------------------------------------")

# Función para leer la información de un estudiante específico
def leer_estudiante():
    estudiantes = cargar_estudiantes()
    
    carne = input("\nIngrese el carnet del estudiante: ")
    if carne in estudiantes:
        info = estudiantes[carne]
        print("--------------------------------------------")
        print(f"Nombre: {info['nombre']}")
        print(f"Carrera: {info['carrera']}")
        print(f"Dirección: {info['direccion']}")
        print(f"Teléfono: {info['telefono']}")
        print(f"Email: {info['email']}")
        print(f"Fecha de nacimiento: {info['fecha_nac']}")
        print("--------------------------------------------")
    else:
        print("Estudiante no encontrado.")

# Función para actualizar la información de un estudiante
def actualizar_estudiante():
    estudiantes = cargar_estudiantes()
    
    carne = input("\nIngrese el carnet del estudiante: ")
    if carne in estudiantes:
        # Mostrar opciones numéricas para los campos a actualizar
        print("Opciones disponibles para actualizar:")
        print("1. Carrera")
        print("2. Dirección")
        print("3. Teléfono")
        print("4. Email")
        print("5. Fecha de nacimiento")
        print("6. Actualizar nota de un curso")
        
        opcion = input("Seleccione la opción a actualizar (1-6): ")
        
        if opcion in ['1', '2', '3', '4', '5']:  # Actualizar información personal
            campo = {
                '1': 'carrera',
                '2': 'direccion',
                '3': 'telefono',
                '4': 'email',
                '5': 'fecha_nac'
            }[opcion]
            
            if campo == 'fecha_nac': # Para solicitar fecha de nacimiento en formato YYYY-MM-DD
                
                nueva_fecha_str = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
                
                try:
                    nueva_fecha = datetime.datetime.strptime(nueva_fecha_str, '%Y-%m-%d').date()
                    estudiantes[carne][campo] = nueva_fecha
                    guardar_estudiantes(estudiantes)  # se hace el cambio en la base de datos
                    print("Fecha de nacimiento actualizada correctamente.")
                except ValueError:
                    print("Formato de fecha incorrecto. Por favor, ingrese la fecha en formato YYYY-MM-DD.")
            
            else:
                nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")
                estudiantes[carne][campo] = nuevo_valor
                guardar_estudiantes(estudiantes)  # se hace el cambio en la base de datos
                print(f"Información actualizada correctamente.")
        
        elif opcion == '6':  # Actualizar nota de un curso
            curso = input("Ingrese el nombre del curso a actualizar la nota: ")
            if curso in estudiantes[carne]["cursos"]:
                nueva_nota = input(f"Ingrese la nueva nota para el curso {curso}: ")
                try:
                    nueva_nota = float(nueva_nota) # se convierte en float
                    if 0 <= nueva_nota <= 10:
                        estudiantes[carne]["cursos"][curso] = nueva_nota
                        guardar_estudiantes(estudiantes)  # se hace el cambio en la base de datos
                        print(f"Nota actualizada correctamente para el curso {curso}.")
                    else:
                        print("La nota debe ser un número entre 0 y 10.")
                except ValueError:
                    print("Ingrese un valor numérico válido para la nota.")
            else:
                print(f"El estudiante no está matriculado en el curso {curso}.")
        
        else:
            print("Opción no válida.")
    else:
        print("Estudiante no encontrado.")

# Función para eliminar la información de un curso para un estudiante
def eliminar_curso():
    estudiantes = cargar_estudiantes()
    
    carne = input("\nIngrese el carnet del estudiante: ")
    if carne in estudiantes:
        curso = input("Ingrese el nombre del curso a eliminar: ")
        if curso in estudiantes[carne]["cursos"]:
            del estudiantes[carne]["cursos"][curso] # metodo para eliminar
            guardar_estudiantes(estudiantes) # se hace el cambio en la base de datos
            print(f"Curso '{curso}' eliminado correctamente para el estudiante.")
        else:
            print(f"El estudiante no está matriculado en el curso {curso}.")
    else:
        print("Estudiante no encontrado.")

# Función para eliminar un estudiante completo
def eliminar_estudiante():
    estudiantes = cargar_estudiantes()
    
    carne = input("\nIngrese el carnet del estudiante a eliminar: ")
    if carne in estudiantes:
        del estudiantes[carne] # metodo para eliminar
        guardar_estudiantes(estudiantes) # se hace el cambio en la base de datos
        print(f"Estudiante con carnet {carne} eliminado correctamente.")
    else:
        print("Estudiante no encontrado.")

#Función principal que implementa un menú de opciones para interactuar
def menu():
    while True:
        print("\n==== Menú ====")
        print("1. Crear nuevo estudiante")
        print("2. Matricular nuevo curso para un estudiante")
        print("3. Leer información de todos los estudiantes")
        print("4. Leer información de un estudiante específico")
        print("5. Actualizar información de un estudiante")
        print("6. Eliminar curso de un estudiante")
        print("7. Eliminar estudiante")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crear_estudiante()
        elif opcion == '2':
            matricular_curso()
        elif opcion == '3':
            leer_todos_los_estudiantes()
        elif opcion == '4':
            leer_estudiante()
        elif opcion == '5':
            actualizar_estudiante()
        elif opcion == '6':
            eliminar_curso()
        elif opcion == '7':
            eliminar_estudiante()
        elif opcion == '8':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

menu()
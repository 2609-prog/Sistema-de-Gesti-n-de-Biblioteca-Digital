# Sistema de Gestión Digital

# Clase Libro
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.info = (titulo, autor)  # tupla (inmutable)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"{self.info[0]} de {self.info[1]} - Categoria: {self.categoria} - ISBN: {self.isbn}"


# Clase Usuario
class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        self.libros_prestados = []  # lista de libros prestados

    def __str__(self):
        return f"Usuario: {self.nombre} - ID: {self.user_id} - Libros Prestados: {len(self.libros_prestados)}"


# Clase Biblioteca
class Biblioteca:
    def __init__(self):
        self.libros_disponibles = {}      # Diccionario ISBN -> Libro
        self.usuarios_registrados = set() # IDs únicos
        self.datos_usuarios = {}          # ID -> Usuario

    # Gestión de libros
    def agregar_libro(self, libro):
        if libro.isbn not in self.libros_disponibles:
            self.libros_disponibles[libro.isbn] = libro
            print(f"Libro agregado: {libro}")
        else:
            print(f"El libro con ISBN {libro.isbn} ya existe en la biblioteca.")

    def quitar_libro(self, isbn):
        if isbn in self.libros_disponibles:
            del self.libros_disponibles[isbn]
            print(f"Libro con ISBN {isbn} ha sido removido de la biblioteca.")
        else:
            print(f"No se encontró el libro con ISBN {isbn} en la biblioteca.")

    # Gestión de usuarios
    def registrar_usuario(self, usuario):
        if usuario.user_id not in self.usuarios_registrados:
            self.usuarios_registrados.add(usuario.user_id)
            self.datos_usuarios[usuario.user_id] = usuario
            print(f"Usuario {usuario.nombre} registrado con ID {usuario.user_id}")
        else:
            print(f"El usuario con ID {usuario.user_id} ya está registrado.")

    def dar_baja_usuario(self, user_id):
        if user_id in self.usuarios_registrados:
            self.usuarios_registrados.remove(user_id)
            self.datos_usuarios.pop(user_id, None)
            print(f"Usuario con ID {user_id} ha sido dado de baja.")
        else:
            print(f"No se encontró el usuario con ID {user_id}.")

    # Gestión de préstamos
    def prestar_libro(self, isbn, user_id):
        if user_id not in self.usuarios_registrados:
            print(f"Usuario con ID {user_id} no está registrado.")
            return
        if isbn not in self.libros_disponibles:
            print(f"El libro con ISBN {isbn} no está disponible.")
            return

        libro = self.libros_disponibles.pop(isbn)
        self.datos_usuarios[user_id].libros_prestados.append(libro)
        print(f"Libro prestado: {libro} al usuario {self.datos_usuarios[user_id].nombre}")

    def devolver_libro(self, isbn, user_id):
        if user_id not in self.usuarios_registrados:
            print("Usuario no registrado.")
            return

        usuario = self.datos_usuarios[user_id]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros_disponibles[isbn] = libro
                print(f"Libro con ISBN {isbn} devuelto por {usuario.nombre}")
                return
        print(f"El usuario {usuario.nombre} no tiene el libro con ISBN {isbn} prestado.")

    # Búsqueda de libros
    def buscar_por_titulo(self, titulo):
        return [libro for libro in self.libros_disponibles.values() if libro.info[0].lower() == titulo.lower()]

    def buscar_por_autor(self, autor):
        return [libro for libro in self.libros_disponibles.values() if libro.info[1].lower() == autor.lower()]

    def buscar_por_categoria(self, categoria):
        return [libro for libro in self.libros_disponibles.values() if libro.categoria.lower() == categoria.lower()]

    # Listar libros prestados
    def listar_libros_prestados(self, user_id):
        if user_id in self.datos_usuarios:
            usuario = self.datos_usuarios[user_id]
            if usuario.libros_prestados:
                print(f"Libros prestados por {usuario.nombre}:")
                for libro in usuario.libros_prestados:
                    print(f" - {libro}")
            else:
                print(f"El usuario {usuario.nombre} no tiene libros prestados.")
        else:
            print("Usuario no registrado.")


# PRUEBA DEL SISTEMA
if __name__ == "__main__":
    biblioteca = Biblioteca()
    libro1 = Libro("Cien Años de Soledad", "Gabriel Garcia Marquez", "Novela", "ISBN001")
    libro2 = Libro("1984", "George Orwell", "Distopía", "ISBN002")
    libro3 = Libro("El Principito", "Antoine de Saint-Exupéry", "Fantasía", "ISBN003")

    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)
    biblioteca.agregar_libro(libro3)

    usuario1 = Usuario("Anastasia", "U001")
    usuario2 = Usuario("Bruno", "U002")

    biblioteca.registrar_usuario(usuario1)
    biblioteca.registrar_usuario(usuario2)

    biblioteca.prestar_libro("ISBN001", "U001")
    biblioteca.prestar_libro("ISBN002", "U002")

    biblioteca.listar_libros_prestados("U001")
    biblioteca.listar_libros_prestados("U002")

    biblioteca.devolver_libro("ISBN001", "U001")

    resultados = biblioteca.buscar_por_categoria("Novela")
    print("Resultados de búsqueda por categoría 'Novela':")
    for r in resultados:
        print(" -", r)

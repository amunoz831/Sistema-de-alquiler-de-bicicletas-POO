import tkinter as tk
from datetime import datetime

class Bicicleta:
    def __init__(self, numero_serie, modelo):
        self.numero_serie = numero_serie
        self.modelo = modelo
        self.disponible = True

    def alquilar(self):
        self.disponible = False

    def devolver(self):
        self.disponible = True

class Usuario:
    def __init__(self, nombre, correo, identificacion):
        self.nombre = nombre
        self.correo = correo
        self.identificacion = identificacion

class Tarifas:
    def __init__(self):
        self.tarifas = {}

    def agregar_tarifa(self, numero_serie, tarifa_por_hora):
        self.tarifas[numero_serie] = tarifa_por_hora

    def obtener_tarifa(self, numero_serie):
        return self.tarifas.get(numero_serie, 0)

class SistemaAlquiler:
    def __init__(self):
        self.bicicletas = []
        self.usuarios = []
        self.transacciones = []
        self.tarifas = Tarifas()  
        self.registrar_bicicletas_disponibles()  

    def registrar_bicicleta(self, numero_serie, modelo, tarifa_por_hora):
        bicicleta = Bicicleta(numero_serie, modelo)
        self.tarifas.agregar_tarifa(numero_serie, tarifa_por_hora)  
        self.bicicletas.append(bicicleta)

    def registrar_bicicletas_disponibles(self):
        seriales_disponibles = ["B001", "B002", "B003", "B004", "B005", "B006", "B007", "B008", "B009", "B010",
                                "B011", "B012", "B013", "B014", "B015", "B016", "B017", "B018", "B019", "B020"]
        for serial in seriales_disponibles:
            self.registrar_bicicleta(serial, "Modelo Ejemplo", 5.0)  

    def registrar_usuario(self, nombre, correo, identificacion):
        usuario = Usuario(nombre, correo, identificacion)
        self.usuarios.append(usuario)

    def obtener_bicicletas_disponibles(self):
        disponibles = [bicicleta for bicicleta in self.bicicletas if bicicleta.disponible]
        return disponibles

    def alquilar_bicicleta(self, usuario, numero_serie):
        for bicicleta in self.bicicletas:
            if bicicleta.numero_serie == numero_serie and bicicleta.disponible:
                bicicleta.alquilar()
                self.transacciones.append((usuario, bicicleta, datetime.now()))
                return True
        return False

    def devolver_bicicleta(self, usuario, numero_serie):
        for usuario, bicicleta, inicio_alquiler in self.transacciones:
            if bicicleta.numero_serie == numero_serie and usuario == usuario and not bicicleta.disponible:
                inicio_alquiler = inicio_alquiler
                tiempo_alquiler = (datetime.now() - inicio_alquiler).total_seconds() / 3600
                if tiempo_alquiler <= 0.5:  
                    return "El servicio ha sido gratis."
                else:
                    bicicleta.devolver()
                    costo = self.calcular_tarifa(tiempo_alquiler)
                    self.transacciones.append((usuario, bicicleta, inicio_alquiler, datetime.now(), costo))
                    return f"La tarifa a cobrar es de: ${costo}"

        return "No se pudo devolver la bicicleta."

    def calcular_tarifa(self, tiempo_alquiler):
        tarifa_hora = 800  
        tiempo_gratis = 0.5  
        if tiempo_alquiler <= tiempo_gratis:
            return 0
        else:
            tiempo_cobrar = tiempo_alquiler - tiempo_gratis
            tarifa_total = tiempo_cobrar * tarifa_hora
            return tarifa_total

class InterfazAlquilerBicicletas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Alquiler de Bicicletas")

        self.sistema = SistemaAlquiler()

        self.usuario_label = tk.Label(ventana, text="Registro de Usuario:")
        self.usuario_label.pack()

        self.nombre_label = tk.Label(ventana, text="Nombre:")
        self.nombre_label.pack()
        self.nombre_entry = tk.Entry(ventana)
        self.nombre_entry.pack()

        self.correo_label = tk.Label(ventana, text="Correo:")
        self.correo_label.pack()
        self.correo_entry = tk.Entry(ventana)
        self.correo_entry.pack()

        self.identificacion_label = tk.Label(ventana, text="Identificación:")
        self.identificacion_label.pack()
        self.identificacion_entry = tk.Entry(ventana)
        self.identificacion_entry.pack()

        self.registrar_usuario_button = tk.Button(ventana, text="Registrar Usuario", command=self.registrar_usuario)
        self.registrar_usuario_button.pack()

        self.bicicleta_label = tk.Label(ventana, text="Número de Serie de Bicicleta:")
        self.bicicleta_label.pack()

        self.numero_serie_entry = tk.Entry(ventana)
        self.numero_serie_entry.pack()

        self.alquilar_button = tk.Button(ventana, text="Alquilar Bicicleta", command=self.alquilar_bicicleta)
        self.alquilar_button.pack()

        self.devolver_button = tk.Button(ventana, text="Devolver Bicicleta", command=self.devolver_bicicleta)
        self.devolver_button.pack()

        self.resultado_label = tk.Label(ventana, text="")
        self.resultado_label.pack()

        self.bicicletas_disponibles_label = tk.Label(ventana, text="Bicicletas Disponibles:")
        self.bicicletas_disponibles_label.pack()

        self.bicicletas_disponibles_listbox = tk.Listbox(ventana)
        self.bicicletas_disponibles_listbox.pack()

        self.tarifa_label = tk.Label(ventana, text="")
        self.tarifa_label.pack()

        self.actualizar_lista_bicicletas_disponibles()

    def registrar_usuario(self):
        nombre = self.nombre_entry.get()
        correo = self.correo_entry.get()
        identificacion = self.identificacion_entry.get()
        self.sistema.registrar_usuario(nombre, correo, identificacion)
        self.resultado_label.config(text=f"Usuario {nombre} registrado correctamente.")

    def alquilar_bicicleta(self):
        numero_serie = self.numero_serie_entry.get()
        if not self.sistema.usuarios:
            self.resultado_label.config(text="No hay usuarios registrados. Registre al menos uno antes de alquilar.")
            return
        usuario = self.sistema.usuarios[0]  
        if self.sistema.alquilar_bicicleta(usuario, numero_serie):
            self.resultado_label.config(text=f"Bicicleta {numero_serie} alquilada.")
            self.actualizar_lista_bicicletas_disponibles()
        else:
            self.resultado_label.config(text=f"Bicicleta {numero_serie} no disponible.")

    def devolver_bicicleta(self):
        numero_serie = self.numero_serie_entry.get()
        if not self.sistema.usuarios:
            self.resultado_label.config(text="No hay usuarios registrados. Registre al menos uno antes de devolver.")
            return
        usuario = self.sistema.usuarios[0]  
        resultado = self.sistema.devolver_bicicleta(usuario, numero_serie)
        if "gratis" in resultado:
            self.resultado_label.config(text=resultado)
            self.tarifa_label.config(text="")
        elif "tarifa" in resultado:
            self.resultado_label.config(text=resultado)
            self.tarifa_label.config(text="La tarifa debe ser pagada en el corresponsal Metro más cercano o sus reemplazos para volver a usar el servicio.")
        else:
            self.resultado_label.config(text=resultado)
            self.tarifa_label.config(text="")

    def actualizar_lista_bicicletas_disponibles(self):
        bicicletas_disponibles = self.sistema.obtener_bicicletas_disponibles()
        self.bicicletas_disponibles_listbox.delete(0, tk.END)  
        for bicicleta in bicicletas_disponibles:
            self.bicicletas_disponibles_listbox.insert(tk.END, bicicleta.numero_serie)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazAlquilerBicicletas(ventana)
    ventana.mainloop()

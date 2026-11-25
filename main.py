import tkinter as tk
from tkinter import ttk, messagebox
from logica import obtener_datos_bce, convertir_divisa


class ConversorApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Conversor de Divisas (BCE)")
        self.ventana.geometry("380x320")
        self.ventana.resizable(False, False)

        # Carga automática de los datos del BCE al iniciar
        try:
            self.fecha, self.tasas = obtener_datos_bce()
        except Exception as e:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudieron cargar los datos del BCE:\n{e}"
            )
            self.ventana.destroy()
            return

        self.monedas = list(self.tasas.keys())
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        tk.Label(
            self.ventana,
            text="Conversor de Divisas (BCE)",
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 5))

        # Fecha de actualización del XML
        tk.Label(
            self.ventana,
            text=f"Fecha de actualización: {self.fecha}",
            font=("Arial", 9),
            fg="gray"
        ).pack(pady=(0, 15))

        # Marco para los campos del formulario
        marco = tk.Frame(self.ventana)
        marco.pack(pady=5)

        # Cantidad a convertir
        tk.Label(marco, text="Cantidad:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
        self.entrada_cantidad = tk.Entry(marco, width=18)
        self.entrada_cantidad.insert(0, "100")
        self.entrada_cantidad.grid(row=0, column=1, pady=6)

        # Moneda de origen
        tk.Label(marco, text="Moneda origen:").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.combo_origen = ttk.Combobox(marco, values=self.monedas, state="readonly", width=15)
        self.combo_origen.set("EUR")
        self.combo_origen.grid(row=1, column=1, pady=6)

        # Moneda de destino
        tk.Label(marco, text="Moneda destino:").grid(row=2, column=0, sticky="e", padx=8, pady=6)
        self.combo_destino = ttk.Combobox(marco, values=self.monedas, state="readonly", width=15)
        self.combo_destino.set("USD" if "USD" in self.monedas else self.monedas[0])
        self.combo_destino.grid(row=2, column=1, pady=6)

        # Botón para calcular
        tk.Button(
            self.ventana,
            text="Calcular Conversión",
            command=self.calcular,
            bg="#0078D7",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=5
        ).pack(pady=15)

        # Etiqueta para mostrar el resultado o errores
        self.etiqueta_resultado = tk.Label(
            self.ventana,
            text="Introduce una cantidad y pulsa calcular.",
            font=("Arial", 11, "bold")
        )
        self.etiqueta_resultado.pack(pady=5)

    def calcular(self):
        texto_importe = self.entrada_cantidad.get().strip().replace(",", ".")

        # Validación de entrada numérica
        try:
            importe = float(texto_importe)
        except ValueError:
            self.etiqueta_resultado.config(
                text="Error: introduce un número válido.",
                fg="red"
            )
            return

        if importe < 0:
            self.etiqueta_resultado.config(
                text="Error: la cantidad no puede ser negativa.",
                fg="red"
            )
            return

        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        resultado = convertir_divisa(importe, origen, destino, self.tasas)

        self.etiqueta_resultado.config(
            text=f"{importe:.2f} {origen} = {resultado:.2f} {destino}",
            fg="green"
        )


if __name__ == "__main__":
    raiz = tk.Tk()
    app = ConversorApp(raiz)
    raiz.mainloop()

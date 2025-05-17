import ttkbootstrap as ttk
from caracteristicas_productos import CaracteristicasProductos
from cayal.parametros_contpaqi import ParametrosContpaqi


if __name__ == '__main__':
    parametros = ParametrosContpaqi()
    #parametros.cadena_conexion = 'Mac'
    #parametros.id_principal = 1170

    ventana = ttk.Window()
    instancia = CaracteristicasProductos(ventana, parametros)
    ventana.mainloop()
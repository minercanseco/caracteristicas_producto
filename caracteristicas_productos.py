from cayal.ventanas import Ventanas
from cayal.comandos_base_datos import ComandosBaseDatos
from cayal.util import Utilerias

class CaracteristicasProductos:
    def __init__(self, master, parametros):
        self._parametros = parametros
        self._utilerias = Utilerias()
        self._product_id = self._parametros.id_principal
        self._info_producto = {}
        self._master = master
        self._ventanas = Ventanas(self._master)
        self._base_de_datos = ComandosBaseDatos(self._parametros.cadena_conexion)

        self._cargar_componentes()
        self._rellenar_componentes()
        self._cargar_eventos()
        self._agregar_validaciones()
        self._ventanas.configurar_ventana_ttkbootstrap(titulo='Características producto')

    def _cargar_componentes(self):
        componentes = [
            ('tbx_producto', 'Producto:'),
            ('tbx_clave', 'Clave:'),
            ('cbx_area', 'Área:'),
            ('tbx_unidad', 'Unidad:'),
            ('tbx_equivalencia', 'Equiva:'),
            ('btn_guardar', 'Guardar')

        ]
        self._ventanas.crear_formulario_simple(componentes)

    def _rellenar_componentes(self):
        areas = ['Minisuper', 'Producción', 'Almacén']
        self._ventanas.rellenar_cbx('cbx_area', areas, sin_seleccione=True)

        self._info_producto = self._buscar_info_producto(self._product_id)

        equivalencia = self._utilerias.redondear_valor_cantidad_a_decimal(self._info_producto['Equivalencia'])

        self._ventanas.insertar_input_componente('tbx_equivalencia', equivalencia)
        self._ventanas.insertar_input_componente('tbx_producto', self._info_producto['ProductName'])
        self._ventanas.insertar_input_componente('tbx_clave', self._info_producto['ProductKey'])
        self._ventanas.insertar_input_componente('tbx_unidad', self._info_producto['Unit'])
        self._ventanas.insertar_input_componente('cbx_area', self._info_producto['Area'])


        bloqueados = ['tbx_producto', 'tbx_clave', 'tbx_unidad', 'tbx_equivalencia']
        for componente in bloqueados:
            if componente == 'tbx_equivalencia' and self._info_producto['ClaveUnidad'] == 'KGM':
                    continue

            self._ventanas.bloquear_componente(componente)

    def _buscar_info_producto(self, product_id):
        consulta =  self._base_de_datos.fetchall("""
            SELECT  ProductName,
                    ProductKey,
                    ISNULL(CAST(Equivalencia AS DECIMAL(10, 2)), 0) AS Equivalencia,
                    Unit,
                    ClaveUnidad,
                    CASE WHEN ProductTypeIDCayal = 0 THEN 'Minisuper'
						WHEN ProductTypeIDCayal = 1 THEN 'Producción'
						ELSE 'Almacén' END Area
            FROM orgProduct WHERE ProductID = ?
        """, (product_id,))

        if consulta:
            return consulta[0]

    def _cargar_eventos(self):
        eventos = {
            'btn_cancelar': self._master.destroy,
            'btn_guardar': self._guardar_caracteristicas
        }
        self._ventanas.cargar_eventos(eventos)

    def _agregar_validaciones(self):
        self._ventanas.agregar_validacion_tbx('tbx_equivalencia', 'cantidad')

    def _guardar_caracteristicas(self):
        area = self._ventanas.obtener_input_componente('cbx_area')

        areas_ids = {
            'Minisuper': 0,
            'Producción': 1,
            'Almacén': 2
        }

        equivalencia = self._ventanas.obtener_input_componente('tbx_equivalencia')

        if not self._utilerias.es_cantidad(equivalencia):
            self._ventanas.mostrar_mensaje('Ingrese un valor válido para la equivalencia.')
            return

        area_id = areas_ids[area]

        self._base_de_datos.command("""
            UPDATE orgProduct SET ProductTypeIDCayal = ?, Equivalencia = ?
            WHERE ProductID = ?
        """,(area_id, equivalencia, self._product_id,))

        self._master.destroy()



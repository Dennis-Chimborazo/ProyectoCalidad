from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestTechstoreBaseConocimiento(TransactionCase):

    def setUp(self):
        super().setUp()

        self.TipoEquipo = self.env["techstore.tipo.equipo"]
        self.BaseConocimiento = self.env["techstore.base.conocimiento"]

        self.tipo_equipo = self.TipoEquipo.create({
            "name": "Laptop Base Test",
            "descripcion": "Tipo de equipo para base de conocimiento.",
            "activo": True,
        })

    def test_01_crear_base_conocimiento_valida(self):
        registro = self.BaseConocimiento.create({
            "error_title": "Equipo no enciende",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "El equipo no prende ni muestra señales de energía.",
            "root_cause": "Posible falla en fuente de poder o batería.",
            "solution": "Revisar cargador, batería, fuente y placa principal.",
            "keywords": "energia, bateria, cargador",
            "activo": True,
        })

        self.assertTrue(registro.id)
        self.assertEqual(registro.error_title, "Equipo no enciende")
        self.assertEqual(registro.equipment_type_id.id, self.tipo_equipo.id)
        self.assertTrue(registro.activo)

    def test_02_titulo_menor_a_cinco_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.BaseConocimiento.create({
                "error_title": "Err",
                "equipment_type_id": self.tipo_equipo.id,
                "symptoms": "El equipo presenta síntomas suficientes para validar.",
                "root_cause": "La causa raíz tiene longitud suficiente.",
                "solution": "La solución documentada tiene longitud suficiente.",
            })

    def test_03_sintomas_menor_a_diez_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.BaseConocimiento.create({
                "error_title": "Pantalla azul",
                "equipment_type_id": self.tipo_equipo.id,
                "symptoms": "Corto",
                "root_cause": "La causa raíz tiene longitud suficiente.",
                "solution": "La solución documentada tiene longitud suficiente.",
            })

    def test_04_causa_raiz_menor_a_diez_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.BaseConocimiento.create({
                "error_title": "Sistema lento",
                "equipment_type_id": self.tipo_equipo.id,
                "symptoms": "El sistema responde lentamente al iniciar.",
                "root_cause": "Corto",
                "solution": "La solución documentada tiene longitud suficiente.",
            })

    def test_05_solucion_menor_a_diez_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.BaseConocimiento.create({
                "error_title": "No conecta WiFi",
                "equipment_type_id": self.tipo_equipo.id,
                "symptoms": "El equipo no logra conectarse a la red inalámbrica.",
                "root_cause": "Controlador de red dañado o desactualizado.",
                "solution": "Corto",
            })

    def test_06_normalizar_datos_al_crear(self):
        registro = self.BaseConocimiento.create({
            "error_title": "   Falla de teclado   ",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Algunas teclas no responden correctamente.",
            "root_cause": "Suciedad o daño físico en el teclado.",
            "solution": "Realizar limpieza o reemplazar el teclado.",
            "keywords": " TECLADO, LIMPIEZA, FALLA ",
            "activo": True,
        })

        self.assertEqual(registro.error_title, "Falla de teclado")
        self.assertEqual(registro.keywords, "teclado, limpieza, falla")

    def test_07_normalizar_datos_al_actualizar(self):
        registro = self.BaseConocimiento.create({
            "error_title": "Falla inicial de audio",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "El equipo no reproduce sonido correctamente.",
            "root_cause": "Controlador de audio dañado o mal configurado.",
            "solution": "Actualizar controlador y revisar configuración de audio.",
            "keywords": "audio",
            "activo": True,
        })

        registro.write({
            "error_title": "   Falla de audio actualizada   ",
            "keywords": " AUDIO, DRIVER ",
        })

        self.assertEqual(registro.error_title, "Falla de audio actualizada")
        self.assertEqual(registro.keywords, "audio, driver")

    def test_08_titulo_duplicado_mismo_tipo_debe_fallar(self):
        self.BaseConocimiento.create({
            "error_title": "Falla duplicada test",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "El síntoma registrado tiene longitud suficiente.",
            "root_cause": "La causa registrada tiene longitud suficiente.",
            "solution": "La solución registrada tiene longitud suficiente.",
            "keywords": "duplicado",
            "activo": True,
        })

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(Exception):
                self.BaseConocimiento.create({
                    "error_title": "Falla duplicada test",
                    "equipment_type_id": self.tipo_equipo.id,
                    "symptoms": "Otro síntoma registrado con longitud suficiente.",
                    "root_cause": "Otra causa registrada con longitud suficiente.",
                    "solution": "Otra solución registrada con longitud suficiente.",
                    "keywords": "duplicado",
                    "activo": True,
                })

    def test_09_mismo_titulo_en_otro_tipo_debe_permitirse(self):
        otro_tipo = self.TipoEquipo.create({
            "name": "Impresora Base Test",
            "descripcion": "Tipo de equipo alterno para pruebas.",
            "activo": True,
        })

        primero = self.BaseConocimiento.create({
            "error_title": "Falla compartida por tipo",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntoma válido para el primer tipo de equipo.",
            "root_cause": "Causa válida para el primer tipo de equipo.",
            "solution": "Solución válida para el primer tipo de equipo.",
            "keywords": "tipo uno",
            "activo": True,
        })

        segundo = self.BaseConocimiento.create({
            "error_title": "Falla compartida por tipo",
            "equipment_type_id": otro_tipo.id,
            "symptoms": "Síntoma válido para el segundo tipo de equipo.",
            "root_cause": "Causa válida para el segundo tipo de equipo.",
            "solution": "Solución válida para el segundo tipo de equipo.",
            "keywords": "tipo dos",
            "activo": True,
        })

        self.assertTrue(primero.id)
        self.assertTrue(segundo.id)
        self.assertNotEqual(primero.equipment_type_id.id, segundo.equipment_type_id.id)

    def test_10_base_conocimiento_to_dict(self):
        registro = self.BaseConocimiento.create({
            "error_title": "Falla de pantalla",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "La pantalla muestra líneas o parpadeos constantes.",
            "root_cause": "Cable flex dañado o pantalla defectuosa.",
            "solution": "Revisar cable flex y reemplazar pantalla si aplica.",
            "keywords": "pantalla, flex",
            "activo": True,
        })

        data = registro._base_conocimiento_to_dict()

        self.assertEqual(data["id"], registro.id)
        self.assertEqual(data["error_title"], "Falla de pantalla")
        self.assertEqual(data["equipment_type_id"], self.tipo_equipo.id)
        self.assertEqual(data["equipment_type"], self.tipo_equipo.name)
        self.assertEqual(data["keywords"], "pantalla, flex")
        self.assertTrue(data["activo"])

    def test_11_get_base_conocimiento_data_sin_filtro(self):
        self.BaseConocimiento.create({
            "error_title": "Falla general de prueba",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntomas generales con longitud suficiente.",
            "root_cause": "Causa general con longitud suficiente.",
            "solution": "Solución general con longitud suficiente.",
            "keywords": "general",
            "activo": True,
        })

        data = self.BaseConocimiento.get_base_conocimiento_data()

        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)

    def test_12_get_base_conocimiento_data_filtrado_por_tipo(self):
        otro_tipo = self.TipoEquipo.create({
            "name": "Router Base Test",
            "descripcion": "Tipo de equipo para filtro.",
            "activo": True,
        })

        self.BaseConocimiento.create({
            "error_title": "Falla para laptop",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntoma válido para laptop de prueba.",
            "root_cause": "Causa válida para laptop de prueba.",
            "solution": "Solución válida para laptop de prueba.",
            "keywords": "laptop",
            "activo": True,
        })

        self.BaseConocimiento.create({
            "error_title": "Falla para router",
            "equipment_type_id": otro_tipo.id,
            "symptoms": "Síntoma válido para router de prueba.",
            "root_cause": "Causa válida para router de prueba.",
            "solution": "Solución válida para router de prueba.",
            "keywords": "router",
            "activo": True,
        })

        data = self.BaseConocimiento.get_base_conocimiento_data(self.tipo_equipo.id)

        self.assertTrue(len(data) >= 1)

        for item in data:
            self.assertEqual(item["equipment_type_id"], self.tipo_equipo.id)

    def test_13_get_base_conocimiento_by_id_custom(self):
        registro = self.BaseConocimiento.create({
            "error_title": "Falla por ID",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntomas suficientes para búsqueda por ID.",
            "root_cause": "Causa suficiente para búsqueda por ID.",
            "solution": "Solución suficiente para búsqueda por ID.",
            "keywords": "id",
            "activo": True,
        })

        data = self.BaseConocimiento.get_base_conocimiento_by_id_custom(registro.id)

        self.assertEqual(data["id"], registro.id)
        self.assertEqual(data["error_title"], "Falla por ID")

    def test_14_get_base_conocimiento_by_id_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.BaseConocimiento.get_base_conocimiento_by_id_custom(999999)

    def test_15_create_base_conocimiento_custom(self):
        data = self.BaseConocimiento.create_base_conocimiento_custom({
            "error_title": "Falla custom",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntomas válidos para método custom.",
            "root_cause": "Causa válida para método custom.",
            "solution": "Solución válida para método custom.",
            "keywords": "custom",
            "activo": True,
        })

        self.assertIn("id", data)
        self.assertEqual(data["error_title"], "Falla custom")
        self.assertEqual(data["equipment_type_id"], self.tipo_equipo.id)

    def test_16_update_base_conocimiento_custom(self):
        registro = self.BaseConocimiento.create({
            "error_title": "Falla antes de actualizar",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntomas antes de actualizar registro.",
            "root_cause": "Causa antes de actualizar registro.",
            "solution": "Solución antes de actualizar registro.",
            "keywords": "antes",
            "activo": True,
        })

        data = self.BaseConocimiento.update_base_conocimiento_custom(registro.id, {
            "error_title": "Falla actualizada",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntomas actualizados correctamente.",
            "root_cause": "Causa actualizada correctamente.",
            "solution": "Solución actualizada correctamente.",
            "keywords": "actualizado",
            "activo": True,
        })

        self.assertEqual(data["id"], registro.id)
        self.assertEqual(data["error_title"], "Falla actualizada")
        self.assertEqual(data["keywords"], "actualizado")

    def test_17_update_base_conocimiento_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.BaseConocimiento.update_base_conocimiento_custom(999999, {
                "error_title": "No existe",
                "equipment_type_id": self.tipo_equipo.id,
                "symptoms": "Síntomas válidos para registro inexistente.",
                "root_cause": "Causa válida para registro inexistente.",
                "solution": "Solución válida para registro inexistente.",
                "keywords": "no existe",
                "activo": True,
            })

    def test_18_toggle_base_conocimiento_activo_custom(self):
        registro = self.BaseConocimiento.create({
            "error_title": "Falla toggle",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "Síntomas válidos para toggle.",
            "root_cause": "Causa válida para toggle.",
            "solution": "Solución válida para toggle.",
            "keywords": "toggle",
            "activo": True,
        })

        data = self.BaseConocimiento.toggle_base_conocimiento_activo_custom(registro.id)

        self.assertEqual(data["id"], registro.id)
        self.assertFalse(data["activo"])

        registro.invalidate_recordset()
        self.assertFalse(registro.activo)

    def test_19_toggle_base_conocimiento_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.BaseConocimiento.toggle_base_conocimiento_activo_custom(999999)
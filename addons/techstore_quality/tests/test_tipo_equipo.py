from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger
import uuid


@tagged("post_install", "-at_install")
class TestTechstoreTipoEquipo(TransactionCase):

    def setUp(self):
        super().setUp()
        self.TipoEquipo = self.env["techstore.tipo.equipo"]

    def _unique_name(self, label):
        return f"TEST Tipo Equipo {label} {uuid.uuid4().hex[:8]}"

    def test_01_crear_tipo_equipo_valido(self):
        name = self._unique_name("Laptop")

        tipo = self.TipoEquipo.create({
            "name": name,
            "descripcion": "Equipo portátil de uso general.",
            "activo": True,
        })

        self.assertTrue(tipo.id)
        self.assertEqual(tipo.name, name)
        self.assertEqual(tipo.descripcion, "Equipo portátil de uso general.")
        self.assertTrue(tipo.activo)

    def test_02_nombre_menor_a_tres_caracteres_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.TipoEquipo.create({
                "name": "PC",
                "descripcion": "Nombre demasiado corto.",
                "activo": True,
            })

    def test_03_normalizar_nombre_al_crear(self):
        name = self._unique_name("Impresora")

        tipo = self.TipoEquipo.create({
            "name": f"   {name}   ",
            "descripcion": "Equipo de impresión.",
            "activo": True,
        })

        self.assertEqual(tipo.name, name)

    def test_04_normalizar_nombre_al_actualizar(self):
        name = self._unique_name("Router")
        new_name = self._unique_name("Router Empresarial")

        tipo = self.TipoEquipo.create({
            "name": name,
            "descripcion": "Equipo de red.",
            "activo": True,
        })

        tipo.write({
            "name": f"   {new_name}   "
        })

        self.assertEqual(tipo.name, new_name)

    def test_05_nombre_duplicado_debe_fallar(self):
        name = self._unique_name("Servidor")

        self.TipoEquipo.create({
            "name": name,
            "descripcion": "Equipo servidor.",
            "activo": True,
        })

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(Exception):
                self.TipoEquipo.create({
                    "name": name,
                    "descripcion": "Equipo servidor duplicado.",
                    "activo": True,
                })

    def test_06_tipo_equipo_to_dict(self):
        name = self._unique_name("Monitor")

        tipo = self.TipoEquipo.create({
            "name": name,
            "descripcion": "Pantalla para computador.",
            "activo": True,
        })

        data = tipo._tipo_equipo_to_dict()

        self.assertEqual(data["id"], tipo.id)
        self.assertEqual(data["name"], name)
        self.assertEqual(data["descripcion"], "Pantalla para computador.")
        self.assertTrue(data["activo"])

    def test_07_get_tipos_equipo_data(self):
        name = self._unique_name("Tablet")

        self.TipoEquipo.create({
            "name": name,
            "descripcion": "Dispositivo táctil.",
            "activo": True,
        })

        data = self.TipoEquipo.get_tipos_equipo_data()

        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)

        nombres = [item["name"] for item in data]
        self.assertIn(name, nombres)

    def test_08_get_tipo_equipo_by_id_custom(self):
        name = self._unique_name("Scanner")

        tipo = self.TipoEquipo.create({
            "name": name,
            "descripcion": "Equipo de digitalización.",
            "activo": True,
        })

        data = self.TipoEquipo.get_tipo_equipo_by_id_custom(tipo.id)

        self.assertEqual(data["id"], tipo.id)
        self.assertEqual(data["name"], name)

    def test_09_get_tipo_equipo_by_id_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.TipoEquipo.get_tipo_equipo_by_id_custom(999999)

    def test_10_create_tipo_equipo_custom(self):
        name = self._unique_name("Camara")

        data = self.TipoEquipo.create_tipo_equipo_custom({
            "name": name,
            "descripcion": "Equipo de captura de imagen.",
            "activo": True,
        })

        self.assertIn("id", data)
        self.assertEqual(data["name"], name)
        self.assertEqual(data["descripcion"], "Equipo de captura de imagen.")
        self.assertTrue(data["activo"])

    def test_11_update_tipo_equipo_custom(self):
        name = self._unique_name("Switch")
        new_name = self._unique_name("Switch Administrable")

        tipo = self.TipoEquipo.create({
            "name": name,
            "descripcion": "Equipo de red básico.",
            "activo": True,
        })

        data = self.TipoEquipo.update_tipo_equipo_custom(tipo.id, {
            "name": new_name,
            "descripcion": "Equipo de red administrable.",
            "activo": True,
        })

        self.assertEqual(data["id"], tipo.id)
        self.assertEqual(data["name"], new_name)
        self.assertEqual(data["descripcion"], "Equipo de red administrable.")

    def test_12_update_tipo_equipo_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.TipoEquipo.update_tipo_equipo_custom(999999, {
                "name": "TEST No Existe",
                "descripcion": "Registro inexistente.",
                "activo": True,
            })

    def test_13_toggle_tipo_equipo_activo_custom(self):
        name = self._unique_name("Proyector")

        tipo = self.TipoEquipo.create({
            "name": name,
            "descripcion": "Equipo de proyección.",
            "activo": True,
        })

        data = self.TipoEquipo.toggle_tipo_equipo_activo_custom(tipo.id)

        self.assertEqual(data["id"], tipo.id)
        self.assertFalse(data["activo"])

        tipo.invalidate_recordset()
        self.assertFalse(tipo.activo)

    def test_14_toggle_tipo_equipo_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.TipoEquipo.toggle_tipo_equipo_activo_custom(999999)
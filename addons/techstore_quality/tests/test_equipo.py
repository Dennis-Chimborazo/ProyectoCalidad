from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger
import uuid


@tagged("post_install", "-at_install")
class TestTechstoreEquipo(TransactionCase):

    def setUp(self):
        super().setUp()

        self.TipoEquipo = self.env["techstore.tipo.equipo"]
        self.Equipo = self.env["techstore.equipo"]
        self.DetalleEquipo = self.env["techstore.detalle.equipo"]

        self.test_uid = uuid.uuid4().hex[:8]

        self.tipo_equipo = self.TipoEquipo.create({
            "name": f"TEST Tipo Equipo {self.test_uid}",
            "descripcion": "Tipo de equipo usado para pruebas unitarias.",
            "activo": True,
        })

    def _crear_equipo(self, suffix="001"):
        return self.Equipo.create({
            "name": f"TEST Equipo {self.test_uid} {suffix}",
            "tipo_equipo_id": self.tipo_equipo.id,
            "marca": "Dell",
            "modelo": "Inspiron",
            "numero_serie": f"TEST-EQ-{self.test_uid}-{suffix}",
            "color": "Negro",
            "descripcion": "Equipo creado para pruebas.",
        })

    def test_01_crear_equipo_valido_sin_detalles(self):
        equipo = self._crear_equipo("001")

        self.assertTrue(equipo.id)
        self.assertEqual(equipo.name, f"TEST Equipo {self.test_uid} 001")
        self.assertEqual(equipo.tipo_equipo_id.id, self.tipo_equipo.id)
        self.assertEqual(equipo.marca, "Dell")
        self.assertEqual(equipo.modelo, "Inspiron")
        self.assertEqual(equipo.numero_serie, f"TEST-EQ-{self.test_uid}-001".upper())
        self.assertEqual(len(equipo.detalle_ids), 0)

    def test_02_crear_equipo_con_detalles_complementarios(self):
        equipo = self._crear_equipo("002")

        detalle_ram = self.DetalleEquipo.create({
            "equipo_id": equipo.id,
            "name": "RAM",
            "valor": "16GB",
        })

        detalle_disco = self.DetalleEquipo.create({
            "equipo_id": equipo.id,
            "name": "Disco",
            "valor": "SSD 512GB",
        })

        self.assertTrue(detalle_ram.id)
        self.assertTrue(detalle_disco.id)

        equipo.invalidate_recordset()

        self.assertEqual(len(equipo.detalle_ids), 2)

        detalles = equipo.detalle_ids.mapped("name")
        self.assertIn("RAM", detalles)
        self.assertIn("Disco", detalles)

    def test_03_nombre_menor_a_tres_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Equipo.create({
                "name": "PC",
                "tipo_equipo_id": self.tipo_equipo.id,
                "marca": "Dell",
                "modelo": "Inspiron",
                "numero_serie": f"TEST-EQ-{self.test_uid}-003",
            })

    def test_04_numero_serie_menor_a_tres_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Equipo.create({
                "name": f"TEST Equipo Serie Corta {self.test_uid}",
                "tipo_equipo_id": self.tipo_equipo.id,
                "marca": "Dell",
                "modelo": "Inspiron",
                "numero_serie": "AB",
            })

    def test_05_normalizar_datos_al_crear(self):
        equipo = self.Equipo.create({
            "name": f"   TEST Equipo Normalizado {self.test_uid}   ",
            "tipo_equipo_id": self.tipo_equipo.id,
            "marca": "   Dell   ",
            "modelo": "   Latitude   ",
            "numero_serie": f"   test-eq-{self.test_uid}-005   ",
            "color": "   Gris   ",
            "descripcion": "Equipo con datos normalizados.",
        })

        self.assertEqual(equipo.name, f"TEST Equipo Normalizado {self.test_uid}")
        self.assertEqual(equipo.marca, "Dell")
        self.assertEqual(equipo.modelo, "Latitude")
        self.assertEqual(equipo.numero_serie, f"TEST-EQ-{self.test_uid}-005".upper())
        self.assertEqual(equipo.color, "Gris")

    def test_06_normalizar_datos_al_actualizar(self):
        equipo = self._crear_equipo("006")

        equipo.write({
            "name": f"   TEST Equipo Actualizado {self.test_uid}   ",
            "marca": "   HP   ",
            "modelo": "   EliteBook   ",
            "numero_serie": f"   test-eq-{self.test_uid}-006-up   ",
            "color": "   Plateado   ",
        })

        self.assertEqual(equipo.name, f"TEST Equipo Actualizado {self.test_uid}")
        self.assertEqual(equipo.marca, "HP")
        self.assertEqual(equipo.modelo, "EliteBook")
        self.assertEqual(equipo.numero_serie, f"TEST-EQ-{self.test_uid}-006-UP".upper())
        self.assertEqual(equipo.color, "Plateado")

    def test_07_numero_serie_duplicado_debe_fallar(self):
        serie = f"TEST-EQ-{self.test_uid}-007"

        self.Equipo.create({
            "name": f"TEST Equipo Duplicado A {self.test_uid}",
            "tipo_equipo_id": self.tipo_equipo.id,
            "marca": "Dell",
            "modelo": "Inspiron",
            "numero_serie": serie,
            "color": "Negro",
        })

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(Exception):
                self.Equipo.create({
                    "name": f"TEST Equipo Duplicado B {self.test_uid}",
                    "tipo_equipo_id": self.tipo_equipo.id,
                    "marca": "HP",
                    "modelo": "EliteBook",
                    "numero_serie": serie,
                    "color": "Gris",
                })

    def test_08_equipo_to_dict_sin_detalles(self):
        equipo = self._crear_equipo("008")

        data = equipo._equipo_to_dict()

        self.assertEqual(data["id"], equipo.id)
        self.assertEqual(data["name"], equipo.name)
        self.assertEqual(data["tipo_equipo_id"], self.tipo_equipo.id)
        self.assertEqual(data["tipo_equipo"], self.tipo_equipo.name)
        self.assertEqual(data["marca"], "Dell")
        self.assertEqual(data["modelo"], "Inspiron")
        self.assertEqual(data["numero_serie"], f"TEST-EQ-{self.test_uid}-008".upper())
        self.assertEqual(data["detalles"], [])

    def test_09_equipo_to_dict_con_detalles(self):
        equipo = self._crear_equipo("009")

        self.DetalleEquipo.create({
            "equipo_id": equipo.id,
            "name": "RAM",
            "valor": "16GB",
        })

        self.DetalleEquipo.create({
            "equipo_id": equipo.id,
            "name": "Procesador",
            "valor": "Intel Core i7",
        })

        data = equipo._equipo_to_dict()

        self.assertEqual(data["id"], equipo.id)
        self.assertEqual(len(data["detalles"]), 2)

        caracteristicas = [item["caracteristica"] for item in data["detalles"]]
        self.assertIn("RAM", caracteristicas)
        self.assertIn("Procesador", caracteristicas)

    def test_10_get_equipos_data(self):
        equipo = self._crear_equipo("010")

        data = self.Equipo.get_equipos_data()

        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)

        ids = [item["id"] for item in data]
        self.assertIn(equipo.id, ids)

    def test_11_get_equipo_by_id_custom(self):
        equipo = self._crear_equipo("011")

        data = self.Equipo.get_equipo_by_id_custom(equipo.id)

        self.assertEqual(data["id"], equipo.id)
        self.assertEqual(data["name"], equipo.name)
        self.assertEqual(data["tipo_equipo_id"], self.tipo_equipo.id)

    def test_12_get_equipo_by_id_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Equipo.get_equipo_by_id_custom(999999)

    def test_13_create_equipo_custom(self):
        data = self.Equipo.create_equipo_custom({
            "name": f"TEST Equipo Custom {self.test_uid}",
            "tipo_equipo_id": self.tipo_equipo.id,
            "marca": "Lenovo",
            "modelo": "ThinkPad",
            "numero_serie": f"TEST-EQ-{self.test_uid}-013",
            "color": "Negro",
            "descripcion": "Equipo creado desde método custom.",
        })

        self.assertIn("id", data)
        self.assertEqual(data["name"], f"TEST Equipo Custom {self.test_uid}")
        self.assertEqual(data["tipo_equipo_id"], self.tipo_equipo.id)
        self.assertEqual(data["marca"], "Lenovo")
        self.assertEqual(data["modelo"], "ThinkPad")
        self.assertEqual(data["numero_serie"], f"TEST-EQ-{self.test_uid}-013".upper())

    def test_14_update_equipo_custom(self):
        equipo = self._crear_equipo("014")

        data = self.Equipo.update_equipo_custom(equipo.id, {
            "name": f"TEST Equipo Custom Update {self.test_uid}",
            "tipo_equipo_id": self.tipo_equipo.id,
            "marca": "Asus",
            "modelo": "Vivobook",
            "numero_serie": f"TEST-EQ-{self.test_uid}-014-UP",
            "color": "Azul",
            "descripcion": "Equipo actualizado desde método custom.",
        })

        self.assertEqual(data["id"], equipo.id)
        self.assertEqual(data["name"], f"TEST Equipo Custom Update {self.test_uid}")
        self.assertEqual(data["marca"], "Asus")
        self.assertEqual(data["modelo"], "Vivobook")
        self.assertEqual(data["numero_serie"], f"TEST-EQ-{self.test_uid}-014-UP".upper())

    def test_15_update_equipo_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Equipo.update_equipo_custom(999999, {
                "name": "TEST Equipo Inexistente",
                "tipo_equipo_id": self.tipo_equipo.id,
                "marca": "Dell",
                "modelo": "Inspiron",
                "numero_serie": f"TEST-EQ-{self.test_uid}-015",
            })

    def test_16_delete_equipo_custom(self):
        equipo = self._crear_equipo("016")
        equipo_id = equipo.id

        data = self.Equipo.delete_equipo_custom(equipo_id)

        self.assertEqual(data["id"], equipo_id)
        self.assertTrue(data["deleted"])

        equipo_borrado = self.Equipo.browse(equipo_id)
        self.assertFalse(equipo_borrado.exists())

    def test_17_delete_equipo_custom_con_detalles_elimina_complementos(self):
        equipo = self._crear_equipo("017")

        detalle = self.DetalleEquipo.create({
            "equipo_id": equipo.id,
            "name": "RAM",
            "valor": "16GB",
        })

        detalle_id = detalle.id
        equipo_id = equipo.id

        data = self.Equipo.delete_equipo_custom(equipo_id)

        self.assertTrue(data["deleted"])

        equipo_borrado = self.Equipo.browse(equipo_id)
        detalle_borrado = self.DetalleEquipo.browse(detalle_id)

        self.assertFalse(equipo_borrado.exists())
        self.assertFalse(detalle_borrado.exists())

    def test_18_delete_equipo_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Equipo.delete_equipo_custom(999999)
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestTechstoreTecnico(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Tecnico = self.env["techstore.tecnico"]

    def test_01_crear_tecnico_valido(self):
        tecnico = self.Tecnico.create({
            "name": "TEST Técnico Hardware 01",
            "cedula": "1799000001",
            "email": "test.tecnico.hardware01@techstore.com",
            "telefono": "0999000001",
            "especialidad": "hardware",
            "nivel_experiencia": "senior",
            "activo": True,
        })

        self.assertTrue(tecnico.id)
        self.assertEqual(tecnico.name, "TEST Técnico Hardware 01")
        self.assertEqual(tecnico.cedula, "1799000001")
        self.assertEqual(tecnico.email, "test.tecnico.hardware01@techstore.com")
        self.assertEqual(tecnico.telefono, "0999000001")
        self.assertEqual(tecnico.especialidad, "hardware")
        self.assertEqual(tecnico.nivel_experiencia, "senior")
        self.assertTrue(tecnico.activo)

    def test_02_nombre_menor_a_tres_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.create({
                "name": "AB",
                "cedula": "1799000002",
                "email": "test.tecnico.nombre02@techstore.com",
                "telefono": "0999000002",
                "especialidad": "hardware",
                "nivel_experiencia": "junior",
                "activo": True,
            })

    def test_03_cedula_con_letras_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.create({
                "name": "TEST Técnico Cedula Mala",
                "cedula": "17990ABC03",
                "email": "test.tecnico.cedula03@techstore.com",
                "telefono": "0999000003",
                "especialidad": "software",
                "nivel_experiencia": "intermedio",
                "activo": True,
            })

    def test_04_cedula_menor_a_diez_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.create({
                "name": "TEST Técnico Cedula Corta",
                "cedula": "179900",
                "email": "test.tecnico.cedula04@techstore.com",
                "telefono": "0999000004",
                "especialidad": "software",
                "nivel_experiencia": "intermedio",
                "activo": True,
            })

    def test_05_email_invalido_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.create({
                "name": "TEST Técnico Email Malo",
                "cedula": "1799000005",
                "email": "correo_malo",
                "telefono": "0999000005",
                "especialidad": "mantenimiento_general",
                "nivel_experiencia": "junior",
                "activo": True,
            })

    def test_06_telefono_con_letras_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.create({
                "name": "TEST Técnico Telefono Malo",
                "cedula": "1799000006",
                "email": "test.tecnico.telefono06@techstore.com",
                "telefono": "0999ABC006",
                "especialidad": "hardware",
                "nivel_experiencia": "junior",
                "activo": True,
            })

    def test_07_telefono_menor_a_siete_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.create({
                "name": "TEST Técnico Telefono Corto",
                "cedula": "1799000007",
                "email": "test.tecnico.telefono07@techstore.com",
                "telefono": "12345",
                "especialidad": "hardware",
                "nivel_experiencia": "junior",
                "activo": True,
            })

    def test_08_telefono_mayor_a_diez_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.create({
                "name": "TEST Técnico Telefono Largo",
                "cedula": "1799000008",
                "email": "test.tecnico.telefono08@techstore.com",
                "telefono": "099900000888",
                "especialidad": "software",
                "nivel_experiencia": "senior",
                "activo": True,
            })

    def test_09_normalizar_datos_al_crear(self):
        tecnico = self.Tecnico.create({
            "name": "   TEST Técnico Normalizado   ",
            "cedula": " 1799000009 ",
            "email": " TEST.TECNICO.NORMALIZADO09@TECHSTORE.COM ",
            "telefono": " 0999000009 ",
            "especialidad": "mantenimiento_general",
            "nivel_experiencia": "intermedio",
            "activo": True,
        })

        self.assertEqual(tecnico.name, "TEST Técnico Normalizado")
        self.assertEqual(tecnico.cedula, "1799000009")
        self.assertEqual(tecnico.email, "test.tecnico.normalizado09@techstore.com")
        self.assertEqual(tecnico.telefono, "0999000009")

    def test_10_normalizar_datos_al_actualizar(self):
        tecnico = self.Tecnico.create({
            "name": "TEST Técnico Antes",
            "cedula": "1799000010",
            "email": "test.tecnico.antes10@techstore.com",
            "telefono": "0999000010",
            "especialidad": "hardware",
            "nivel_experiencia": "junior",
            "activo": True,
        })

        tecnico.write({
            "name": "   TEST Técnico Después   ",
            "email": " TEST.TECNICO.DESPUES10@TECHSTORE.COM ",
            "telefono": " 0988000010 ",
        })

        self.assertEqual(tecnico.name, "TEST Técnico Después")
        self.assertEqual(tecnico.email, "test.tecnico.despues10@techstore.com")
        self.assertEqual(tecnico.telefono, "0988000010")

    def test_11_cedula_duplicada_debe_fallar(self):
        self.Tecnico.create({
            "name": "TEST Técnico Duplicado A",
            "cedula": "1799000011",
            "email": "test.tecnico.dup.a11@techstore.com",
            "telefono": "0999000011",
            "especialidad": "hardware",
            "nivel_experiencia": "junior",
            "activo": True,
        })

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(Exception):
                self.Tecnico.create({
                    "name": "TEST Técnico Duplicado B",
                    "cedula": "1799000011",
                    "email": "test.tecnico.dup.b11@techstore.com",
                    "telefono": "0999000012",
                    "especialidad": "software",
                    "nivel_experiencia": "senior",
                    "activo": True,
                })

    def test_12_email_duplicado_debe_fallar(self):
        self.Tecnico.create({
            "name": "TEST Técnico Email Duplicado A",
            "cedula": "1799000012",
            "email": "test.tecnico.email.duplicado12@techstore.com",
            "telefono": "0999000012",
            "especialidad": "hardware",
            "nivel_experiencia": "junior",
            "activo": True,
        })

        with mute_logger("odoo.sql_db"):
            with self.assertRaises(Exception):
                self.Tecnico.create({
                    "name": "TEST Técnico Email Duplicado B",
                    "cedula": "1799000013",
                    "email": "test.tecnico.email.duplicado12@techstore.com",
                    "telefono": "0999000013",
                    "especialidad": "software",
                    "nivel_experiencia": "intermedio",
                    "activo": True,
                })

    def test_13_tecnico_to_dict(self):
        tecnico = self.Tecnico.create({
            "name": "TEST Técnico To Dict",
            "cedula": "1799000014",
            "email": "test.tecnico.dict14@techstore.com",
            "telefono": "0999000014",
            "especialidad": "software",
            "nivel_experiencia": "senior",
            "activo": True,
        })

        data = tecnico._tecnico_to_dict()

        self.assertEqual(data["id"], tecnico.id)
        self.assertEqual(data["name"], "TEST Técnico To Dict")
        self.assertEqual(data["cedula"], "1799000014")
        self.assertEqual(data["email"], "test.tecnico.dict14@techstore.com")
        self.assertEqual(data["especialidad"], "software")
        self.assertEqual(data["nivel_experiencia"], "senior")
        self.assertTrue(data["activo"])

    def test_14_get_tecnicos_data(self):
        self.Tecnico.create({
            "name": "TEST Técnico Lista",
            "cedula": "1799000015",
            "email": "test.tecnico.lista15@techstore.com",
            "telefono": "0999000015",
            "especialidad": "mantenimiento_general",
            "nivel_experiencia": "intermedio",
            "activo": True,
        })

        data = self.Tecnico.get_tecnicos_data()

        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)

        nombres = [item["name"] for item in data]
        self.assertIn("TEST Técnico Lista", nombres)

    def test_15_get_tecnico_by_id_custom(self):
        tecnico = self.Tecnico.create({
            "name": "TEST Técnico Buscar ID",
            "cedula": "1799000016",
            "email": "test.tecnico.buscar16@techstore.com",
            "telefono": "0999000016",
            "especialidad": "hardware",
            "nivel_experiencia": "senior",
            "activo": True,
        })

        data = self.Tecnico.get_tecnico_by_id_custom(tecnico.id)

        self.assertEqual(data["id"], tecnico.id)
        self.assertEqual(data["name"], "TEST Técnico Buscar ID")

    def test_16_get_tecnico_by_id_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.get_tecnico_by_id_custom(999999)

    def test_17_create_tecnico_custom(self):
        data = self.Tecnico.create_tecnico_custom({
            "name": "TEST Técnico Custom",
            "cedula": "1799000017",
            "email": "test.tecnico.custom17@techstore.com",
            "telefono": "0999000017",
            "especialidad": "software",
            "nivel_experiencia": "intermedio",
            "activo": True,
        })

        self.assertIn("id", data)
        self.assertEqual(data["name"], "TEST Técnico Custom")
        self.assertEqual(data["cedula"], "1799000017")
        self.assertEqual(data["especialidad"], "software")
        self.assertEqual(data["nivel_experiencia"], "intermedio")

    def test_18_update_tecnico_custom(self):
        tecnico = self.Tecnico.create({
            "name": "TEST Técnico Antes Update",
            "cedula": "1799000018",
            "email": "test.tecnico.update18@techstore.com",
            "telefono": "0999000018",
            "especialidad": "hardware",
            "nivel_experiencia": "junior",
            "activo": True,
        })

        data = self.Tecnico.update_tecnico_custom(tecnico.id, {
            "name": "TEST Técnico Después Update",
            "cedula": "1799000018",
            "email": "test.tecnico.update18@techstore.com",
            "telefono": "0988000018",
            "especialidad": "mantenimiento_general",
            "nivel_experiencia": "senior",
            "activo": True,
        })

        self.assertEqual(data["id"], tecnico.id)
        self.assertEqual(data["name"], "TEST Técnico Después Update")
        self.assertEqual(data["telefono"], "0988000018")
        self.assertEqual(data["especialidad"], "mantenimiento_general")
        self.assertEqual(data["nivel_experiencia"], "senior")

    def test_19_update_tecnico_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.update_tecnico_custom(999999, {
                "name": "TEST Técnico No Existe",
                "cedula": "1799000019",
                "email": "test.tecnico.noexiste19@techstore.com",
                "telefono": "0999000019",
                "especialidad": "hardware",
                "nivel_experiencia": "junior",
                "activo": True,
            })

    def test_20_toggle_tecnico_activo_custom(self):
        tecnico = self.Tecnico.create({
            "name": "TEST Técnico Toggle",
            "cedula": "1799000020",
            "email": "test.tecnico.toggle20@techstore.com",
            "telefono": "0999000020",
            "especialidad": "hardware",
            "nivel_experiencia": "junior",
            "activo": True,
        })

        data = self.Tecnico.toggle_tecnico_activo_custom(tecnico.id)

        self.assertEqual(data["id"], tecnico.id)
        self.assertFalse(data["activo"])

        tecnico.invalidate_recordset()
        self.assertFalse(tecnico.activo)

    def test_21_toggle_tecnico_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Tecnico.toggle_tecnico_activo_custom(999999)
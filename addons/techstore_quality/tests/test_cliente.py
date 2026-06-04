from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestTechstoreCliente(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Cliente = self.env["techstore.cliente"]

    def test_01_crear_cliente_particular_valido(self):
        cliente = self.Cliente.create({
            "name": "Dennis Chimborazo",
            "tipo_cliente": "particular",
            "cedula": "1801234567",
            "email": "dennis@test.com",
            "telefono": "0999999999",
            "activo": True,
        })

        self.assertTrue(cliente.id)
        self.assertEqual(cliente.name, "Dennis Chimborazo")
        self.assertEqual(cliente.tipo_cliente, "particular")
        self.assertEqual(cliente.cedula, "1801234567")
        self.assertEqual(cliente.email, "dennis@test.com")
        self.assertTrue(cliente.activo)

    def test_02_crear_cliente_corporativo_valido(self):
        cliente = self.Cliente.create({
            "name": "TechStore Ecuador",
            "tipo_cliente": "corporativo",
            "cedula": "1899999999001",
            "email": "empresa@test.com",
            "telefono": "032999999",
            "activo": True,
        })

        self.assertTrue(cliente.id)
        self.assertEqual(cliente.tipo_cliente, "corporativo")
        self.assertEqual(cliente.cedula, "1899999999001")

    def test_03_nombre_menor_a_tres_caracteres_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Cliente.create({
                "name": "AB",
                "tipo_cliente": "particular",
                "cedula": "1801234568",
                "email": "ab@test.com",
            })

    def test_04_email_invalido_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Cliente.create({
                "name": "Cliente Email Malo",
                "tipo_cliente": "particular",
                "cedula": "1801234569",
                "email": "correo_malo",
            })

    def test_05_cedula_con_letras_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Cliente.create({
                "name": "Cliente Cedula Mala",
                "tipo_cliente": "particular",
                "cedula": "180ABC4567",
                "email": "cedula@test.com",
            })

    def test_06_cliente_particular_con_cedula_menor_a_10_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Cliente.create({
                "name": "Cliente Particular Malo",
                "tipo_cliente": "particular",
                "cedula": "12345",
                "email": "particular@test.com",
            })

    def test_07_cliente_corporativo_con_ruc_menor_a_13_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Cliente.create({
                "name": "Empresa Mala",
                "tipo_cliente": "corporativo",
                "cedula": "1899999999",
                "email": "empresa.mala@test.com",
            })

    def test_08_normalizar_datos_al_crear(self):
        cliente = self.Cliente.create({
            "name": "   Cliente Normalizado   ",
            "tipo_cliente": "particular",
            "cedula": " 1801234570 ",
            "email": " CLIENTE@TEST.COM ",
            "telefono": " 0999999998 ",
        })

        self.assertEqual(cliente.name, "Cliente Normalizado")
        self.assertEqual(cliente.cedula, "1801234570")
        self.assertEqual(cliente.email, "cliente@test.com")
        self.assertEqual(cliente.telefono, "0999999998")

    def test_09_create_cliente_custom(self):
        data = self.Cliente.create_cliente_custom({
            "name": "Cliente Custom",
            "tipo_cliente": "particular",
            "cedula": "1801234571",
            "email": "custom@test.com",
            "telefono": "0988888888",
            "activo": True,
        })

        self.assertIn("id", data)
        self.assertEqual(data["name"], "Cliente Custom")
        self.assertEqual(data["tipo_cliente"], "particular")
        self.assertEqual(data["tipo_cliente_label"], "Particular")
        self.assertTrue(data["activo"])

    def test_10_update_cliente_custom(self):
        cliente = self.Cliente.create({
            "name": "Cliente Antes",
            "tipo_cliente": "particular",
            "cedula": "1801234572",
            "email": "antes@test.com",
        })

        data = self.Cliente.update_cliente_custom(cliente.id, {
            "name": "Cliente Después",
            "tipo_cliente": "particular",
            "cedula": "1801234572",
            "email": "despues@test.com",
            "telefono": "0977777777",
            "activo": True,
        })

        self.assertEqual(data["name"], "Cliente Después")
        self.assertEqual(data["email"], "despues@test.com")
        self.assertEqual(data["telefono"], "0977777777")

    def test_11_toggle_cliente_activo_custom(self):
        cliente = self.Cliente.create({
            "name": "Cliente Toggle",
            "tipo_cliente": "particular",
            "cedula": "1801234573",
            "email": "toggle@test.com",
            "activo": True,
        })

        data = self.Cliente.toggle_cliente_activo_custom(cliente.id)

        self.assertEqual(data["id"], cliente.id)
        self.assertFalse(data["activo"])

        cliente.invalidate_recordset()
        self.assertFalse(cliente.activo)

    def test_12_get_clientes_data(self):
        self.Cliente.create({
            "name": "Cliente Lista",
            "tipo_cliente": "particular",
            "cedula": "1801234574",
            "email": "lista@test.com",
        })

        data = self.Cliente.get_clientes_data()

        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestTechstoreVenta(TransactionCase):

    def setUp(self):
        super().setUp()

        self.Cliente = self.env["techstore.cliente"]
        self.Producto = self.env["techstore.producto"]
        self.Venta = self.env["techstore.venta"]

        self.cliente = self.Cliente.create({
            "name": "Cliente Venta",
            "tipo_cliente": "particular",
            "cedula": "1801234580",
            "email": "venta@test.com",
            "activo": True,
        })

        self.producto = self.Producto.create({
            "name": "Laptop Test Venta",
            "codigo": "VENTA-001",
            "precio_unitario": 100,
            "stock_disponible": 10,
            "activo": True,
        })

    def test_01_crear_venta_descuenta_stock(self):
        data = self.Venta.create_venta_custom({
            "cliente_id": self.cliente.id,
            "descuento": 0,
            "observacion": "Venta de prueba",
            "detalles": [
                {
                    "producto_id": self.producto.id,
                    "cantidad": 2,
                }
            ],
        })

        self.assertIn("id", data)
        self.assertEqual(data["cliente_id"], self.cliente.id)
        self.assertEqual(data["subtotal"], 200)
        self.assertEqual(data["iva"], 30)
        self.assertEqual(data["total"], 230)

        self.producto.invalidate_recordset()
        self.assertEqual(self.producto.stock_disponible, 8)

    def test_02_venta_sin_detalles_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Venta.create_venta_custom({
                "cliente_id": self.cliente.id,
                "descuento": 0,
                "observacion": "Sin detalles",
                "detalles": [],
            })

    def test_03_venta_con_stock_insuficiente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Venta.create_venta_custom({
                "cliente_id": self.cliente.id,
                "descuento": 0,
                "observacion": "Stock insuficiente",
                "detalles": [
                    {
                        "producto_id": self.producto.id,
                        "cantidad": 999,
                    }
                ],
            })

    def test_04_descuento_mayor_subtotal_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Venta.create_venta_custom({
                "cliente_id": self.cliente.id,
                "descuento": 500,
                "observacion": "Descuento inválido",
                "detalles": [
                    {
                        "producto_id": self.producto.id,
                        "cantidad": 1,
                    }
                ],
            })

    def test_05_eliminar_venta_restaura_stock(self):
        data = self.Venta.create_venta_custom({
            "cliente_id": self.cliente.id,
            "descuento": 0,
            "observacion": "Venta a eliminar",
            "detalles": [
                {
                    "producto_id": self.producto.id,
                    "cantidad": 3,
                }
            ],
        })

        self.producto.invalidate_recordset()
        self.assertEqual(self.producto.stock_disponible, 7)

        self.Venta.delete_venta_custom(data["id"])

        self.producto.invalidate_recordset()
        self.assertEqual(self.producto.stock_disponible, 10)
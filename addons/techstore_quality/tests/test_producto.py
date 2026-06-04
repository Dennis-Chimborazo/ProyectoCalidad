from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestTechstoreProducto(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Producto = self.env["techstore.producto"]

    def test_01_crear_producto_valido(self):
        producto = self.Producto.create({
            "name": "Laptop Lenovo",
            "codigo": "PROD-001",
            "precio_unitario": 850.50,
            "stock_disponible": 10,
            "activo": True,
        })

        self.assertTrue(producto.id)
        self.assertEqual(producto.codigo, "PROD-001")
        self.assertEqual(producto.precio_unitario, 850.50)
        self.assertEqual(producto.stock_disponible, 10)

    def test_02_precio_cero_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Producto.create({
                "name": "Producto Sin Precio",
                "codigo": "PROD-002",
                "precio_unitario": 0,
                "stock_disponible": 5,
            })

    def test_03_stock_negativo_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Producto.create({
                "name": "Producto Stock Malo",
                "codigo": "PROD-003",
                "precio_unitario": 100,
                "stock_disponible": -1,
            })

    def test_04_codigo_invalido_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Producto.create({
                "name": "Producto Codigo Malo",
                "codigo": "CODIGO * MALO",
                "precio_unitario": 100,
                "stock_disponible": 5,
            })

    def test_05_create_producto_custom(self):
        data = self.Producto.create_producto_custom({
            "name": "Mouse Logitech",
            "codigo": "PROD-004",
            "precio_unitario": 25.75,
            "stock_disponible": 30,
            "activo": True,
        })

        self.assertIn("id", data)
        self.assertEqual(data["name"], "Mouse Logitech")
        self.assertEqual(data["codigo"], "PROD-004")
        self.assertEqual(data["stock_disponible"], 30)

    def test_06_update_producto_custom(self):
        producto = self.Producto.create({
            "name": "Teclado Antiguo",
            "codigo": "PROD-005",
            "precio_unitario": 30,
            "stock_disponible": 8,
        })

        data = self.Producto.update_producto_custom(producto.id, {
            "name": "Teclado Mecánico",
            "codigo": "PROD-005",
            "precio_unitario": 55,
            "stock_disponible": 12,
            "activo": True,
        })

        self.assertEqual(data["name"], "Teclado Mecánico")
        self.assertEqual(data["precio_unitario"], 55)
        self.assertEqual(data["stock_disponible"], 12)

    def test_07_toggle_producto_activo_custom(self):
        producto = self.Producto.create({
            "name": "Monitor Samsung",
            "codigo": "PROD-006",
            "precio_unitario": 180,
            "stock_disponible": 4,
            "activo": True,
        })

        data = self.Producto.toggle_producto_activo_custom(producto.id)

        self.assertFalse(data["activo"])
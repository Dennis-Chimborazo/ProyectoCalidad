from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
import uuid


@tagged("post_install", "-at_install")
class TestTechstoreMantenimiento(TransactionCase):

    def setUp(self):
        super().setUp()

        self.Cliente = self.env["techstore.cliente"]
        self.Tecnico = self.env["techstore.tecnico"]
        self.TipoEquipo = self.env["techstore.tipo.equipo"]
        self.Equipo = self.env["techstore.equipo"]
        self.DetalleEquipo = self.env["techstore.detalle.equipo"]
        self.BaseConocimiento = self.env["techstore.base.conocimiento"]
        self.Mantenimiento = self.env["techstore.mantenimiento"]
        self.MantenimientoEquipo = self.env["techstore.mantenimiento.equipo"]
        self.MantenimientoEquipoFalla = self.env["techstore.mantenimiento.equipo.falla"]

        self.test_uid = uuid.uuid4().hex[:8]

        self.cliente = self.Cliente.create({
            "name": f"TEST Cliente Mantenimiento {self.test_uid}",
            "tipo_cliente": "particular",
            "cedula": self._cedula("10"),
            "email": f"test.cliente.mantenimiento.{self.test_uid}@techstore.com",
            "telefono": "0991111111",
            "activo": True,
        })

        self.tecnico = self.Tecnico.create({
            "name": f"TEST Técnico Mantenimiento {self.test_uid}",
            "cedula": self._cedula("20"),
            "email": f"test.tecnico.mantenimiento.{self.test_uid}@techstore.com",
            "telefono": "0992222222",
            "especialidad": "hardware",
            "nivel_experiencia": "senior",
            "activo": True,
        })

        self.tipo_equipo = self.TipoEquipo.create({
            "name": f"TEST Laptop Mantenimiento {self.test_uid}",
            "descripcion": "Tipo de equipo usado para pruebas de mantenimiento.",
            "activo": True,
        })

        self.equipo = self.Equipo.create({
            "name": f"TEST Equipo Dell {self.test_uid}",
            "tipo_equipo_id": self.tipo_equipo.id,
            "marca": "Dell",
            "modelo": "Latitude",
            "numero_serie": f"TEST-SERIE-{self.test_uid}",
            "color": "Negro",
            "descripcion": "Equipo usado para pruebas de mantenimiento.",
        })

        self.base_conocimiento = self.BaseConocimiento.create({
            "error_title": f"TEST Falla encendido {self.test_uid}",
            "equipment_type_id": self.tipo_equipo.id,
            "symptoms": "El equipo no enciende y no muestra actividad eléctrica.",
            "root_cause": "Posible falla en cargador, batería o circuito de alimentación.",
            "solution": "Verificar cargador, batería y realizar diagnóstico de placa.",
            "keywords": "encendido, energia, bateria",
            "activo": True,
        })

    def _cedula(self, prefix):
        number = int(self.test_uid[:6], 16) % 1000000
        return f"17{prefix}{number:06d}"[:10]

    def _crear_mantenimiento(self, prioridad="media", descripcion=None):
        return self.Mantenimiento.create_mantenimiento_custom({
            "cliente_id": self.cliente.id,
            "tecnico_id": self.tecnico.id,
            "prioridad": prioridad,
            "descripcion_general": descripcion or "Mantenimiento preventivo de equipo portátil para pruebas.",
        })

    def test_01_crear_mantenimiento_valido(self):
        data = self._crear_mantenimiento()

        self.assertIn("id", data)
        self.assertEqual(data["cliente_id"], self.cliente.id)
        self.assertEqual(data["tecnico_id"], self.tecnico.id)
        self.assertEqual(data["estado"], "pendiente")
        self.assertEqual(data["prioridad"], "media")
        self.assertTrue(data["name"].startswith("MANT-"))

    def test_02_descripcion_corta_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self._crear_mantenimiento(
                prioridad="media",
                descripcion="Corto"
            )

    def test_03_tecnico_inactivo_debe_fallar(self):
        self.tecnico.write({
            "activo": False
        })

        with self.assertRaises(ValidationError):
            self._crear_mantenimiento(
                prioridad="alta",
                descripcion="Mantenimiento con técnico inactivo."
            )

    def test_04_actualizar_estado_en_proceso(self):
        data = self._crear_mantenimiento(
            prioridad="alta",
            descripcion="Mantenimiento correctivo de laptop."
        )

        updated = self.Mantenimiento.update_estado_mantenimiento_custom(
            data["id"],
            "en_proceso"
        )

        self.assertEqual(updated["estado"], "en_proceso")

    def test_05_finalizar_mantenimiento(self):
        data = self._crear_mantenimiento(
            prioridad="alta",
            descripcion="Mantenimiento para finalizar correctamente."
        )

        updated = self.Mantenimiento.finalizar_mantenimiento_custom(data["id"])

        self.assertEqual(updated["estado"], "finalizado")
        self.assertTrue(updated["fecha_fin"])

    def test_06_cancelar_mantenimiento(self):
        data = self._crear_mantenimiento(
            prioridad="baja",
            descripcion="Mantenimiento para probar cancelación."
        )

        updated = self.Mantenimiento.cancelar_mantenimiento_custom(data["id"])

        self.assertEqual(updated["estado"], "cancelado")

    def test_07_estado_invalido_debe_fallar(self):
        data = self._crear_mantenimiento(
            prioridad="media",
            descripcion="Mantenimiento para validar estado inválido."
        )

        with self.assertRaises(ValidationError):
            self.Mantenimiento.update_estado_mantenimiento_custom(
                data["id"],
                "estado_malo"
            )

    def test_08_get_mantenimiento_by_id_custom(self):
        data = self._crear_mantenimiento(
            prioridad="media",
            descripcion="Mantenimiento para búsqueda por ID."
        )

        found = self.Mantenimiento.get_mantenimiento_by_id_custom(data["id"])

        self.assertEqual(found["id"], data["id"])
        self.assertEqual(found["cliente_id"], self.cliente.id)
        self.assertEqual(found["tecnico_id"], self.tecnico.id)

    def test_09_get_mantenimiento_by_id_inexistente_debe_fallar(self):
        with self.assertRaises(ValidationError):
            self.Mantenimiento.get_mantenimiento_by_id_custom(999999)

    def test_10_flujo_completo_mantenimiento_con_equipo_detalle_y_falla(self):
        mantenimiento_data = self._crear_mantenimiento(
            prioridad="critica",
            descripcion="Mantenimiento integral para validar flujo completo."
        )

        mantenimiento_id = mantenimiento_data["id"]

        detalle = self.DetalleEquipo.create({
            "equipo_id": self.equipo.id,
            "name": "RAM",
            "valor": "16GB",
        })

        self.assertTrue(detalle.id)

        mantenimiento_equipo = self.MantenimientoEquipo.create_mantenimiento_equipo_custom({
            "mantenimiento_id": mantenimiento_id,
            "equipo_id": self.equipo.id,
            "falla_reportada": "El equipo no enciende correctamente.",
            "solucion": "",
        })

        self.assertIn("id", mantenimiento_equipo)
        self.assertEqual(mantenimiento_equipo["mantenimiento_id"], mantenimiento_id)
        self.assertEqual(mantenimiento_equipo["equipo_id"], self.equipo.id)
        self.assertEqual(mantenimiento_equipo["estado_equipo"], "pendiente")

        falla = self.MantenimientoEquipoFalla.create_mantenimiento_equipo_falla_custom({
            "mantenimiento_equipo_id": mantenimiento_equipo["id"],
            "base_conocimiento_id": self.base_conocimiento.id,
        })

        self.assertIn("id", falla)
        self.assertEqual(falla["mantenimiento_equipo_id"], mantenimiento_equipo["id"])
        self.assertEqual(falla["base_conocimiento_id"], self.base_conocimiento.id)

        solucion = self.MantenimientoEquipo.update_solucion_equipo_custom(
            mantenimiento_equipo["id"],
            {
                "solucion": "Se verificó cargador, batería y circuito de alimentación."
            }
        )

        self.assertEqual(
            solucion["solucion"],
            "Se verificó cargador, batería y circuito de alimentación."
        )

        estado_equipo = self.MantenimientoEquipo.update_estado_equipo_custom(
            mantenimiento_equipo["id"],
            "finalizado"
        )

        self.assertEqual(estado_equipo["estado_equipo"], "finalizado")
        self.assertTrue(estado_equipo["mantenimiento_cerrado"])

        info = self.Mantenimiento.get_mantenimiento_info_custom(mantenimiento_id)

        self.assertEqual(info["id"], mantenimiento_id)
        self.assertEqual(info["total_equipos"], 1)
        self.assertEqual(info["total_finalizados"], 1)
        self.assertEqual(info["total_con_solucion"], 1)
        self.assertEqual(info["total_con_base_conocimiento"], 1)
        self.assertEqual(len(info["equipos"]), 1)
        self.assertEqual(len(info["equipos"][0]["detalles"]), 1)
        self.assertEqual(len(info["equipos"][0]["fallas_base"]), 1)

    def test_11_create_or_attach_equipo_custom_crea_equipo_y_detalles(self):
        mantenimiento_data = self._crear_mantenimiento(
            prioridad="alta",
            descripcion="Mantenimiento para crear equipo desde flujo completo."
        )

        response = self.MantenimientoEquipo.create_or_attach_equipo_custom({
            "mantenimiento_id": mantenimiento_data["id"],
            "equipo": {
                "name": f"TEST Equipo Nuevo {self.test_uid}",
                "tipo_equipo_id": self.tipo_equipo.id,
                "marca": "HP",
                "modelo": "EliteBook",
                "numero_serie": f"TEST-NEW-{self.test_uid}",
                "color": "Gris",
                "descripcion": "Equipo creado desde mantenimiento.",
                "falla_reportada": "Equipo presenta fallo de encendido.",
                "solucion": "",
                "detalles": [
                    {
                        "name": "Procesador",
                        "valor": "Intel Core i5",
                    },
                    {
                        "name": "Almacenamiento",
                        "valor": "SSD 512GB",
                    },
                ],
            },
        })

        self.assertTrue(response["success"])
        self.assertIn("item", response)
        self.assertEqual(response["item"]["estado_equipo"], "pendiente")
        self.assertEqual(len(response["item"]["detalles"]), 2)

    def test_12_create_or_attach_equipo_duplicado_mismo_mantenimiento_debe_fallar(self):
        mantenimiento_data = self._crear_mantenimiento(
            prioridad="media",
            descripcion="Mantenimiento para validar equipo duplicado."
        )

        self.MantenimientoEquipo.create_mantenimiento_equipo_custom({
            "mantenimiento_id": mantenimiento_data["id"],
            "equipo_id": self.equipo.id,
            "falla_reportada": "Primera falla reportada del equipo.",
            "solucion": "",
        })

        with self.assertRaises(ValidationError):
            self.MantenimientoEquipo.create_mantenimiento_equipo_custom({
                "mantenimiento_id": mantenimiento_data["id"],
                "equipo_id": self.equipo.id,
                "falla_reportada": "Segunda falla reportada del equipo.",
                "solucion": "",
            })

    def test_13_falla_documentada_repetida_debe_fallar(self):
        mantenimiento_data = self._crear_mantenimiento(
            prioridad="media",
            descripcion="Mantenimiento para validar falla repetida."
        )

        mantenimiento_equipo = self.MantenimientoEquipo.create_mantenimiento_equipo_custom({
            "mantenimiento_id": mantenimiento_data["id"],
            "equipo_id": self.equipo.id,
            "falla_reportada": "Falla reportada para base de conocimiento.",
            "solucion": "",
        })

        self.MantenimientoEquipoFalla.create_mantenimiento_equipo_falla_custom({
            "mantenimiento_equipo_id": mantenimiento_equipo["id"],
            "base_conocimiento_id": self.base_conocimiento.id,
        })

        with self.assertRaises(ValidationError):
            self.MantenimientoEquipoFalla.create_mantenimiento_equipo_falla_custom({
                "mantenimiento_equipo_id": mantenimiento_equipo["id"],
                "base_conocimiento_id": self.base_conocimiento.id,
            })

    def test_14_dashboard_mantenimientos_data(self):
        mantenimiento_data = self._crear_mantenimiento(
            prioridad="media",
            descripcion="Mantenimiento para validar dashboard."
        )

        self.MantenimientoEquipo.create_mantenimiento_equipo_custom({
            "mantenimiento_id": mantenimiento_data["id"],
            "equipo_id": self.equipo.id,
            "falla_reportada": "Falla para dashboard de mantenimiento.",
            "solucion": "",
        })

        dashboard = self.Mantenimiento.get_dashboard_mantenimientos_data()

        self.assertIn("mantenimientos", dashboard)
        self.assertIn("equipos", dashboard)
        self.assertIn("clientes", dashboard)
        self.assertIn("tipos_equipo", dashboard)

        mantenimiento_ids = [item["id"] for item in dashboard["mantenimientos"]]
        self.assertIn(mantenimiento_data["id"], mantenimiento_ids)
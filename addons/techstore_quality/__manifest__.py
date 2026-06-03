{
    "name": "TechStore Quality",
    "version": "1.0",
    "summary": "Sistema personalizado TechStore Quality",
    "description": """
        Módulo personalizado para gestionar clientes, productos y ventas
        mediante componentes OWL reutilizables.
    """,
    "author": "Dennis Chimborazo",
    "category": "Custom",
    "license": "LGPL-3",

    "depends": [
        "base",
        "web",
    ],

    "data": [
        "security/ir.model.access.csv",
        "views/menu_views.xml",
    ],

    "assets": {
        "web.assets_backend": [
            "techstore_quality/static/src/core/**/*.js",
            "techstore_quality/static/src/components/**/*.js",
            "techstore_quality/static/src/js/**/*.js",
            "techstore_quality/static/src/components/**/*.xml",
            "techstore_quality/static/src/xml/**/*.xml",
            "techstore_quality/static/src/scss/**/*.scss",
        ],
    },

    "installable": True,
    "application": True,
    "auto_install": False,
}
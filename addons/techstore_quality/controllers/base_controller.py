from odoo.http import request
import json


class TechstoreBaseController:

    def _json_response(self, data, status=200):
        return request.make_response(
            json.dumps(data, ensure_ascii=False),
            headers=[
                ("Content-Type", "application/json; charset=utf-8")
            ],
            status=status
        )

    def _get_json_body(self):
        try:
            raw_body = request.httprequest.get_data(as_text=True)

            if not raw_body:
                return {}

            return json.loads(raw_body)

        except Exception:
            return {}
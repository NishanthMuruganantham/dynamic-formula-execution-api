from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

class ErrorTests:

    def test_missing_data_field(self):
        request_body = {
            "formulas": [
                {
                    "expression": "varA + varB",
                    "inputs": [{"varName": "fieldA", "varType": "float"}],
                    "outputVar": "sumResult"
                }
            ]
        }
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 400
        assert ("data" and "'Field required'") in response.json()['detail']

    def test_missing_formulas_field(self):
        request_body = {
            "data": [
                {
                    "id": 1,
                    "fieldA": 10.5,
                    "fieldB": 2.0
                }
            ]
        }
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 400
        assert ("formula" and "'Field required'") in response.json()['detail']

    def test_formula_with_undefined_variable(self):
        data = [
            {"id": 1, "fieldA": 10},
            {"id": 2, "fieldA": 20},
        ]

        formulas = [
            {
                "outputVar": "result",
                "expression": "undefinedField + 10",
                "inputs": [
                    {"varName": "undefinedField", "varType": "number"}
                ],
            }
        ]

        response = client.post("/api/execute-formula", json={"data": data, "formulas": formulas})

        assert response.status_code == 400
        assert "Invalid input variable: 'undefinedField'" in response.json()["detail"]

    def test_formula_with_invalid_variable_type(self):
        data = [
            {"id": 1, "fieldA": "invalid_string"},
            {"id": 2, "fieldA": 20},
        ]

        formulas = [
            {
                "outputVar": "result",
                "expression": "fieldA + 10",
                "inputs": [
                    {"varName": "fieldA", "varType": "number"}
                ],
            }
        ]

        response = client.post("/api/execute-formula", json={"data": data, "formulas": formulas})

        assert response.status_code == 400
        assert "Input should be a valid number, unable to parse string as a number" in response.json()["detail"]

    def test_invalid_formula_expression(self):
        request_body = {
            "data": [
                {
                    "id": 1,
                    "fieldA": 10.5,
                    "fieldB": 2.0
                }
            ],
            "formulas": [
                {
                    "expression": "fieldA + + fieldB",
                    "inputs": [{"varName": "fieldA", "varType": "float"}],
                    "outputVar": "sumResult"
                }
            ]
        }
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 400
        assert "Invalid expression" in response.json()['detail']

    def test_undefined_variable_in_formula(self):
        request_body = {
            "data": [
                {
                    "id": 1,
                    "fieldA": 10.5
                }
            ],
            "formulas": [
                {
                    "expression": "fieldA + nonExistentField",
                    "inputs": [{"varName": "fieldA", "varType": "float"}],
                    "outputVar": "sumResult"
                }
            ]
        }
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 400
        assert "name 'nonExistentField' is not defined" in response.json()['detail']

    def test_missing_expression_in_formula(self):
        request_body = {
            "data": [
                {
                    "id": 1,
                    "fieldA": 10.5,
                    "fieldB": 2.0
                }
            ],
            "formulas": [
                {
                    "inputs": [{"varName": "fieldA", "varType": "float"}],
                    "outputVar": "sumResult"
                }
            ]
        }
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 400
        assert "Field required" in response.json()['detail']

    def test_missing_inputs_in_formula(self):
        request_body = {
            "data": [
                {
                    "id": 1,
                    "fieldA": 10.5,
                    "fieldB": 2.0
                }
            ],
            "formulas": [
                {
                    "expression": "fieldA + fieldB",
                    "outputVar": "sumResult"
                }
            ]
        }
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 400
        assert "'Field required'" in response.json()['detail']

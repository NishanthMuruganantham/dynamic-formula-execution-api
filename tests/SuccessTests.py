import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class SuccessTests:

    simple_addition_data = [
        {"id": 1, "fieldA": 10},
        {"id": 2, "fieldA": 20},
    ]
    
    simple_addition_formulas = [
        {
            "outputVar": "result",
            "expression": "fieldA + 10",
            "inputs": [
                {"varName": "fieldA", "varType": "number"}
            ],
        }
    ]
    
    revenue_data = [
        {"id": 1, "product": "Laptop", "unitPrice": "1000 USD", "quantity": 5, "discount": "10%"},
        {"id": 2, "product": "Smartphone", "unitPrice": "500 USD", "quantity": 10, "discount": "5%"},
        {"id": 3, "product": "Tablet", "unitPrice": "300 USD", "quantity": 15, "discount": "0%"}
    ]

    revenue_formulas = [
        {
            "outputVar": "revenue",
            "expression": "((unitPrice * quantity) - (unitPrice * quantity * (discount / 100)))",
            "inputs": [
                {"varName": "unitPrice", "varType": "currency"},
                {"varName": "quantity", "varType": "number"},
                {"varName": "discount", "varType": "percentage"}
            ]
        }
    ]

    chained_formula_data = [
        {"id": 1, "fieldA": 10, "fieldB": 2},
        {"id": 2, "fieldA": 20, "fieldB": 3}
    ]

    chained_formula_formulas = [
        {
            "outputVar": "sumResult",
            "expression": "fieldA + fieldB",
            "inputs": [
                {"varName": "fieldA", "varType": "number"},
                {"varName": "fieldB", "varType": "number"}
            ]
        },
        {
            "outputVar": "finalResult",
            "expression": "sumResult * 2 + fieldA",
            "inputs": [
                {"varName": "sumResult", "varType": "number"},
                {"varName": "fieldA", "varType": "number"}
            ]
        }
    ]

    @pytest.mark.parametrize(
        "data, formulas, expected_output",
        [
            (
                simple_addition_data,
                simple_addition_formulas,
                {
                    "results": {"result": [20, 30]},
                    "status": "success",
                    "message": "The formulas were executed successfully."
                }
            )
        ]
    )
    def test_execute_simple_addition_formula_success(self, data, formulas, expected_output):
        request_body = {"data": data, "formulas": formulas}
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 200
        assert response.json()["results"]["result"] == expected_output["results"]["result"]
        assert response.json()["status"] == expected_output["status"]
        assert response.json()["message"] == expected_output["message"]

    @pytest.mark.parametrize(
        "data, formulas, expected_output",
        [
            (
                revenue_data,
                revenue_formulas,
                {
                    "results": {"revenue": [4500, 4750, 4500]},
                    "status": "success",
                    "message": "The formulas were executed successfully."
                }
            )
        ]
    )
    def test_execute_revenue_formula_success(self, data, formulas, expected_output):
        request_body = {"data": data, "formulas": formulas}
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 200
        assert response.json()["results"]["revenue"] == expected_output["results"]["revenue"]
        assert response.json()["status"] == expected_output["status"]
        assert response.json()["message"] == expected_output["message"]

    @pytest.mark.parametrize(
        "data, formulas, expected_output",
        [
            (
                chained_formula_data,
                chained_formula_formulas,
                {
                    "results": {
                        "sumResult": [12, 23],
                        "finalResult": [34, 66]
                    },
                    "status": "success",
                    "message": "The formulas were executed successfully."
                }
            )
        ]
    )
    def test_execute_chained_formula_success(self, data, formulas, expected_output):
        request_body = {"data": data, "formulas": formulas}
        response = client.post("/api/execute-formula", json=request_body)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["results"]["sumResult"] == expected_output["results"]["sumResult"]
        assert response_json["results"]["finalResult"] == expected_output["results"]["finalResult"]
        assert response_json["status"] == expected_output["status"]
        assert response_json["message"] == expected_output["message"]

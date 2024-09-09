import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

@pytest.mark.parametrize(
    "data, formulas, expected_output",
    [
        (
            [
                {"id": 1, "fieldA": 10},
                {"id": 2, "fieldA": 20},
            ],
            [
                {
                    "outputVar": "result",
                    "expression": "fieldA + 10",
                    "inputs": [
                        {"varName": "fieldA", "varType": "number"}
                    ],
                }
            ],
            {
                "results": {
                    "result": [20, 30]
                },
                "status": "success",
                "message": "The formulas were executed successfully."
            }
        )
    ]
)
def test_execute_simple_addition_formula_success(data, formulas, expected_output):
    request_body = {
        "data": data,
        "formulas": formulas
    }
    
    response = client.post("/api/execute-formula", json=request_body)
    
    assert response.status_code == 200
    assert response.json()["results"]["result"] == expected_output["results"]["result"]
    assert response.json()["status"] == expected_output["status"]
    assert response.json()["message"] == expected_output["message"]


@pytest.mark.parametrize(
    "data, formulas, expected_output",
    [
        (
            [
                {
                    "id": 1,
                    "product": "Laptop",
                    "unitPrice": "1000 USD",
                    "quantity": 5,
                    "discount": "10%"
                },
                {
                    "id": 2,
                    "product": "Smartphone",
                    "unitPrice": "500 USD",
                    "quantity": 10,
                    "discount": "5%"
                },
                {
                    "id": 3,
                    "product": "Tablet",
                    "unitPrice": "300 USD",
                    "quantity": 15,
                    "discount": "0%"
                }
            ],
            [
                {
                    "outputVar": "revenue",
                    "expression": "((unitPrice * quantity) - (unitPrice * quantity * (discount / 100)))",
                    "inputs": [
                        {"varName": "unitPrice", "varType": "currency"},
                        {"varName": "quantity", "varType": "number"},
                        {"varName": "discount", "varType": "percentage"}
                    ]
                }
            ],
            {
                "results": {
                    "revenue": [4500, 4750, 4500]
                },
                "status": "success",
                "message": "The formulas were executed successfully."
            }
        )
    ]
)
def test_execute_revenye_formula_success(data, formulas, expected_output):
    request_body = {
        "data": data,
        "formulas": formulas
    }
    
    response = client.post("/api/execute-formula", json=request_body)
    
    assert response.status_code == 200
    assert response.json()["results"]["revenue"] == expected_output["results"]["revenue"]
    assert response.json()["status"] == expected_output["status"]
    assert response.json()["message"] == expected_output["message"]

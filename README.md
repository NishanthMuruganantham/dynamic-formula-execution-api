
# Dynamic Formula Execution API 🚀

## Overview 📝

The **Dynamic Formula Execution API** is a Python-based API that interprets and executes complex mathematical formulas on structured datasets. It supports formula chaining, validation, and real-time calculation of values across various data types, such as numbers, strings, booleans, dates, and currencies. The solution ensures efficient performance with sub-second response times, making it suitable for large datasets and complex workflows.

This API was developed as part of a coding challenge to demonstrate key skills in Python and API development.

## Why FastAPI? 🏎️

FastAPI was selected for the following reasons:
- **⚡ Performance**: FastAPI is one of the fastest Python web frameworks, built on top of ASGI and supports async programming, which helps to efficiently handle I/O-bound operations.
- **💼 Ease of Use**: FastAPI has automatic request validation, serialization, and generation of OpenAPI documentation, which helps to reduce boilerplate code and improve development speed.

## Requirements 📦

- **Python 3.8+** 🐍
- **Pydantic**: For data validation. 🛠️
- **FastAPI**: For building the API. 🚧
- **Uvicorn**: For serving the application. 🌐
- **re**: For regex operations in currency/percentage parsing. 💲

## Project Structure 🗂️

```bash
.
├── src
│   ├── app.py              # 💻 it houses the core FastAPI app
│   ├── logic.py            # 🧬 it houses all the logic associated with the API which involves Formula validation, execution, etc.,
│   ├── models.py           # 📊 Contains the pydantic models needed such as Data, Formula, Inputs, and ResultBody models
│   └── routes.py           # 🔗 Contains the route function for the given endpoint /api/execute-formula
├── tests
│   └── ErrorTests.py       # ❌ Pytests for validating Exception cases
│   └── SuccessTests.py     # ✅ Pytests for validating expected success scenarios
├── .gitignore              # 🙈 specifies files and directories Git should ignore
├── main.py                 # 🚀 runs the FastAPI app with live reloading using Uvicorn server 
└── pyproject.toml          # 🧩 Project metadata and configuration settings
├── README.md               # 📄 This file
├── requirements.txt        # 📜 Dependencies for the project
├── vercel.json             # ✈️ Contains the vercel deployment configuration
```

## Setup Instructions 🛠️

### Prerequisites

Before setting up the project, ensure that the following dependencies are installed:

- Python 3.8+
- FastAPI
- Pydantic
- pytest (for running tests)

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/NishanthMuruganantham/dynamic-formula-execution-api.git
    cd dynamic-formula-execution-api
    ```

2. **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:

    Use `pip` to install the required dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Tests**:

    Execute the unit tests to ensure everything is set up correctly:

    ```bash
    pytest
    ```

### API Endpoints 🌐

The API exposes endpoints to execute formulas dynamically using FastAPI. The main endpoint accepts the dataset and the list of formulas to be executed.

#### Endpoint: `/api/execute-formula`
- **Method**: `POST`
- **Description**: Executes the provided formulas on the given data and returns the results.

## Usage 📈

To use the API, you can run the FastAPI server locally:

```bash
python main.py
```

This will start the API, and you can use tools like **Postman** or **cURL** to send requests to the `/execute-formulas` endpoint.

### Example - 1 | Simple Addition 

#### Request Payload:
```json
{
    "data": [
        {
            "id": 1,
            "fieldA": 10
        },
        {
            "id": 2,
            "fieldA": 20
        }
    ],
    "formulas": [
        {
            "outputVar": "result",
            "expression": "fieldA + 10",
            "inputs": [
                {
                    "varName": "fieldA",
                    "varType": "number"
                }
            ]
        }
    ]
}
```

#### Response:
```json
{
    "results": {
        "result": [
            20,
            30
        ]
    },
    "message": "The formulas were executed successfully.",
    "status": "success"
}
```

### Example - 2 | Formula Chaining

#### Request Payload:
```json
{
    "data": [
        {
            "id": 1,
            "fieldA": 10,
            "fieldB": 2
        },
        {
            "id": 2,
            "fieldA": 20,
            "fieldB": 3
        }
    ],
    "formulas": [
        {
            "outputVar": "sumResult",
            "expression": "fieldA + fieldB",
            "inputs": [
                {
                    "varName": "fieldA",
                    "varType": "number"
                },
                {
                    "varName": "fieldB",
                    "varType": "number"
                }
            ]
        },
        {
            "outputVar": "finalResult",
            "expression": "sumResult * 2 + fieldA",
            "inputs": [
                {
                    "varName": "sumResult",
                    "varType": "number"
                },
                {
                    "varName": "fieldA",
                    "varType": "number"
                }
            ]
        }
    ]
}
```

#### Response Example:
```json
{
    "results": {
        "sumResult": [
            12,
            23
        ],
        "finalResult": [
            34,
            66
        ]
    },
    "message": "The formulas were executed successfully.",
    "status": "success"
}
```

### Example - 3 | Sales Revenue

#### Request Payload:
```json
{
    "data": [
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
    "formulas": [
        {
            "outputVar": "revenue",
            "expression": "((unitPrice * quantity) - (unitPrice * quantity * (discount / 100)))",
            "inputs": [
                {
                    "varName": "unitPrice",
                    "varType": "currency"
                },
                {
                    "varName": "quantity",
                    "varType": "number"
                },
                {
                    "varName": "discount",
                    "varType": "percentage"
                }
            ]
        }
    ]
}
```

#### Response Example:
```json
{
    "results": {
        "revenue": [
            4500,
            4750,
            4500
        ]
    },
    "message": "The formulas were executed successfully.",
    "status": "success"
}
```

## Public Deployment 🌎

The **Dynamic Formula Execution API** has been **publicly deployed** and can be accessed via **Vercel**.

**Live API URL**: [https://dynamic-formula-execution-api.vercel.app](https://dynamic-formula-execution-api.vercel.app)

This live deployment allows users to directly interact with the API for formula execution. Access it from Postman to perform POST calls.

## Features  🌟

- **Dynamic Expression Evaluation**: Supports dynamic evaluation of mathematical expressions based on input variables.
- **Formula Chaining**: Formulas can depend on the output of other formulas, allowing for complex workflows.
- **Topological Sorting**: Ensures that formulas are executed in the correct order based on their dependencies.
- **Error Handling**: Provides robust error handling for invalid expressions and missing input variables.
- **Extensible Framework**: Easily extendable to support additional data types or more complex formula logic.

## Key Components 🔑

### FormulaExecutor Class

The `FormulaExecutor` class is responsible for processing a list of formulas on the dataset. It first sorts the formulas based on their dependencies using topological sorting and then evaluates each formula dynamically.

#### Key Methods:
- **`perform_formula_execution`**: Executes all formulas in the correct order and returns the results.
- **`_perform_topogical_sort_for_formulas`**: Sorts formulas based on dependencies.
- **`_execute_formula_for_given_data`**: Safely evaluates a single formula on a given dataset.

### Models 📋

- **Data**: Represents the dataset structure.
- **Formula**: Defines each formula's expression and input-output variables.
- **Inputs**: Represents input variables for formulas.
- **ResultBody**: Holds the results of formula executions.

## Links 🔗

1) 🏁 Hackathon Link - https://hackathon-app.doselect.com/1464/problem/1poryb
2) 💻 Vercel Hosted API domain - https://dynamic-formula-execution-api.vercel.app
3) 📜 Swagger UI - An interactive documentation interface provided by FastAPI - https://dynamic-formula-execution-api.vercel.app/docs
4) ReDoc -  Another option for API documentation, offering a different interface. - https://dynamic-formula-execution-api.vercel.app/redoc

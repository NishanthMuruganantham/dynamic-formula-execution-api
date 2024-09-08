from src.models import Data, Formula, ResultBody
from typing import Any, List, Dict


class FormulaExecutor:

    def __init__(self, data_list: List[Data], formula_list: List[Formula]) -> None:
        self.data_list = data_list
        self.formula_list = formula_list

    @staticmethod
    def _safe_eval(expression: str, variables: Dict[str, Any]) -> Any:
        try:
            return eval(expression, {}, variables)
        except Exception as e:
            raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")

    def perform_formula_execution(self) -> List[ResultBody]:
        result_body = ResultBody()
        for formula in self.formula_list:
            expression = formula.expression
            inputs = formula.inputs
            output_var = formula.outputVar
            result_list = []
            for data in self.data_list:
                result_body = ResultBody()
                variables = {input_var.varName: getattr(data, input_var.varName) for input_var in inputs}
                result = self._safe_eval(expression, variables)
                result_list.append(result)
            setattr(result_body, output_var, result_list)
        
        return result_body

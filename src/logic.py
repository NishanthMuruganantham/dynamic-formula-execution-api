from src.models import Data, Formula, ResultBody, Inputs
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

    def _execute_formula_for_given_data(
        self, expression: str, list_of_incoming_inputs: List[Inputs], given_data: Data
    ) -> Any:
        input_variables = {input_variable.varName: given_data.model_dump()[input_variable.varName] for input_variable in list_of_incoming_inputs}
        expression_output = self._safe_eval(expression, input_variables)
        return expression_output

    def perform_formula_execution(self) -> List[ResultBody]:
        result_body: ResultBody = ResultBody()
        for formula_considered in self.formula_list:
            expression: str = formula_considered.expression
            list_of_incoming_inputs: List[Inputs] = formula_considered.inputs
            output_variable: str = formula_considered.outputVar
            output_list: List[float] = []
            
            for data in self.data_list:
                formula_output = self._execute_formula_for_given_data(expression, list_of_incoming_inputs, data)
                output_list.append(formula_output)
            setattr(result_body, output_variable, output_list)
        return result_body


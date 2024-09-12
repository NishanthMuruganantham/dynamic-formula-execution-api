from src.models import Data, Formula, ResultBody, Inputs
from typing import Any, List, Dict
from collections import defaultdict, deque


class FormulaExecutor:

    def __init__(self, data_list: List[Data], formula_list: List[Formula]) -> None:
        self.data_list = data_list
        self.formula_list = formula_list

    def perform_formula_execution(self) -> List[ResultBody]:
        result_body: ResultBody = ResultBody()
        sorted_formulas = self._perform_topogical_sort_for_formulas()
        
        
        for data in self.data_list:
            
            dynamic_attributes_for_data = {}
            
            for index, formula in enumerate(sorted_formulas):
                expression: str = formula.expression
                list_of_incoming_inputs: List[Inputs] = formula.inputs
                output_variable: str = formula.outputVar
                if getattr(result_body, output_variable, None) is None: setattr(result_body, output_variable, [])


                if index > 0:
                    for input_variable in list_of_incoming_inputs:
                        if input_variable.varName in dynamic_attributes_for_data:
                            setattr(data, input_variable.varName, dynamic_attributes_for_data[input_variable.varName])
                
                formula_output = self._execute_formula_for_given_data(expression, list_of_incoming_inputs, data)
                new_list: List = getattr(result_body, output_variable)
                new_list.append(formula_output)
                setattr(result_body, output_variable, new_list)
                dynamic_attributes_for_data[str(output_variable)] = formula_output
        
        return result_body

    def _execute_formula_for_given_data(
        self, expression: str, list_of_incoming_inputs: List[Inputs], given_data: Data
    ) -> Any:
        try:
            input_variables = {input_variable.varName: given_data.model_dump()[input_variable.varName] for input_variable in list_of_incoming_inputs}
        except KeyError as e:
            raise ValueError(f"Invalid input variable: {str(e)}")
        expression_output = self._safe_eval(expression, input_variables)
        return expression_output

    def _perform_topogical_sort_for_formulas(self) -> None:
        graph = defaultdict(list)
        in_count = defaultdict(int)

        formula_mapping_with_its_output_var = {formula.outputVar: formula for formula in self.formula_list}

        for formula in self.formula_list:
            for input_variable in formula.inputs:
                if input_variable.varName in formula_mapping_with_its_output_var:
                    graph[formula_mapping_with_its_output_var[input_variable.varName].outputVar].append(formula.outputVar)
                    in_count[formula.outputVar] += 1

        queue = deque([formula.outputVar for formula in self.formula_list if in_count[formula.outputVar] == 0])

        sorted_formulas = []
        while queue:
            output_var = queue.popleft()
            sorted_formulas.append(formula_mapping_with_its_output_var[output_var])

            for dependent in graph[output_var]:
                in_count[dependent] -= 1
                if in_count[dependent] == 0:
                    queue.append(dependent)

        if len(sorted_formulas) != len(self.formula_list):
            raise ValueError("The formula chain is broken!")

        return sorted_formulas

    @staticmethod
    def _safe_eval(expression: str, variables: Dict[str, Any]) -> Any:
        try:
            return eval(expression, {}, variables)
        except Exception as e:
            raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")

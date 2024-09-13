from collections import defaultdict, deque
from typing import Any, Dict, List
from src.models import Data, Formula, Inputs, ResultBody


class FormulaExecutor:
    """
    Class to execute formulas on a dataset and return results. 
    The formulas are topologically sorted to ensure proper dependency resolution.
    """

    def __init__(self, data_list: List[Data], formula_list: List[Formula]) -> None:
        """
        Initializes the FormulaExecutor with data and formulas.

        :param data_list: A list of Data objects representing the data to apply formulas to.
        :param formula_list: A list of Formula objects that define the formulas to be executed.
        """
        self.data_list = data_list
        self.formula_list = formula_list

    def perform_formula_execution(self) -> ResultBody:
        """
        Executes the formulas on the given data and returns the result in the form of a ResultBody.

        :return: ResultBody objects containing the formula execution results.
        """
        result_body: ResultBody = ResultBody()
        sorted_formulas = self._perform_topogical_sort_for_formulas()

        for data in self.data_list:

            dynamic_attributes_for_data = {}
            for index, formula in enumerate(sorted_formulas):
                expression: str = formula.expression
                list_of_incoming_inputs: List[Inputs] = formula.inputs
                output_variable: str = formula.outputVar
                if getattr(result_body, output_variable, None) is None:
                    setattr(result_body, output_variable, [])

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
        """
        Executes a single formula on a given data input.

        :param expression: The mathematical expression/formula to be evaluated.
        :param input_vars: A list of input variables required by the expression.
        :param data: The data object representing a single record.
        :return: The result of the formula execution.
        """
        try:
            input_variables = {input_variable.varName: given_data.model_dump()[input_variable.varName] for input_variable in list_of_incoming_inputs}
        except KeyError as e:
            raise ValueError(f"Invalid input variable: {str(e)}") from e
        expression_output = self._safe_eval(expression, input_variables)
        return expression_output

    def _perform_topogical_sort_for_formulas(self) -> List[Formula]:
        """
        Performs a topological sort on the formulas based on their input-output dependencies.
        This ensures that formulas are executed in the correct order.

        :return: A list of formulas sorted in execution order.
        :raises ValueError: If the formula chain contains a circular dependency.
        """

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
        """
        Safely evaluates a mathematical expression using the provided variables.

        :param expression: The mathematical expression to evaluate.
        :param variables: A dictionary of variable names and their corresponding values.
        :return: The result of the evaluated expression.
        :raises ValueError: If the expression is invalid.
        """
        try:
            return eval(expression, {}, variables)      # pylint: disable=eval-used
        except Exception as e:
            raise ValueError(f"Invalid expression: '{expression}'. Error: {str(e)}") from e

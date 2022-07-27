from piperider_cli.assertion_engine.assertion import AssertionContext, AssertionResult, ValidationResult
from piperider_cli.assertion_engine.types import BaseAssertionType, register_assertion_function


class AssertColumnAvgInRange(BaseAssertionType):
    def name(self):
        return "assert_column_avg_in_range"

    def execute(self, context: AssertionContext, table: str, column: str, metrics: dict):
        return assert_column_avg_in_range(context, table, column, metrics)

    def validate(self, context: AssertionContext) -> ValidationResult:
        print(ValidationResult(context))
        result = ValidationResult(context).require('avg')
        print(result)
        if result.has_errors():
            return result

        return result.require_range_pair('avg').require_same_types('avg')

class AssertNothingTableExample(BaseAssertionType):
    def name(self):
        return 'assert_nothing_table_example'

    def execute(self, context: AssertionContext, table: str, column: str, metrics: dict) -> AssertionResult:
        table_metrics = metrics.get('tables', {}).get(table)
        if table_metrics is None:
            # cannot find the table in the metrics
            return context.result.fail()

        # 1. Get the metric for the current table
        # We support two metrics for table level metrics: ['row_count', 'col_count']
        row_count = table_metrics.get('row_count')
        # col_count = table_metrics.get('col_count')

        # 2. Get expectation from assert input
        expected = context.asserts.get('something', [])

        # 3. Implement your logic to check requirement between expectation and actual value in the metrics

        # 4. send result

        # 4.1 mark it as failed result
        # return context.result.fail('what I saw in the metric')

        # 4.2 mark it as success result
        # return context.result.success('what I saw in the metric')

        return context.result.success('what I saw in the metric')

    def validate(self, context: AssertionContext) -> ValidationResult:
        result = ValidationResult(context)
        # result.errors.append('explain to users why this broken')
        return result


class AssertNothingColumnExample(BaseAssertionType):
    def name(self):
        return "assert_nothing_column_example"

    def execute(self, context: AssertionContext, table: str, column: str, metrics: dict) -> AssertionResult:
        column_metrics = metrics.get('tables', {}).get(table, {}).get('columns', {}).get(column)
        if column_metrics is None:
            # cannot find the column in the metrics
            return context.result.fail()

        # 1. Get the metric for the column metrics
        total = column_metrics.get('total')
        non_nulls = column_metrics.get('non_nulls')

        # 2. Get expectation from assert input
        expected = context.asserts.get('something', [])

        # 3. Implement your logic to check requirement between expectation and actual value in the metrics

        # 4. send result

        # 4.1 mark it as failed result
        # return context.result.fail('what I saw in the metric')

        # 4.2 mark it as success result
        # return context.result.success('what I saw in the metric')

        return context.result.success('what I saw in the metric')

    def validate(self, context: AssertionContext) -> ValidationResult:
        result = ValidationResult(context)
        # result.errors.append('explain to users why this broken')
        return result


def assert_column_avg_in_range(context: AssertionContext, table: str, column: str, metrics: dict) -> AssertionResult:
    return _assert_column_in_range(context, table, column, metrics, target_metric='avg')

def _assert_column_in_range(context: AssertionContext, table: str, column: str, metrics: dict,
                            **kwargs) -> AssertionResult:
    table_metrics = metrics.get('tables', {}).get(table)
    if table_metrics is None:
        return context.result.fail_with_metric_not_found_error(context.table, None)

    column_metrics = table_metrics.get('columns', {}).get(column)
    if column_metrics is None:
        return context.result.fail_with_metric_not_found_error(context.table, context.column)

    # Check assertion input
    target_metric = kwargs.get('target_metric')
    values = context.asserts.get(target_metric)
    if values is None or len(values) != 2:
        return context.result.fail_with_assertion_error('Expect a range [min_value, max_value].')

    class Observed(object):
        def __init__(self, column_metrics: dict, target_metric: str):
            self.column_metrics = column_metrics
            self.target_metric = target_metric
            self.column_type = column_metrics.get('type')
            self.actual = []

            if self.target_metric == 'range':
                self.actual = [column_metrics.get('min'), column_metrics.get('max')]
            else:
                self.actual = [column_metrics.get(target_metric)]

        def is_metric_available(self):
            return [x for x in self.actual if x is None] == []

        def check_range(self, min_value, max_value):
            for metric in self.actual:
                metric = self.to_numeric(metric)
                if metric is None:
                    yield context.result.fail_with_assertion_error('Column not support range.')
                else:
                    yield min_value <= metric <= max_value

        def to_numeric(self, metric):
            if self.column_type == 'datetime':
                # TODO: check datetime format. Maybe we can leverage the format checking by YAML parser
                return datetime.strptime(metric, '%Y-%m-%d %H:%M:%S.%f')
            elif self.column_type in ['integer', 'numeric']:
                return metric
            else:
                return None

        def actual_value(self):
            if len(self.actual) == 1:
                return self.actual[0]
            return self.actual

    observed = Observed(column_metrics, target_metric)
    if not observed.is_metric_available():
        return context.result.fail_with_metric_not_found_error(context.table, context.column)

    context.result.actual = {target_metric: observed.actual_value()}

    results = []
    for result in observed.check_range(values[0], values[1]):
        results.append(result)

    non_bools = [x for x in results if not isinstance(x, bool)]
    if non_bools:
        return non_bools[0]

    bools = [x for x in results if isinstance(x, bool)]
    if set(bools) == set([True]):
        return context.result.success()
    return context.result.fail()


# register new assertions
register_assertion_function(AssertNothingTableExample)
register_assertion_function(AssertNothingColumnExample)
register_assertion_function(AssertColumnAvgInRange)

import pandas as pd
import pytest

from .label_times import LabelTimes


@pytest.fixture(scope="module")
def labels():
    records = [
        {
            'label_id': 0,
            'customer_id': 1,
            'cutoff_time': '2014-01-01 00:45:00',
            'my_labeling_function': 226.92999999999998
        },
        {
            'label_id': 1,
            'customer_id': 1,
            'cutoff_time': '2014-01-01 00:48:00',
            'my_labeling_function': 47.95
        },
        {
            'label_id': 2,
            'customer_id': 2,
            'cutoff_time': '2014-01-01 00:01:00',
            'my_labeling_function': 283.46000000000004
        },
        {
            'label_id': 3,
            'customer_id': 2,
            'cutoff_time': '2014-01-01 00:04:00',
            'my_labeling_function': 31.54
        },
    ]

    dtype = {'cutoff_time': 'datetime64[ns]'}
    values = pd.DataFrame(records).astype(dtype).set_index('label_id')
    values = values[['customer_id', 'cutoff_time', 'my_labeling_function']]
    values = LabelTimes(values, name='my_labeling_function', target_entity='customer_id')
    return values


@pytest.fixture(autouse=True)
def add_labels(doctest_namespace, labels):
    doctest_namespace['labels'] = labels

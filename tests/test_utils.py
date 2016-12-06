from nxviz.utils import is_data_homogenous, infer_data_type, is_data_diverging

categorical = ['sun', 'moon', 'light']
ordinal = [1, 2, 3, 4, 5]
mixed = ['sun', 1, 2.5]
continuous = [1.0, 1.1, 1.2]
diverging_ordinal = [1, 2, 3, 4, -1, -2, -3, -4]
diverging_continuous = [0.0, 0.1, 0.2, 0.3, -0.1, -0.2, -0.3]


def test_is_data_homogenous():
    assert not is_data_homogenous(mixed)
    assert is_data_homogenous(categorical)
    assert is_data_homogenous(ordinal)
    assert is_data_homogenous(continuous)


def test_infer_data_type():
    assert infer_data_type(categorical) == 'categorical'
    assert infer_data_type(ordinal) == 'ordinal'
    assert infer_data_type(continuous) == 'continuous'


def test_is_data_diverging():
    assert is_data_diverging(diverging_ordinal)
    assert is_data_diverging(diverging_continuous)

    assert not is_data_diverging(ordinal)
    assert not is_data_diverging(continuous)

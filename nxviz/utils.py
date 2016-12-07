def is_data_homogenous(data_container):
    """
    Checks that all of the data in the container are of the same Python data
    type.
    """
    data_types = set([type(i) for i in data_container])
    return len(data_types) == 1


def infer_data_type(data_container):
    """
    For a given container of data, infer the type of data as one of
    continuous, categorical, or ordinal.

    For now, it is a one-to-one mapping as such:
    - str:   categorical
    - int:   ordinal
    - float: continuous
    """
    # Defensive programming checks.
    # 1. Don't want to deal with only single values.
    assert isinstance(data_container, list) or \
        isinstance(data_container, tuple), \
        "data_container should be a list or tuple"
    assert len(set(data_container)) > 1, \
        "there should be more than one value in the data container."
    # 2. Don't want to deal with mixed data.
    assert is_data_homogenous(data_container), \
        "data are not of a homogenous type!"

    datum = data_container[0]

    # Return statements below
    if isinstance(datum, str):
        return 'categorical'

    elif isinstance(datum, int):
        return 'ordinal'

    elif isinstance(datum, float):
        return 'continuous'

    else:
        raise ValueError('Not possible to tell what the data type is.')


def is_data_diverging(data_container):
    """
    We want to use this to check whether the data are diverging or not.

    This is a simple check, can be made much more sophisticated.
    """
    assert infer_data_type(data_container) in ['ordinal', 'continuous'], \
        "data type should be ordinal or continuous"

    # Check whether the data contains negative and positive values.
    has_negative = False
    has_positive = False
    for i in data_container:
        if i < 0:
            has_negative = True
        elif i > 0:
            has_positive = True
    if has_negative and has_positive:
        return True
    else:
        return False

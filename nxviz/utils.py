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

    There may be better ways that are not currently implemented below. For
    example, with a list of numbers, we can check whether the number of unique
    entries is less than or equal to 12, but has over 10000+ entries. This
    would be a good candidate for floats being categorical.
    """
    # Defensive programming checks.
    # 0. Ensure that we are dealing with lists or tuples, and nothing else.
    assert isinstance(data_container, list) or \
        isinstance(data_container, tuple), \
        "data_container should be a list or tuple."
    # 1. Don't want to deal with only single values.
    assert len(set(data_container)) > 1, \
        "There should be more than one value in the data container."
    # 2. Don't want to deal with mixed data.
    assert is_data_homogenous(data_container), \
        "Data are not of a homogenous type!"

    # Once we check that the data type of the container is homogenous, we only
    # need to check the first element in the data container for its type.
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
        "Data type should be ordinal or continuous"

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


def is_groupable(data_container):
    """
    Returns whether the data container is a "groupable" container or not.

    By "groupable", we mean it is a 'categorical' or 'ordinal' variable.

    If the data_container contains continuous variables, it'd be good to
    """
    is_groupable = False
    if infer_data_type(data_container) in ['categorical', 'ordinal']:
        is_groupable = True
    return is_groupable

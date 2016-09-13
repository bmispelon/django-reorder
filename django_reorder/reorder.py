from django.db.models import Case, IntegerField, Value, When


class BEFORE:
    pass


class AFTER:
    pass


def reorder(_default=AFTER, _reverse=False, **kwargs):
    """
    Return a database expression that can be used in an order_by() so that
    the queryset will be sorted according to the order of values given.
    """
    if not 0 < len(kwargs) <= 1:
        raise TypeError("reorder() takes one non-optional keyword argument")
    fieldname, new_order = kwargs.popitem()

    if _default is BEFORE:
        _default = -1
    elif _default is AFTER:
        _default = len(new_order)

    whens = [When(**{fieldname: v, 'then': i}) for i, v in enumerate(new_order)]

    casewhen = Case(*whens, default=Value(_default), output_field=IntegerField())

    if _reverse:
        return casewhen.desc()
    else:
        return casewhen.asc()


def null_first(fieldname):
    """
    Return a database expression that can be used in an order_by() close
    so that rows whose `fieldname` is NULL are sorted at the beginning.
    """
    return reorder(_default=AFTER, **{fieldname: [None]})


def null_last(fieldname):
    """
    Similar to null_first but NULL rows are sorted at the end.
    """
    return reorder(_default=BEFORE, **{fieldname: [None]})

import typing as t


def printf(*args: t.Any, **kwargs: t.Any) -> None:
    kwargs["flush"] = True
    print(*args, **kwargs)


def filter_nones(mapping: t.Mapping[str, t.Any]) -> t.Dict[str, t.Any]:
    return {key: value for key, value in mapping.items() if value is not None}


def pick(
    mapping: t.Mapping[str, t.Any], keys: t.Sequence[str]
) -> t.Dict[str, t.Any]:
    return {key: mapping[key] for key in keys if key in mapping}


def omit(
    mapping: t.Mapping[str, t.Any], keys: t.Sequence[str]
) -> t.Dict[str, t.Any]:
    return {key: mapping[key] for key in mapping if key not in keys}

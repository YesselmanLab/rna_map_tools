import os
import yaml
import json
import jsonschema
from jsonschema import Draft4Validator, validators

from rna_map_tools.logger import get_logger

log = get_logger("PARAMETERS")

PY_DIR = os.path.dirname(os.path.realpath(__file__))


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property_, subschema in properties.items():
            if "default" in subschema and not isinstance(instance, list):
                instance.setdefault(property_, subschema["default"])

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    return validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


def validate_parameters(params):
    path = PY_DIR + "/resources/params_schema.json"
    with open(path) as f:
        schema = json.load(f)
    # Validate the params against the schema
    FillDefaultValidatingDraft4Validator = extend_with_default(Draft4Validator)
    try:
        FillDefaultValidatingDraft4Validator(schema).validate(params)
    except jsonschema.exceptions.ValidationError as e:
        raise ValueError(e.message)


def parse_parameters_from_file(param_file):
    """
    Parse a YAML file and validate from a schema file loaded from json
    """
    # load param_file and validate against schema
    with open(param_file) as f:
        params = yaml.safe_load(f)
    if params is None:
        params = {}
    validate_parameters(params)
    return params


def get_default_params():
    """
    Get the default parameters
    """
    path = PY_DIR + "/resources/default.yml"
    return parse_parameters_from_file(path)

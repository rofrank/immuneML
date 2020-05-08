import os
from copy import copy


class Util:

    @staticmethod
    def to_dict_recursive(obj, base_path):
        if not hasattr(obj, "__dict__"):
            if hasattr(obj, "name"):
                return obj.name
            elif isinstance(obj, list):
                return [Util.to_dict_recursive(element, base_path) for element in obj]
            elif isinstance(obj, str) and os.path.isfile(obj):
                return Util.get_relative_path(base_path, obj)
            else:
                return obj if obj is not None else ""
        else:
            vars_obj = vars(obj)
            return {
                attribute_name: Util.to_dict_recursive(vars_obj[attribute_name], base_path) for attribute_name in vars_obj.keys()
            }

    @staticmethod
    def get_css_content(css_path: str):
        with open(css_path, "rb") as file:
            content = file.read()
        return content

    @staticmethod
    def get_relative_path(base_path, tmp_path):
        path = copy(tmp_path)
        common_path = os.path.commonpath([base_path, tmp_path])
        path = path.replace(common_path, ".")
        return path
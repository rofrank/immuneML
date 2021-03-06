class NameBuilder:

    @staticmethod
    def build_name_from_dict(dictionary: dict, level=0):

        """ Creates a name from dictionary which includes all of its parameters;
            Handles nested dictionaries up to depth of 10 inclusively
            Keyword arguments:
            :param dictionary - dictionary to create the name from
            :param level - controls recursion level, user should keep default
            :return name
        """

        if level > 10:
            raise Exception("Too many nested dicts for serialization in NameBuilder!")

        name = ""

        keys = sorted(list(dictionary.keys()))
        for key in keys:

            if isinstance(dictionary[key], dict):
                value = "{" + NameBuilder.build_name_from_dict(dictionary[key], level=level + 1) + "}"
            else:
                value = str(dictionary[key])

            name = name + key + "_" + value + "__"

        name = name[0:(len(name) - 2)]
        name = name.replace(" ", "")

        return name

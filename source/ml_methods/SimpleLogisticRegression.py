from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV

from source.ml_methods.SklearnMethod import SklearnMethod


class SimpleLogisticRegression(SklearnMethod):
    """
    Logistic regression wrapper of the corresponding scikit-learn's method.

    For usage and YAML specification, check :py:obj:`~source.ml_methods.SklearnMethod.SklearnMethod`.
    For valid parameters, see `scikit-learn documentation <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html>`_.

    If you are interested in plotting the coefficients of the logistic regression model,
    consider running the :py:obj:`~source.reports.ml_reports.Coefficients.Coefficients` report.

    YAML specification:

    .. indent with spaces
    .. code-block:: yaml

        my_logistic_regression: # user-defined method name
            SimpleLogisticRegression: # name of the ML method
                # sklearn parameters (same names as in original sklearn class)
                penalty: l1 # use l1 regularization
                C: 10 # regularization constant
                # Additional parameter that determines whether to print convergence warnings
                show_warnings: True
        # alternative way to define ML method with default values:
        my_default_logistic_regression: SimpleLogisticRegression

    """

    default_parameters = {"max_iter": 1000, "solver": "saga"}

    def __init__(self, parameter_grid: dict = None, parameters: dict = None):
        parameters = {**self.default_parameters, **(parameters if parameters is not None else {})}

        if parameter_grid is not None:
            parameter_grid = parameter_grid
        else:
            parameter_grid = {"max_iter": [1000],
                                    "penalty": ["l1", "l2"],
                                    "C": [0.001, 0.01, 0.1, 10, 100, 1000],
                                    "class_weight": ["balanced"]}

        super(SimpleLogisticRegression, self).__init__(parameter_grid=parameter_grid, parameters=parameters)




    def _get_ml_model(self, cores_for_training: int=2, X=None):
        params = self._parameters.copy()
        params["n_jobs"] = cores_for_training
        return LogisticRegression(**params)

    def can_predict_proba(self) -> bool:
        return True

    def get_params(self, label):
        if label is None:
            tmp_label = list(self.models.keys())[0]
        else:
            tmp_label = label

        params = self.models[tmp_label].estimator.get_params() if isinstance(self.models[tmp_label], RandomizedSearchCV) \
            else self.models[tmp_label].get_params()
        params["coefficients"] = self.models[tmp_label].coef_[0].tolist()
        params["intercept"] = self.models[tmp_label].intercept_.tolist()
        return params

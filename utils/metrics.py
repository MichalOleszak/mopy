import numpy as np
from sklearn.calibration import calibration_curve


def calibration_score(y_test, X_test, model, n_bins=10):
    """
    Computes Mean Squared Error between the model and perfect calibration curves, over {n_bins} probability bins.
    The {model} argument needs to have the predict_proba method implemented in the sklearn fashion.
    Lower is better. Zero is perfect.
    """
    cal = calibration_curve(y_test, model.predict_proba(X_test)[:, 1], n_bins=n_bins, strategy="quantile")
    return np.sum((cal[0] - cal[1]) ** 2)


def accuracy_calibration_error(accuracy, calibration, accuracy_calibration_weight):
    """
    Combine the accuracy and calibration of the method. The overall metric is a weighted sum.
    Small value indicates a good model. Accuracy is ~0.8, calibration is ~0.003, hence
    accuracy_calibration_weight around 20 seems to provide good balance between them.
    """
    return (1.0 - accuracy) + accuracy_calibration_weight * calibration

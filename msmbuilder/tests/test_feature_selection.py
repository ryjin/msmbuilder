import numpy as np

from sklearn.feature_selection import VarianceThreshold as VarianceThresholdR

from ..featurizer import DihedralFeaturizer
from ..feature_selection import FeatureSelector, VarianceThreshold
from ..example_datasets import fetch_alanine_dipeptide as fetch_data

FEATS = [
        ('phi', DihedralFeaturizer(types=['phi'], sincos=True)),
        ('psi', DihedralFeaturizer(types=['psi'], sincos=True)),
    ]


def test_featureselector():
    dataset = fetch_data()
    trajectories = dataset["trajectories"]

    fs = FeatureSelector(FEATS, which_feat='phi')

    assert fs.which_feat == ['phi']

    y1 = fs.partial_transform(trajectories[0])
    y_ref1 = FEATS[0][1].partial_transform(trajectories[0])

    np.testing.assert_array_almost_equal(y_ref1, y1)


def test_featureselector_transform():
    dataset = fetch_data()
    trajectories = dataset["trajectories"]

    fs = FeatureSelector(FEATS, which_feat='psi')

    y1 = fs.transform(trajectories)

    assert len(y1) == len(trajectories)


def test_variancethreshold_vs_sklearn():
    dataset = fetch_data()
    trajectories = dataset["trajectories"]

    fs = FeatureSelector(FEATS)

    vt = VarianceThreshold(0.1)
    vtr = VarianceThresholdR(0.1)

    y = fs.partial_transform(trajectories[0])

    z1 = vt.fit_transform([y])[0]
    z_ref1 = vtr.fit_transform(y)

    np.testing.assert_array_almost_equal(z_ref1, z1)

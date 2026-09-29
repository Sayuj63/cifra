"""Configuration shared by the DVC pipeline and Python entry points."""

import yaml

from ml.common import ROOT

PARAMS = yaml.safe_load((ROOT / "params.yaml").read_text(encoding="utf-8"))
if (
    abs(
        sum(PARAMS[name] for name in ("train_fraction", "calibration_fraction", "test_fraction"))
        - 1
    )
    > 1e-9
):
    raise ValueError("train, calibration, and test fractions must sum to one")
if not 0 < PARAMS["nominal_interval_coverage"] < 1:
    raise ValueError("nominal_interval_coverage must be between zero and one")

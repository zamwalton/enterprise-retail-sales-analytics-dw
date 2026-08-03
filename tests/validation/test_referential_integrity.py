import pandas as pd
import pytest

from etl.validation.referential_integrity import (
    validate_referential_integrity,
)


def test_validate_referential_integrity_passes():

    fact_df = pd.DataFrame(
        {
            "customer_key": [1, 2, 3, 4],
        }
    )

    dimension_df = pd.DataFrame(
        {
            "customer_key": [1, 2, 3, 4, 5],
        }
    )

    validate_referential_integrity(
        fact_df=fact_df,
        fact_column="customer_key",
        dimension_df=dimension_df,
        dimension_column="customer_key",
    )


def test_validate_referential_integrity_detects_orphan_keys():

    fact_df = pd.DataFrame(
        {
            "customer_key": [1, 2, 999],
        }
    )

    dimension_df = pd.DataFrame(
        {
            "customer_key": [1, 2, 3],
        }
    )

    with pytest.raises(ValueError, match="orphan"):
        validate_referential_integrity(
            fact_df=fact_df,
            fact_column="customer_key",
            dimension_df=dimension_df,
            dimension_column="customer_key",
        )


def test_validate_referential_integrity_detects_missing_fact_column():

    fact_df = pd.DataFrame(
        {
            "wrong_column": [1, 2, 3],
        }
    )

    dimension_df = pd.DataFrame(
        {
            "customer_key": [1, 2, 3],
        }
    )

    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        validate_referential_integrity(
            fact_df=fact_df,
            fact_column="customer_key",
            dimension_df=dimension_df,
            dimension_column="customer_key",
        )


def test_validate_referential_integrity_detects_missing_dimension_column():

    fact_df = pd.DataFrame(
        {
            "customer_key": [1, 2, 3],
        }
    )

    dimension_df = pd.DataFrame(
        {
            "wrong_column": [1, 2, 3],
        }
    )

    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        validate_referential_integrity(
            fact_df=fact_df,
            fact_column="customer_key",
            dimension_df=dimension_df,
            dimension_column="customer_key",
        )
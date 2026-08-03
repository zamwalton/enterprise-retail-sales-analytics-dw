import pandas as pd
import pytest

from etl.validation.range_validation import (
    validate_numeric_range,
)


def test_validate_numeric_range_passes():

    df = pd.DataFrame(
        {
            "quantity": [1, 2, 5, 10],
        }
    )

    validate_numeric_range(
        df=df,
        column="quantity",
        minimum=1,
        maximum=10,
    )


def test_validate_numeric_range_detects_below_minimum():

    df = pd.DataFrame(
        {
            "quantity": [1, 2, 0, 5],
        }
    )

    with pytest.raises(
        ValueError,
        match="Range validation failed",
    ):
        validate_numeric_range(
            df=df,
            column="quantity",
            minimum=1,
        )


def test_validate_numeric_range_detects_above_maximum():

    df = pd.DataFrame(
        {
            "discount_percentage": [10, 25, 50, 120],
        }
    )

    with pytest.raises(
        ValueError,
        match="Range validation failed",
    ):
        validate_numeric_range(
            df=df,
            column="discount_percentage",
            minimum=0,
            maximum=100,
        )


def test_validate_numeric_range_detects_missing_column():

    df = pd.DataFrame(
        {
            "quantity": [1, 2, 3],
        }
    )

    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        validate_numeric_range(
            df=df,
            column="unit_price",
            minimum=0,
        )
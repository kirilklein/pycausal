import pandas as pd
from pycausal.utils.helpers import check_required_columns


def compute_matching_ate(
    Y: pd.Series,
    matching_df: pd.DataFrame,
    treated_col: str = "treated_pid",
    control_col: str = "control_pid",
) -> float:
    """
    Compute the effect using matching with vectorized Pandas operations.

    Args:
        Y (pd.Series): Outcomes for both treated and control units.
        matching_df (pd.DataFrame): DataFrame containing matching results with columns
                                    treated_col and control_col indicating the
                                    matched treated and control unit IDs.

    Returns:
        float: The estimated ATE using the matched data.
    """
    check_required_columns(matching_df, [treated_col, control_col])
    # Merge the treated outcomes with the control outcomes
    merged_df = matching_df.merge(
        Y.rename("treated_outcome"), left_on=treated_col, right_index=True
    )
    merged_df = merged_df.merge(
        Y.rename("control_outcome"), left_on=control_col, right_index=True
    )

    # Compute the average control outcome for each treated unit using groupby
    avg_control_outcomes = merged_df.groupby(treated_col)["control_outcome"].mean()

    # Compute the difference between treated outcome and control outcome for each treated unit
    treated_outcomes = Y[
        avg_control_outcomes.index
    ]  # Ensure we're aligning with grouped treated pids
    diffs = treated_outcomes - avg_control_outcomes

    # Return the average difference (ATE)
    return diffs.mean()

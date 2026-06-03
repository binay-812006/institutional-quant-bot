import pandas as pd


def analyze_feature_importance(

    model,

    features

):

    importance_df = pd.DataFrame({

        'feature': features,

        'importance': model.feature_importances_

    })

    importance_df = importance_df.sort_values(

        by='importance',

        ascending=False

    )

    return importance_df
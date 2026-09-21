# ============================================================
# PREPROCESSING MODULE
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# ============================================================

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


# ============================================================
# CREATE PREPROCESSOR
# ============================================================

def create_preprocessor(X):
    """
    Automatically identifies numerical and categorical columns
    and creates a preprocessing pipeline.

    Parameters:
    -----------
    X : pandas DataFrame
        Input feature dataset.

    Returns:
    --------
    preprocessor : ColumnTransformer
        Complete preprocessing pipeline.
    """

    # --------------------------------------------------------
    # IDENTIFY NUMERICAL FEATURES
    # --------------------------------------------------------

    numerical_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()


    # --------------------------------------------------------
    # IDENTIFY CATEGORICAL FEATURES
    # --------------------------------------------------------

    categorical_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    # --------------------------------------------------------
    # NUMERICAL PIPELINE
    # --------------------------------------------------------

    numerical_transformer = Pipeline(

        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),

            (
                "scaler",
                StandardScaler()
            )

        ]

    )


    # --------------------------------------------------------
    # CATEGORICAL PIPELINE
    # --------------------------------------------------------

    categorical_transformer = Pipeline(

        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )

        ]

    )


    # --------------------------------------------------------
    # COMBINE PREPROCESSING
    # --------------------------------------------------------

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "numerical",
                numerical_transformer,
                numerical_features
            ),

            (
                "categorical",
                categorical_transformer,
                categorical_features
            )

        ],

        remainder="drop"

    )


    return preprocessor


# ============================================================
# GET FEATURE TYPES
# ============================================================

def get_feature_types(X):
    """
    Returns numerical and categorical feature names.
    """

    numerical_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()


    categorical_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    return numerical_features, categorical_features
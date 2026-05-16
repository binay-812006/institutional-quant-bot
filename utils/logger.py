import json


def save_results(
    metrics,
    capital,
    filepath="research/results.json"
):

    output = {
        "FinalCapital": capital,
        "Metrics": metrics
    }

    with open(filepath, "w") as f:

        json.dump(
            output,
            f,
            indent=4
        )

    print(
        f"Results saved to {filepath}"
    )
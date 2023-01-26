import pandas as pd


def create_html_table(data: list[list[str]], columns: list[str]) -> str:
    """
    Creates an HTML table from a list of data and a list of column names.
    """
    df = pd.DataFrame(
        data,
        columns=columns,
    )
    html_table = df.to_html(index=False)
    return html_table


def save_to_file(title: str, table: str, data_type: str) -> None:
    """
    Saves an HTML table to a file with the specified name.
    """
    with open(f"{title}-{data_type}.html", "w", encoding="UTF-8") as file:
        file.write(table)
    print("Your file with requested data is ready.")

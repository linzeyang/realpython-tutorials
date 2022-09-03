from argparse import ArgumentParser, Namespace
from typing import Optional


def read_user_cli_args() -> Namespace:
    """_summary_

    Returns:
        Namespace: _description_
    """
    parser = ArgumentParser(
        prog="rpchecker", description="check the availability of sites"
    )

    parser.add_argument(
        "-u",
        "--urls",
        metavar="URLs",
        nargs="+",
        type=str,
        default=[],
        help="one or more websites' URLs",
    )

    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="file containing URLs",
    )

    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="switch on async mode",
    )

    return parser.parse_args()


def display_check_result(
    result: bool, url: str, error: str = "", time: Optional[float] = None
) -> None:
    """_summary_

    Args:
        result (bool): _description_
        url (str): _description_
        error (str, optional): _description_. Defaults to "".
    """
    print(f"The status of {url:<30} is:", end=" ")

    if result:
        print(f'"Online!" 👍 | Took: {time:.3f} secs')
    else:
        print(f'"Offline?" 👎\n Error: {error}')

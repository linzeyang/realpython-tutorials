import asyncio
import pathlib
import sys
from argparse import Namespace
from time import perf_counter
from typing import List

from .checker import async_site_is_online, site_is_online
from .cli import display_check_result, read_user_cli_args


def _get_websites_urls(user_args: Namespace) -> List[str]:
    """_summary_

    Args:
        user_args (Namespace): _description_

    Returns:
        List[str]: _description_
    """
    urls: List[str] = user_args.urls

    if file := user_args.input_file:
        urls.extend(_read_urls_from_file(file))

    return urls


def _read_urls_from_file(file: str) -> List[str]:
    """_summary_

    Args:
        file (str): _description_

    Returns:
        List[str]: _description_
    """
    file_path = pathlib.Path(file)

    if not file_path.is_file():
        print("Input file not found/not a file", file=sys.stderr)
        return []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            urls = list(map(lambda line: line.strip(), f))
    except Exception as e:
        print(str(e), file=sys.stderr)
        return []

    return urls


def _synchronous_check(urls: List[str]) -> None:
    """_summary_

    Args:
        urls (List[str]): _description_
    """
    for url in urls:
        a = perf_counter()
        try:
            result = site_is_online(url=url)
        except Exception as e:
            display_check_result(result=False, url=url, error=str(e))
        else:
            display_check_result(result=result, url=url, time=perf_counter() - a)


async def _asynchronous_check(urls: List[str]) -> None:
    """_summary_

    Args:
        urls (List[str]): _description_
    """

    async def _wrapper(url: str) -> None:
        a = perf_counter()
        try:
            result = await async_site_is_online(url=url)
        except Exception as e:
            display_check_result(result=False, url=url, error=str(e))
        else:
            display_check_result(result=result, url=url, time=perf_counter() - a)

    await asyncio.gather(*(_wrapper(url) for url in urls))


def main() -> None:
    a = perf_counter()

    user_args = read_user_cli_args()
    urls = _get_websites_urls(user_args)

    if not urls:
        print("Error: no URLs provided", file=sys.stderr)
        sys.exit(1)

    if not user_args.asynchronous:
        _synchronous_check(urls)
    else:
        asyncio.run(_asynchronous_check(urls))

    print(f"Time elapsed: {perf_counter() - a} seconds")


if __name__ == "__main__":
    main()

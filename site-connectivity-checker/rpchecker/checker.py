import asyncio
from http.client import HTTPConnection
from urllib.parse import urlparse

import aiohttp


def site_is_online(url: str, timeout: int = 2) -> bool:
    """_summary_

    Args:
        url (str): _description_
        timeout (int, optional): _description_. Defaults to 2.

    Raises:
        error: _description_

    Returns:
        bool: _description_
    """
    is_online = False

    error = Exception("UNKNOWN ERROR")

    parser = urlparse(url=url)

    host = parser.netloc or parser.path.split("/")[0]

    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout=timeout)

        try:
            connection.request(method="HEAD", url="/")
        except Exception as e:
            error = e
        else:
            is_online = True
        finally:
            connection.close()

    if is_online:
        return is_online
    raise error


async def async_site_is_online(url: str, timeout: int = 2) -> bool:
    """_summary_

    Args:
        url (str): _description_
        timeout (int, optional): _description_. Defaults to 2.

    Returns:
        bool: _description_
    """
    is_online = False

    error = Exception("UNKNOWN ERROR")

    parser = urlparse(url=url)

    host = parser.netloc or parser.path.split("/")[0]

    for scheme in ("https", "http"):
        target = f"{scheme}://{host}"

        async with aiohttp.ClientSession() as session:
            try:
                await session.head(url=target, timeout=timeout)
            except asyncio.exceptions.TimeoutError:
                error = Exception("Timed out!")
            except Exception as e:
                error = e
            else:
                is_online = True

    if is_online:
        return is_online
    raise error

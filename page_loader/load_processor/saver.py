from pathlib import Path
from typing import Union, Callable


def save_data_to_file(data: Union[str, bytes],
                      file_path: Path,
                      mode: str) -> None:
    '''Saves data to the specified file.\n
    Saving occurs in binary mode if the data is binary,
    in other cases in text mode.'''
    with file_path.open(mode) as file:
        file.write(data)


def save_page(data: str, file_path: Path) -> Callable[..., None]:
    '''Writes page data in standard mode.'''
    save_data_to_file(data, file_path, 'w')


def save_resource(data: bytes, file_path: Path) -> Callable[..., None]:
    '''Writes resource data in binary mode.'''
    save_data_to_file(data, file_path, 'wb')

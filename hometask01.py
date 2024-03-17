import argparse
import asyncio
import logging
import os
from aiopath import AsyncPath
from aioshutil import copyfile


# Створюємо об'єкт ArgumentParser для обробки аргументів командного рядка.
parser = argparse.ArgumentParser(description="Sorting files")

# Додаємо необхідні аргументи для визначення вихідної та цільової папок.
parser.add_argument("--source", "-s", required=True, help="Source dir")
parser.add_argument("--output", "-o", help="Output dir", default="destination")
args = vars(parser.parse_args())
# Ініціалізуємо асинхронні шляхи для вихідної та цільової папок.
source = AsyncPath(args["source"])
output = AsyncPath(args["output"])

# Асинхронна функція, яка рекурсивно читає всі файли у вихідній папці та її підпапках.
async def read_folder(path: AsyncPath):
    if os.path.exists(path):    
        async for file in path.iterdir():
            if await file.is_dir():
                await read_folder(file)
            else:
                await copy_file(file)
    else:
        print(f"Помилка: Директорії '{path}' не існує.")
        exit()

# Асинхронна функція, яка копіює кожен файл у відповідну підпапку у цільовій папці на основі його розширення.
async def copy_file(file: AsyncPath):
    folder = output / file.suffix[1:]
    try:
        await folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, folder / file.name)
    except OSError as e:
        logging.error(e)


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    asyncio.run(read_folder(source))

    print(f"Всі файли скопійовані у '{output}'.")
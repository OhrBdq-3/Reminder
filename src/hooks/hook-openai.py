from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("openai")

# openai 2.x 的隐式依赖（非常关键）
hiddenimports += [
    "jiter",
    "pydantic",
    "pydantic_core",
    "typing_inspection",
    "anyio",
    "httpx",
    "httpcore",
    "sniffio",
]

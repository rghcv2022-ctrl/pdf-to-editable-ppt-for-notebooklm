from .core import (
    SUPPORTED_EXTENSIONS,
    build_output_path,
    convert_file,
    create_ocr_engine,
    get_runtime_summary,
    initialize_runtime,
    is_supported_input,
    log_runtime_summary,
    resolve_poppler_path,
)


def cli_main() -> int:
    from .cli import main

    return main()


def example_main() -> int:
    from .example import main

    return main()


def __getattr__(name: str):
    if name == "App":
        from .gui import App

        return App
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "build_output_path",
    "convert_file",
    "create_ocr_engine",
    "get_runtime_summary",
    "initialize_runtime",
    "is_supported_input",
    "log_runtime_summary",
    "resolve_poppler_path",
    "SUPPORTED_EXTENSIONS",
    "cli_main",
    "example_main",
    "App",
]

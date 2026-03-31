from __future__ import annotations

from convertppt.core import build_ocr_dependency_error_message


def test_build_ocr_dependency_error_message_explains_protobuf_fix() -> None:
    message = build_ocr_dependency_error_message(
        TypeError("Descriptors cannot be created directly.")
    )

    assert "protobuf<=3.20.3" in message
    assert "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python" in message

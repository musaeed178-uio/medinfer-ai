# SPDX-License-Identifier: AGPL-3.0-or-later
"""MedInfer AI — entry point.

Follows the ``building-multi-ui-apps`` skill pattern:
one entry point per interface, composition root wires everything.

Currently only the GUI interface is shipped.  A future CLI could be
added as another ``@app.command`` (or a separate script) that calls
:func:`bootstrap.create_manager` and drives the terminal.
"""

from __future__ import annotations

import sys


def main() -> None:
    """Launch the GUI (the primary and only shipped interface)."""
    from bootstrap import create_manager  # noqa: PLC0415 - lazy import
    from gui import ModernMedicalGUI     # noqa: PLC0415 - lazy import

    try:
        manager = create_manager()
    except Exception as exc:  # noqa: BLE001
        from tkinter import messagebox  # noqa: PLC0415
        messagebox.showerror("MedInfer AI could not start", str(exc))
        raise SystemExit(1) from exc

    app = ModernMedicalGUI(manager=manager)
    app.run()


if __name__ == "__main__":
    main()

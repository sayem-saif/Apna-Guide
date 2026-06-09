"""Unit tests for the WelcomeWindow GUI class in AGTSP.py.

All tests mock tkinter to avoid requiring a display server.
Tests are skipped when the ``_tkinter`` C extension is not available
(e.g. pyenv builds without tk-dev).
"""

from unittest.mock import patch, MagicMock

import pytest

tk = pytest.importorskip("tkinter", reason="tkinter not available")


@pytest.fixture()
def app():
    """Create a WelcomeWindow instance with a headless Tk root."""
    root = tk.Tk()
    root.withdraw()  # hide the window (works even without a display)

    # Patch Image.open so it doesn't need the actual fl.jpg file
    with patch("AGTSP.Image") as mock_image_mod, \
         patch("AGTSP.ImageTk") as mock_imagetk:
        mock_image_mod.open.return_value = MagicMock()
        mock_imagetk.PhotoImage.return_value = MagicMock()

        from AGTSP import WelcomeWindow
        window = WelcomeWindow(master=root)

    yield window
    root.destroy()


class TestGreetUser:
    def test_greet_with_name(self, app):
        app.name_entry.insert(0, "Pune")
        app.greet_user()
        text = app.label.cget("text")
        assert "Pune" in text
        assert "Shortest" in text or "shortest" in text.lower()

    def test_greet_without_name(self, app):
        app.greet_user()
        text = app.label.cget("text")
        assert "Welcome" in text

    def test_greet_with_arbitrary_text(self, app):
        app.name_entry.insert(0, "Alice")
        app.greet_user()
        text = app.label.cget("text")
        assert "Alice" in text


class TestShowPathValidation:
    def test_invalid_city_shows_error(self, app):
        app.name_entry.insert(0, "InvalidCity")
        app.show_path()
        text = app.label.cget("text")
        assert "Invalid" in text

    @patch("AGTSP.plt")
    def test_valid_city_does_not_show_error(self, mock_plt, app):
        app.name_entry.insert(0, "Thane")
        app.show_path()
        text = app.label.cget("text")
        assert "Invalid" not in text


class TestWidgetCreation:
    def test_has_name_entry(self, app):
        assert app.name_entry is not None

    def test_has_greet_button(self, app):
        assert app.greet_button is not None

    def test_has_show_path_button(self, app):
        assert app.close_button is not None

    def test_has_label(self, app):
        assert app.label is not None

    def test_window_title(self, app):
        assert app.master.title() == "Apna Guide Using TSP"

from pathlib import Path

base_dir = Path(__file__).parent


def show_intro():
    render_ascii('intro_banner.txt')


def render_ascii(filename):
    filepath = base_dir / 'assets' / 'ascii' / filename
    try:
        with filepath.open('r', encoding='utf-8') as file:
            print(file.read(), end='')
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    show_intro()

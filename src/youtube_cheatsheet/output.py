import pathlib

import pytube.helpers
from jinja2 import BaseLoader, Environment, PackageLoader, Template

import youtube_cheatsheet.exceptions


def setup_jinja_env() -> Environment:
    """Render the output template with the provided inputs."""
    return Environment(loader=jinja_loader(), autoescape=True)


def jinja_loader() -> BaseLoader:
    """Return a Jinja2 PackageLoader object for the "youtube_cheatsheet" package."""
    return PackageLoader("youtube_cheatsheet")


def get_template(env: Environment, template_name: str = "output.md.j2") -> Template:
    """Get the Jinja2 template for generating output files."""
    return env.get_template(template_name)


def get_output(
    title: str,
    youtube_data_metadata: str | None,
    output_takeaways: str | None,
    output_summary: str | None,
) -> str:
    """Render the output template with the provided inputs."""
    output_dict = locals()
    env = setup_jinja_env()
    template = get_template(env)
    return template.render(**output_dict)


def create_file_path(filename: str, path: pathlib.Path) -> pathlib.Path:
    """Create a file path by joining the given filename with the provided path and changing the file extension to '.md'."""
    # Separate the file creation process for better readability
    return path.joinpath(filename).with_suffix(".md")


def write_file(title: str, content: str, path: pathlib.Path) -> None:
    """Write the given content to a file with the specified title and path."""
    file = create_file_path(pytube.helpers.safe_filename(title), path)

    if not validate_output_path(file, path):
        raise youtube_cheatsheet.exceptions.OutputPathValidationError()

    file.write_text(content)


def validate_output_path(file_path: pathlib.Path, dir_path: pathlib.Path) -> bool:
    """Validate the output file and directory paths."""
    return dir_path.exists() and dir_path.is_dir() and not file_path.exists()

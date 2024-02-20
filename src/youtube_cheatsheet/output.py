import pathlib

import slugify
from jinja2 import Environment, PackageLoader, Template

import youtube_cheatsheet.exceptions
import pytube.helpers
# import pytube.helpers.safe_filename


def setup_jinja_env() -> Environment:
    return Environment(
        loader=PackageLoader("youtube_cheatsheet"),
        autoescape=True,
    )


def get_template(env: Environment, template_name: str = "output.md.j2") -> Template:
    return env.get_template(template_name)


def get_output(
    title: str,
    youtube_data_metadata: str | None,
    output_takeaways: str | None,
    output_summary: str | None,
) -> str:
    output_dict = locals()
    env = setup_jinja_env()
    template = get_template(env)
    return template.render(**output_dict)


def create_file_path(filename: str, path: pathlib.Path) -> pathlib.Path:
    # Separate the file creation process for better readability
    return path.joinpath(filename).with_suffix(".md")


def write_file(title: str, content: str, path: pathlib.Path) -> None:
    file = create_file_path(pytube.helpers.safe_filename(title), path)

    if not validate_output_path(file, path):
        raise youtube_cheatsheet.exceptions.OutputPathValidationError()

    file.write_text(content)


def validate_output_path(file_path: pathlib.Path, dir_path: pathlib.Path) -> bool:
    return dir_path.exists() and dir_path.is_dir() and not file_path.exists()

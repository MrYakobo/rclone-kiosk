#!/usr/bin/env python3

import argparse
from glob import glob
import os
import subprocess
import mimetypes
import tempfile
from jinja2 import Environment, FileSystemLoader

script_path = os.path.dirname(os.path.realpath(__file__))

jinja_env = Environment(
    loader=FileSystemLoader(f"{script_path}/templates/"),
    trim_blocks=True,
    lstrip_blocks=True,
)

template = jinja_env.get_template("reveal.html.j2")

from dataclasses import dataclass, field


@dataclass
class Asset:
    filename: str
    webroot_base: str = ""
    webroot_filename: str = field(init=False)
    mimetype: str = field(init=False)

    def __post_init__(self) -> None:
        self.mimetype = mimetypes.guess_type(self.filename)[0]
        self.webroot_filename = os.path.join(self.webroot_base, self.filename)

    def __lt__(self, other):
        # sort alphabetically
        return self.webroot_filename < other.webroot_filename


def run(*args):
    subprocess.run(args, check=True)


def get_source(rclone_config_filename, local_dir):
    run("rm", "-rf", local_dir)
    run(
        "rclone", "--progress", "--config", rclone_config_filename, "sync", "source:", local_dir
    )


def render(source_dir):
    cwd = os.getcwd()
    os.chdir(source_dir)
    assets = [Asset(f) for f in glob("*")]
    os.chdir(cwd)
    html = template.render(assets=assets)
    with open(f"{source_dir}/index.html", "w") as f:
        f.write(html)

def upload_to_remote(rclone_config_filename, source_dir):
    run(
        "rclone", "--progress", "--config", rclone_config_filename, "-v", "sync", source_dir, "remote:"
    )


def rclone_kiosk(rclone_config_filename):
    with tempfile.TemporaryDirectory() as source_dir:
        # download sources
        print("downloading from [source]...")
        get_source(rclone_config_filename,source_dir)

        # render index.html
        print("rendering index.html...")
        render(source_dir)

        # push to server
        print("pushing to [remote]...")
        upload_to_remote(rclone_config_filename, source_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=os.path.expanduser('~/.config/rclone/rclone.conf'))
    args = parser.parse_args()
    rclone_kiosk(args.config)

if __name__=='__main__':
    main()
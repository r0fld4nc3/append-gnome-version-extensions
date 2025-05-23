# What it does
 A command line script that appends the given GNOME version each extension's `metadata.json`.

 Before modifying the file, it creates a backup in the same directory. Better safe than sorry. If it is successful in modifying the file, it unlinks the backup.

# Usage:

#### Arguments:
- `root_dir`: Specifies which directory to set as the root of iteration. If left unspecified, defaults to: `~/.local/share/gnome-shell/extensions/`

- `-vn`, `--version-number`: The numeric string value to append to the supported extension version.

#### Example:
```shell
git clone https://github.com/r0fld4nc3/append-gnome-version-extensions.git
cd append-gnome-version-extensions/append-gnome-version-extensions
python3 append_version_to_extensions.py -vn 48
```

To have this readily available, it can be aliased in your terminal config file (.zshrc, .bashrc, etc)

```shell
alias="python3 path/to/script/append_version_to_extensions.py"
```

When calling it, don't forget to set at least a version number or any other argument that needs to be dynamic. If you `root_dir` differs from the default, you can alias it like:

```shell
alias="python3 path/to/script/append_version_to_extensions.py path/to/your/root/dir"
```

# Disclaimer
This is not a permanent solution to the issue nor does it aim to automatically fix broken or unsupported extensions. This is a temporary solution just to get things up and running if they can after an update where certain extensions become "unsupported" or disabled.

This was created with the aim of quickly enabling some extensions which *technically* work, but the fix is to append the current GNOME version if it hasn't already.
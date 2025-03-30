# What it does
 A command line script that appens the given GNOME version each extension's `metadata.json`.

 Before modifying the file, it creates a backup in the same directory. Better safe than sorry. If it is successful in modifying the file, it unlinks the backup.

# Usage:

#### Arguments:
- `root_dir`: Specifies which directory to set as the root of iteration. If left unspecified, defaults to: `~/.local/share/gnome-shell/extensions/`

- `-vn`, `--version-number`: The numeric string value to append to the supported extension version.

#### Example:
```python
python3 append-gnome-version-extensions.py -vn 48
```

To have this readily available, it can be aliased in your terminal config file (.zshrc, .bashrc, etc)

```shell
alias="python3 path/to/script/append_version_to_extensions.py"
```

When calling it, don't forget to set at least a version number or any other argument that needs to be dynamic. If you `root_dir` differs from the default, you can alias it like:

```shell
alias="python3 path/to/script/append_version_to_extensions.py path/to/your/root/dir"
```

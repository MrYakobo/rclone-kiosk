# rclone-kiosk: generates a slideshow from assets on cloud storage

this very simple script does the following:

1. Downloads assets from the [rclone][1] target `[source]`
2. Generates an HTML slideshow in index.html
3. Uploads index.html + assets to the rclone target `[remote]`

[1]: https://rclone.org/

## Dependencies

rclone obviously needs to be installed on the host.

## Installation

```bash
pip3 install git+https://github.com/MrYakobo/rclone-kiosk.git
rclone-kiosk --config rclone.conf
```

## Configuration

the configuration is done 100% in rclone toml.

```
[source]
type = drive
scope = drive.readonly

# replace with https://drive.google.com/drive/u/0/folders/XXX
root_folder_id = XXX

token = {"access_token":"","token_type":"Bearer","refresh_token":"","expiry":""}

[sftp_remote]
type = sftp
host = myhost
user = sftpser
port = 22
key_file = /path/to/some_keyfile_without_passphrase
shell_type = unix
md5sum_command = md5sum
sha1sum_command = sha1sum

[remote]
type = alias
remote = sftp_remote:/path/to/webroot
```
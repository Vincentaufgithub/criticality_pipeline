# mdrs-client-python

The mdrs-client-python is python library and a command-line client for up- and downloading files to and from MDRS based repository.

## Installing

```shell
poetry install
```

## Example Usage

### config create

Create remote host configuration

```shell
mdrs config create neurodata https://neurodata.riken.jp/api
```

### login

Login to remote host

```shell
mdrs login neurodata:
Username: (enter your login name)
Password: (enter your password)

mdrs login -u USERNAME -p PASSWORD neurodata:
```

### logout

Logout from remote host

```shell
mdrs logout neurodata:
```

### whoami

Print current user name

```shell
mdrs whoami neurodata:
```

### labs

List all laboratories

```shell
mdrs labs neurodata:
```

### ls

List the folder contents

```shell
mdrs ls neurodata:/NIU/Repository/
mdrs ls -p PW_OPEN_PASSWORD neurodata:/NIU/Repository/PW_Open/
mdrs ls -r neurodata:/NIU/Repository/Dataset1/
mdrs ls -J -r neurodata:/NIU/Repository/Dataset1/
```

### mkdir

Create a new folder

```shell
mdrs mkdir neurodata:/NIU/Repository/TEST
```

### upload

Upload the file or directory

```shell
mdrs upload ./sample.dat neurodata:/NIU/Repository/TEST/
mdrs upload -r ./dataset neurodata:/NIU/Repository/TEST/
mdrs upload -r -s ./dataset neurodata:/NIU/Repository/TEST/
```

### download

Download the file or folder

```shell
mdrs download neurodata:/NIU/Repository/TEST/sample.dat ./
mdrs download -r neurodata:/NIU/Repository/TEST/dataset/ ./
mdrs download -p PW_OPEN_PASSWORD neurodata:/NIU/Repository/PW_Open/Readme.dat ./
mdrs download -r  --exclude /NIU/Repository/TEST/dataset/skip neurodata:/NIU/Repository/TEST/dataset/ ./
```

### mv

Move or rename the file or folder

```shell
mdrs mv neurodata:/NIU/Repository/TEST/sample.dat neurodata:/NIU/Repository/TEST2/sample2.dat
mdrs mv neurodata:/NIU/Repository/TEST/dataset neurodata:/NIU/Repository/TEST2/
```

### cp

Copy the file and folder

```shell
mdrs cp neurodata:/NIU/Repository/TEST/sample.dat neurodata:/NIU/Repository/TEST2/sample2.dat
mdrs cp -r neurodata:/NIU/Repository/TEST/dataset neurodata:/NIU/Repository/TEST2/
```

### rm

Remove the file or folder

```shell
mdrs rm neurodata:/NIU/Repository/TEST/sample.dat
mdrs rm -r neurodata:/NIU/Repository/TEST/dataset
```

### chacl

Change the folder access level

```shell
mdrs chacl private neurodata:/NIU/Repository/Private
mdrs chacl cbs_open -r neurodata:/NIU/Repository/CBS_Open
mdrs chacl pw_open -r -p PW_OPEN_PASSWORD neurodata:/NIU/Repository/PW_Open
```

### metadata

Get a folder metadata

```shell
mdrs metadata neurodata:/NIU/Repository/TEST/
mdrs metadata -p PW_OPEN_PASSWORD neurodata:/NIU/Repository/PW_Open/
```

### file-metadata

Get the file metadata

```shell
mdrs file-metadata neurodata:/NIU/Repository/TEST/dataset/sample.dat
mdrs file-metadata -p PW_OPEN_PASSWORD neurodata:/NIU/Repository/PW_Open/Readme.txt
```

### help

Show the help message and exit

```shell
mdrs -h
```

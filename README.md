# ![tuxware logo](assets/logo_150.png)

A little linux demonstrative ransomware written in Python with Docker.

## Prerequisites

- docker

## 🛠️ Installation

```bash
git clone https://github.com/CORT1N/tuxware.git
```

## ⚙️ Usage

There is already some fake funny data in client volume so you can test it.

```bash
cd tuxware
docker compose up --build
```

You'll see the program up and running on the server (*penguinet*) and the files being encrypted on the client (tuxware) and sent.

A new file will appear, a little message from the attackers.

The key used to encrypt these data is available in `server/volumes/data/keys` and files in `server/volumes/data/uploads`.

You can rollback easyly by deleting `client/volumes/data` and `unzip client/volumes/data_backup.zip`

There is also a directory named **never_used** (little joke jajaja) where you can run a docker compose to rollback files with Python. You only need to fill the environment variable **KEY_FILE** with the good path for the new key.

## ⚠️ Explanation

❗ Use this project that I created to end a course at ESGI only for educational purposes. ❗

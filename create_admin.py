import getpass
import sqlite3
import sys
from pathlib import Path

import bcrypt


def main():
    if len(sys.argv) != 2:
        print("Utilisation : python create_admin.py <base.db>")
        return

    database_path = Path(sys.argv[1])

    if not database_path.exists():
        print(f"Erreur : la base '{database_path}' n'existe pas.")
        return

    username = input("Nom d'utilisateur administrateur : ").strip()
    password = getpass.getpass("Mot de passe : ")
    confirmation = getpass.getpass("Confirmez le mot de passe : ")

    if not username:
        print("Erreur : le nom d'utilisateur est obligatoire.")
        return

    if not password:
        print("Erreur : le mot de passe est obligatoire.")
        return

    if password != confirmation:
        print("Erreur : les mots de passe ne correspondent pas.")
        return

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                """
                INSERT INTO USERS (username, password_hash, role, is_blocked)
                VALUES (?, ?, 'ADMIN', 0)
                """,
                (username, password_hash),
            )

        print(f"L'administrateur '{username}' a été créé avec succès.")

    except sqlite3.IntegrityError:
        print(f"Erreur : l'utilisateur '{username}' existe déjà.")

    except sqlite3.OperationalError as error:
        print(f"Erreur SQLite : {error}")


if __name__ == "__main__":
    main()
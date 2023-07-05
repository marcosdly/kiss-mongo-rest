from typing import Optional, Union
from os import getenv
import logging
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ConfigurationError, InvalidName
from dataclasses import dataclass
from src.messages import ErrorResponse


@dataclass(init=False, frozen=True)
class APIDatabaseOperations:
    @classmethod
    def connection_failed(cls, uri: str, tries: int = 3) -> Optional[ConnectionFailure]:
        """Tests the connection and returns an instance an exception if failed."""
        client: MongoClient = MongoClient(uri)
        while True:
            try:
                client.admin.command("ping")
            except ConnectionFailure:
                tries -= 1
                if tries <= 0:
                    return ConnectionFailure(
                        f"Test connections failed. Attempted {tries} times. Check your database credentials.")
            else:
                return None
            finally:
                client.close()

    @classmethod
    def get_collection(cls, client: MongoClient, db: str,
                       col: str) -> Union[Collection, ErrorResponse]:
        """Returns the specified collection from the specified database *assuming
        the connection to the database is working*."""
        try:
            return client.get_database(db).get_collection(col)
        except ConfigurationError:
            # Database isn't defined neither in the connection uri nor
            # as a "default database" kind or parameter to mongo client,
            # so it will raise a configuration error in case the database
            # doesn't exist (because there's no fallback database set).
            #
            # As of pymongo 4.4.0 the fallback database for when none is
            # specified is hard coded, so take a look on that in case of
            # problems handling this error.
            return ErrorResponse(404, f"Database '{db}' doesn't exist.")
        except InvalidName:
            return ErrorResponse(404, f"Collection '{col}' doesn't exist.")


def client() -> Union[MongoClient, ErrorResponse]:
    # Trying so hard to turn the URI string into a mini-namespace for organization
    # purposes. Now everything in this module is either a regular class
    # or a glorified namespace.

    user_env_var: str = "DATABASE_USER"
    passwd_env_var: str = "DATABASE_PASSWORD"
    host_env_var: str = "DATABASE_HOST"

    def get_credential(base_env_var_name: str) -> Optional[str]:
        """Tries to get docker secret. Upon fail tries to get regular env
        variable content. Upon another fail returns None, else return the
        actual credential."""
        cred: Optional[str] = getenv(base_env_var_name + "_FILE")
        if not cred:
            cred = getenv(base_env_var_name)
            if not cred:
                return None
            return cred

        try:
            return open(cred, "rt").read().strip()
        except FileNotFoundError:
            return None

    def get_connection_uri() -> str:
        user: Optional[str] = get_credential(user_env_var)
        passwd: Optional[str] = get_credential(passwd_env_var)
        host: Optional[str] = get_credential(host_env_var)

        if not user:
            logging.error("Credential for database user not found.")
            raise ValueError("Credential for database user not found")

        if not passwd:
            logging.error("Credential for database password not found.")
            raise ValueError("Credential for database password not found.")

        if not host:
            logging.error("Host address not found.")
            raise ValueError("Host address not found.")

        # TODO find a way to specify replica sets
        return f"mongodb://{user}:{passwd}@{host}"

    uri: str = get_connection_uri()

    if err := APIDatabaseOperations.connection_failed(uri):
        logging.error(str(err))
        return ErrorResponse(503, str(err))

    return MongoClient(uri)

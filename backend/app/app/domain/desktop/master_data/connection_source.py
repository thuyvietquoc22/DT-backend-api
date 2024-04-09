from app.repository.desktop.master_data.connect_source import connection_source_repo, ConnectSourceRepository


class ConnectSourceDomain:

    @property
    def connection_source_repo(self) -> ConnectSourceRepository:
        return connection_source_repo

    def get_connection_source(self):
        return self.connection_source_repo.find_all_connection_source()


connection_source_domain = ConnectSourceDomain()

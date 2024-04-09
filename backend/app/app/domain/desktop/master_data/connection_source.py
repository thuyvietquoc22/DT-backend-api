from app.repository.desktop.master_data.connect_source import connection_source_repo, ConnectSourceRepository


class ConnectSourceDomain:

    @property
    def connection_source_repo(self) -> ConnectSourceRepository:
        return connection_source_repo

    def get_connection_source(self):
        return self.connection_source_repo.find_all_connection_source()

    def get_connection_source_by_keyname(self, connection_source_keyname):
        return self.connection_source_repo.find_connection_source_by_keyname(connection_source_keyname)

    def create_connection_source(self, connection_source_create):
        self.connection_source_repo.create(connection_source_create)

    def update_connection_source(self, connection_source_keyname, connection_source_update):
        result = self.connection_source_repo.update_connection_source(connection_source_keyname,
                                                                      connection_source_update)

        if result.modified_count == 0:
            raise Exception("Not found record to update")

    def delete_connection_source(self, connection_source_keyname):
        self.connection_source_repo.delete_by_keyname(connection_source_keyname)


connection_source_domain = ConnectSourceDomain()

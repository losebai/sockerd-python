from typing import Dict, Optional
from ..transport.Client import IClient
from socketd.transport.client.ClientFactory import ClientFactory
from urllib.parse import urlparse


class SocketD:
    @staticmethod
    def version() -> str:
        return "2.0"

    client_factory_map: Dict[str, ClientFactory] = {}
    server_factory_map: Dict[str, ServerFactory] = {}

    @staticmethod
    def __load_factories(factory_class: type, factory_map: Dict[str, factory_class]) -> None:
        factories = list(factory_class().__class__.load())
        for factory in factories:
            for schema in factory.schema():
                factory_map[schema] = factory

    @staticmethod
    def __get_schema(url: str) -> Optional[str]:
        parsed_url = urlparse(url)
        if parsed_url:
            return parsed_url.scheme
        return None

    @staticmethod
    def create_server(server_config: ServerConfig) -> Server:
        factory = SocketD.server_factory_map.get(server_config.schema)
        if factory is None:
            raise RuntimeError("No ServerBroker providers were found.")
        return factory.create_server(server_config)

    @staticmethod
    def create_client(server_url: str) -> IClient:
        schema = SocketD.__get_schema(server_url)
        if schema is None:
            raise ValueError("Invalid server URL.")

        client_config = ClientConfig(server_url)
        factory = SocketD.client_factory_map.get(client_config.schema)
        if factory is None:
            raise RuntimeError("No ClientBroker providers were found.")
        return factory.create_client(client_config)



# Initialize the client and server factory maps
SocketD.__load_factories(ClientFactory, SocketD.client_factory_map)
SocketD.__load_factories(ServerFactory, SocketD.server_factory_map)
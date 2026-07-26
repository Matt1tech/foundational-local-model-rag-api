from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class VectorStore:
    """Stores and retrieves document embeddings in Qdrant."""

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
        vector_size: int,
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.vector_size = vector_size

    def create_collection(self) -> None:
        """Create the collection if it does not exist."""

        collections = self.client.get_collections().collections

        if any(
            collection.name == self.collection_name
            for collection in collections
        ):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def add(
        self,
        point_id: str,
        embedding: list[float],
        payload: dict,
    ) -> None:
        """Add one document chunk."""

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload,
                )
            ],
        )

    def search(
        self,
        query_embedding: list[float],
        limit: int,
    ):
        """Search for similar document chunks."""

        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        ).points
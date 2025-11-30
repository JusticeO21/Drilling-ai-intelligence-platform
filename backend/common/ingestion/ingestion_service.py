from .cleaning.data_cleaner import DataCleaner
from .loaders.file_loader import StructuredFileLoader
from .profiling.data_profiler import DataFrameProfiler
from .storage import RedisStoreRepository, VectorStoreRepository


class DataIngestionService:

    def __init__(
        self,
        loader: StructuredFileLoader,
        cleaner: DataCleaner,
        profiler: DataFrameProfiler,
        vector_repo: VectorStoreRepository,
        redis_repo: RedisStoreRepository,
    ):
        self.loader = loader
        self.cleaner = cleaner
        self.profiler = profiler
        self.vector_repo = vector_repo
        self.redis_repo = redis_repo

    def ingest(
        self,
        dataset_id: str,
        dataframe=None,
        file_path: str = None,
        user_id: str = None,
        dataset_name: str = None,
    ):
        if dataframe is None and file_path:
            df = self.loader.load(file_path)
        elif dataframe is not None:
            df = dataframe
        else:
            raise ValueError("Either dataframe or file_path must be provided")

        df = self.cleaner.clean(df)

        # Create profiler instance with the dataframe
        profiler = self.profiler(df, dataset_name)
        full_profile = profiler.generate_full_profile()

        # Store complete profile in vector store
        self.vector_repo.store_full_profile(dataset_id, user_id, full_profile)

        # Store dataframe in redis
        self.redis_repo.store_dataframe(dataset_id, df)

        return {
            "dataset_id": dataset_id,
            "columns": list(df.columns),
            "profile": full_profile,
        }

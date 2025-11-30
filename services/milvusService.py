from typing import Optional, Sequence
from pymilvus import MilvusClient,Collection, CollectionSchema, FieldSchema, DataType, connections,utility
from agents.embedder import embed_query_batch_gemini,generate_embedding_gemini
from utils.utils import clean_string_list,clean_milvus_results,split_into_chunks
import pandas as pd
import logging
import os
from pymilvus import WeightedRanker,AnnSearchRequest 
from services import candidatService
from services import offreService


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

milvus_host = os.getenv('MILVUS_HOST')
milvus_api_key = os.getenv('MILVUS_APIKEY')

class MilvusService:
    def __init__(self):
        connections.connect(alias="default",uri=f"https://{milvus_host}",token=milvus_api_key ) #host=settings.milvus_host,port=settings.milvus_port
        self.collection_name = "cvoffre_collection"
        # self.server_addr = f"http://{settings.milvus_host}:{settings.milvus_port}"
        self.server_addr = f"https://{milvus_host}" 
        self.client = MilvusClient(uri=self.server_addr,token=milvus_api_key)
        self._create_collection_if_not_exist()
        self._create_cv_partition_if_not_exist()
        self._create_offre_partition_if_not_exist()
        
    def _create_collection_if_not_exist(self):
        if not utility.has_collection(self.collection_name):
            print("Collection non trouvée, creation ....")
            schema = self.client.create_schema(
                auto_id=False,
                enable_dynamic_fields=True,
            )
            schema.add_field(field_name="id", datatype=DataType.VARCHAR, is_primary=True,max_length=300)
            schema.add_field(field_name="doc_id", datatype=DataType.VARCHAR,max_length=300)            
            schema.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=10000)
            schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=3072)
            index_params = self.client.prepare_index_params()
            index_params.add_index(
                field_name="vector",
                index_name="vector_index",
                index_type="AUTOINDEX",
                metric_type="COSINE"
            )
            index_params.add_index(
                field_name="doc_id",
                index_name="doc_id_index",
                index_type="AUTOINDEX"
            )
            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params,
                properties = {"mmap.enabled":True},
                # dimension=768
            )
            
    def _create_cv_partition_if_not_exist(self):
        if not self.client.has_partition(collection_name = self.collection_name,partition_name = "cvs_vector"):            
            self.client.create_partition(
                collection_name = self.collection_name,
                partition_name = "cvs_vector",                
            )
    
    def _create_offre_partition_if_not_exist(self):
        if not self.client.has_partition(collection_name = self.collection_name,partition_name = "offres_vector"):            
            self.client.create_partition(
                collection_name = self.collection_name,
                partition_name = "offres_vector",                
            )


    def _description_collection(self):
        if utility.has_collection(self.collection_name):
            res = self.client.describe_collection(
                collection_name=self.collection_name
            )
            return res
        
    def _collection_load_state(self):
        if utility.has_collection(self.collection_name):
            res = self.client.get_load_state(
                collection_name=self.collection_name
            )
            return res
    def _cv_partition_load_state(self):
        if self.client.has_partition(collection_name = self.collection_name,partition_name = "cvs_vector"):
            res = self.client.get_load_state(
                collection_name=self.collection_name,
                partition_name="cvs_vector"
            )
            return res
        
    def _offre_partition_load_state(self):
        if self.client.has_partition(collection_name = self.collection_name,partition_name = "offres_vector"):
            res = self.client.get_load_state(
                collection_name=self.collection_name,
                partition_name="offres_vector"
            )
            return res
            
    def _clean_cv_partition(self):
        if self.client.has_partition(collection_name = self.collection_name,partition_name = "cvs_vector"):
            self.client.release_partitions(
                collection_name=self.collection_name,
                partition_names=["cvs_vector"]
            )
            self.client.drop_partition(
                collection_name=self.collection_name,
                partition_name="cvs_vector"
            )
    def _clean_offre_partition(self):
        if self.client.has_partition(collection_name = self.collection_name,partition_name = "offres_vector"):
            self.client.release_partitions(
                collection_name=self.collection_name,
                partition_names=["offres_vector"]
            )
            self.client.drop_partition(
                collection_name=self.collection_name,
                partition_name="offres_vector"
            )

            
    def _clean_collection(self):
        if utility.has_collection(self.collection_name):
            self.client.release_collection(
                collection_name=self.collection_name
            )
            self.client.drop_collection(
                collection_name=self.collection_name
            )
    
    def list_cvs(self):
        filter = 'id is not null'
        results = self.client.query(
            collection_name=self.collection_name,
            partition_names=["cvs_vector"],
            filter=filter,
             group_by_field="doc_id",
            group_size=1, # p to 2 entities to return from each group otherwise 1 per group
            output_fields=["id","doc_id","content"]            
        )
        logger.info(results)

        return results
    
    def list_existing_cv_ids(self) -> set[str]:
        filter_expr = "id is not null"

        results = self.client.query(
            collection_name=self.collection_name,
            partition_names=["cvs_vector"],
            filter=filter_expr,
            group_by_field="doc_id",
            group_size=1,
            output_fields=["doc_id"]
        )

        existing_ids: set[str] = set()
        for hit in results:
            existing_ids.add(str(hit["doc_id"]))

        return existing_ids
    
    def list_existing_offre_ids(self) -> set[str]:
        filter_expr = "id is not null"

        results = self.client.query(
            collection_name=self.collection_name,
            partition_names=["offres_vector"],
            filter=filter_expr,
            group_by_field="doc_id",
            group_size=1,
            output_fields=["doc_id"]
        )

        existing_ids: set[str] = set()
        for hit in results:
            existing_ids.add(str(hit["doc_id"]))

        return existing_ids

    def list_offres(self):
        filter = 'id is not null'
        results = self.client.query(
            collection_name=self.collection_name,
            partition_names=["offres_vector"],
            filter=filter,
            output_fields=["id","doc_id","content"]            
        )
      
        return results
       

       
    async def bulk_insert_cvs_to_milvus(self):
        existing_ids = self.list_existing_cv_ids()
        logger.info("CVs déjà présents dans Milvus: %s", len(existing_ids))
        cvs = await candidatService.get_candidates_chunk_not_in_ids(
            existing_ids=existing_ids,
            limit=5
        )
        message = ""
        if not cvs:
            message = "Aucun cv à insérer."
            logger.info(message)
            return message
        df = pd.DataFrame([cv.dict() for cv in cvs])    
        # vectors = embed_query_batch_gemini(df["contenu"].tolist())         
        # delete ids 
        # self._clean_cv_partition()
        # logger.warning("cvs partition supprimés dans Milvus.")
        self._create_cv_partition_if_not_exist()
        insert_data = []
        for i, row in df.iterrows():
            doc_id = str(row["id"])
            content_chunks = split_into_chunks(row["contenu"])
            if not content_chunks:
                logger.warning(f"Aucun chunk généré pour {doc_id}")
                continue
            chunk_vectors = embed_query_batch_gemini(content_chunks)
            logger.warning(f"doc {doc_id} ")
            for idx, chunk_text in enumerate(content_chunks):
                logger.warning(f"chunk {idx} ")
                insert_data.append({
                    "id": f"{doc_id}_{idx}",
                    "doc_id": doc_id,                   
                    "content": chunk_text[:10000],  # Truncation sécurité
                    "vector": chunk_vectors[idx],  
                })
        if not insert_data:
            logger.warning("Aucune donnée insérée dans Milvus (tous les contenus vides ?)")
            return "Aucun insert réalisé"                       
        logger.warning(f"Insertion de {len(insert_data)} chunks dans Milvus.")
        self.client.upsert(
            collection_name=self.collection_name,
            partition_name="cvs_vector",
            data=insert_data
        )
        message = f"{len(insert_data)} chunks insérés dans Milvus."
        logger.info(message)
        return message

    async def bulk_insert_offres_to_milvus(self):
        existing_ids = self.list_existing_offre_ids()
        logger.info("Offres déjà présents dans Milvus: %s", len(existing_ids))
        offres = await offreService.get_offres_chunk_not_in_ids(
            existing_ids=existing_ids,
            limit=5
        )
        message = ""
        if not offres:
            message = "Aucun offre à insérer."
            logger.info(message)
            return message
        df = pd.DataFrame([offre.dict() for offre in offres])    
        # vectors = embed_query_batch_gemini(df["contenu"].tolist())         
        # delete ids 
        # self._clean_offre_partition()
        # logger.warning("offres partition supprimés dans Milvus.")
        self._create_offre_partition_if_not_exist()
        insert_data = []
        for i, row in df.iterrows():
            doc_id = str(row["id"])
            content_chunks = split_into_chunks(row["contenu"])
            if not content_chunks:
                logger.warning(f"Aucun chunk généré pour {doc_id}")
                continue
            chunk_vectors = embed_query_batch_gemini(content_chunks)
            logger.warning(f"doc {doc_id} ")
            for idx, chunk_text in enumerate(content_chunks):
                logger.warning(f"chunk {idx} ")
                insert_data.append({
                    "id": f"{doc_id}_{idx}",
                    "doc_id": doc_id,                   
                    "content": chunk_text[:10000],  # Truncation sécurité
                    "vector": chunk_vectors[idx],  
                })
        if not insert_data:
            logger.warning("Aucune donnée insérée dans Milvus (tous les contenus vides ?)")
            return "Aucun insert réalisé"                       
        logger.warning(f"Insertion de {len(insert_data)} chunks dans Milvus.")
        self.client.upsert(
            collection_name=self.collection_name,
            partition_name="offres_vector",
            data=insert_data
        )
        message = f"{len(insert_data)} chunks insérés dans Milvus."
        logger.info(message)
        return message


    def search(self,query,  top_n=10, partitions: Optional[Sequence[str]] = None,
):
        query_multimodal_vector = generate_embedding_gemini(query)
        # logger.info(",".join(f"'{group}'" for group in user.groups))

        res = self.client.search(
            data=[query_multimodal_vector],
            collection_name=self.collection_name,
            anns_field="vector",
            limit=top_n,
            search_params={"metric_type": "COSINE"}, 
            partition_names=list(partitions) if partitions else [],
            group_by_field="doc_id",
            group_size=1, # p to 2 entities to return from each group otherwise 1 per group
            # filter='partition_key in ["459923178704175677"]',
            output_fields=["id","doc_id","content"]
            )
        # logger.info(res)
        MIN_SCORE = 0.65
        res = clean_milvus_results(res)
        res = [r for r in res if r.get("score", 0) >= MIN_SCORE]       
        
        return res
    
    
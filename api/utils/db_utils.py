class DBUtils:
    def convert_mongo_id(doc):
        if "_id" in doc:
            # Handle both $id and $oid
            if isinstance(doc["_id"], dict):
                id_val = doc["_id"].get("$id") or doc["_id"].get("$oid")
                if id_val:
                    doc["id"] = id_val
            else:
                doc["id"] = str(doc["_id"])
            del doc["_id"]
        return doc
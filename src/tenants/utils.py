import hashlib


def generate_unique_schema_name(tenant_id: str, max_length:int = 60):
    base_name = f"tenant_{tenant_id}"
    base_name = base_name.replace("-", "")
    hash_suffix = hashlib.sha256(base_name.encode('utf-8')).hexdigest()[:16]
    unique_name = base_name[:40]
    schema_name = f"{unique_name}_{hash_suffix}"
    schema_name = schema_name.replace("-", "")
    final_name = schema_name[:max_length]
    return final_name
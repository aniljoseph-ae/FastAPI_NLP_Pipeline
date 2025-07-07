from pathlib import Path

# Define the project structure
project_structure = {
    "app": {
        "__init__.py": None,
        "main.py": None,
        "api": {
            "__init__.py": None,
            "v1": {
                "__init__.py": None,
                "endpoints.py": None,
                "schemas.py": None
            }
        },
        "core": {
            "__init__.py": None,
            "config.py": None,
            "logging.py": None,
            "dependencies.py": None
        },
        "services": {
            "__init__.py": None,
            "nlp_service.py": None,
            "rag_service.py": None,
            "webhook_service.py": None
        },
        "tasks": {
            "__init__.py": None,
            "celery_tasks.py": None
        },
        "utils": {
            "__init__.py": None,
            "embedding.py": None,
            "reranker.py": None,
            "vector_store.py": None
        }
    },
    "tests": {
        "__init__.py": None,
        "test_endpoints.py": None,
        "test_nlp_service.py": None,
        "test_rag_service.py": None
    },
    "mlflow": {
        "tracking.py": None,
        "experiments": {}
    },
    "scripts": {
        "setup_weaviate.py": None,
        "ingest_data.py": None
    },
    ".github": {
        "workflows": {
            "ci_cd.yml": None
        }
    },
    "Dockerfile": None,
    "docker-compose.yml": None,
    "requirements.txt": None,
    "README.md": None,
    "setup.py": None,
    "project_template.py": None
}


def create_structure(base_path: Path, structure: dict):
    """
    Recursively create directories and files based on a nested dictionary.
    """
    for name, content in structure.items():
        path = base_path / name
        if content is None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
            print(f"Created file: {path}")
        else:
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {path}")
            create_structure(path, content)


if __name__ == "__main__":
    base_dir = Path.cwd()  # Use current directory as root
    print(f"Creating project in: {base_dir}\n")
    create_structure(base_dir, project_structure)

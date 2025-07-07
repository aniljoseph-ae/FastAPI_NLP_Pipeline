import mlflow
from app.core.config import settings
import time
import logging

logger = logging.getLogger("nlp_pipeline")

def log_model_metrics(task_type: str, metrics: dict, execution_time: float):
    try:
        mlflow.set_tracking_uri("file://./mlflow/experiments")
        with mlflow.start_run(run_name=f"nlp_task_{task_type}"):
            mlflow.log_params({
                "model": settings.MODEL_NAME,
                "task_type": task_type
            })
            mlflow.log_metric("execution_time", execution_time)
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)
            logger.info(f"Logged metrics for {task_type} to MLflow.")
    except Exception as e:
        logger.error(f"MLflow logging failed: {str(e)}")
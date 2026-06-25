from src.training.train import run_training
from src.training.evaluate import run_evaluation
from src.training.register import register_model, update_champion


model, run_id = run_training()
metrics = run_evaluation(model, run_id)
version = register_model(run_id, metrics)
update_champion("ctr_model", version, metrics)
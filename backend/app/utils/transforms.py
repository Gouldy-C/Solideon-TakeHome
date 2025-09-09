import app.utils.config_loader as cfg

def transform_scan_value(raw: float) -> float:
    value_a = cfg.CONFIG["equations_vars"]["distance_a"]
    value_b = cfg.CONFIG["equations_vars"]["distance_b"]
    return raw * value_a + value_b
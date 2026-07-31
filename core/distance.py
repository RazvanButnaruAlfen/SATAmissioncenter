def interpolate_distance(start_km: int, progress_percent: int) -> int:
    progress = max(0, min(100, progress_percent))
    return round(start_km * (1 - progress / 100))

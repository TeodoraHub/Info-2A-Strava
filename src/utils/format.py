def format_h_m(hours: float) -> str:
    """Convertit une durée exprimée en heures (float) en hh:mm."""
    if hours is None:
        return "0h00"

    h = int(hours)
    m = int(round((hours - h) * 60))
    return f"{h}h{m:02d}"


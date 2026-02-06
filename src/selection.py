# Select the tempo most likely perceived as the beat.
def select_perceived_tempo(candidates, min_pref=60, max_pref=120):
    preferred = [t for t in candidates if min_pref <= t <= max_pref]

    if preferred:
        # If multiple choosing the lower one (more likely beat than subdivision)
        return min(preferred)

    # Fallback case, choosing the slowest candidate
    return min(candidates)

def filter_by_duration(results, max_duration):
    if max_duration is None:
        return results
    filtered = []
    for result in results:
        duration = result.get("duration")
        if duration is None:
            continue
        duration = str(duration).lower()
        if "untimed" in duration:
            continue
        try:
            minutes = int(duration.split()[0])
            if minutes <= max_duration:
                filtered.append(result)
        except:
            filtered.append(result)
    return filtered

def filter_by_assessment_type(results, assessment_types):
    if not assessment_types:
        return results
    filtered = []
    for result in results:
        test_type = result["assessment_type"].lower()
        for assessment in assessment_types:
            if assessment.lower() in test_type:
                filtered.append(result)
                break
    return filtered

def filter_by_job_level(results, seniority):
    if seniority is None:
        return results
    filtered = []
    for result in results:
        level = str(result.get("job_level","")).lower()
        if seniority.lower() in level:
            filtered.append(result)
    return filtered

def apply_filters(results, state):
    results = filter_by_duration(
        results,
        state.max_duration
    )
    results = filter_by_assessment_type(
        results,
        state.assessment_types
    )
    results = filter_by_job_level(
        results,
        state.seniority
    )
    return results


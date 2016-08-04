def state_json(state_class, user):
    doc = '{}'
    try:
        state = state_class.objects.get(user=user)
        if (len(state.json) > 0):
            doc = state.json
    except state_class.DoesNotExist:
        pass

    return doc

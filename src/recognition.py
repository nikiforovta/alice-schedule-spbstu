def group_recognition(tokens):
    group = ""
    if len(tokens) == 2:
        return "/".join(tokens)
    for token in tokens:
        try:
            int(token)
            group += token
        except ValueError:
            if token in ['/', '\\', 'дробь', 'косая', 'деление', 'слэш', 'слеш']:
                group += '/'
            elif token in [',', 'черта']:
                continue
            else:
                group += token
    try:
        if group[-6] != '/':
            group = '/'.join([group[:-5], group[-5:]])
    except IndexError:
        return None
    return group

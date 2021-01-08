def extract_options_chain_item(o_list, item):
    out = []
    for o in o_list:
        if hasattr(o, item):
            out.append(getattr(o, item))
    return out

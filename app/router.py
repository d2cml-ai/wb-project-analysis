import intention_router as intention


def detectQueryType(query: str):
    info_dict, specific = intention.get_info(query)
    if specific:
        # Specific, filter pandas dataframe
        return specific, info_dict
    else:
        return specific, {}


# a = input("insert query: ")


# print(detectQueryType(a))

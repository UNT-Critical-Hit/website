def get_campaign_by_id(campaigns, id):
    return log_search(arr=campaigns, val=id)

def log_search(arr, val):
    if len(arr) == 1:
        if arr[0].id == val:
            return arr[0]
        else:
            return None
    mid = len(arr) // 2
    if arr[mid].id == val:
        return arr[mid]
    if arr[mid].id < val:
        return log_search(arr[:mid], val)
    return log_search(arr[mid:], val)
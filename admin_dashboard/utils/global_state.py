# utils/global_state.py
global_edit_data = {
    "item": None,
    "feature": None
}

def set_edit_data(item, feature):
    global_edit_data["item"] = item
    global_edit_data["feature"] = feature

def get_edit_data():
    return global_edit_data["item"], global_edit_data["feature"]

def clear_edit_data():
    global_edit_data["item"] = None
    global_edit_data["feature"] = None

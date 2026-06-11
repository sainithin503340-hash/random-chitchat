# matching.py

waiting_users = []
active_chats = {}

def find_match(user_id):
    if waiting_users and waiting_users[0] != user_id:
        partner = waiting_users.pop(0)

        active_chats[user_id] = partner
        active_chats[partner] = user_id

        return partner

    waiting_users.append(user_id)
    return None


def next_chat(user_id):
    if user_id in active_chats:
        partner = active_chats.pop(user_id)

        if partner in active_chats:
            active_chats.pop(partner)

        return partner

    return None
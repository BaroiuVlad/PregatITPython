import time

EVENT_LOG = []
UNDO_STACK = []


def add_event(name: str, priority: str = 'LOW', **kwargs):
    event_id = int(time.time() * 1000)

    new_event = {
        'id': event_id,
        'name': name,
        'priority': priority
    }

    new_event.update(kwargs)
    EVENT_LOG.append(new_event)
    return event_id
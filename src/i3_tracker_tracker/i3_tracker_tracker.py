import datetime
import requests
import i3ipc
import json


def register_event(event):
    event['time'] = datetime.datetime.now().isoformat()
    print(event)
    print()
    request = requests.post('http://tracker/register/', data=json.dumps(event))
    if request.status_code == 200:
        status = 'OK'
    else:
        status = 'KO'
    with open('/dev/shm/i3-tracker-status.txt', 'w') as status_file:
        try:
            status_text = event['window_class']
        except:
            status_text = event["name"]
        status = f'[{status}]: {status_text}'.ljust(30) + '|'
        status_file.write(status)


def on_workspace_focus(i3, e):
    event = {}
    event['type'] = 'workspace::focus'
    if e.current:
        event['name'] = e.current.name
        event['leaves'] = [w.name for w in e.current.leaves()]
    register_event(event)


def on_window_focus(i3, e):
    focused = i3.get_tree().find_focused()
    event = {}
    event['type'] = 'window::focus'
    event['name'] = focused.name
    event['workspace'] = focused.workspace().name
    event['window_class'] = focused.window_class
    register_event(event)


def on_window_title(i3, e):
    focused = i3.get_tree().find_focused()
    event = {}
    event['type'] = 'window::title'
    event['name'] = focused.name
    event['workspace'] = focused.workspace().name
    event['window_class'] = focused.window_class
    register_event(event)


def i3_tracker_backend():
    i3 = i3ipc.Connection()

    i3.on('workspace::focus', on_workspace_focus)
    i3.on("window::focus", on_window_focus)
    i3.on("window::title", on_window_title)

    i3.main()


if __name__ == '__main__':
    i3_tracker_backend()

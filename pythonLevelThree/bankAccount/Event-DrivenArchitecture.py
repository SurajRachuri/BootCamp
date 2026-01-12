# from typing import Callable, Any, List, Dict
# from dataclasses import dataclass, field
# from datetime import datetime
# import asyncio
# import fnmatch
# import inspect

# @dataclass
# class Event:
#     name: str
#     data: Any
#     timestamp: datetime = field(default_factory=datetime.now)
#     source: str = ""


# class EventEmitter:
#     def __init__(self, keep_history: bool = False, history_limit: int = 1000):
#         self._listeners: Dict[str, List[Callable]] = {}
#         self._once_listeners: Dict[str, List[Callable]] = {}
#         self._history: List[Event] = []
#         self._keep_history = keep_history
#         self._history_limit = history_limit

#     # ---------------- SUBSCRIBE ----------------
#     def on(self, event_name: str, callback: Callable) -> None:
#         self._listeners.setdefault(event_name, []).append(callback)

#     def once(self, event_name: str, callback: Callable) -> None:
#         self._once_listeners.setdefault(event_name, []).append(callback)

#     # ---------------- UNSUBSCRIBE ----------------
#     def off(self, event_name: str, callback: Callable = None) -> None:
#         if callback is None:
#             self._listeners.pop(event_name, None)
#             self._once_listeners.pop(event_name, None)
#         else:
#             if event_name in self._listeners:
#                 self._listeners[event_name] = [
#                     cb for cb in self._listeners[event_name] if cb != callback
#                 ]
#             if event_name in self._once_listeners:
#                 self._once_listeners[event_name] = [
#                     cb for cb in self._once_listeners[event_name] if cb != callback
#                 ]

#     # ---------------- EMIT (SYNC) ----------------
#     def emit(self, event_name: str, data: Any = None, source: str = "") -> int:
#         event = Event(event_name, data, source=source)
#         count = 0

#         # Save history
#         if self._keep_history:
#             self._history.append(event)
#             if len(self._history) > self._history_limit:
#                 self._history.pop(0)

#         # Match listeners (supports wildcards)
#         for pattern, callbacks in list(self._listeners.items()):
#             if fnmatch.fnmatch(event_name, pattern):
#                 for cb in callbacks:
#                     cb(event)
#                     count += 1

#         # Once listeners
#         for pattern, callbacks in list(self._once_listeners.items()):
#             if fnmatch.fnmatch(event_name, pattern):
#                 for cb in callbacks:
#                     cb(event)
#                     count += 1
#                 self._once_listeners.pop(pattern, None)

#         return count

#     # ---------------- EMIT (ASYNC) ----------------
#     async def emit_async(self, event_name: str, data: Any = None) -> int:
#         event = Event(event_name, data)
#         tasks = []

#         if self._keep_history:
#             self._history.append(event)
#             if len(self._history) > self._history_limit:
#                 self._history.pop(0)

#         for pattern, callbacks in list(self._listeners.items()):
#             if fnmatch.fnmatch(event_name, pattern):
#                 for cb in callbacks:
#                     if inspect.iscoroutinefunction(cb):
#                         tasks.append(cb(event))
#                     else:
#                         cb(event)
#         if tasks:
#             await asyncio.gather(*tasks)

#         return len(tasks)

#     # ---------------- HISTORY REPLAY ----------------
#     def replay(self, event_pattern: str, callback: Callable) -> int:
#         count = 0
#         for event in self._history:
#             if fnmatch.fnmatch(event.name, event_pattern):
#                 callback(event)
#                 count += 1
#         return count

#     def get_history(self, event_pattern: str = "*", limit: int = None) -> List[Event]:
#         filtered = [
#             e for e in self._history
#             if fnmatch.fnmatch(e.name, event_pattern)
#         ]
#         return filtered[-limit:] if limit else filtered
# def log_event(event):
#     print(f"[LOG] {event.name} → {event.data}")

# async def async_handler(event):
#     await asyncio.sleep(1)
#     print(f"[ASYNC] {event.name}")

# emitter = EventEmitter(keep_history=True)

# emitter.on("user.*", log_event)
# emitter.once("user.login", lambda e: print("Login only once"))

# emitter.emit("user.login", {"id": 1})
# emitter.emit("user.logout", {"id": 1})

# emitter.replay("user.*", log_event)

# asyncio.run(emitter.emit_async("user.update", {"name": "Suraj"}))



import asyncio
from typing import Callable, Any, List, Dict
from dataclasses import dataclass, field
from datetime import datetime
import fnmatch
import inspect

# ---------------- EVENT MODEL ----------------
@dataclass
class Event:
    name: str
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""


# ---------------- EVENT EMITTER ----------------
class EventEmitter:
    def __init__(self, keep_history: bool = False, history_limit: int = 1000):
        self._listeners: Dict[str, List[Callable]] = {}
        self._once_listeners: Dict[str, List[Callable]] = {}
        self._history: List[Event] = []
        self._keep_history = keep_history
        self._history_limit = history_limit

    def on(self, event_name: str, callback: Callable):
        self._listeners.setdefault(event_name, []).append(callback)

    def once(self, event_name: str, callback: Callable):
        self._once_listeners.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, data: Any = None):
        event = Event(event_name, data)

        if self._keep_history:
            self._history.append(event)
            if len(self._history) > self._history_limit:
                self._history.pop(0)

        for pattern, callbacks in self._listeners.items():
            if fnmatch.fnmatch(event_name, pattern):
                for cb in callbacks:
                    cb(event)

        for pattern, callbacks in list(self._once_listeners.items()):
            if fnmatch.fnmatch(event_name, pattern):
                for cb in callbacks:
                    cb(event)
                self._once_listeners.pop(pattern)

    async def emit_async(self, event_name: str, data: Any = None):
        event = Event(event_name, data)
        tasks = []

        if self._keep_history:
            self._history.append(event)

        for pattern, callbacks in self._listeners.items():
            if fnmatch.fnmatch(event_name, pattern):
                for cb in callbacks:
                    if inspect.iscoroutinefunction(cb):
                        tasks.append(cb(event))
                    else:
                        cb(event)

        if tasks:
            await asyncio.gather(*tasks)

    def replay(self, pattern: str):
        for event in self._history:
            if fnmatch.fnmatch(event.name, pattern):
                print(f"[REPLAY] {event.name} → {event.data}")

    def show_history(self):
        for event in self._history:
            print(f"{event.timestamp} | {event.name} | {event.data}")


# ---------------- LISTENERS ----------------
def log_event(event: Event):
    print(f"[LOG] {event.name} → {event.data}")

async def async_logger(event: Event):
    await asyncio.sleep(1)
    print(f"[ASYNC] {event.name} processed")


# ---------------- MAIN MENU ----------------
def main():
    emitter = EventEmitter(keep_history=True)

    # Default listeners
    emitter.on("*", log_event)
    emitter.on("async.*", async_logger)
    emitter.once("login", lambda e: print("🔥 Login event handled once"))

    while True:
        print("""
1. Emit Event (Sync)
2. Emit Event (Async)
3. Replay Events
4. Show History
5. Exit
""")

        choice = input("Choose option: ")

        if choice == "1":
            name = input("Enter event name: ")
            data = input("Enter event data: ")
            emitter.emit(name, data)

        elif choice == "2":
            name = input("Enter async event name: ")
            data = input("Enter event data: ")
            asyncio.run(emitter.emit_async(name, data))

        elif choice == "3":
            pattern = input("Enter event pattern (e.g user.*): ")
            emitter.replay(pattern)

        elif choice == "4": 
            emitter.show_history()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

# Event-Driven Architecture Implementation
# Implements a publish/subscribe event system with advanced features

from typing import Callable, Any, List, Dict
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import fnmatch

@dataclass
class Event:
    """Data class representing an event with metadata"""
    name: str                                           # Event name/type
    data: Any                                          # Event payload data
    timestamp: datetime = field(default_factory=datetime.now)  # When event occurred
    source: str = ""                                   # Source identifier of the event

class EventEmitter:
    """Main event emitter class implementing pub/sub pattern"""
    
    def __init__(self, keep_history: bool = False, history_limit: int = 1000):
        """Initialize event emitter with optional history tracking"""
        self._listeners: Dict[str, List[Callable]] = {}      # Regular event listeners
        self._once_listeners: Dict[str, List[Callable]] = {} # One-time event listeners
        self._history: List[Event] = []                      # Event history storage
        self._keep_history = keep_history                    # Whether to track history
        self._history_limit = history_limit                  # Max events to keep in history

    def on(self, event_name: str, callback: Callable) -> None:
        """Subscribe to an event - callback will be called every time event is emitted"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def once(self, event_name: str, callback: Callable) -> None:
        """Subscribe to event once - callback will be called only on first emission"""
        if event_name not in self._once_listeners:
            self._once_listeners[event_name] = []
        self._once_listeners[event_name].append(callback)

    def off(self, event_name: str, callback: Callable = None) -> None:
        """Unsubscribe from event - removes specific callback or all callbacks for event"""
        # Remove from regular listeners
        if event_name in self._listeners:
            if callback is None:
                # Remove all listeners for this event
                del self._listeners[event_name]
            else:
                # Remove specific callback
                if callback in self._listeners[event_name]:
                    self._listeners[event_name].remove(callback)
                # Clean up empty list
                if not self._listeners[event_name]:
                    del self._listeners[event_name]
        
        # Remove from once listeners
        if event_name in self._once_listeners:
            if callback is None:
                del self._once_listeners[event_name]
            else:
                if callback in self._once_listeners[event_name]:
                    self._once_listeners[event_name].remove(callback)
                if not self._once_listeners[event_name]:
                    del self._once_listeners[event_name]

    def emit(self, event_name: str, data: Any = None, source: str = "") -> int:
        """Emit event synchronously, returns number of listeners called"""
        event = Event(name=event_name, data=data, source=source)
        
        # Add to history if enabled
        if self._keep_history:
            self._history.append(event)
            # Maintain history limit
            if len(self._history) > self._history_limit:
                self._history.pop(0)
        
        listeners_called = 0
        
        # Call regular listeners (including wildcard matches)
        for pattern, callbacks in self._listeners.items():
            if fnmatch.fnmatch(event_name, pattern):
                for callback in callbacks:
                    callback(event)
                    listeners_called += 1
        
        # Call once listeners and remove them
        once_to_remove = []
        for pattern, callbacks in self._once_listeners.items():
            if fnmatch.fnmatch(event_name, pattern):
                for callback in callbacks:
                    callback(event)
                    listeners_called += 1
                once_to_remove.append(pattern)
        
        # Remove once listeners that were called
        for pattern in once_to_remove:
            del self._once_listeners[pattern]
        
        return listeners_called

    async def emit_async(self, event_name: str, data: Any = None) -> int:
        """Emit event asynchronously - runs callbacks concurrently"""
        event = Event(name=event_name, data=data)
        
        # Add to history if enabled
        if self._keep_history:
            self._history.append(event)
            if len(self._history) > self._history_limit:
                self._history.pop(0)
        
        tasks = []
        
        # Collect all matching callbacks
        for pattern, callbacks in self._listeners.items():
            if fnmatch.fnmatch(event_name, pattern):
                for callback in callbacks:
                    # Wrap sync callbacks to make them async-compatible
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(callback(event))
                    else:
                        tasks.append(asyncio.create_task(asyncio.to_thread(callback, event)))
        
        # Handle once listeners
        once_to_remove = []
        for pattern, callbacks in self._once_listeners.items():
            if fnmatch.fnmatch(event_name, pattern):
                for callback in callbacks:
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(callback(event))
                    else:
                        tasks.append(asyncio.create_task(asyncio.to_thread(callback, event)))
                once_to_remove.append(pattern)
        
        # Remove once listeners
        for pattern in once_to_remove:
            del self._once_listeners[pattern]
        
        # Execute all callbacks concurrently
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        return len(tasks)

    def replay(self, event_pattern: str, callback: Callable) -> int:
        """Replay historical events matching pattern to a specific callback"""
        if not self._keep_history:
            return 0
        
        replayed = 0
        # Find and replay matching events from history
        for event in self._history:
            if fnmatch.fnmatch(event.name, event_pattern):
                callback(event)
                replayed += 1
        
        return replayed

    def get_history(self, event_pattern: str = "*", limit: int = None) -> List[Event]:
        """Get event history filtered by pattern with optional limit"""
        if not self._keep_history:
            return []
        
        # Filter events by pattern
        matching_events = [
            event for event in self._history 
            if fnmatch.fnmatch(event.name, event_pattern)
        ]
        
        # Apply limit if specified
        if limit is not None:
            matching_events = matching_events[-limit:]
        
        return matching_events
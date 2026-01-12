from Event_DrivenArchitecture import EventEmitter, Event
import asyncio

# Create event emitter with history tracking
emitter = EventEmitter(keep_history=True, history_limit=100)

# Define event handlers
def user_login_handler(event: Event):
    print(f"User logged in: {event.data['username']} at {event.timestamp}")

def user_logout_handler(event: Event):
    print(f"User logged out: {event.data['username']}")

def all_user_events_handler(event: Event):
    print(f"User event detected: {event.name}")

# Subscribe to specific events
emitter.on('user.login', user_login_handler)
emitter.on('user.logout', user_logout_handler)

# Subscribe to wildcard pattern (all user events)
emitter.on('user.*', all_user_events_handler)

# One-time subscription
emitter.once('app.startup', lambda event: print("App started!"))

# Emit events
emitter.emit('app.startup')  # Triggers once listener
emitter.emit('user.login', {'username': 'john_doe'})
emitter.emit('user.logout', {'username': 'john_doe'})
# Emit events
emitter.emit('app.startup')  # Triggers once listener
emitter.emit('user.login', {'username': 'Suraj'})
emitter.emit('user.logout', {'username': 'Suraj'})


# Async usage
async def async_handler(event: Event):
    await asyncio.sleep(0.1)  # Simulate async work
    print(f"Async processed: {event.name}")

emitter.on('async.event', async_handler)

async def main():
    # Emit async event
    # await emitter.emit_async('async.event', {'data': 'test'})
    
    # Get event history
    history = emitter.get_history('user.*', limit=5)
    print(f"Found {len(history)} user events in history")
    
    # Replay events
    def replay_handler(event: Event):
        print(f"Replaying: {event.name} from {event.timestamp}")
    
    emitter.replay('user.*', replay_handler)

# Run async example
if __name__ == "__main__":
    asyncio.run(main())
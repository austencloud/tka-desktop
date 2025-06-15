# **Task 2.3: Event-Driven Service Integration**

**Timeline**: Week 1 of Phase 2  
**Priority**: HIGH  
**Goal**: Update services to publish events instead of direct method calls

---

## **Update Services to Use Events:**

### **FILE: src/application/services/core/sequence_management_service.py**

```python
class SequenceManagementService:
    """Enhanced with event publishing."""

    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus
        self._current_sequence: Optional[SequenceData] = None

    def create_sequence(self, name: str = "New Sequence") -> SequenceData:
        """Create sequence and publish event."""
        sequence = SequenceData(name=name)
        self._current_sequence = sequence

        # Publish event instead of directly calling other components
        self.event_bus.publish(SequenceCreatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            sequence=sequence
        ))

        return sequence

    def update_sequence(self, sequence: SequenceData, change_type: str = "general") -> SequenceData:
        """Update sequence and publish event."""
        previous = self._current_sequence
        self._current_sequence = sequence

        self.event_bus.publish(SequenceUpdatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            sequence=sequence,
            previous_sequence=previous,
            change_type=change_type
        ))

        return sequence

    def add_beat(self, beat: BeatData) -> SequenceData:
        """Add beat and publish specific event."""
        if not self._current_sequence:
            raise ValueError("No active sequence")

        updated_sequence = self._current_sequence.add_beat(beat)
        self._current_sequence = updated_sequence

        # Publish both general update and specific beat event
        self.event_bus.publish(BeatCreatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            beat=beat,
            beat_index=len(updated_sequence.beats) - 1,
            sequence_id=updated_sequence.id
        ))

        self.event_bus.publish(SequenceUpdatedEvent(
            timestamp=time.time(),
            source_component="SequenceManagementService",
            sequence=updated_sequence,
            change_type="beat_added"
        ))

        return updated_sequence
```

---

## **Success Criteria:**

By the end of Task 2.3:

- ✅ **Services publish events** instead of direct calls
- ✅ **Decoupled architecture** achieved
- ✅ **Event-driven communication** working
- ✅ **Multiple subscribers** can respond to events
- ✅ **Easier testing** through event verification

---

## **Next Step**

After completing event-driven services, proceed to: [Task 2.4: Component Event Subscriptions](04_component_subscriptions.md)

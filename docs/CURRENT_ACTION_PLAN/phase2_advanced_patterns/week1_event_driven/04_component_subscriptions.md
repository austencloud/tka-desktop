# **Task 2.4: Component Event Subscriptions**

**Timeline**: Week 1 of Phase 2  
**Priority**: HIGH  
**Goal**: Update UI components to respond to events instead of direct calls

---

## **Update Components to Subscribe to Events:**

### **FILE: src/presentation/components/workbench/graph_editor.py**

```python
class GraphEditor(QWidget):
    """Graph editor that responds to events instead of direct calls."""

    def __init__(self, container: DIContainer):
        super().__init__()
        self.container = container
        self.event_bus = container.resolve(IEventBus)
        self._subscription_ids: List[str] = []

        self._setup_event_subscriptions()

    def _setup_event_subscriptions(self):
        """Subscribe to relevant events."""

        # Subscribe to sequence events
        sub_id = self.event_bus.subscribe(
            SequenceUpdatedEvent,
            self._on_sequence_updated
        )
        self._subscription_ids.append(sub_id)

        # Subscribe to beat selection events
        sub_id = self.event_bus.subscribe(
            BeatSelectedEvent,
            self._on_beat_selected
        )
        self._subscription_ids.append(sub_id)

        # Subscribe to pictograph events
        sub_id = self.event_bus.subscribe(
            PictographUpdatedEvent,
            self._on_pictograph_updated
        )
        self._subscription_ids.append(sub_id)

    def _on_sequence_updated(self, event: SequenceUpdatedEvent):
        """Handle sequence updates."""
        logger.debug(f"Graph editor updating for sequence: {event.sequence.name}")

        # Update display based on sequence
        self._update_sequence_display(event.sequence)

        # If this was a beat addition, highlight the new beat
        if event.change_type == "beat_added":
            self._highlight_latest_beat()

    def _on_beat_selected(self, event: BeatSelectedEvent):
        """Handle beat selection."""
        logger.debug(f"Graph editor highlighting beat {event.beat_index}")
        self._highlight_beat(event.beat_index)

    def _on_pictograph_updated(self, event: PictographUpdatedEvent):
        """Handle pictograph updates."""
        logger.debug(f"Graph editor updating pictograph for beat {event.beat_index}")
        self._update_pictograph_display(event.pictograph, event.beat_index)

    def cleanup(self):
        """Unsubscribe from events when component is destroyed."""
        for sub_id in self._subscription_ids:
            self.event_bus.unsubscribe(sub_id)
        self._subscription_ids.clear()
```

---

## **Success Criteria:**

By the end of Task 2.4:

- ✅ **Components subscribe to events** they care about
- ✅ **Automatic cleanup** prevents memory leaks
- ✅ **Decoupled UI updates** work properly
- ✅ **Event-driven rendering** implemented
- ✅ **Responsive UI** updates automatically

---

## **Next Step**

After completing component subscriptions, proceed to: [Week 2: Command Pattern](../week2_command_pattern/01_command_infrastructure.md)

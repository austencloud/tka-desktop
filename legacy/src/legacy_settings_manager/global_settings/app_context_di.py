from typing import Optional, Dict, Any, Type, TypeVar, cast
from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager

T = TypeVar('T')

class AppContextDI:
    """Transitional AppContext implementation that uses dependency injection."""
    
    _instance = None
    _services: Dict[Type, Any] = {}
    
    @classmethod
    def init(cls, **services):
        """Initialize the context with services."""
        cls._services = services
        cls._instance = cls()
    
    @classmethod
    def get_service(cls, service_type: Type[T]) -> T:
        """Get a service by type."""
        if service_type in cls._services:
            return cast(T, cls._services[service_type])
        raise KeyError(f"Service {service_type} not registered")
    
    @classmethod
    def settings_manager(cls) -> ISettingsManager:
        """Get the settings manager."""
        return cls.get_service(ISettingsManager)
    
    @classmethod
    def json_manager(cls) -> IJsonManager:
        """Get the JSON manager."""
        return cls.get_service(IJsonManager)
    
    # Add other service getters as needed

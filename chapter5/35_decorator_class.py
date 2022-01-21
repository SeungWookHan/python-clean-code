"""
클래스 데코레이터는 함수 데코레이터와 다른 타입을 사용하는 것만 다를 뿐 차이점 없음.

- 클래스 데코레이터는 코드 재사용과 DRY원칙의 모든 이점을 공유한다.
- 유지보수 시 데코레이터를 사용해 기존 로직을 훨씬 쉽게 변경할 수 있다.
"""

from datetime import datetime
from ipaddress import ip_address

from black import Timestamp

def hide_field(field) -> str:
  return "**민감한 정보 삭제**"

def format_time(field_timestamp: datetime) -> str:
  return field_timestamp.strftime("%Y-%m-%d %H:%M")

def show_original(event_field):
  return event_field

class EventSerializer:
  def __init__(self, serialization_fields: dict) -> None:
    self.serialization_fields = serialization_fields
  
  def serialize(self, event) -> dict:
    return {
      field: transformation(getattr(event, field))
      for field, transformation in
      self.serialization_fields.items()
    }
  
class Serialization:
  def __init__(self, **transformations) -> None:
      self.serializer = EventSerializer(transformations)
  
  def __call__(self, event_class):
      def serialize_method(event_instance):
        return self.serializer.serialize(event_instance)
      event_class.serialize = serialize_method
      return event_class

@Serialization(
  username=show_original,
  password=hide_field,
  ip=show_original,
  timestamp=format_time,
)
class LoginEvent:
  def __init__(self, username, password, ip, timestamp) -> None:
      self.username = username
      self.password = password
      self.ip = ip
      self.timestamp = timestamp
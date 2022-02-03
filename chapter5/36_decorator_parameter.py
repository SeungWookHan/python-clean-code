"""
데코레이터의 강력함은 파라미터를 전달 받아 로직을 추상화한다면 더더욱 강력해진다.
1. 간접 참조(indirection)를 통해 새로운 레벨의 중첩 함수 만들기
2. 데코레이터를 위한 클래스 만들기

일반적으로 2번이 가독성이 좋은데, 중첩된 클로저 함수보다는 객체가 이해하기 쉽기 때문.
"""

# 중첩 함수의 데코레이터
"""
크게 보면 데코레이터는 함수를 파라미터로 받아서 함수를 반환하는 함수로써 고차 함수(higher-order-function)이라고 할 수 있다.
"""
from ast import With
from functools import wraps


class ControlledException(Exception):
  """도메인에서 발생하는 일반적인 예외"""
  
RETRIES_LIMIT = 3

def with_retry(retries_limit=RETRIES_LIMIT, allowed_exceptions=None):
  allowed_exceptions = allowed_exceptions or (ControlledException,)

  def retry(operation):
    @wraps(operation)
    def wrapped(*args, **kwars):
      last_raised = None
      for _ in range(retries_limit):
        try:
          return operation(*args, **kwargs)
        except allowed_exceptions as e:
          logger.info("retrying %s due to %s", operation, e)
          last_raised = e
      raise last_raised
    return wrapped
  return retry

# 위 데코레이터를 함수에 적용
@with_retry()
def run_operation(task):
  return task.run()

@with_retry(retries_limit=5)
def run_with_custom_retries_limit(task):
  return task.run()

@with_retry(allowed_exceptions=(AttributeError,))
def run_with_custom_exception(task):
  return task.run()

@with_retry(
  retries_limit=4, allowed_exceptions=(ZeroDivisionError, AttributeError)
)
def run_with_custom_parameters(task):
  return task.run()

# 데코레이터 객체
class WithRetry:
  def __init__(self, retries_limit=RETRIES_LIMIT, allowed_exceptions=None):
    self.retries_limit = retries_limit
    self.allowed_exception = allowed_exceptions
  
  def __call__(self, operation):
    
    @wraps(operation)
    def wrapped(*args, **kwagrs):
      last_raised = None
      
      for _ in range(self.retries_limit):
        try:
          return operation(*args, **kwargs)
        except self.allowed_exception as e:
          logger.info("retrying %s due to %s", operation, e)
          last_raised = e
      raise last_raised
    return wrapped

# 위 데코레이터를 함수에 적용
@WithRetry(retries_limit=5)
def run_with_custom_retries_limit2(task):
  return task.run()

  """
  1. 먼저 @ 연산 전에 전달된 파라미터를 사용해 데코레이터 객체 생성
  2. __init__ 메서드에서 정해진 로직에 따라 초기화
  3. @ 연산 호출
  4. with_custom_retries_limit2 함수를 래핑하여 __call__ 매직 메서드 호출
  5. 원본 함수를 래핑하여 우리가 원하는 로직이 적용된 새로운 함수 반환
  """
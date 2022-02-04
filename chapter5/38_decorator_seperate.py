# 데코레이터와 관심사의 분리

import functools

def traced_function(function):
  @functools.wraps(function)
  def wrapped(*args, **kwagrs):
    logger.info("%s 함수 실행", function.__qualname__)
    start_time = time.time()
    result = function(*args, **kwagrs)
    logger.info(
      "함수 %s 처리 소요시간 %.2fs",
      function.__qualname__,
      time.time() - start_time
    )
    return result
  return wrapped

## 하나 이상의 작업을 수행하고 있는 이를 분리
## 호출된 것 기록, 실행하는데 걸린 시간 기록 각 책임을 명확하게 분리

def log_execution(function):
  @functools.wraps(function)
  def wrapped(*args, **kwagrs):
    logger.info("started execution of %s", function.__qualtime__)
    return function(*args, **kwagrs)
  return wrapped

def measure_time(function):
  @functools.wraps(function)
  def wrapped(*args, **kwargs):
    start_time = time.time()
    result = function(*args, **kwargs)
    
    logger.info("function %s took %.2f", function.__qualtime__, time.time() - start_time)
    return result
  return wrapped

## 사용
@measure_time
@log_execution
def operation():
  pass
    
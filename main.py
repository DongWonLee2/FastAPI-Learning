from fastapi import FastAPI, Query, Body, HTTPException
from typing import List, Dict, Optional, TypeVar, Generic, Union
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()

# [기본 라우팅] Get 메서드 http://127.0.0.1:8000/에 Get요청 시 return문 응답
'''
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}
'''
# [엔드포인트] 데코레이터와 함수 정의, 그리고 그 함수의 본문까지를 포함하는 요청 처리 단위를 의미한다.

# [경로 매개변수] 사용자의 요청을 구체적으로 명시하기 위해 경로 매개변수, 쿼리 매개변수가 쓰인다.
# 경로 매개변수는 URL의 특정 부분을 변수로써 사용하여 동적으로 변할 수 있는 값을 처리할 때 사용한다.
# URL에서 {item_id}부분의 값을 read_item() 함수에 전달한다. 기본적으로 경로 매개변수를 문자열로 처리한다.
'''
@app.get("items/{item_id}")
def read_item(item_id):
    return {"item_id" : item_id}
'''
# 예시 2 / 두 개의 경로 매개변수
'''
@app.get("users/{user_id}/items/{item_name}")
def read_user_item(user_id, item_name):
    return {"user_id": user_id, "item_name": item_name}
'''

# [쿼리 매개변수] URL의 경로 이후 ?로 시작되는 부분에 정의되는 변수로 키-값 쌍의 형태로 정보를 전달하는데 사용된다.
# 필터링, 정렬, 페이지네이션 등과 같이 요청을 더 세부적으로 조정할 필요가 있을 때 활용된다.
# 사용자가 /items/?skip=5&limit=5와 같이 요청을 보내면 해당하는 값을 함수의 매개변수로 활용한다.
'''
@app.get("/items/")
def read_items(skip, limit): # skip, limit 매개변수가 쿼리 매개변수이다. 기본값을 설정하려면 def read_items(skip = 0, limit = 10):처럼 작성하면 된다.
    return {"skip": skip, "limit": limit}
'''

# [기본 타입 힌트] 변수나 함수의 예상 타입을 명시적으로 표시하는 기술이다. 안정적인 API를 구축할 수 있다.
# 해당 타임에 맞지 않는 요청은 자동으로 거부된다. 마찬가지로 매개변수에 기본값을 설정하여 선택적으로 만들 수 있다.
'''
@app.get("items/{item_id}")
def read_item(item_id: int):
    return {"item_id" : item_id}

@app.get("/getdata/")
def read_items(data: str = "funcoding"):
    return {"data": data}
'''

# [고급 타입 힌트] typing모튤에서 제공하는 List, Dict 같은 고급 타입 힌트를 사용하여 요청 데이터를 쉽게 다룰 수 있다.
# Query는 쿼리 매개변수의 기본값을 설정하는 데 사용되며, 유효성 겁사 및 메타데이터 선언에도 사용된다.
# Query([])는 해당 쿼리 매개변수가 필수가 아님을 나타내고 기본값으로 빈 리스트르 제공한다.
# Dict와는 달리 List타입 힌트의 경우에는 반드시 Query([]) 관련 구문을 함께 넣어주어야 한다.
'''
# List 데이터 타입을 쿼리 매개변수로 받는 라우트 예제
@app.get("/items/")
def read_item(q : List[int] = Query([])):
    return {"q" : q}
# Dict 데이터 타입을 요청 바디로 받는 라우트 예제
@app.post("/create-item/")
def create_item(item : Dict[str, int]):
    return item
'''

# [HTTP 메서드] 클라이언트가 서버에게 어떤 동작을 해달라고 요청하는 방식을 정의한다.
# GET : 서버로부터 정보를 요청할 때 사용한다. 데이터를 가져오는 read-only 작업에 적합하며, 서버의 상태나 데이터를 변경하지 않는다. @app.get()
# POST : 서버에 데이터를 전송하여 새로운 리소스를 생성하려고 할 때 POST 메서드를 사용한다. 데이터를 서버의 특정 경로에 제출하며 해당 데이터는 주로 요청 바디에 포함된다. @app.post()
# PUT : 지정된 리소스의 전체 업데이트를 수행한다. 예를 들어, 사용자의 전체 프로필을 업데이트하는 경우에 PUT요청을 사용한다. 리소스가 존재하지 않는 경우 새로 생성할 수 있지만, 주로 기존 리소스의 완전한 교체를 의미한다. @app.put()
# DELETE : 지정된 리소스를 삭제할 때 사용한다. 서버에 리소스의 제거를 지시하며, 성공적으로 처리된 경우 리소스에 더 이상 접근할 수 없다. @app.delete()
'''
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}

@app.get("items/{item_id}")
def read_item(item_id):
    return {"item_id" : item_id}

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10): 
    return {"skip": skip, "limit": limit}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "update_item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "Item {} has been deleted".format(item_id)}
'''
# [curl 명령어] Client URL의 약자로 다양한 프로토콜을 지원하는 명령행 기반의 네트워크 도구이다. 주로 웹 서버와의 상호작용을 위해 사용되며 HTTP, HTTPS, FTP 등 다양한 프로토콜을 지원한다. 기능 테스트 특히, POST 방식 요청을 테스트해야 할 때는 웹 주소 외에 특별한 방법이 필요한데 이를 간단히 테스트할 수 있는 명령어가 curl이다. 문자열 내의 특수 문자나 변수 등을 이스케이프하거나 해석할 필요가 있을 때 큰따옴표를 사용한다. 큰따옴표 안의 큰따옴표는 백슬래시를 사용하여 이스케이프해야 한다.
# - curl 주요 옵션
'''
curl -X POST "http://127.0.0.1:8000/items/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Smartphone\", \"description\": \"Latest model\", \"image\": {\"url\": \"http://example.com/image.jpg\", \"name\": \"front_view\"}}"
{"item":{"name":"Smartphone","description":"Latest model","image":{"url":"http://example.com/image.jpg","name":"front_view"}}}
1. -X 또는 --request : 사용할 HTTP 메서드를 지정한다.
    curl -X POST http://example.com
2. -H 또는 --header : HTTP 헤더를 추가한다.
    curl -H "Content-Type: application/json" http://example.com
3. -d 또는 --data : POST 요청에 데이터를 담는다.
    curl -d "param1=value1&param2=value2" http://example.com
4. --data-raw : POST 요청에 원시 데이터를 담는다.
    curl --data-raw "raw data" http://example.com
5. -F 또는 --form : 멀티파트 폼 데이터를 전송한다.
    curl -F "file=@/path/to/file" http://example.com/upload
6. -u 또는 --user : Basic 인증을 위한 사용자 이름과 패스워드를 지정한다.
    curl -u username:password http://example.com
7. -o 또는 --output : 출력 결과를 파일에 저장한다.
    curl -o output.html http://example.com
8. -I 또는 --head : 헤더 정보만을 출력한다.
    curl -I http://example.com
9. -v 또는 -verbose : 요청과 응답 정보를 자세히 출력한다.
    curl -v http://example.com
'''

# [Pydantic] 파이단틱은 데이터 검증과 데이터 직렬화를 매우 쉽게 만들어준다.
# 데이터 검증 : 사용자나 다른 시스템이 보내는 데이터가 올바른 형식과 값인지 확인하는 과정이다. 잘못된 데이터가 처리되는 것을 막아서 버그나 다양한 문제를 예방
# 데이터 직렬화 : 복잡한 데이터 구조를 바이트나 문자열로 변환해서 다른 시스템과 쉽게 교환할 수 있는 형태로 만드는 것이다. 반대 과정을 역직렬화라고 한다. 서로 다른 시스템끼리 데이터를 쉽게 주고받을 수 있게 해준다.
'''
from pydantic import BaseModel

class Item(BaseModel):
    name : str
    price : float
    is_offer : bool = None

@app.post("/items/")
def create_item(item: Item):
    return {"item": item.dict()}
'''
# [Pydantic 기본문법]
# 변수타입 : int, float, bool, str, datetime.datetime(날짜와 시간), Optional(typing 모듈의 일부로, 필드가 선택적임을 나타낸다. 이는 None값도 허용한다는 것을 의미한다.)
'''
from typing import Optional

class Item(BaseModel):
    name : str
    description : Optional[str] = None # 문자열, 선택적이며 기본값은 None
    price : float
    tax : float = 0.1 # 부동소수점 숫자, 선택적이며 기본값은 0.1

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item.dict()}
'''

# [필드 제약 조건] Field는 Pydantic 모델에서 필드에 추가적인 정보나 제약 조건을 지정할 때 사용하는 함수이다. 다양한 인자를 통해 세부 설정이 가능하다.
# - 주요 옵션
'''
1. default : 필드의 기본값을 지정한다. 만약 기본값이 없다면 필수 입력 필드가 된다.
2. alias : JSON 필드의 이름을 파이썬 변수와 다르게 지정할 때 사용한다.
3. title : 스키마에서 볼 수 있는 추가적인 정보로, 주로 문서화에 사용된다.
4. description : 필드에 대한 설명을 추가한다. 주로 API 문서에서 확인할 수 있다.
5. min_length & max_length : 문자열 길이의 최솟값과 최댓값을 지정한다.
6. gt(greater than), lt(less than) : 숫자의 크기 제약을 추가한다.
7. regex : 정규 표현식을 통한 패턴 매칭을 할 수 있다.
'''

'''
from pydantic import Field

class Item(BaseModel):
    name: str = Field(..., title = "Item Name", min_length = 2, max_length = 50) # ...(줄임표, ellipsis)는 필드가 필수임을 나타낸다.
    description: str = Field(None, description = "The discription of the item", max_length = 300) # 기본값으로 None이 설정되어 선택 필드이다.
    price: float = Field(..., gt = 0, description = "The price must be greater than zero")
    tag : List[str] = Field(default = [], alias = "item-tags") # 기본값으로 빈 리스트를 가지므로 선택 필드이고 alias 매개변수를 통해 JSON에서 사용될 때의 이름을 "item-tags"로 지정하고 있다.

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item.dict()}
'''

# [중첩된 모델] 하나의 모델이 다른 모델을 포함하는 구조를 의미한다. 이런 구조는 복잡한 데이터 형태를 모델링할 때 유용하다. 
# 장점 : 재사용성, 가독성, 유지보수
'''
# 이미지 정보를 담는 모델.
class Image(BaseModel):
    url: str
    name : str

# 아이템에 대한 정보를 담는 모델. image 필드의 타입은 앞서 정의한 Image 클래스이다.
class Item(BaseModel):
    name: str
    description: str
    image: Image

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item.dict()}

# [curl 실행문]
# curl -X POST "http://127.0.0.1:8000/items/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Smartphone\", \"description\": \"Latest model\", \"image\": {\"url\": \"http://example.com/image.jpg\", \"name\": \"front_view\"}}"
'''


# [List와 Union] 복잡한 데이터 구조와 다형성(하나의 메서드나 클래스가 있을 때 다양한 방법으로 동작하는 것)을 모델링할 때 유용한 타입 힌트이다.
# List[type], Union[type1, type2, ...] : 여러 타입 중 하나를 허용하는 변수를 정의할 수 있다. 

# [제네릭 타입] 여러 다른 타입에 대해 동일한 로직을 적용하는 데 사용된다. typing모듈의 TypeVar와 Generic 클래스를 이용한다.
# TypeVar : 타입 변수를 생성하며, 제네릭 클래스나 함수가 사용할 수 있는 타입 매개 변수를 정의한다. T = TypeVar('T')와 같이 작성하여 선언한다. 
# T는 Type의 첫글자로 관례적으로 많이 사용한다. 왼쪽의 T는 타입 변수의 이름이고 오른쪽 T는 객체를 생성할 때 내부적으로 사용되는 식별자이다. 차이가 있다! 이 구분은 주로 타입 체크 도구나 런타임이 아닌 타입 힌트를 분석할 때 중요하다.
# Generic : 제네릭 클래스를 정의할 때 사용한다. Generic[T]는 T를 타입 매개변수로 가진다.
'''
from typing import TypeVar, Generic

T = TypeVar('T')

# Generic[T]를 상속받는 클래스를 정의함으로써, GenericItem은 어떤 타입 T도 받을 수 있는 제네릭 클래스가 된다. 따라서 content의 타입은 동적으로 결정된다.
class GenericItem(BaseModel, Generic[T]):
    name: str
    content: T

@app.post("/generic_items/")
def create_item(item: GenericItem[int]):
    return {"item": item.dict()}

# [curl 실행문] 
# curl -X POST "http://127.0.0.1:8000/generic_items/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Generic\", \"content\": 42}"
# 서버에서는 GenericItem[int] 타입에 따라 content가 정수인지 검사하고, 타입이 일치하면 요청된 데이터를 그대로 반환한다. 만약 content로 정수가 아닌 다른 타입의 데이터를 보내면, Pydantic은 타입 에러를 반환하여 요청이 유효하지 않음을 알려준다.
'''

# [FastAPI 응답 모델] 클라이언트에 반환되는 데이터의 구조를 정의하는 데 사용되는 강력한 기능이다. 매우 권장되는 기능이다.
# 응답 모델을 사용하면 API가 반환하는 데이터의 구조를 명확하게 정의하고, API 문서를 자동으로 생성하여 사용자에게 제공할 수 있으며 반환 데이터의 유효성 검사를 자동으로 수행할 수 있다.
# FastAPI의 경로 연산에서 response_model 매개변수를 사용하여 응답 모델을 지정할 수 있다. 이 매개변수는 경로 연산 함수에 의해 반환되는 데이터의 형태를 Pydantic 모델로 정의하게 해준다. 이 모델은 반환된 데이터가 클라이언트로 전송되기 전에 시리얼라이즈되는 방식을 결정한다. 시리얼라이즈란 데이터를 일련의 비트로 변환하여 파일, 메모리, 네트워크를 통해 저장하거나 전송할 수 있는 형식으로 만드는 과정을 말한다.
# - 장점
'''
1. 데이터 검증 : 반환되는 데이터가 response_model에 정의된 모델의 필드 및 타입과 일치하는지 FastAPI에 의해 자동으로 검증
2. 자동 문서 생성 : response_model을 사용하여 API 문서에 정확한 응답 형식을 표시한다. 이는 API 사용자가 기대할 수 있는 응답의 구조를 이해하는데 도움이 된다.]
3. 보안 : 경로 연산이 노출할 데이터를 제한하는 데 사용할 수 있다. 예를 들어, 모델에서 반환하지 않아야 하는 내부 정보를 숨길 수 있다.
'''
# - 주요 응답 모델
'''
1. 기본 응답 모델 : Pydantic 클래스를 이용해 모델을 정의할 수 있다.
2. Generic 응답 모델 : 제네릭 타입을 활용하여 다양한 타입의 응답을 동일한 엔드포인트에서 다룰 수 있다.
3. Union 응답 모델 : 여러 가능한 모델 중 하나가 될 수 있는 경우에 유용하다.
4. List 응답 모델 : 리스트 형태의 데이터를 반환할 때 사용한다.
'''
# 예시 코드
'''
class Item(BaseModel):
    name: str
    description: str = None
    price: float

def get_item_from_db(id):
    return {
        "name": "Simple Item",
        "description": "A simple item description",
        "price": 50.0,
        "dis_price": 45.0
    }

#response_model로 Item을 사용한다. 이는 함수가 Item 인스턴스를 반환하거나 Item 모델로 시리얼라이즈 할 수 있는 데이터를 반환한다는 의미이다.
@app.get("/items/{item_id}", response_model = Item)
def read_item(item_id: int):
    item = get_item_from_db(item_id)
    return item
'''

# [기본 응답 모델]
'''
# pydantic 모델을 정의. 이 모델은 응답 데이터의 구조를 나타낸다.
class Item(BaseModel):
    name: str
    price: float

@app.get("/item/", response_model=Item)
def get_item():
    return {"name": "milk", "price": 3.5}
'''

# [Generic 응답 모델] 유연한 응답 타입을 정의할 수 있게 하여 다양한 데이터 타입에 대해 재사용 가능한 응답 모델을 만들 수 있다.
'''
from pydantic.generics import GenericModel

T = TypeVar("T")
# GenericModel을 상속 받아 제네릭 응답 모델을 생성한다.
class GenericItem(GenericModel, Generic[T]):
    data: T

# 경로 연산에서 'response_model'을 GenericItem[str]로 지정하여 반환되는 'data' 필드가 문자열 타입임을 명시
@app.get("/generic_item/", response_model=GenericItem[str])
async def get_generic_item():
    # 응답 모델에 맞춰 'data' 필드에 문자열 값을 반환한다.
    return {"data": "generic item"}
'''

# [Union 응답 모델] 하나의 경로 연산에서 여러 다른 모델 중 하나를 반환할 수 있도록 한다.
'''
class Cat(BaseModel):
    name: str

class Dog(BaseModel):
    name: str

@app.get("/animal/", response_model=Union[Cat, Dog])
async def get_animal(animal: str):
    if animal == "cat":
        return Cat(name="Whiskers")
    else:
        return Dog(name="Fido")
    
# [curl 실행문]
# curl -X GET "http://127.0.0.1:8000/animal/?animal=cat"
# curl -X GET "http://127.0.0.1:8000/animal/?animal=dog"
'''

# [List 응답 모델]
'''
class Item(BaseModel):
    name: str

@app.get("/items/", response_model=List[Item])
async def get_items():
    # 데이터베이스나 다른 데이터 소스에서 아이템 리스트를 가져와 반환하지만 여기서는 예시를 위해 고정된 리스트를 반환한다.
    return [{"name": "Itme 1"}, {"name": "Item 2"}]
'''

# [FastAPI 응답 클래스] 응답 클래스는 서버가 클라이언트에게 반환하는 HTTP 응답의 종류를 정의한다. 반환되는 데이터의 형식을 제어하고, 특정 HTTP 응답의 동작을 세밀하게 조정할 수 있다.
# - 응답 클래스 리스트
'''
1. JSONResponse : 클라이언트에게 JSON 형식의 데이터를 반환한다. 파이썬의 딕셔너리나 Pydantic 모델을 JSON 문자열로 변환하여 응답 바디에 담아 전송한다.
2. HTMLResponse : 클라이언트에게 HTML 형식의 데이터를 반환한다. 주로 웹페이지의 내용을 반환할 때 사용한다.
3. PlainTextResponse : 클라이언트에게 단순 텍스트 형식의 응답을 반환한다. 로깅, 간단한 메시지 전달 등에 적합하다.
4. RedirectResponse : 클라이언트를 지정된 다른 URL로 리디렉션 하는 HTTP 응답을 생성한다. 사용자를 다른 페이지로 유도할 때 유용하다.
'''

# [JSONResponse]
'''
from fastapi.responses import JSONResponse
# JSONResponse를 response_class로 사용하여 경로 연산을 정의한다.
@app.get("/json", response_class=JSONResponse)
def read_json():
    # 딕셔너리를 반환하면, FastAPI는 이를 JSONResponse 객체로 변환하여 응답한다.
    return {"msg": "This is JSON"}
'''

# [HTMLResponse]
'''
from fastapi.responses import HTMLResponse

@app.get("/html", response_class=HTMLResponse)
def read_html():
    return "<h1>This is HTML</h1>"

'''

# [PlainTextResponse]
'''
from fastapi.responses import PlainTextResponse

@app.get("/text", response_class=PlainTextResponse)
def read_text():
    return "This is Plain Text"
'''

# [RedirectResponse]
'''
from fastapi.responses import RedirectResponse

@app.get("/redirect")
def read_redirect():
    return RedirectResponse(url="/text")

@app.get("/text", response_class=PlainTextResponse)
def read_text():
    return "This is Plain Text"

# [curl 실행문]
# curl -X GET "http://127.0.0.1:8000/redirect" -L
# -L 옵션은 리디렉션을 따르도록 지시한다. 이 옵션이 없으면 curl은 리디렉션된 URL의 내용을 자동으로 가져오지 않는다.
'''

# [요청(request)] 클라이언트가 서버로부터 정보를 얻거나 서버에 정보를 전달하기 위해 보내는 HTTP 메시지이다. 데이터 전송 방법 중 쿼리 매개변수와 요청 바디가 가장 흔히 사용된다.

# [쿼리 매개변수]
'''
# 이 경로 연산은 쿼리 매개변수 'q'를 받아들인다.
@app.get("/users/")
def read_users(q: str = Query(None, max_length=50)): # 선택적, 길이 제약
    return {"q": q}
'''

# - Query 클래스의 주요 옵션 Field 옵션과 조금 비슷함.
'''
Query(default, 옵션리스트)
0. default : 매개변수의 기본값을 지정한다. 값이 None이면 선택적이 된다.
1. min_length : 문자열 매개변수에 대한 최소 길이를 지정한다.
2. max_length : 문자열 매개변수에 대한 최대 길이를 지정한다.
3. alias : 매개변수의 별칭을 지정한다.(클라이언트 요청 시 사용하는 별칭) URL에서 사용하는 이름과 함수 내에서 사용하는 이름을 다르게 할 수 있다.
4. deprecated : 매개변수가 더 이상 사용되지 않음을 명시한다. API 문서에 표시되어 사용자가 해당 매개변수를 사용하지 않도록 경고한다.
5. discription : 매개변수에 대한 설명을 추가한다. 이 설명은 API 문서에 표시되어 매개변수의 사용 목적이나 기대되는 값 등을 설명할 수 있다.
6. ge(greater than or equal to) : 매개변숫값이 지정된 값 이상이어야 함을 명시한다.
7. le(less than or equal to) : 매개변숫값이 지정된 값 이하이어야 함을 명시한다.  
8. regex : 매개변숫값이 일치해야 하는 정규 표현식 패턴을 지정한다.
9. title : 매개변수의 설명 제목을 지정한다. 이는 주로 API 문서에서 매개변수의 예상 입력값을 보여주는 데 도움을 준다.
10. example : 매개변수의 예시 값을 제공한다. 이는 문서에서 매개변수의 예상 입력값을 보여주는 데 도움을 준다.
'''

# [alias] 클라이언트와 서버 간의 인터페이스를 유연하게 관리할 수 있으며, API 설계 시 내부 구현 로직을 추상화하여 깔끔하고 안전한 API를 제공할 수 있다.
'''
@app.get("/items/")
def read_items(internal_query: str = Query(None, alias="search")):
    # 클러이언트는 'search'라는 이름으로 쿼리 매개변수를 전송한다. FastAPI 애플리케이션은 이를 'internal_query'라는 내부 변수로 처리한다.
    return {"query_handled": internal_query}
'''

# [deprecated] 변경 사항을 관리할 수 있게 해준다. 특정 쿼리 매개변수가 더 이상 사용되지 않을 때 deprecated = True로 설정하여 API 사용자에게 해당 매개변수를 향후 사용하지 말 것을 권장하는 신호를 보낸다.
'''
@app.get("/users/")
def read_users(q: str = Query(None, deprecated=True)):
    # 클러이언트는 'q'라는 이름으로 쿼리 매개변수를 전송할 수 있으나 이 매개변수는 곧 지원되지 않을 예정임을 명시한다.
    return {"q": q}
'''

# [description] 쿼리 매개변수에 대한 상세한 설명을 추가할 수 있다. 특히 복잡하거나 추가적인 컨텍스트가 필요한 매개변수를 문서화할 때 유용하다.
'''
@app.get("/info/")
def read_info(info: str = Query(None, description="Write infomation")): # 한국어도 가능!
    # 클러이언트는 'info'라는 이름으로 쿼리 매개변수를 전송할 수 있고 이 매개변수에 대한 설명은 Swagger UI에서 확인할 수 있다.
    return {"info": info}
'''

# [요청 바디]
# [HTTP 프로토콜과 요청] 프로토콜은 컴퓨터나 원격 장치 간 통신을 위한 규칙의 집합이다. 네트워크상에서 정보가 어떻게 전송되어야 하는지를 정의한다. 일반적인 통신 프로토콜에는 TCP/IP, HTTP, FTP 등이 있으며, 각각은 다양한 통신 요구 사항을 충족하기 위해 설계되었다. HTTP는 웹에서 데이터를 교환하기 위한 프로토콜이다. WWW의 기초가 되는 이 프로토콜은 클라이언트와 서버 간에 HTML 문서나 이미지 같은 리소스를 요청하고 전송하는 데 사용된다. HTTP는 상태가 없는 프로토콜이지만, 쿠키 등의 기술을 사용하여 상태 정보를 유지할 수 있다.
# - HTTP 요청 구성 요소
'''
1. Method : 서버에 요청하는 작업의 유형을 정의한다(GET, POST, PUT 등)
2. URL : 요청이 지시되는 리소스의 위치를 나타낸다.
3. Headers : 요청에 대한 메타데이터를 포함하며 인증, 캐싱, 클라이언트 유형 등의 정보를 담는다.
4. Body : 일부 HTTP 메서드(POST, PUT)에서 사용되며, 전송할 데이터를 담는다.
'''

# [FastAPI에서의 요청 바디 처리] 요청 바디는 클라이언트가 서버로 전송하는 데이터의 본문이다. 주로 POST, PUT, PATCH 메서드를 사용할 때 볼 수 있으며, 서버가 수행해야 할 상세한 작업이나 서버에 제출할 데이터를 포함한다. 
# Headers : 예를 들어 Content-Type 헤더는 서버에게 바디의 데이터 유형이 application/json인 JSON 데이터임을 알린다.
# Body : 실제 데이터를 담고 있으며 클라이언트가 서버에 제공하려는 내용을 포함한다. GET 요청은 메서드는 Body() 함수를 사용하지 않는다.
'''
from fastapi import FastAPI, Body

@app.post("/items/")
def create_item(item: dict = Body(...)):
    # 클라이언트가 전송하는 JSON 바디 데이터를 'item'이라는 변수로 받는다. 'dict' 타입은 JSON 바디가 Python 딕셔너리로 파싱될 것임을 나타낸다. Body(...)는 이 필드가 클라이언트로부터 필수로 제공되어야 함을 나타낸다.
    return {"item": item}

# [curl 실행문]
# curl -X POST "http://127.0.0.1:8000/items/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"key\":\"value\"}"
'''

# [요청 바디의 다양한 옵션]
'''
# 제목과 상세 설명이 redoc에서만 보임... 
@app.post("/advanced_items/")
def create_advanced_item(
    item: dict = Body(
        default = None, # 필드 기본값 설정
        example={"key": "value"}, # 문서에 표시 될 예시 값
        media_type="application/json", # 미디어 타입 지정. JSON 형식의 데이터를 전송받을 것임을 명시
        alias="item_alias", # 별칭 설정
        title="Sample Item", # 문서 제목
        description="This is a sampel item", # 요청 바디 상세 설명
        deprecated=False # 사용 중단 여부
        )
    ):
    return {"item": item}
'''

# [예외 처리] 프로그래밍에서 발생할 수 있는 예상치 못한 에러 또는 예외 상황에 대처하는 프로세스이다. 

# [기본 예외 처리] try/except 문법을 사용하여 예외를 처리한다. 
'''
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    try:
        if item_id < 0:
            raise ValueError("음수는 허용되지 않습니다.")
    except ValueError as e:
        # 발생한 ValueError를 HTTPException으로 변환하여 처리한다.
        # 클라이언트에게 상태 코드 400과 에러 메시지를 반환한다.
        raise HTTPException(status_code=400, detail=str(e))
'''

# [HTTPException 클래스] 다양한 에러 상황에 대해 HTTP 상태 코드와 에러 메시지를 정의하고 반환할 수 있다. 
'''
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found!", headers={"X-Error": "There was an error"}) # headers : 응답과 함께 전달할 HTTP 헤더 설정
    return {"item_id": item_id}

'''

# [HTTP 헤더] 클라이언트와 서버 간의 통신에서 추가적인 정보를 제공하는 중요한 역할을 한다. 
# [WWW-Authenticate 헤더] 클라이언트에게 어떤 인증 방식을 사용해야 하는지 알려준다. 주로 401 Unauthorized 응답과 함께 사용된다.
'''
raise HTTPException(
    status_code=401, # 인증이 필요함을 나타낸다.
    detail="Not authenticated", 
    headers={"WWW-Authenticate": "Bearer"}
)
'''

# [Retry-After 헤더] 클라이언트가 서비스에 대한 요청을 너무 많이 보냈을 때 일정 시간 후에 다시 시도라하는 지시를 전달한다.
'''
raise HTTPException(
    status_code=429, 
    detail="Too Many Requests", 
    headers={"Retry-After": "120"}
)
'''

# [X-Rate-Limit 헤더] 사용자가 한정된 시간 내에 요청할 수 있는 최대 횟수를 알려준다.
'''
raise HTTPException(
    status_code=429, 
    detail="Rate limit exceeded", 
    headers={"X-Rate-Limit": "100"}
)
'''

# [X-Error 헤더] 내부 서버 에러 발생 시, 에러의 세부 사항을 클라이언트에게 전달한다.
'''
raise HTTPException(
    status_code=500, # 서버 내부에 에러가 발생했음을 나타낸다.
    detail="Internal Server Error", 
    headers={"X-Error": "Database connection failed"}
)
'''

# [Cache-Control 헤더] 클라이언트에게 해당 응답을 캐시하지 말라는 지시를 한다. 데이터가 실시간으로 갱신되어야 할 때 유용하다.
'''
raise HTTPException(
    status_code=200, # 요청이 성공적으로 처리되었음을 알려준다.
    detail="Response Information", 
    headers={"Cache-Control": "no-cache"}
)
'''

# [Location 헤더] 새로 생성된 리소스의 URI를 클라이언트에게 제공한다. 주로 201 Created 응답에서 사용된다.
'''
raise HTTPException(
    status_code=201, # 요청이 성공적으로 처리되었고, 새로운 리소스가 생성되었음을 알려준다.
    detail="New item created", 
    headers={"Location": "/items/5"}
)
'''
# [나머지 HTTP 상태 코드 값] 403 : 서버가 요청을 이해했으나 승인을 거부, 404 : 서버가 요청한 리소스를 찾을 수 없음.
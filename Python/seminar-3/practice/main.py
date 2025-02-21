# template_app.py

from fastapi import FastAPI, WebSocket
from strawberry.fastapi import GraphQLRouter
import strawberry
import grpc
from concurrent import futures
import weather_pb2, weather_pb2_grpc
import random
import asyncio
import datetime

app = FastAPI()

# Общая задача: Система "Прогноз погоды" с тремя компонентами:
# 1. gRPC — получение случайных данных о погоде.
# 2. GraphQL — запрос прогноза и истории.
# 3. WebSocket — оповещения об изменении погоды.


# 1. gRPC сервер: генерирует данные о погоде
class WeatherService(example_pb2_grpc.WeatherServicer):
    def GetWeather(self, request, context):
        # Генерируем случайные погодные данные
        raise NotImplementedError()


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_WeatherServicer_to_server(WeatherService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


# 2. GraphQL схема для запросов прогноза
weather_data = {}


@strawberry.type
class Weather:
    city: str
    temperature: float
    humidity: int
    description: str
    timestamp: str

def get_city_and_weather() -> Dict[str, Weather]:
    return weather_data
    
@strawberry.type
class Query:
    @strawberry.field
    def cities_and_weather(self) -> Dict[str, Weather]:
        return get_city_and_weather()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def delete_weather(self, city: str) -> bool:
        if city in weather_data:
            del weather_data[city]
            return True
        return False
        
schema = strawberry.Schema(query=Query, mutation=Mutation)
app.include_router(GraphQLRouter(schema), prefix="/graphql")


# 3. WebSocket для уведомлений о новых записях
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    raise NotImplementedError()


if __name__ == "__main__":
    import uvicorn
    import threading

    # Запуск gRPC сервера в фоновом потоке
    threading.Thread(target=serve_grpc, daemon=True).start()

    # Запуск FastAPI сервера
    uvicorn.run("template_app:app", host="127.0.0.1", port=8000, reload=True)

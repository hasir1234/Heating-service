import grpc
import heating_pb2
import heating_pb2_grpc

channel = grpc.insecure_channel("localhost:8061")
stub = heating_pb2_grpc.HeatingPredictStub(channel)

request = heating_pb2.HeatingFeatures(
    Hubids=60,
    Eircode="A67",
    Month=1,
    TwoHrSlot=18,
    gas_pct=0.7555
)

response = stub.predict_heating(request)

print("Predicted heat_mean:", response.predicted_heat_mean)
print("Alert:", response.alert)
print("Tariff:", response.tariff)

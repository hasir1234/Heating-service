import time
from concurrent import futures
import grpc

import heating_pb2
import heating_pb2_grpc
import predict_heating as ph


class HeatingPredictServicer(heating_pb2_grpc.HeatingPredictServicer):
    def predict_heating(self, request, context):
        result = ph.predict_heating(
            request.Hubids,
            request.Eircode,
            request.Month,
            request.TwoHrSlot,
            request.gas_pct
        )

        return heating_pb2.HeatingPrediction(
            predicted_heat_mean=result["predicted_heat_mean"],
            alert=result["alert"],
            tariff=result["tariff"]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    heating_pb2_grpc.add_HeatingPredictServicer_to_server(
        HeatingPredictServicer(), server
    )
    server.add_insecure_port("[::]:8061")
    server.start()
    print("Server started on port 8061")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()

import 'dart:io';
import 'dart:async';

class UdpCommunicator {
  List<int> _data = [];
  RawDatagramSocket? _socket;

  set data(List<int> value) {
    _data = value;
  }

  UdpCommunicator(Function callBack) {
    _startListening(callBack);
    RawDatagramSocket.bind(InternetAddress.anyIPv4, 0)
        .then((RawDatagramSocket socket) {
      _socket = socket;
      socket.broadcastEnabled = true;
      Timer.periodic(const Duration(milliseconds: 20), (arg) async {
        sendPacket(_data);
      });
    });
  }

  void sendPacket(List<int> data) {
    _socket?.send(data, InternetAddress('239.1.2.3'), 10001);
  }

  void dispose() {
    _socket?.close();
  }

  void _startListening(Function callBack) {
    RawDatagramSocket.bind(InternetAddress.anyIPv4, 10002)
        .then((RawDatagramSocket socket) {
      _socket = socket;
      socket.broadcastEnabled = true;
      socket.joinMulticast(InternetAddress('239.1.2.3'));
      socket.listen((RawSocketEvent event) {
        if (event == RawSocketEvent.read) {
          Datagram? datagram = socket.receive();
          if (datagram != null) {
            if (callBack != null) {
              callBack(datagram);
            }
          }
        }
      });
    });
  }
}


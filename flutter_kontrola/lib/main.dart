import 'package:flutter/material.dart';
import 'slider_widget.dart';
import 'udpcommunicator.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ar;kkdsnvzc',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'bkthbzfl;kbnzv '),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final left = GlobalKey<MojSliderState>();
  final right = GlobalKey<MojSliderState>();

  UdpCommunicator udpc = UdpCommunicator(callBack);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          children: [
            Container(
              height: 300,
            ),
            Expanded(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  MojSlider(
                    key: left,
                    onChanged: (int) {
                      udpc.data = [
                        left.currentState!.getValue(),
                        right.currentState!.getValue()
                      ];
                    },
                  ),
                  Container(
                    padding: EdgeInsets.all(30),
                    width: 200,
                    child: ElevatedButton(
                      style: ButtonStyle(
                          shape:
                              MaterialStateProperty.all<RoundedRectangleBorder>(
                                  RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(0.0),
                                      side: BorderSide(color: Colors.red)))),
                      onPressed: () {
                        left.currentState!.setValue(0.0);
                        right.currentState!.setValue(0.0);
                        udpc.data = [
                          left.currentState!.getValue(),
                          right.currentState!.getValue()
                        ];
                      },
                      child: const Text('STOP'),
                    ),
                  ),
                  MojSlider(
                    key: right,
                    onChanged: (int) {
                      udpc.data = [
                        left.currentState!.getValue(),
                        right.currentState!.getValue()
                      ];
                    },
                  ),
                ],
              ),
            ),
            Container(
              height: 30,
            ),
          ],
        ),
      ),
    );
  }

  static callBack() {
    print("primo");
  }
}

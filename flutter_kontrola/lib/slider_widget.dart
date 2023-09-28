import 'package:flutter/material.dart';

class MojSlider extends StatefulWidget {
  final Function(int) onChanged;
  // const MojSlider({Key? key}) : super(key: key);
  const MojSlider({super.key, required this.onChanged});

  @override
  State<MojSlider> createState() => MojSliderState();
}

class MojSliderState extends State<MojSlider> {
  double _value = 0;

  // Metoda za postavljanje vrednosti slajdera
  void setValue(double newValue) {
    setState(() {
      _value = newValue;
    });
  }

  // Metoda za čitanje trenutne vrednosti slajdera
  int getValue() {
    return _value.round();
  }

  @override
  Widget build(BuildContext context) {
    return SliderTheme(
        data: SliderThemeData(
          trackHeight: 40,
          thumbShape: SliderComponentShape.noOverlay,
          overlayShape: SliderComponentShape.noOverlay,
          valueIndicatorShape: SliderComponentShape.noOverlay,
          trackShape: RectangularSliderTrackShape(),
        ),
        child: Stack(
          alignment: Alignment.center,
          children: [
            RotatedBox(
              quarterTurns: 3,
              child: Slider(
                  activeColor: Colors.green,
                  inactiveColor: Colors.red,
                  value: _value,
                  min: -100,
                  max: 100,
                  onChanged: (value) {
                    setState(() {
                      _value = value;
                      widget.onChanged(value.round());
                    });
                  }),
            ),
            Center(
              child: Text(
                "${_value.round()}",
                style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 16),
              ),
            ),
          ],
        ));
  }
}

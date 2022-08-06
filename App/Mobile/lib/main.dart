import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(
  title: "Req Quartz Mobile Application",
  home: HomeWidget(),
));

class HomeWidget extends StatefulWidget {
  const HomeWidget({Key? key}) : super(key: key);

  @override
  State<HomeWidget> createState() => _HomeWidgetState();
}

class _HomeWidgetState extends State<HomeWidget> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: SafeArea(
        child: Text("Hello from scratch"),
      ),
    );
  }
}

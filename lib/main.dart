import 'package:flutter/material.dart';
import 'package:health_card/App_pages/doctor_navigation.dart';
import 'package:health_card/App_pages/home_page.dart';
import 'package:health_card/App_pages/patient_doctor_login.dart';
import 'package:health_card/App_pages/patient_navigation.dart';

void main() => runApp(MyApp());

class MyApp extends StatefulWidget {
  static const routeName = '/root';
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Health_Card',
      routes: {
        MyApp.routeName: (context) => MyApp(),
        patient_doctor_login.routeName: (context) => patient_doctor_login(),
        Patient_Navigation.routeName: (context) => Patient_Navigation(),
        Doctor_Navigation.routeName: (context) => Doctor_Navigation(),
      },
      home: Home_page(),
    );
  }
}

import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:health_card/App_pages/patient_navigation.dart';
import 'package:health_card/App_pages/doctor_navigation.dart';

Future<String> login(
    String email, String password, String user, BuildContext context) async {
  var decodedJson;
  http.Response response = await http.get(
      "http://192.168.43.212:3000/" + user + "/login/" + email + "-" + password,
      headers: {"Accept": "application.json"});
  decodedJson = jsonDecode(response.body);
  print(decodedJson);
  if (user == 'patient') {
    Navigator.pushNamed(context, Patient_Navigation.routeName,
        arguments: decodedJson);
  } else {
    Navigator.pushNamed(context, Doctor_Navigation.routeName,
        arguments: decodedJson);
  }
}

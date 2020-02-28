import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:health_card/Models/patient_model.dart';

Future<String> getPatientProfile(String aadharno) async {
  var decodedJson;
  http.Response response = await http.get(
      "http://192.168.43.212:3000/patient/" + aadharno,
      headers: {"Accept": "application.json"});
  decodedJson = jsonDecode(response.body);
  return decodedJson;
}

import 'package:flutter/material.dart';
import 'package:health_card/Models/doctor_model.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Profile_page extends StatefulWidget {
  var aadharno;
  Profile_page(this.aadharno);
  @override
  _Profile_pageState createState() => _Profile_pageState(aadharno);
}

class _Profile_pageState extends State<Profile_page> {
  _Profile_pageState(this.aadharno);
  var decodejson;
  var body;
  var aadharno;
  Doctor_Model dm;
  void dm_change(
      var name, var aadhar, var gen, var cerno, var emal, var conno) {
    dm = Doctor_Model(name, emal, conno, gen, aadhar, cerno);
  }

  Future profile_get() async {
    http.Response response = await http.get(
        "http://192.168.43.212:3000/doctor/profile/" + aadharno,
        headers: {"Accept": "application.json"});
    print(response.body);
    //return response.body;
    decodejson = jsonDecode(response.body);
    setState(() {
      dm_change(
        decodejson['Name'],
        decodejson['AadharNo'],
        decodejson['Gender'],
        decodejson['CertificateNo'],
        decodejson['Email'],
        decodejson['ContactNo'],
      );
    });
  }

  @override
  void initState() {
    profile_get();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(dm.Name.toString(), style: TextStyle(fontSize: 20)),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(dm.AadharNo.toString(), style: TextStyle(fontSize: 20)),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(dm.Gender.toString(), style: TextStyle(fontSize: 20)),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 0, 20, 0),
            child: Text(dm.CertificateNo.toString(),
                style: TextStyle(fontSize: 20)),
          ),
          Row(
            children: <Widget>[
              Icon(
                Icons.phone,
                color: Colors.blue,
              ),
              Text(dm.ContactNo.toString(), style: TextStyle(fontSize: 20)),
            ],
          ),
          Row(
            children: <Widget>[
              Icon(
                Icons.email,
                color: Colors.blue,
              ),
              Text(dm.Email.toString(), style: TextStyle(fontSize: 20)),
            ],
          ),
        ],
      ),
    );
  }
}
